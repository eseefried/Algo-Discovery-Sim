import json

import anthropic
import httpx2
import pytest
from test_swarm_runtime import FakeExecutor

from algo_discovery.config import Settings
from algo_discovery.swarm.model import HaikuExecutor, ProviderBlocked, response_contract
from algo_discovery.swarm.models import PENDING_EQUATIONS, REQUIREMENTS, initial_genotypes


def test_haiku_structured_contribution_uses_bounded_genotype_settings(monkeypatch):
    settings = Settings(api_key="test-key")
    genotype = initial_genotypes()[0]
    ctx = {
        "requirements": REQUIREMENTS,
        "already_completed": [],
        "abstract": "An abstract long enough for a quantum reconstruction.",
    }
    artifact, _ = FakeExecutor(settings).execute(ctx, genotype)
    ctx["current_specification"] = artifact.specification.model_dump()
    contract_result = {
        "completed_requirement_1": "problem",
        "completed_requirement_2": "equations",
        "specification_patch": artifact.specification.model_dump(),
        "child_groups": artifact.child_groups,
        "new_assumptions": [],
        "new_missing_information": [],
        "changes": [],
        "summary": artifact.summary,
    }

    def respond(request):
        payload = json.loads(request.content)
        assert payload["model"] == "claude-haiku-5-5"
        assert payload["max_tokens"] == 6144
        assert payload["output_config"]["effort"] == "medium"
        assert payload["output_config"]["format"]["type"] == "json_schema"
        assert "tools" not in payload
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "claude-haiku-5-5",
                "content": [{"type": "text", "text": json.dumps(contract_result)}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 100, "output_tokens": 50},
            },
        )

    client = anthropic.Anthropic(
        api_key="test-key",
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
    )
    monkeypatch.setattr("algo_discovery.swarm.model.anthropic.Anthropic", lambda **_: client)
    result, usage = HaikuExecutor(settings).execute(ctx, genotype)
    assert result.completed_requirements == ["problem", "equations"]
    assert usage["input_tokens"] == 100 and usage["output_tokens"] == 50


def test_provider_credit_error_is_actionable_without_echoing_key(monkeypatch):
    def respond(_):
        return httpx2.Response(
            400,
            headers={"request-id": "req_test"},
            json={
                "type": "error",
                "error": {
                    "type": "invalid_request_error",
                    "message": "Your credit balance is too low. test-key must never be echoed.",
                },
            },
        )

    client = anthropic.Anthropic(
        api_key="test-key",
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
    )
    monkeypatch.setattr("algo_discovery.swarm.model.anthropic.Anthropic", lambda **_: client)
    with pytest.raises(ProviderBlocked, match="credit balance") as caught:
        HaikuExecutor(Settings(api_key="test-key")).execute(
            {"requirements": ["audit"]}, initial_genotypes()[0]
        )
    assert "test-key" not in str(caught.value)
    assert "req_test" in str(caught.value)


def test_contract_schema_excludes_sibling_work_and_extra_progress_slots():
    genotype = initial_genotypes()[0].model_copy(update={"max_parts": 1})
    contract = response_contract({"requirements": ["circuit_plan", "measurement"]}, genotype)
    schema = contract.model_json_schema()
    assert "completed_requirement_2" not in schema["properties"]
    assert schema["properties"]["child_groups"]["items"]["items"]["enum"] == [
        "circuit_plan",
        "measurement",
    ]
    assert "equations" not in schema["$defs"]["SpecificationPatch"]["properties"]


def test_problem_only_contribution_before_equations_is_accepted(monkeypatch):
    """A first worker may finish only the problem; that must not fail the 'partial' rule."""
    settings = Settings(api_key="test-key")
    genotype = initial_genotypes()[0]
    ctx = {
        "requirements": REQUIREMENTS,
        "already_completed": [],
        "abstract": "An abstract long enough for a quantum reconstruction.",
    }
    artifact, _ = FakeExecutor(settings).execute(ctx, genotype)
    spec = artifact.specification.model_dump()
    ctx["current_specification"] = spec | {"equations": [], "steps": [], "missing_information": []}
    contract_result = {
        "completed_requirement_1": "problem",
        "completed_requirement_2": None,
        # What Haiku actually sent: status "partial" with the equations left for later.
        "specification_patch": ctx["current_specification"] | {"status": "partial"},
        "child_groups": [["equations", "circuit_plan"], ["measurement", "audit"]],
        "new_assumptions": [],
        "new_missing_information": [],
        "changes": [],
        "summary": "Problem stated; the rest is delegated.",
    }

    def respond(request):
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "claude-haiku-5-5",
                "content": [{"type": "text", "text": json.dumps(contract_result)}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 5},
            },
        )

    client = anthropic.Anthropic(
        api_key="test-key",
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
    )
    monkeypatch.setattr("algo_discovery.swarm.model.anthropic.Anthropic", lambda **_: client)
    result, _ = HaikuExecutor(settings).execute(ctx, genotype)
    assert result.completed_requirements == ["problem"]
    assert result.specification.status == "insufficient_information"
    assert result.specification.missing_information == [PENDING_EQUATIONS]
