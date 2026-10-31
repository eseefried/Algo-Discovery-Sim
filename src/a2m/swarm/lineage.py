"""Population memory. Deaths become negative feedback and earnings positive feedback, both
injected into the prompts and role affinities of newly spawned agents."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass, field

from a2m.swarm.agent import ROLES, Agent


@dataclass
class DeathRecord:
    agent_id: str
    tick: int
    generation: int
    families: list[str]
    roles: dict[str, int]
    earned: float
    reason: str


@dataclass
class SuccessRecord:
    agent_id: str
    tick: int
    family: str
    role: str
    amount: float
    gap: float


@dataclass
class Lineage:
    deaths: list[DeathRecord] = field(default_factory=list)
    successes: list[SuccessRecord] = field(default_factory=list)
    failures: list[tuple[str, str]] = field(default_factory=list)  # (family, diagnosis)

    def record_death(self, agent: Agent, tick: int):
        self.deaths.append(DeathRecord(agent.id, tick, agent.generation,
                                       sorted(agent.families_backed), dict(agent.roles_played),
                                       round(agent.earned, 3),
                                       agent.last_failure or "spent its energy without progress"))

    def record_success(self, agent_id: str, tick: int, family: str, role: str, amount: float,
                       gap: float):
        self.successes.append(SuccessRecord(agent_id, tick, family, role, round(amount, 3), gap))

    def record_failure(self, family: str, diagnosis: str):
        self.failures.append((family, diagnosis[:300]))

    def family_scores(self) -> dict[str, float]:
        s: dict[str, float] = defaultdict(float)
        for d in self.deaths:
            for f in d.families:
                s[f] -= 1.0
        for r in self.successes:
            s[r.family] += r.amount
        for fam, _ in self.failures:
            s[fam] -= 4.0  # a stalled or broken lineage outweighs its partial progress
        return dict(s)

    def role_affinities(self) -> dict[str, float]:
        """Roles that earned the most get the highest affinity in respawned agents."""
        earned = {r: 0.0 for r in ROLES}
        for r in self.successes:
            earned[r.role] = earned.get(r.role, 0.0) + r.amount
        total = sum(earned.values())
        if total <= 0:
            return {r: 1.0 for r in ROLES}
        return {r: 0.5 + 1.5 * earned[r] / total for r in ROLES}

    def prefer_avoid(self, k: int = 3) -> tuple[list[str], list[str]]:
        scores = self.family_scores()
        prefer = [f for f, v in sorted(scores.items(), key=lambda x: -x[1]) if v > 0][:k]
        avoid = [f for f, v in sorted(scores.items(), key=lambda x: x[1]) if v < 0][:k]
        return prefer, avoid

    def feedback(self, k: int = 3) -> str:
        prefer, avoid = self.prefer_avoid(k)
        lines = []
        if prefer:
            lines.append("- Method families that produced measured progress: " + ", ".join(prefer))
        if avoid:
            lines.append("- Families whose backers ran out of energy: " + ", ".join(avoid))
        for d in self.deaths[-k:]:
            lines.append(f"- {d.agent_id} died at round {d.tick}: {d.reason}")
        for fam, diag in self.failures[-k:]:
            lines.append(f"- {fam} failed: {diag}")
        return "\n".join(lines)

    def dump(self) -> dict:
        return {"deaths": [asdict(d) for d in self.deaths],
                "successes": [asdict(s) for s in self.successes],
                "failures": self.failures, "family_scores": self.family_scores()}
