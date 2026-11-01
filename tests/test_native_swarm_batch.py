import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def batch():
    spec = importlib.util.spec_from_file_location("swarm_batch", Path("scripts/run_native_swarm_batch.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cohort_includes_completed_failures_but_excludes_inflight_papers(batch, tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    for paper in ("1411.5949", "1407.6402"):
        (logs / f"{paper}.done").touch()
    (logs / "1409.3305.json").write_text("{}")
    assert batch.completed_ids(tmp_path, 2) == ["1407.6402", "1411.5949"]
    with pytest.raises(ValueError):
        batch.completed_ids(tmp_path, 3)


def test_global_budget_stops_and_resume_skips_completed_papers(batch, tmp_path, monkeypatch):
    baseline = tmp_path / "baseline"
    (baseline / "logs").mkdir(parents=True)
    for paper in ("1407.6402", "1409.3305", "1411.5949"):
        (baseline / "logs" / f"{paper}.done").touch()
    out = tmp_path / "swarm"
    calls = []

    def fake_run(paper, directory, **kwargs):
        calls.append(paper)
        p = directory / "runs" / paper / "attempt"
        p.mkdir(parents=True)
        result = {"paper": paper, "status": "no_reviewed_candidate", "wall_seconds": 1,
                  "paid_budget": {"usd": 0.1}, "swarm": {"deaths": 1, "respawns": 1}}
        (p / "summary.json").write_text(json.dumps(result))
        return result

    monkeypatch.setattr(batch, "run", fake_run)
    monkeypatch.setattr(batch.httpx, "get", lambda *a, **kw: SimpleNamespace(
        raise_for_status=lambda: None, json=lambda: {"data": [{"id": "nemotron-quantum"}]}))
    args = ["batch", "--baseline", str(baseline), "--out", str(out), "--limit", "3", "--max-usd"]
    monkeypatch.setattr(batch.sys, "argv", [*args, "0.2"])
    assert batch.main() == 3
    assert calls == ["1407.6402", "1409.3305"]
    monkeypatch.setattr(batch.sys, "argv", [*args, "0.4"])
    assert batch.main() == 0
    assert calls == ["1407.6402", "1409.3305", "1411.5949"]
    assert batch.total_spend(out) == pytest.approx(0.3)
