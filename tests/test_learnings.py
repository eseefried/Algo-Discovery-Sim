"""Learnings artifacts: judged runs become shareable Markdown under skills/<domain>/learnings/."""

import json

import pytest

from a2m import learnings, skills
from a2m.judge.sealed import SealedJudge
from a2m.run import run


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Keep generated artifacts out of the checked-in skill tree."""
    tree = tmp_path / "skills"
    for domain in skills.available():
        (tree / domain).mkdir(parents=True)
        (tree / domain / "SKILL.md").write_text(
            (skills.root() / domain / "SKILL.md").read_text())
    monkeypatch.setenv("A2M_SKILLS_DIR", str(tree))
    monkeypatch.setenv("A2M_RUNS_DIR", str(tmp_path / "runs"))


def test_distilled_artifact_records_the_rubric_breakdown():
    run_dir = run("swarm", "arxiv-1407.6402", seed=0, llm_mode="mock", verbose=False)
    SealedJudge("mock", verbose=False).judge(run_dir)
    path = learnings.distill(run_dir)

    text = path.read_text()
    assert path.parent == skills.learnings_dir("quantum")
    assert "claim reproduced" in text and "method match" in text
    assert "## Which parts of the paper's method came back" in text
    assert "## Method families the run explored" in text
    # every rubric item of the task appears with a verdict
    judge = json.loads((run_dir / "judge.json").read_text())
    for item_id in judge["rubric_scores"]:
        assert f"| {item_id}:" in text
    assert any(mark in text for mark in ("| yes |", "| no |", "| partial |"))


def test_index_aggregates_recovery_rates_across_runs():
    for seed in (0, 1):
        d = run("swarm", "arxiv-1407.6402", seed=seed, llm_mode="mock", verbose=False)
        SealedJudge("mock", verbose=False).judge(d)
        learnings.distill(d)

    index = (skills.learnings_dir("quantum") / "INDEX.md").read_text()
    assert "2 judged run(s)" in index
    assert "## Method components by recovery rate" in index
    assert "## Runs" in index
    assert "arxiv-1407.6402" in index


def test_artifacts_are_not_reachable_from_an_agent_prompt():
    from a2m import domains

    d = run("swarm", "arxiv-1407.6402", seed=0, llm_mode="mock", verbose=False)
    SealedJudge("mock", verbose=False).judge(d)
    path = learnings.distill(d)

    sealed_phrase = "only appears as an unobservable global phase"  # sealed rubric wording
    assert sealed_phrase in path.read_text().lower()
    assert sealed_phrase not in domains.load("quantum").prompt_block().lower()


def test_unjudged_runs_are_refused():
    d = run("swarm", "arxiv-1407.6402", seed=0, llm_mode="mock", verbose=False)
    with pytest.raises(FileNotFoundError, match="judge it first"):
        learnings.distill(d)
