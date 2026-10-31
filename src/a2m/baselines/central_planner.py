"""Baseline: a planner model assigns every worker an action each round. Same workers, actions
and runner as the swarm; no economy, no index, no self-selection."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from a2m import actions
from a2m.llm import prompts as P
from a2m.llm.client import LLM, BudgetExhausted, LLMError
from a2m.schema import Candidate
from a2m.workspace import Workspace


@dataclass
class PlannerConfig:
    planner_model: str = "claude-opus-5-5"
    models: list[str] = field(default_factory=lambda: ["claude-haiku-5-5"])
    n_workers: int = 6
    max_ticks: int = 25
    max_attempts: int = 3
    critiques_required: int = 1
    stop_when_ready: int = 2
    max_submissions: int = 3
    parallel: int = 8

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> PlannerConfig:
        known = set(cls.__dataclass_fields__)
        return cls(**{k: v for k, v in d.items() if k in known})


class CentralPlanner:
    name = "central_planner"

    def __init__(self, ws: Workspace, llms: dict[str, LLM], cfg: PlannerConfig, seed: int):
        self.ws, self.cfg, self.llms = ws, cfg, llms
        self.planner = llms[cfg.planner_model]
        self.workers = [(f"w{i + 1}", cfg.models[i % len(cfg.models)]) for i in range(cfg.n_workers)]
        self.fallback_rounds = 0

    def _table(self) -> str:
        rows = []
        for c in self.ws.candidates.values():
            passes = sum(1 for k in c.critiques if not k["confirmed"])
            rows.append(f"{c.id} family={c.family} status={c.status} gap={c.gap:.3f} "
                        f"attempts={c.attempts} critiques_passed={passes}")
        return "\n".join(rows) or "(none yet)"

    def _heuristic(self) -> list[tuple[str, str, str]]:
        """Deterministic plan used when the planner's output is unusable."""
        self.fallback_rounds += 1
        cands = list(self.ws.candidates.values())
        queue = [("critique", c.id) for c in cands if c.status == "passing"]
        queue += [("implement", c.id) for c in cands if c.status == "sketch"]
        queue += [("implement", c.id) for c in sorted(cands, key=lambda c: c.gap)
                  if c.status in ("failing", "broken") and c.attempts < self.cfg.max_attempts
                  and not self._superseded(c)]
        plan = []
        for w, _ in self.workers:
            act, tgt = queue.pop(0) if queue else ("hypothesize", "")
            plan.append((w, act, tgt))
        return plan

    def _superseded(self, c: Candidate) -> bool:
        return any(o.parent == c.id for o in self.ws.candidates.values())

    def _plan(self) -> list[tuple[str, str, str]]:
        prompt = P.PLAN.format(k=len(self.workers), workers=", ".join(w for w, _ in self.workers),
                               candidates=self._table())
        try:
            out = self.planner.call("plan", P.render_system(self.ws.card), prompt, P.PLAN_SCHEMA, {})
        except (LLMError, BudgetExhausted) as e:
            self.ws.log("llm_error", who="planner", action="plan", error=str(e))
            return self._heuristic()
        names = {w for w, _ in self.workers}
        plan, seen = [], set()
        for a in out.get("assignments", []):
            if a["worker"] in names and a["worker"] not in seen:
                tgt = a.get("target", "")
                if a["action"] != "hypothesize" and tgt not in self.ws.candidates:
                    continue
                plan.append((a["worker"], a["action"], tgt))
                seen.add(a["worker"])
        return plan or self._heuristic()

    def _execute(self, worker: str, action: str, target: str):
        llm = self.llms[dict(self.workers)[worker]]
        cand = self.ws.candidates.get(target)
        if action == "hypothesize":
            return actions.hypothesize(self.ws, llm, worker)
        if action == "implement" and cand is not None:
            new = actions.implement(self.ws, llm, worker, cand)
            if new is not None:
                actions.simulate(self.ws, "runner", new)
            return new
        if action == "critique" and cand is not None and cand.status == "passing":
            return actions.critique(self.ws, llm, worker, cand)
        return None

    def run(self) -> list[Candidate]:
        ws = self.ws
        for tick in range(self.cfg.max_ticks):
            ws.tick = tick
            ready = len({c.family for c in ws.candidates.values() if c.status == "ready"})
            if ws.budget.exhausted or ready >= self.cfg.stop_when_ready:
                break
            plan = self._plan()
            ws.log("plan", assignments=json.dumps(plan))
            # one worker per candidate per round
            dedup, used = [], set()
            for w, act, tgt in plan:
                if tgt and tgt in used:
                    continue
                used.add(tgt)
                dedup.append((w, act, tgt))
            with ThreadPoolExecutor(max_workers=self.cfg.parallel) as pool:
                list(pool.map(lambda p: self._execute(*p), dedup))
            for c in ws.candidates.values():
                if c.status != "passing":
                    continue
                if c.critiques and c.critiques[-1]["confirmed"]:
                    c.status = "broken"
                elif sum(1 for k in c.critiques if not k["confirmed"]) >= self.cfg.critiques_required:
                    c.status = "ready"
                    ws.log("ready", cand=c.id, family=c.family)
        return ws.submission_candidates(self.cfg.max_submissions)

    def stats(self) -> dict[str, Any]:
        return {"fallback_rounds": self.fallback_rounds, "workers": self.workers}
