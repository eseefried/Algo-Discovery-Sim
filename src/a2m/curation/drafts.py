"""Curator tooling. Drafts are proposals for a human to check; nothing here creates a scored
task. A task becomes runnable only once a curator writes its claim card, evaluator, reference
and vault by hand (see docs/ADDING_TASKS.md)."""

from __future__ import annotations

import json
from pathlib import Path

from a2m import config
from a2m.evaluators import REGISTRY
from a2m.llm import prompts as P
from a2m.llm.client import LLM, Budget
from a2m.tasks import load_manifest

DRAFTS = Path("data/drafts")


def _record(task_id: str):
    for r in load_manifest():
        if r.id == task_id:
            return r
    raise SystemExit(f"{task_id} is not in {config.dataset_dir() / 'manifest.jsonl'}")


def draft(task_id: str, model: str = "claude-fable-5-1", max_usd: float = 3.0) -> Path:
    rec = _record(task_id)
    ds = config.dataset_dir()
    abstract = (ds / rec.files["abstract"]).read_text()
    paper = (ds / rec.files["paper"]).read_text()
    cap = (rec.proposed_simulation.get("total_qubit_budget") or [0, 12])[-1] or 12
    llm = LLM(model, Budget(max_usd), "anthropic", effort="high", max_tokens=32000)
    out = llm.call("draft_card", "You help curate a reproducibility benchmark.",
                   P.DRAFT_CARD.format(cap=cap, evaluators=", ".join(sorted(REGISTRY)),
                                       abstract=abstract, paper=paper),
                   P.DRAFT_CARD_SCHEMA)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    path = DRAFTS / f"{task_id}.json"
    path.write_text(json.dumps({"task_id": task_id, "title": rec.title, "model": model,
                                "status": "draft_unreviewed", **out}, indent=2))
    return path


def recall_check(task_id: str, models: list[str], max_usd: float = 1.0) -> Path:
    """Contamination probe: can a model name the paper or its method from the abstract?"""
    rec = _record(task_id)
    abstract = (config.dataset_dir() / rec.files["abstract"]).read_text()
    budget = Budget(max_usd)
    results = {}
    for m in models:
        llm = LLM(m, budget, "anthropic", effort="low")
        results[m] = llm.call("recall", "Answer factually.", P.RECALL.format(abstract=abstract),
                              P.RECALL_SCHEMA)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    path = DRAFTS / f"{task_id}.recall.json"
    path.write_text(json.dumps({"task_id": task_id, "true_title": rec.title,
                                "results": results, "usage": budget.snapshot()}, indent=2))
    return path
