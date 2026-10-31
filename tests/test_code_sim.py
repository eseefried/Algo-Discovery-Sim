import json
from types import SimpleNamespace

import pytest

from algo_discovery import code_sim_cli, pipeline_cli
from algo_discovery.simulation import SimulationReport

ABSTRACT = "We apply a Hadamard gate to a single qubit initially in the zero state."
SPEC = {
    "status": "partial",
    "problem": "Prepare an equal superposition.",
    "reconstruction_scope": "One ideal qubit.",
    "symbols": [{"symbol": "H", "meaning": "Hadamard gate", "domain": "2x2 unitary"}],
    "equations": [
        {
            "id": "eq_1",
            "label": "Hadamard action",
            "latex": r"H|0\rangle=(|0\rangle+|1\rangle)/\sqrt{2}",
            "description": "Prepare the plus state.",
            "provenance": "abstract_explicit",
            "abstract_quote": "Hadamard gate to a single qubit",
            "justification": "Stated in the abstract.",
            "assumptions": [],
        }
    ],
    "registers": [{"name": "q", "size": "1", "role": "State register"}],
    "initial_state": "|0>",
    "steps": [{"description": "Apply H.", "equation_ids": ["eq_1"]}],
    "measurement": None,
    "classical_postprocessing": None,
    "assumptions": [],
    "missing_information": ["Nothing else is specified."],
}


@pytest.fixture
def stages(tmp_path, monkeypatch):
    """Stub the code model and Docker/Aer; the real hash-checked code request is built."""
    seen = {}
    monkeypatch.setenv("CLAUDE_HACKATHON_API", "test-key")
    monkeypatch.setenv("ARTIFACT_DIR", str(tmp_path))

    def code(request, settings):
        seen["request"] = request
        directory = settings.artifact_dir / "code1"
        directory.mkdir()
        (directory / "instance.json").write_text("{}")
        return SimpleNamespace(
            run_id="code1",
            static_checks_passed=True,
            artifact=SimpleNamespace(status="generated", source_python="def build_circuit(i): ..."),
            validation=SimpleNamespace(status="build_passed"),
        )

    def simulate(source, instance, reference, inputs, *, shots, seed):
        return "{}\n", SimulationReport(status="simulated", detail="stub", cases_run=1)

    monkeypatch.setattr(pipeline_cli, "generate_code", code)
    monkeypatch.setattr(pipeline_cli, "simulate_source", simulate)
    return SimpleNamespace(seen=seen, root=tmp_path)


def run_cli(monkeypatch, spec_file, *extra):
    monkeypatch.setattr("sys.argv", ["run-code-sim", "--spec", str(spec_file), *extra])
    return code_sim_cli.main()


def write(tmp_path, data):
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(data))
    return path


def test_swarm_spec_runs_through_the_same_code_stage(stages, tmp_path, monkeypatch, capsys):
    spec_file = write(tmp_path, {"source": "swarm", "abstract": ABSTRACT, "specification": SPEC})
    assert run_cli(monkeypatch, spec_file) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["stopped_at"] is None
    assert summary["equations"]["source"] == "swarm"
    request = stages.seen["request"]
    assert request.equation_request.abstract == ABSTRACT
    assert request.equation_result.specification.model_dump() == SPEC
    assert request.equation_result.model == "external:swarm"
    saved = stages.root / summary["equations"]["run_id"]
    assert {p.name for p in saved.iterdir()} >= {"request.json", "result.json", "equations.md"}


def test_block_one_result_is_accepted_and_labelled_single_agent(
    stages, tmp_path, monkeypatch, capsys
):
    from algo_discovery.config import Settings
    from algo_discovery.external_spec import ExternalSpec, save_as_equation_run

    settings = Settings(api_key="test", artifact_dir=tmp_path / "earlier")
    spec = ExternalSpec(source="x", abstract=ABSTRACT, specification=SPEC)
    result = save_as_equation_run(spec, settings)
    result_file = settings.artifact_dir / result.run_id / "result.json"
    assert run_cli(monkeypatch, result_file) == 0
    assert json.loads(capsys.readouterr().out)["equations"]["source"] == "single_agent"


@pytest.mark.parametrize(
    "data",
    [
        {"source": "swarm", "abstract": ABSTRACT, "specification": SPEC | {"equations": []}},
        {"source": "swarm", "specification": SPEC},
        {
            "source": "swarm",
            "abstract": ABSTRACT.replace("Hadamard", "Pauli"),
            "specification": SPEC,
        },
    ],
    ids=["schema", "no-abstract", "quote-not-in-abstract"],
)
def test_invalid_spec_is_a_counted_stage_stop(stages, tmp_path, monkeypatch, capsys, data):
    assert run_cli(monkeypatch, write(tmp_path, data)) == 2
    summary = json.loads(capsys.readouterr().out)
    assert summary["stopped_at"] == "equations"
    assert summary["equations"]["status"] == "invalid_spec"
    assert "request" not in stages.seen
