import json
import sys

import anthropic
import httpx
import httpx2
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from algo_discovery.api import app
from algo_discovery.code_generation import generate_code, load_code_request
from algo_discovery.code_schemas import CircuitValidation, CodeRequest
from algo_discovery.config import Settings
from algo_discovery.equations import GenerationError, sha256
from algo_discovery.prompt import user_message
from algo_discovery.sandbox import bounded_run, docker_command
from algo_discovery.schemas import EquationRequest, EquationResult, MathSpecification, Usage
from algo_discovery.source_checks import check_source

SOURCE = """from qiskit import QuantumCircuit

def build_circuit(instance):
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc
"""


def test_local_code_generation_preserves_validation_and_context(code_request, code_artifact, tmp_path, monkeypatch):
    def no_anthropic(*args, **kwargs):
        raise AssertionError("local code must not construct an Anthropic client")

    monkeypatch.setattr(anthropic, "Anthropic", no_anthropic)

    def respond(request):
        payload = json.loads(request.content)
        assert payload["model"] == "nemotron-quantum"
        assert [m["role"] for m in payload["messages"]] == ["system", "user", "assistant", "user"]
        assert "authorization" not in request.headers
        return httpx.Response(200, json={
            "model": "nemotron-quantum", "choices": [{"finish_reason": "stop",
            "message": {"content": json.dumps(code_artifact)}}],
            "usage": {"prompt_tokens": 200, "completion_tokens": 300},
        })

    settings = Settings(api_key="", backend="local", model="nemotron-quantum",
                        base_url="http://127.0.0.1:8000/v1", artifact_dir=tmp_path)
    request = code_request.model_copy(update={"validate_circuit": False})
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        result = generate_code(request, settings, client=client)
    assert result.backend == "local" and result.static_checks_passed
    assert result.usage.input_tokens == 200 and result.usage.output_tokens == 300
    assert (tmp_path / result.run_id / "circuit.py").exists()


