"""Shared index of open needs: the swarm's only coordination surface. No planner, no messages."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

NEED_ROLE = {"needs_hypothesis": "hypothesize", "needs_implementation": "implement",
             "needs_simulation": "simulate", "needs_critique": "critique"}


@dataclass
class Need:
    id: str
    kind: str
    candidate: str | None
    created: int
    promise: float = 0.5
    shared: bool = False  # several agents may serve it at once (hypotheses)
    claimed_by: set[str] = field(default_factory=set)
    exclude: set[str] = field(default_factory=set)  # agents that may not serve it

    @property
    def role(self) -> str:
        return NEED_ROLE[self.kind]


class SharedIndex:
    def __init__(self):
        self.needs: dict[str, Need] = {}
        self._ids = itertools.count(1)

    def open(self, kind: str, candidate: str | None, tick: int, promise: float = 0.5,
             shared: bool = False, exclude: set[str] | None = None) -> Need:
        n = Need(f"n{next(self._ids)}", kind, candidate, tick, promise, shared,
                 exclude=set(exclude or ()))
        self.needs[n.id] = n
        return n

    def close(self, need_id: str):
        self.needs.pop(need_id, None)

    def open_needs(self, agent_id: str | None = None) -> list[Need]:
        return [n for n in self.needs.values()
                if agent_id is None or agent_id not in n.exclude]

    def count(self, kind: str) -> int:
        return sum(n.kind == kind for n in self.needs.values())

    def summary(self) -> list[dict]:
        return [{"id": n.id, "kind": n.kind, "candidate": n.candidate, "promise": round(n.promise, 3),
                 "claimed_by": sorted(n.claimed_by)} for n in self.needs.values()]
