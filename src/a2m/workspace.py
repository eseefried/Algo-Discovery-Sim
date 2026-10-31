"""State shared by every system: candidates, trusted simulation, event log."""

from __future__ import annotations

import itertools
import json
import threading
import time
from pathlib import Path
from typing import Any

from a2m.evaluators import get as get_evaluator
from a2m.llm.client import Budget
from a2m.sandbox import Sandbox
from a2m.schema import Candidate, ClaimCard
from a2m.scoring import claim_gap, criterion_gap


class Workspace:
    def __init__(self, card: ClaimCard, sandbox: Sandbox, budget: Budget, run_dir: Path,
                 verbose: bool = True, prefix: str = ""):
        self.card, self.sandbox, self.budget, self.run_dir = card, sandbox, budget, run_dir
        self.evaluator = get_evaluator(card.evaluator)
        self.candidates: dict[str, Candidate] = {}
        self.verbose, self.prefix = verbose, prefix
        self.tick = 0
        self.t0 = time.time()
        self._ids = itertools.count(1)
        self._lock = threading.Lock()
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "candidates").mkdir(exist_ok=True)
        self._events = open(run_dir / "events.jsonl", "a")  # noqa: SIM115 - open for the run

    # ------------------------------------------------------------------ logging

    def log(self, kind: str, **data: Any):
        rec = {"t": round(time.time() - self.t0, 2), "tick": self.tick, "kind": kind, **data}
        with self._lock:
            self._events.write(json.dumps(rec, default=str) + "\n")
            self._events.flush()
        if self.verbose:
            brief = " ".join(f"{k}={v}" for k, v in data.items() if k not in ("reason", "error"))
            tag = f"{self.prefix:<4}" if self.prefix else ""
            print(f"[t{self.tick:02d} ${self.budget.usd:7.4f}] {tag}{kind:<12} {brief}"[:160],
                  flush=True)

    def close(self):
        self._events.close()

    # --------------------------------------------------------------- candidates

    def new_candidate(self, family: str, sketch: str, author: str) -> Candidate:
        with self._lock:
            cid = f"{self.prefix}c{next(self._ids):03d}"
        cand = Candidate(id=cid, family=family, sketch=sketch, chain=[(author, "hypothesize")])
        self.candidates[cid] = cand
        return cand

    def child(self, parent: Candidate) -> Candidate:
        with self._lock:
            cid = f"{self.prefix}c{next(self._ids):03d}"
        cand = Candidate(id=cid, parent=parent.id, family=parent.family, sketch=parent.sketch,
                         chain=list(parent.chain), attempts=parent.attempts, gap=parent.gap)
        self.candidates[cid] = cand
        return cand

    def families(self) -> list[str]:
        return sorted({c.family for c in self.candidates.values()})

    def parent_gap(self, cand: Candidate) -> float:
        return self.candidates[cand.parent].gap if cand.parent else 1.0

    def best_gap(self, exclude: str | None = None) -> float:
        gaps = [c.gap for c in self.candidates.values()
                if c.code and c.results and c.id != exclude]
        return min(gaps, default=1.0)

    # --------------------------------------------------------------- simulation

    def run_tests(self, code: str, systems) -> dict[str, dict[str, Any]]:
        return {t.name: self.evaluator.evaluate(code, t.params, self.sandbox,
                                                self.card.allowed_imports, self.card.qubit_cap)
                for t in systems}

    def simulate(self, cand: Candidate) -> float:
        cand.results = self.run_tests(cand.code, self.card.test_systems)
        cand.gap = claim_gap(self.card.criteria, cand.results)
        cand.status = "passing" if cand.gap == 0.0 else "failing"
        (self.run_dir / "candidates" / f"{cand.id}.py").write_text(cand.code)
        return cand.gap

    def stress_params(self) -> dict[str, Any]:
        """A suggested larger instance, offered to critics as an example."""
        base = dict(self.card.test_systems[-1].params)
        for key in ("n", "m"):
            if key in base:
                base[key] = int(base[key]) + 1
        return base

    def validate_stress(self, raw: str) -> dict[str, Any] | None:
        try:
            params = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            return None
        if not isinstance(params, dict):
            return None
        base = dict(self.card.test_systems[-1].params)
        if set(params) - set(base):
            return None
        merged = {**base, **params}
        size = int(merged.get("n", merged.get("m", 0)))
        if size < 1 or size > 6 or (isinstance(merged.get("instances"), int)
                                    and merged["instances"] > 64):
            return None
        return merged

    def diagnostics(self, cand: Candidate) -> str:
        lines = []
        for name, r in cand.results.items():
            if not r.get("ok"):
                lines.append(f"{name}: ERROR {r.get('error', '')[-1200:]}")
                continue
            m = r["metrics"]
            misses = [f"{c.metric}={m.get(c.metric)} (needs {c.comparator} {c.target})"
                      for c in self.card.criteria if criterion_gap(c, m.get(c.metric)) > 0]
            lines.append(f"{name}: metrics={json.dumps(m)}"
                         + (f"; misses: {', '.join(misses)}" if misses else "; meets claim"))
        for c in cand.critiques:
            if c.get("confirmed"):
                lines.append(f"stress test {c['stress_test']} failed: {c.get('stress_result')}")
        return "\n".join(lines)

    def ranked(self) -> list[Candidate]:
        return rank(self.candidates.values())

    def submission_candidates(self, k: int) -> list[Candidate]:
        return select(self.candidates.values(), k)


def _rank_key(c: Candidate):
    passes = sum(1 for k in c.critiques if not k.get("confirmed"))
    order = {"ready": 0, "passing": 1}.get(c.status, 2)
    cost = min((r.get("metrics", {}).get("two_qubit_gates", 1e9) for r in c.results.values()),
               default=1e9)
    return (order, c.gap, -passes, cost, c.id)


def rank(cands) -> list[Candidate]:
    """Best first: ready, then passing, then by gap; cheaper circuits break ties."""
    return sorted((c for c in cands if c.code and c.results), key=_rank_key)


def select(cands, k: int) -> list[Candidate]:
    """Top k, one per family where possible."""
    chosen, fams = [], set()
    ranked = rank(cands)
    for c in ranked:
        if c.family not in fams and len(chosen) < k:
            chosen.append(c)
            fams.add(c.family)
    for c in ranked:
        if len(chosen) >= k:
            break
        if c not in chosen:
            chosen.append(c)
    return chosen
