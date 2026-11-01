"""Structured Claude/local model clients with shared spend or execution limits."""

from __future__ import annotations

import json
import math
import os
import threading
import time
from typing import Any

import anthropic
import httpx
import jsonschema

from a2m import config
from a2m.llm.mock_corpus import MockBackend

# USD per million tokens (input, output). Anthropic first-party rates, 2026-10.
PRICES = {
    "claude-fable-5-1": (10.00, 50.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "mock": (1.00, 5.00),
}
CACHE_READ_FRACTION = 0.05  # cache reads bill at roughly 5% of input on current models
# Models that accept server-side refusal fallback (`fallbacks="default"`).
FALLBACK_MODELS = {"claude-fable-5-1", "claude-opus-5-5", "claude-sonnet-5-5"}


class BudgetExhausted(RuntimeError):
    pass


class LLMError(RuntimeError):
    """Refusal, truncation, invalid output, or API failure. The calling action fails."""


class Budget:
    def __init__(self, max_usd: float | None, max_tokens: int | None = None,
                 *, max_calls: int | None = None, max_seconds: float | None = None):
        for name, value in (("max_usd", max_usd), ("max_tokens", max_tokens),
                            ("max_calls", max_calls), ("max_seconds", max_seconds)):
            if value is not None and (not math.isfinite(value) or value < 0):
                raise ValueError(f"{name} must be finite and nonnegative")
        self.max_usd, self.max_tokens = max_usd, max_tokens
        self.max_calls, self.max_seconds = max_calls, max_seconds
        self.started = time.monotonic()
        self.usd = 0.0
        self.input_tokens = self.output_tokens = self.cache_read_tokens = self.calls = 0
        self.by_model: dict[str, dict[str, float]] = {}
        self._lock = threading.Lock()

    @property
    def exhausted(self) -> bool:
        tokens = self.input_tokens + self.output_tokens
        return ((self.max_usd is not None and self.usd >= self.max_usd)
                or (self.max_tokens is not None and tokens >= self.max_tokens)
                or (self.max_calls is not None and self.calls >= self.max_calls)
                or (self.max_seconds is not None
                    and time.monotonic() - self.started >= self.max_seconds))

    def check(self):
        if self.exhausted:
            raise BudgetExhausted(f"execution budget exhausted: {self.snapshot()}")

    def charge(self, model: str, inp: int, out: int, cache_read: int = 0, *, local: bool = False):
        pin, pout = PRICES.get(model, PRICES["claude-fable-5-1"])
        cost = 0.0 if local else (
            inp * pin + cache_read * pin * CACHE_READ_FRACTION + out * pout) / 1e6
        with self._lock:
            self.usd += cost
            self.input_tokens += inp
            self.output_tokens += out
            self.cache_read_tokens += cache_read
            self.calls += 1
            m = self.by_model.setdefault(model, {"usd": 0.0, "calls": 0, "input": 0, "output": 0})
            m["usd"] += cost
            m["calls"] += 1
            m["input"] += inp
            m["output"] += out

    def snapshot(self) -> dict[str, Any]:
        return {"usd": round(self.usd, 6), "max_usd": self.max_usd, "calls": self.calls,
                "max_calls": self.max_calls, "max_tokens": self.max_tokens,
                "max_seconds": self.max_seconds,
                "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "cache_read_tokens": self.cache_read_tokens, "by_model": self.by_model}


class LLM:
    """One model bound to a budget. Modes: anthropic, local, mock."""

    def __init__(self, model: str, budget: Budget, mode: str = "anthropic", effort: str = "medium",
                 max_tokens: int = 16000, mock_seed: int = 0, timeout_s: float = 600,
                 client: Any = None, base_url: str | None = None, api_key: str | None = None):
        self.model, self.budget, self.mode = model, budget, mode
        self.effort, self.max_tokens = effort, max_tokens
        if mode == "mock":
            self._mock = MockBackend(mock_seed)
        elif mode == "local":
            self._base_url = (base_url or os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1")).rstrip("/")
            self._api_key = api_key or os.getenv("NEMOTRON_API_KEY")
            self._client = client or httpx.Client(timeout=timeout_s)
        elif mode != "anthropic":
            raise ValueError(f"unsupported LLM mode: {mode}")
        elif client is not None:
            self._client = client
        else:
            key = config.api_key()
            if not key:
                raise LLMError("set CLAUDE_HACKATHON_API (or ANTHROPIC_API_KEY), or use --llm mock")
            self._client = anthropic.Anthropic(api_key=key, timeout=timeout_s)

    @property
    def label(self) -> str:
        return "mock" if self.mode == "mock" else self.model

    def call(self, tag: str, system: str, prompt: str, schema: dict[str, Any],
             meta: dict[str, Any] | None = None, *,
             messages: list[dict[str, str]] | None = None) -> dict[str, Any]:
        """Return a dict that conforms to `schema`. `meta` is read only by the mock."""
        self.budget.check()
        if self.mode == "local":
            return self._call_local(tag, system, prompt, schema, messages)
        if self.mode == "mock":
            out = self._mock.respond(tag, meta or {})
            self.budget.charge("mock", (len(system) + len(prompt)) // 4, len(json.dumps(out)) // 4)
            return out
        kwargs: dict[str, Any] = {
            "model": self.model, "max_tokens": self.max_tokens, "system": system,
            "messages": [{"role": "user", "content": prompt}],
            "output_config": {"effort": self.effort,
                              "format": {"type": "json_schema", "schema": schema}},
            "cache_control": {"type": "ephemeral"},
        }
        try:
            if self.model in FALLBACK_MODELS:
                resp = self._client.beta.messages.create(
                    **kwargs, betas=["server-side-fallback-2026-07-01"], fallbacks="default")
            else:
                resp = self._client.messages.create(**kwargs)
        except anthropic.APIStatusError as e:
            raise LLMError(f"{tag}: API error {e.status_code}: {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise LLMError(f"{tag}: connection error: {e}") from e
        u = resp.usage
        self.budget.charge(self.model, u.input_tokens + (u.cache_creation_input_tokens or 0),
                           u.output_tokens, u.cache_read_input_tokens or 0)
        if resp.stop_reason == "refusal":
            cat = resp.stop_details.category if resp.stop_details else None
            raise LLMError(f"{tag}: model declined (category={cat})")
        if resp.stop_reason == "max_tokens":
            raise LLMError(f"{tag}: output truncated at max_tokens={self.max_tokens}")
        text = next((b.text for b in resp.content if b.type == "text"), "")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise LLMError(f"{tag}: invalid JSON output") from e

    def _call_local(self, tag, system, prompt, schema, messages=None):
        """OpenAI-compatible chat endpoint; the served model name selects the LoRA.

        No Anthropic effort, cache, fallback or credential fields reach this endpoint.
        Failed requests still consume one execution call; USD is always zero.
        """
        headers = {"Authorization": f"Bearer {self._api_key}"} if self._api_key else {}
        try:
            response = self._client.post(
                self._base_url + "/chat/completions", headers=headers,
                json={"model": self.model, "max_tokens": self.max_tokens,
                      "messages": [{"role": "system", "content": system}] + (
                          messages if messages is not None else [{"role": "user", "content": prompt}]),
                      "response_format": {"type": "json_schema", "json_schema": {
                          "name": "agent_response", "strict": True, "schema": schema}}},
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            self.budget.charge(self.model, 0, 0, local=True)
            raise LLMError(f"{tag}: local inference request failed ({type(exc).__name__})") from exc
        usage = payload.get("usage") if isinstance(payload, dict) else None
        self.response_model = payload.get("model", self.model) if isinstance(payload, dict) else self.model
        if not isinstance(usage, dict) or not all(
            type(usage.get(k)) is int and usage[k] >= 0
            for k in ("prompt_tokens", "completion_tokens")
        ):
            self.budget.charge(self.model, 0, 0, local=True)
            raise LLMError(f"{tag}: local endpoint must return token usage")
        self.budget.charge(self.model, usage.get("prompt_tokens", 0),
                           usage.get("completion_tokens", 0), local=True)
        try:
            choice = payload["choices"][0]
            if choice.get("finish_reason") != "stop":
                raise LLMError(f"{tag}: local output incomplete ({choice.get('finish_reason')})")
            message = choice["message"]
            if message.get("refusal"):
                raise LLMError(f"{tag}: local model declined")
            out = json.loads(message["content"])
            jsonschema.validate(out, schema)
            if not isinstance(out, dict):
                raise LLMError(f"{tag}: expected a JSON object")
            return out
        except (KeyError, IndexError, TypeError, ValueError, jsonschema.ValidationError) as exc:
            raise LLMError(f"{tag}: invalid local JSON/schema output") from exc
