import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from algo_discovery.config import Settings


@pytest.fixture
def batch():
    spec = importlib.util.spec_from_file_location("native_batch", Path("scripts/run_nemotron_native_batch.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_budget_counts_code_only_and_stops_before_new_requests(batch, tmp_path, monkeypatch):
    ids = tmp_path / "ids"
    ids.mkdir()
    (ids / "1411.5949.json").write_text("{}")
    out = tmp_path / "out"
    saved = out / "results" / "old"
    saved.mkdir(parents=True)
    (saved / "result.json").write_text(json.dumps({
        "stage": "equations_to_qiskit", "model": "claude-sonnet-5-5",
        "usage": {"input_tokens": 10000, "output_tokens": 0}}))
    assert batch.spend(out) == pytest.approx(0.02)
    monkeypatch.setattr(batch.Settings, "from_env", lambda **kw: Settings(api_key="test"))
    monkeypatch.setattr(batch.httpx, "get", lambda *a, **kw: pytest.fail("Budget must stop requests"))
    monkeypatch.setattr(batch.sys, "argv", ["batch", "--ids-dir", str(ids), "--out", str(out), "--max-usd", "0.01"])
    assert batch.main() == 3


def test_completed_papers_resume_without_model_calls(batch, tmp_path, monkeypatch):
    ids = tmp_path / "ids"
    ids.mkdir()
    (ids / "1411.5949.json").write_text("{}")
    out = tmp_path / "out"
    native = out / "native" / "1411.5949"
    native.mkdir(parents=True)
    (native / "result.json").write_text(json.dumps({
        "status": "complete", "abstract": "We use a quantum Fourier transform.",
        "equations": [{"index": 1, "latex": "U=F"}]}))
    monkeypatch.setattr(batch.Settings, "from_env", lambda **kw: Settings(api_key="test"))
    monkeypatch.setattr(batch.httpx, "get", lambda *a, **kw: SimpleNamespace(
        raise_for_status=lambda: None, json=lambda: {"data": [{"id": "nemotron-quantum"}]}))
    calls = []

    def code(args, settings, summary):
        calls.append(args.arxiv_id)
        summary.update(stopped_at="code", code={"status": "insufficient_information"})

    monkeypatch.setattr(batch, "code_sim", code)
    monkeypatch.setattr(batch.sys, "argv", ["batch", "--ids-dir", str(ids), "--out", str(out)])
    assert batch.main() == 0
    assert batch.main() == 0
    assert calls == ["1411.5949"]
