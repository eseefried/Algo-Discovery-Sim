"""Survival economy. Every action costs energy; energy is earned only when the trusted runner
measures progress toward the claim, and flows back along the handover chain."""

from __future__ import annotations

from dataclasses import dataclass, field

from a2m.swarm.agent import Agent


@dataclass
class EconomyConfig:
    enabled: bool = True
    initial_energy: float = 6.0
    cost: dict[str, float] = field(default_factory=lambda: {
        "hypothesize": 1.0, "implement": 2.0, "simulate": 0.5, "critique": 1.0, "idle": 0.25})
    payout_scale: float = 4.0      # paid for closing the whole gap relative to the parent
    frontier_bonus: float = 2.0    # extra for beating the best gap anyone has reached
    ready_bonus: float = 8.0       # candidate survives critique
    credit: dict[str, float] = field(default_factory=lambda: {
        "hypothesize": 0.35, "implement": 0.45, "simulate": 0.20, "critique": 0.15})
    critic_bounty: float = 3.0     # confirmed break
    break_penalty: float = 1.5     # charged to the implementer of a confirmed break
    spawn_threshold: float = 14.0
    spawn_cost: float = 6.0


SURVIVAL_MODES = ("individual", "collective", "both")


class Economy:
    """Routes every energy movement according to the survival mode.

    individual  agents pay their own costs and keep their earnings; agents die at zero.
    collective  costs and earnings go to the colony treasury; agents never die, the colony does.
    both        agents pay their own costs; earnings are taxed into the treasury, which funds
                respawns and upkeep. Agents die at zero, and so can the colony.
    """

    def __init__(self, cfg: EconomyConfig, survival: str = "individual",
                 treasury: float | None = None, tax: float = 0.0):
        if survival not in SURVIVAL_MODES:
            raise ValueError(f"survival must be one of {SURVIVAL_MODES}, got {survival!r}")
        self.cfg, self.survival, self.tax = cfg, survival, tax
        self.treasury = treasury
        self.ledger: list[dict] = []

    def _move(self, agent: Agent, delta: float, why: str, tick: int):
        if not self.cfg.enabled or delta == 0:
            return
        if delta > 0:
            agent.earned += delta
        else:
            agent.spent -= delta
        if self.survival == "collective":
            self.treasury += delta
            self.ledger.append({"tick": tick, "agent": agent.id, "to": "treasury",
                                "delta": round(delta, 4), "why": why})
            return
        if self.survival == "both" and delta > 0 and self.tax > 0:
            cut = delta * self.tax
            self.treasury += cut
            self.ledger.append({"tick": tick, "agent": agent.id, "to": "treasury",
                                "delta": round(cut, 4), "why": f"tax:{why}"})
            delta -= cut
        agent.energy += delta
        self.ledger.append({"tick": tick, "agent": agent.id, "delta": round(delta, 4), "why": why})

    def colony_charge(self, amount: float, why: str, tick: int) -> bool:
        """Debit the treasury. Returns False (and moves nothing) if it cannot pay."""
        if not self.cfg.enabled or self.treasury is None or amount <= 0:
            return True
        if self.treasury < amount:
            return False
        self.treasury -= amount
        self.ledger.append({"tick": tick, "agent": "colony", "to": "treasury",
                            "delta": round(-amount, 4), "why": why})
        return True

    @property
    def agents_mortal(self) -> bool:
        return self.cfg.enabled and self.survival != "collective"

    @property
    def colony_mortal(self) -> bool:
        return self.cfg.enabled and self.survival != "individual" and self.treasury is not None

    def charge(self, agent: Agent, role: str, tick: int):
        self._move(agent, -self.cfg.cost.get(role, 1.0), f"cost:{role}", tick)

    def progress_payout(self, parent_gap: float, gap: float, best_gap: float) -> float:
        return (self.cfg.payout_scale * max(0.0, parent_gap - gap)
                + self.cfg.frontier_bonus * max(0.0, best_gap - gap))

    def distribute(self, chain: list[tuple[str, str]], amount: float, agents: dict[str, Agent],
                   tick: int, why: str):
        """Split `amount` by role. Within a role, the most recent contributor gets two thirds."""
        if amount <= 0:
            return
        for role, share in self.cfg.credit.items():
            ids = [a for a, r in chain if r == role]
            if not ids:
                continue
            latest, earlier = ids[-1], list(dict.fromkeys(ids[:-1]))
            earlier = [a for a in earlier if a != latest]
            parts = [(latest, 1.0)] if not earlier else [(latest, 2 / 3)] + [
                (a, 1 / (3 * len(earlier))) for a in earlier]
            for aid, frac in parts:
                if aid in agents and agents[aid].alive:
                    self._move(agents[aid], amount * share * frac, why, tick)

    def bounty(self, critic: Agent, implementer: Agent | None, tick: int):
        self._move(critic, self.cfg.critic_bounty, "critic_bounty", tick)
        if implementer is not None and implementer.alive:
            self._move(implementer, -self.cfg.break_penalty, "broken_by_critic", tick)

    def is_dead(self, agent: Agent) -> bool:
        return self.agents_mortal and agent.energy <= 0

    def can_spawn(self, agent: Agent) -> bool:
        return self.agents_mortal and agent.energy >= self.cfg.spawn_threshold

    def pay_spawn(self, parent: Agent, tick: int) -> float:
        self._move(parent, -self.cfg.spawn_cost, "spawn", tick)
        return self.cfg.spawn_cost
