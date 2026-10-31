from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

ROLES = ("hypothesize", "implement", "simulate", "critique")


@dataclass
class Agent:
    id: str
    model: str
    energy: float
    affinities: dict[str, float]
    generation: int = 0
    parent: str | None = None
    notes: str = ""
    prefer: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=list)
    born_tick: int = 0
    alive: bool = True
    earned: float = 0.0
    spent: float = 0.0
    roles_played: Counter = field(default_factory=Counter)
    families_backed: set[str] = field(default_factory=set)
    last_failure: str = ""

    def summary(self) -> dict:
        return {"id": self.id, "model": self.model, "generation": self.generation,
                "parent": self.parent, "energy": round(self.energy, 3),
                "earned": round(self.earned, 3), "spent": round(self.spent, 3),
                "alive": self.alive, "roles": dict(self.roles_played),
                "families": sorted(self.families_backed),
                "affinities": {k: round(v, 3) for k, v in self.affinities.items()},
                "born_tick": self.born_tick, "inherited_notes": self.notes}