def test_local_settings_need_no_claude_key(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("CLAUDE_HACKATHON_API", raising=False)
    monkeypatch.delenv("NEMOTRON_API_KEY", raising=False)
    settings = Settings.from_env(backend="local")
    assert settings.backend == "local" and settings.api_key == ""


@pytest.fixture
def code_request():
    original = EquationRequest(abstract="We apply a Hadamard gate to one qubit.")
    spec = MathSpecification(
        status="specified",
        problem="Hadamard operation",
        reconstruction_scope="One qubit",
        symbols=[],
        equations=[
            {
                "id": "eq_1",
                "label": "Hadamard",
                "latex": "H",
                "description": "Apply H",
                "provenance": "standard_background",
                "abstract_quote": None,
                "justification": "Definition",
                "assumptions": [],
            }
        ],
        registers=[],
        initial_state=None,
        steps=[],
        measurement=None,
        classical_postprocessing=None,
        assumptions=[],
        missing_information=[],
    )
    result = EquationResult(
        run_id="source-run",
        created_at="2026-10-31T00:00:00+00:00",
        model="claude-haiku-5-5",
        response_model="claude-haiku-5-5",
        prompt_version="test",
        prompt_sha256=sha256("prompt"),
        abstract_sha256=sha256(original.abstract),
        request_sha256=sha256(user_message(original)),
        elapsed_seconds=1,
        usage=Usage(input_tokens=1, output_tokens=1),
        stop_reason="end_turn",
        specification=spec,
    )
    return CodeRequest(equation_request=original, equation_result=result)


@pytest.fixture
def code_artifact():
    return {
        "status": "generated",
        "summary": "One-qubit Hadamard",
        "source_python": SOURCE,
        "example_instance_json": "{}",
        "register_layout": ["qubit 0: data"],
        "equation_mapping": [
            {
                "equation_id": "eq_1",
                "disposition": "implemented",
                "code_location": "build_circuit",
                "explanation": "qc.h(0)",
            }
        ],
        "specification_changes": [],
        "assumptions": [],
        "unresolved_issues": [],
    }


def sdk_client(artifact):
    def respond(request):
        payload = json.loads(request.content)
        assert len(payload["messages"]) == 3
        assert payload["messages"][1]["role"] == "assistant"
        assert json.loads(payload["messages"][1]["content"])["equations"][0]["id"] == "eq_1"
        assert payload["output_config"]["format"]["type"] == "json_schema"
        assert payload["model"] == "claude-haiku-5-5"
        return httpx2.Response(
            200,
            json={
                "id": "msg_code",
                "type": "message",
                "role": "assistant",
                "model": "claude-haiku-5-5",
                "content": [{"type": "text", "text": json.dumps(artifact)}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 200, "output_tokens": 300},
            },
        )

    return anthropic.Anthropic(
        api_key="test-key",
        max_retries=0,
        http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
    )


def test_generation_uses_math_context_and_saves_code(code_request, code_artifact, tmp_path):
    with sdk_client(code_artifact) as client:
        result = generate_code(
            code_request, Settings(api_key="test-key", artifact_dir=tmp_path), client=client
        )
    assert result.static_checks_passed
    assert result.validation.status == "not_run"
    assert result.parent_run_id == "source-run"
    directory = tmp_path / result.run_id
    assert (directory / "circuit.py").read_text().strip() == SOURCE.strip()
    assert "test-key" not in (directory / "result.json").read_text()
    assert (directory / "implementation.md").exists()


def test_unknown_equation_mapping_rejected(code_request, code_artifact, tmp_path):
    code_artifact["equation_mapping"][0]["equation_id"] = "invented"
    with sdk_client(code_artifact) as client, pytest.raises(GenerationError, match="mapping"):
        generate_code(code_request, Settings(api_key="test", artifact_dir=tmp_path), client=client)


def test_static_failure_never_executes(code_request, code_artifact, tmp_path, monkeypatch):
    code_artifact["source_python"] = "import os\n" + SOURCE
    code_request.validate_circuit = True

    def unexpected(*_):
        pytest.fail("Rejected source reached execution.")

    monkeypatch.setattr("algo_discovery.code_generation.validate_in_docker", unexpected)
    with sdk_client(code_artifact) as client:
        result = generate_code(
            code_request, Settings(api_key="test", artifact_dir=tmp_path), client=client
        )
    assert not result.static_checks_passed
    assert result.validation.status == "failed"
    assert (tmp_path / result.run_id / "circuit.py").exists()  # Retain failure for review.


def test_legacy_equation_run_and_hash_binding(code_request, tmp_path):
    original = tmp_path / "request.json"
    original.write_text(code_request.equation_request.model_dump_json())
    saved = code_request.equation_result.model_dump()
    saved.pop("parameters")
    result = tmp_path / "result.json"
    result.write_text(json.dumps(saved))
    assert load_code_request(result).equation_result.parameters is None
    original.write_text(
        EquationRequest(abstract="A different abstract is substituted here.").model_dump_json()
    )
    with pytest.raises(ValidationError, match="does not match"):
        load_code_request(result)


@pytest.mark.parametrize(
    "source",
    [
        "import os\n" + SOURCE,
        SOURCE + "\nopen('/tmp/unexpected','w')\n",
        SOURCE.replace("qc.h(0)", "qc.unitary([[1,0],[0,1]], [0])"),
        SOURCE.replace("qc.h(0)", "exec('pass')"),
        SOURCE.replace("qc.h(0)", "import math"),
        SOURCE.replace("qc.h(0)", "qc.__class__"),
        "from qiskit.circuit.library import UnitaryGate as U\n" + SOURCE,
    ],
)
def test_static_guardrails(source):
    with pytest.raises((ValueError, TypeError, SyntaxError)):
        check_source(source)


def test_pure_numeric_constants_are_accepted_without_evaluation():
    check_source("MAX_WEIGHT = 2 ** 20\n" + SOURCE)
    with pytest.raises(ValueError, match="exponents"):
        check_source("MAX_WEIGHT = 2 ** 1000000000\n" + SOURCE)
    with pytest.raises(ValueError, match="constants"):
        check_source("VALUE = callable_at_import()\n" + SOURCE)


def test_docker_command_has_required_isolation(tmp_path):
    command = docker_command("test-container", "sha256:" + "a" * 64, tmp_path)
    for flag in [
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--user=65534:65534",
        "--memory=1g",
        "--pids-limit=64",
    ]:
        assert flag in command
    assert not any(".env" in argument or "docker.sock" in argument for argument in command)


def test_worker_buffer_and_time_limits():
    with pytest.raises(ValueError, match="output limit"):
        bounded_run([sys.executable, "-c", "print('x'*100000)"], max_bytes=128)
    with pytest.raises(TimeoutError):
        bounded_run([sys.executable, "-c", "while True: pass"], timeout=0.1)


def test_qiskit_api(code_request, code_artifact, tmp_path, monkeypatch):
    settings = Settings(api_key="test", artifact_dir=tmp_path)
    with sdk_client(code_artifact) as client:
        result = generate_code(code_request, settings, client=client)
    monkeypatch.setattr("algo_discovery.api.Settings.from_env", lambda: settings)
    monkeypatch.setattr("algo_discovery.api.generate_code", lambda *_: result)
    with TestClient(app) as client:
        response = client.post("/qiskit", json=code_request.model_dump())
        assert response.status_code == 200
        assert response.json()["stage"] == "equations_to_qiskit"
        invalid = code_request.model_dump()
        invalid["equation_result"]["abstract_sha256"] = "mismatch"
        assert client.post("/qiskit", json=invalid).status_code == 422


def test_standalone_validation_needs_no_provider_key(tmp_path, monkeypatch, capsys):
    from algo_discovery.validate_cli import main

    code = tmp_path / "circuit.py"
    code.write_text(SOURCE)
    instance = tmp_path / "instance.json"
    instance.write_text("{}")
    report = tmp_path / "report.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-qiskit",
            "--code",
            str(code),
            "--instance-file",
            str(instance),
            "--report",
            str(report),
        ],
    )

    def no_credentials():
        pytest.fail("Standalone validation tried to load model credentials.")

    monkeypatch.setattr("algo_discovery.config.Settings.from_env", no_credentials)
    monkeypatch.setattr(
        "algo_discovery.validate_cli.validate_in_docker",
        lambda *_: (
            CircuitValidation(status="build_passed", detail="Test circuit built."),
            None,
        ),
    )
    assert main() == 0
    assert json.loads(report.read_text())["static_checks_passed"]
    assert json.loads(capsys.readouterr().out)["validation"]["status"] == "build_passed"
