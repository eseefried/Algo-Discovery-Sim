"""End-to-end runs with the scripted mock LLM: every system finishes, writes its artifacts,
and the sealed judge can score it."""

import json

import pytest

from a2m import config
from a2m.judge.sealed import SealedJudge
from a2m.run import run


@pytest.fixture(autouse=True)
def _runs(tmp_path, monkeypatch):
    monkeypatch.setenv("A2M_RUNS_DIR", str(tmp_path / "runs"))


@pytest.mark.parametrize("system", ["swarm", "single_agent", "central_planner", "swarm_no_economy"])
def test_system_runs_and_is_judged(system):
    d = run(system, "arxiv-1407.6402", seed=0, llm_mode="mock", verbose=False)
    for f in ("submission.json", "events.jsonl", "all_candidates.json"):
        assert (d / f).exists()
    sub = json.loads((d / "submission.json").read_text())
    assert 1 <= len(sub["candidates"]) <= 3
    assert sub["usage"]["usd"] > 0 and sub["isolation"] in ("bwrap", "none")
    report = SealedJudge("mock", verbose=False).judge(d)
    assert report.claim_reproduced
    assert (d / "judge.md").exists()
    assert (config.runs_dir() / "latest").is_symlink()


def test_swarm_budget_is_enforced():
    d = run("swarm", "arxiv-1407.6402", seed=0, llm_mode="mock", budget_usd=0.002, verbose=False)
    sub = json.loads((d / "submission.json").read_text())
    # one round of parallel calls can overshoot slightly; nothing runs after that
    assert sub["usage"]["usd"] < 0.002 + 0.01


def test_swarm_kills_and_respawns_with_lineage_feedback(tmp_path):
    from a2m.llm.client import LLM, Budget
    from a2m.sandbox import Sandbox
    from a2m.swarm.economy import EconomyConfig
    from a2m.swarm.runtime import Swarm, SwarmConfig
    from a2m.tasks import load_card
    from a2m.workspace import Workspace

    budget = Budget(1.0)
    ws = Workspace(load_card("arxiv-1407.6402"), Sandbox(), budget, tmp_path / "r", verbose=False)
    cfg = SwarmConfig(n_agents=4, max_ticks=10, stagnation_ticks=10,
                      economy=EconomyConfig(initial_energy=1.5))
    swarm = Swarm(ws, {"claude-haiku-5-5": LLM("claude-haiku-5-5", budget, "mock", mock_seed=2)},
                  cfg, seed=2)
    swarm.run()
    st = swarm.stats()
    assert st["deaths"] >= 1 and st["respawns"] >= 1
    respawned = [a for a in st["agents"] if a["generation"] > 0 and a["parent"] is None]
    assert respawned and all(a["inherited_notes"] for a in respawned)
    assert all(d["reason"] for d in st["lineage"]["deaths"])


def test_judge_separates_paper_method_from_valid_alternative():
    d = run("swarm", "arxiv-1411.5949", seed=0, llm_mode="mock", verbose=False)
    report = SealedJudge("mock", verbose=False).judge(d)
    by_family = {c["family"]: c for c in report.all_candidates}
    assert by_family["qft_phase_adder"]["method_match"] >= 0.7
    if "controlled_increment_cascade" in by_family:
        alt = by_family["controlled_increment_cascade"]
        assert alt["claim_reproduced"] and alt["method_match"] < 0.5
