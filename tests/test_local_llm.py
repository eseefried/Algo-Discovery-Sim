"""Local model contract and resource accounting; no server or GPU required."""
import json

import httpx
import pytest

from a2m.llm.client import LLM, Budget, BudgetExhausted, LLMError

SCHEMA = {"type": "object", "properties": {"x": {"type": "string"}},
          "required": ["x"], "additionalProperties": False}


def local(budget, seen, *, content='{"x":"ok"}', finish="stop", status=200):
    def respond(request):
        seen.append(json.loads(request.content))
        assert request.url.path == "/v1/chat/completions"
        assert "authorization" not in request.headers
        return httpx.Response(status, json={
            "choices": [{"finish_reason": finish, "message": {"content": content}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 20}})
    return LLM("nemotron-quantum", budget, "local",
               base_url="http://localhost:8000/v1/",
               client=httpx.Client(transport=httpx.MockTransport(respond)))


def test_local_schema_and_zero_api_cost(monkeypatch):
    monkeypatch.delenv("NEMOTRON_API_KEY", raising=False)
    seen = []
    budget = Budget(None, max_calls=1)
    llm = local(budget, seen)
    assert llm.call("implement", "system", "prompt", SCHEMA) == {"x": "ok"}
    assert seen[0]["response_format"]["json_schema"]["schema"] == SCHEMA
    assert "output_config" not in seen[0] and "cache_control" not in seen[0]
    assert budget.usd == 0 and budget.input_tokens == 100 and budget.calls == 1
    with pytest.raises(BudgetExhausted):
        llm.call("implement", "system", "prompt", SCHEMA)
    assert len(seen) == 1


@pytest.mark.parametrize("kwargs", [
    {"content": "not json"}, {"content": '{"x":42}'},
    {"content": '{"x":"ok","extra":true}'}, {"finish": "length"}, {"status": 503},
])
def test_bad_responses_consume_call_and_raise(kwargs, monkeypatch):
    monkeypatch.delenv("NEMOTRON_API_KEY", raising=False)
    budget = Budget(None, max_calls=1)
    with pytest.raises(LLMError):
        local(budget, [], **kwargs).call("t", "s", "p", SCHEMA)
    assert budget.calls == 1 and budget.usd == 0


def test_resource_limits_without_prices(monkeypatch):
    budget = Budget(None, max_tokens=10)
    budget.charge("nemotron-quantum", 8, 2, local=True)
    assert budget.exhausted and budget.usd == 0
    timer = Budget(None, max_seconds=2)
    monkeypatch.setattr("a2m.llm.client.time.monotonic", lambda: timer.started + 3)
    assert timer.exhausted
    paid = Budget(0.01)
    paid.charge("claude-sonnet-5-5", 10000, 1000)
    assert paid.exhausted and paid.usd > 0
