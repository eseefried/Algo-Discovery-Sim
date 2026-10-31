"""Baseline: one model, one researcher. It hypothesises, implements, reads the runner's
diagnostics, repairs, and switches method when a lineage stalls. Same actions and runner as
the swarm, no economy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from a2m import actions
from a2m.llm.client import LLM
from a2m.schema import Candidate
from a2m.workspace import Workspace


@dataclass
class SingleAgentConfig:
    models: list[str] = field(default_factory=lambda: ["claude-fable-5-1"])
    max_steps: int = 40
    max_attempts: int = 3
    self_critique: bool = True
    diversity_first: bool = True
    max_submissions: int = 3

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SingleAgentConfig:
        known = set(cls.__dataclass_fields__)
        return cls(**{k: v for k, v in d.items() if k in known})


class SingleAgent:
    name = "single_agent"

    def __init__(self, ws: Workspace, llms: dict[str, LLM], cfg: SingleAgentConfig, seed: int):
        self.ws, self.cfg = ws, cfg
        self.llm = llms[cfg.models[0]]
        self.steps = 0

    def run(self) -> list[Candidate]:
        ws, who = self.ws, "solo"
        current: Candidate | None = None
        while self.steps < self.cfg.max_steps and not ws.budget.exhausted:
            ws.tick = self.steps
            self.steps += 1
            if current is None or current.attempts >= self.cfg.max_attempts:
                current = actions.hypothesize(ws, self.llm, who, diversity=self.cfg.diversity_first)
                continue
            if current.status in ("sketch", "failing", "broken"):
                nxt = actions.implement(ws, self.llm, who, current)
                if nxt is None:
                    continue
                current = nxt
                actions.simulate(ws, who, current)
                continue
            if current.status == "passing":
                if self.cfg.self_critique:
                    rec = actions.critique(ws, self.llm, who, current)
                    if rec is not None and rec["confirmed"]:
                        current.status = "broken"
                        continue
                current.status = "ready"
                ws.log("ready", cand=current.id, family=current.family)
                break
        return ws.submission_candidates(self.cfg.max_submissions)

    def stats(self) -> dict[str, Any]:
        return {"steps": self.steps}
