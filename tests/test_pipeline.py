import json
from types import SimpleNamespace

import pytest

from algo_discovery import pipeline_cli
from algo_discovery.simulation import SimulationReport

ABSTRACT = "A quantum circuit adds a weighted sum of data bits into an accumulator register."


@pytest.fixture
def stages(tmp_path, monkeypatch):
    """Stub the model-backed stages; the pipeline wiring is what is under test."""
    calls = []
    state = {"equation_status": "partial", "simulation_status": "reference_passed"}
    monkeypatch.setenv("CLAUDE_HACKATHON_API", "test-key")
    monkeypatch.setenv("ARTIFACT_DIR", str(tmp_path))

    def equations(request, settings):
        calls.append("equations")
        (settings.artifact_dir / "eq1").mkdir()
        spec = SimpleNamespace(status=state["equation_status"])
        return SimpleNamespace(run_id="eq1", specification=spec)

    def load(path, **kwargs):
        calls.append(("load", path.parent.name, kwargs["validate_circuit"]))
        return kwargs

    def code(request, settings):
        calls.append("code")
        directory = settings.artifact_dir / "code1"
        directory.mkdir()
        (directory / "instance.json").write_text('{"num_target_qubits": 3, "weights": [1, 2]}')
        return SimpleNamespace(
            run_id="code1",
            static_checks_passed=True,
            artifact=SimpleNamespace(status="generated", source_python="def build_circuit(i): ..."),
            validation=SimpleNamespace(status="reference_passed"),
        )

    def simulate(source, instance, reference, inputs, *, shots, seed):
        calls.append(("simulate", instance["weights"], reference, shots))
        report = SimulationReport(
            status=state["simulation_status"], detail="stub", cases_run=32, cases_passed=32
        )
        return '{"simulation": "stub"}\n', report

    monkeypatch.setattr(pipeline_cli, "generate_equations", equations)
    monkeypatch.setattr(pipeline_cli, "load_code_request", load)
    monkeypatch.setattr(pipeline_cli, "generate_code", code)
    monkeypatch.setattr(pipeline_cli, "simulate_source", simulate)
    return SimpleNamespace(calls=calls, state=state, root=tmp_path)


def run_cli(monkeypatch, *extra):
    argv = ["run-pipeline", "--abstract", ABSTRACT, *extra]
    monkeypatch.setattr("sys.argv", argv)
    return pipeline_cli.main()


def test_pipeline_chains_all_stages_and_saves_summary(stages, monkeypatch, capsys):
    assert run_cli(monkeypatch, "--reference", "modular_weighted_sum", "--shots", "64") == 0
    assert stages.calls == [
        "equations",
        ("load", "eq1", True),
        "code",
        ("simulate", [1, 2], "modular_weighted_sum", 64),
    ]
    summary = json.loads(capsys.readouterr().out)
    assert summary["stopped_at"] is None
    assert summary["simulation"]["status"] == "reference_passed"
    assert (stages.root / "code1" / "simulation.json").exists()
    assert json.loads((stages.root / "code1" / "pipeline.json").read_text()) == summary


def test_pipeline_stops_when_abstract_is_insufficient(stages, monkeypatch, capsys):
    stages.state["equation_status"] = "insufficient_information"
    assert run_cli(monkeypatch) == 2
    assert stages.calls == ["equations"]
    assert json.loads(capsys.readouterr().out)["stopped_at"] == "equations"


def test_pipeline_reports_failed_simulation(stages, monkeypatch, capsys):
    stages.state["simulation_status"] = "failed"
    assert run_cli(monkeypatch) == 2
    assert json.loads(capsys.readouterr().out)["stopped_at"] == "simulation"
