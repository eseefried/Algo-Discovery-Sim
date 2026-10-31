import json
from dataclasses import replace

import anthropic
import httpx2
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from algo_discovery.api import app
from algo_discovery.config import ConfigurationError, Settings
from algo_discovery.equations import GenerationError, generate_equations, render_markdown
from algo_discovery.schemas import EquationRequest, MathSpecification

ABSTRACT = "We apply a Hadamard gate to a single qubit initially in the zero state."


@pytest.fixture
def spec():
    return {
        "status": "specified",
        "problem": "Prepare an equal superposition.",
        "reconstruction_scope": "One ideal qubit.",
        "symbols": [{"symbol": "H", "meaning": "Hadamard gate", "domain": "2x2 unitary"}],
        "equations": [
            {
                "id": "eq_1",
                "label": "Hadamard action",
                "latex": r"H|0\rangle=(|0\rangle+|1\rangle)/\sqrt{2}",
                "description": "Prepare the plus state.",
                "provenance": "standard_background",
                "abstract_quote": None,
                "justification": "Definition of the Hadamard gate.",
                "assumptions": [],
            }
        ],
        "registers": [{"name": "q", "size": "1", "role": "State register"}],
        "initial_state": "|0>",
        "steps": [{"description": "Apply H.", "equation_ids": ["eq_1"]}],
        "measurement": None,
        "classical_postprocessing": None,
        "assumptions": [],
        "missing_information": [],
    }


def mock_client(spec, *, stop_reason="end_turn", status_code=200):
    def handle(request):
        payload = json.loads(request.content)
        assert payload["model"] == "claude-fable-5-1"
        assert payload["output_config"]["format"]["type"] == "json_schema"
        assert payload["output_config"]["effort"] == "high"
        assert "tools" not in payload
        assert set(json.loads(payload["messages"][0]["content"])) == {
            "abstract",
            "experiment_scope",
        }
        if status_code != 200:
            return httpx2.Response(
                status_code,
                json={
                    "type": "error",
                    "error": {"type": "authentication_error", "message": "SECRET"},
                },
            )
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "claude-fable-5-1",
                "content": [{"type": "text", "text": json.dumps(spec)}],
                "stop_reason": stop_reason,
                "stop_sequence": None,
                "usage": {"input_tokens": 100, "output_tokens": 150},
            },
        )

    return anthropic.Anthropic(
        api_key="test-token",
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(handle)),
    )


def test_real_sdk_contract_and_artifacts(spec, tmp_path):
    settings = Settings(api_key="test-token", artifact_dir=tmp_path)
    request = EquationRequest(abstract=ABSTRACT)
    with mock_client(spec) as client:
        result = generate_equations(request, settings, client=client)
    assert not result.mathematics_verified
    assert result.usage.input_tokens == 100
    assert result.specification.equations[0].provenance == "standard_background"
    directory = tmp_path / result.run_id
    assert {p.name for p in directory.iterdir()} == {"request.json", "result.json", "equations.md"}
    saved = (directory / "result.json").read_text()
    assert "test-token" not in saved
    assert "not been independently verified" in render_markdown(result)
    assert json.loads(saved)["abstract_sha256"] == result.abstract_sha256
    assert result.prompt_sha256 and result.request_sha256
    assert result.parameters.effort == "high"


def test_fabricated_quote_is_rejected(spec, tmp_path):
    spec["equations"][0].update(
        provenance="abstract_inferred", abstract_quote="The paper contains this equation."
    )
    with mock_client(spec) as client, pytest.raises(GenerationError, match="exact-quote"):
        generate_equations(
            EquationRequest(abstract=ABSTRACT),
            Settings(api_key="test", artifact_dir=tmp_path),
            client=client,
        )
    assert not list(tmp_path.iterdir())


def test_actual_abstract_quote_is_accepted(spec):
    spec["equations"][0].update(
        provenance="abstract_inferred", abstract_quote="apply a Hadamard gate"
    )
    MathSpecification.model_validate(spec).validate_evidence(ABSTRACT)


@pytest.mark.parametrize("mutation", ["duplicate_id", "unknown_reference", "hidden_assumption"])
def test_inconsistent_specifications_are_rejected(spec, mutation):
    if mutation == "duplicate_id":
        spec["equations"].append(spec["equations"][0].copy())
    elif mutation == "unknown_reference":
        spec["steps"][0]["equation_ids"] = ["nonexistent"]
    else:
        spec["equations"][0]["assumptions"] = ["A missing construction is guessed."]
    with pytest.raises(ValidationError):
        MathSpecification.model_validate(spec)


def test_abstention_can_have_no_equations(spec):
    spec.update(
        status="insufficient_information",
        equations=[],
        steps=[],
        missing_information=["The oracle is not defined."],
    )
    assert MathSpecification.model_validate(spec).equations == []


def test_provider_errors_do_not_echo_secrets(spec, tmp_path):
    settings = Settings(api_key="test-token", artifact_dir=tmp_path)
    with (
        mock_client(spec, status_code=401) as client,
        pytest.raises(GenerationError, match="HTTP 401") as caught,
    ):
        generate_equations(EquationRequest(abstract=ABSTRACT), settings, client=client)
    assert "SECRET" not in str(caught.value)
    assert "test-token" not in repr(settings)


@pytest.mark.parametrize("stop_reason", ["max_tokens", "refusal"])
def test_incomplete_or_refused_output_is_rejected(spec, tmp_path, stop_reason):
    with mock_client(spec, stop_reason=stop_reason) as client, pytest.raises(GenerationError):
        generate_equations(
            EquationRequest(abstract=ABSTRACT),
            Settings(api_key="test", artifact_dir=tmp_path),
            client=client,
        )
    assert not list(tmp_path.iterdir())


def test_request_rejects_short_abstract_and_unexpected_fields():
    with pytest.raises(ValidationError):
        EquationRequest(abstract="too short")
    with pytest.raises(ValidationError):
        EquationRequest(abstract=ABSTRACT, paper_path="evaluator/private.txt")


def test_configuration_validation():
    with pytest.raises(ConfigurationError, match="CLAUDE_HACKATHON_API"):
        Settings(api_key="")
    settings = Settings(api_key="test")
    with pytest.raises(ConfigurationError, match="HTTPS"):
        replace(settings, base_url="http://untrusted.example")
    with pytest.raises(ConfigurationError, match="query"):
        replace(settings, base_url="https://api.anthropic.com?key=secret")
    with pytest.raises(ConfigurationError, match="CLAUDE_EFFORT"):
        replace(settings, effort="invalid")


def test_api_validation_does_not_call_model():
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        assert client.post("/equations", json={"abstract": "short"}).status_code == 422


def test_api_success_and_safe_error(spec, tmp_path, monkeypatch):
    settings = Settings(api_key="test", artifact_dir=tmp_path)
    with mock_client(spec) as sdk_client:
        result = generate_equations(EquationRequest(abstract=ABSTRACT), settings, client=sdk_client)
    monkeypatch.setattr("algo_discovery.api.Settings.from_env", lambda: settings)
    monkeypatch.setattr("algo_discovery.api.generate_equations", lambda *_: result)
    with TestClient(app) as client:
        response = client.post("/equations", json={"abstract": ABSTRACT})
        assert response.status_code == 200
        assert response.json()["mathematics_verified"] is False

        def fail(*_):
            raise GenerationError("Claude API connection failed or timed out.")

        monkeypatch.setattr("algo_discovery.api.generate_equations", fail)
        assert client.post("/equations", json={"abstract": ABSTRACT}).status_code == 502
