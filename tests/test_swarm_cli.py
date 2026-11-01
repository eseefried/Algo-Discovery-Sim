import json
from pathlib import Path

from algo_discovery.equations import GenerationError
from algo_discovery.swarm import cli


def test_blackbox_provider_failure_preserves_export_and_summary(tmp_path, monkeypatch, capsys):
    root_id = "test-root"
    output = tmp_path / "outputs"
    directory = output / root_id
    directory.mkdir(parents=True)
    spec = directory / "spec.json"
    spec.write_text("{}")
    monkeypatch.setenv("CLAUDE_HACKATHON_API", "not-used")
    monkeypatch.setattr(
        "sys.argv",
        [
            "run-swarm",
            "--db",
            str(tmp_path / "ledger.sqlite3"),
            "--abstract",
            "A sufficiently long abstract for the CLI fixture.",
            "--output-dir",
            str(output),
            "--blackbox",
        ],
    )
    monkeypatch.setattr(cli, "submit", lambda *_: root_id)
    monkeypatch.setattr(cli, "run_ecosystem", lambda *_, **__: None)
    monkeypatch.setattr(
        cli,
        "export",
        lambda *_: {
            "status": "completed",
            "specification_status": "partial",
            "specification": str(spec),
        },
    )

    def fail(*_):
        raise GenerationError("Provider account unavailable.")

    monkeypatch.setattr("algo_discovery.code_sim_cli.run", fail)
    assert cli.main() == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "completed"
    assert result["blackbox"]["exit_code"] == 1
    assert Path(result["specification"]).exists()
    assert json.loads((directory / "blackbox-summary.json").read_text())["stopped_at"] == "error"
