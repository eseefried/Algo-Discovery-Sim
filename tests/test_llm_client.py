"""Request shape and failure handling through the real SDK with a mocked HTTP transport."""

import json

import anthropic
import httpx2
import pytest

from a2m.llm.client import LLM, Budget, BudgetExhausted, LLMError

SCHEMA = {"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"],
          "additionalProperties": False}


def _client(seen, stop_reason="end_turn", text='{"x": "ok"}'):
    def handle(request):
        seen.append({"url": str(request.url), "headers": dict(request.headers),
                     "body": json.loads(request.content)})
        return httpx2.Response(200, json={
            "id": "msg_1", "type": "message", "role": "assistant", "model": "claude-fable-5-1",
            "content": [{"type": "text", "text": text}], "stop_reason": stop_reason,
            "stop_sequence": None,
            "stop_details": {"type": "refusal", "category": "cyber", "explanation": "x"}
            if stop_reason == "refusal" else None,
            "usage": {"input_tokens": 1000, "output_tokens": 100, "cache_read_input_tokens": 0,
                      "cache_creation_input_tokens": 0}})
    return anthropic.Anthropic(api_key="test",
                               http_client=httpx2.Client(transport=httpx2.MockTransport(handle)))


def test_request_uses_structured_output_effort_and_default_fallback():
    seen = []
    budget = Budget(1.0)
    llm = LLM("claude-fable-5-1", budget, effort="high", client=_client(seen))
    assert llm.call("t", "sys", "hello", SCHEMA) == {"x": "ok"}
    body, headers = seen[0]["body"], seen[0]["headers"]
    assert body["model"] == "claude-fable-5-1"
    assert body["output_config"] == {"effort": "high",
                                     "format": {"type": "json_schema", "schema": SCHEMA}}
    assert body["fallbacks"] == "default"
    assert "server-side-fallback-2026-07-01" in headers["anthropic-beta"]
    assert "thinking" not in body and "temperature" not in body
    assert budget.usd == pytest.approx((1000 * 10 + 100 * 50) / 1e6)


def test_haiku_has_no_server_fallback():
    seen = []
    LLM("claude-haiku-5-5", Budget(1.0), client=_client(seen)).call("t", "s", "p", SCHEMA)
    assert "fallbacks" not in seen[0]["body"]


def test_refusal_and_truncation_raise():
    with pytest.raises(LLMError, match="declined"):
        LLM("claude-opus-5-5", Budget(1.0), client=_client([], "refusal")).call("t", "s", "p", SCHEMA)
    with pytest.raises(LLMError, match="truncated"):
        LLM("claude-opus-5-5", Budget(1.0), client=_client([], "max_tokens")).call("t", "s", "p", SCHEMA)


def test_invalid_json_raises():
    with pytest.raises(LLMError, match="invalid JSON"):
        LLM("claude-opus-5-5", Budget(1.0), client=_client([], text="nope")).call("t", "s", "p", SCHEMA)


def test_exhausted_budget_blocks_calls():
    seen = []
    b = Budget(0.0)
    with pytest.raises(BudgetExhausted):
        LLM("claude-opus-5-5", b, client=_client(seen)).call("t", "s", "p", SCHEMA)
    assert seen == []
