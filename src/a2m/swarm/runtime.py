"""Decentralised swarm. Agents pick needs off a shared index by pressure; the economy decides
who survives; dead and successful agents shape the agents that replace them."""

from __future__ import annotations

import math
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from a2m import actions, domains
from a2m.llm.client import LLM
from a2m.schema import Candidate
from a2m.swarm.agent import ROLES, Agent
from a2m.swarm.economy import Economy, EconomyConfig
from a2m.swarm.index import Need, SharedIndex
from a2m.swarm.lineage import Lineage
from a2m.swarm.matching import choose
from a2m.workspace import Workspace


@dataclass
class SwarmConfig:
    models: list[str] = field(default_factory=lambda: ["claude-haiku-5-5"])
    n_agents: int = 6
    max_agents: int = 10
    max_ticks: int = 25
    max_respawns: int = 24
    diversity_first: bool = True
    min_families: int = 3
    critics_enabled: bool = True
    critiques_required: int = 1
    max_attempts: int = 3
    stop_when_ready: int = 2
    max_submissions: int = 3
    parallel: int = 8
    stagnation_ticks: int = 5
    affinity_noise: float = 0.3
    economy: EconomyConfig = field(default_factory=EconomyConfig)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SwarmConfig:
        d = dict(d)
        eco = EconomyConfig(**d.pop("economy", {}))
        known = set(cls.__dataclass_fields__)
        return cls(economy=eco, **{k: v for k, v in d.items() if k in known})


class Swarm:
    """One colony. Used on its own it is the individual-survival swarm; the colony layer
    (swarm/colonies.py) runs several of these with a treasury and colony-level selection."""

    name = "swarm"

    def __init__(self, ws: Workspace, llms: dict[str, LLM], cfg: SwarmConfig, seed: int,
                 colony_id: str = "", survival: str = "individual", treasury: float | None = None,
                 tax: float = 0.0, respawn_cost: float = 0.0, upkeep: float = 0.0,
                 role_bias: dict[str, float] | None = None, inherited_notes: str = ""):
        self.ws, self.llms, self.cfg = ws, llms, cfg
        self.rng = random.Random(seed)
        self.index = SharedIndex()
        self.economy = Economy(cfg.economy, survival, treasury, tax)
        self.colony_id = colony_id
        self.respawn_cost, self.upkeep = respawn_cost, upkeep
        # Agents start with the field's role mix (more critics where a wrong answer is
        # expensive, more implementers where the code is fiddly) unless a colony genome,
        # which may have mutated away from it, overrides.
        self.role_bias = role_bias or dict(domains.get(ws.card.domain).role_bias)
        self.inherited_notes = inherited_notes
        self.lineage = Lineage()
        self.agents: dict[str, Agent] = {}
        self.respawns = self.spawns = 0
        self.accepted: set[str] = set()
        self._last_progress = 0
        self._n = 0

    # ----------------------------------------------------------------- agents

    def _noisy(self, aff: dict[str, float]) -> dict[str, float]:
        s = self.cfg.affinity_noise
        return {r: max(0.05, aff.get(r, 1.0) * math.exp(self.rng.gauss(0, s))) for r in ROLES}

    def _new_agent(self, parent: Agent | None = None, energy: float | None = None) -> Agent:
        self._n += 1
        model = self.cfg.models[(self._n - 1) % len(self.cfg.models)]
        prefer, avoid = self.lineage.prefer_avoid()
        bias = {r: self.role_bias.get(r, 1.0) for r in ROLES}
        if parent is not None:
            aff, gen = self._noisy(parent.affinities), parent.generation + 1
            notes = self.lineage.feedback() or parent.notes
        elif self.lineage.deaths or self.lineage.successes:
            learned = self.lineage.role_affinities()
            aff = self._noisy({r: learned[r] * bias[r] for r in ROLES})
            gen = 1 + max((d.generation for d in self.lineage.deaths), default=0)
            notes = self.lineage.feedback()
        else:
            aff, gen, notes = self._noisy(bias), 0, ""
        if self.inherited_notes:
            notes = "\n".join(x for x in (self.inherited_notes, notes) if x)
        a = Agent(id=f"{self.colony_id}a{self._n:02d}", model=model,
                  energy=self.cfg.economy.initial_energy if energy is None else energy,
                  affinities=aff, generation=gen, parent=parent.id if parent else None,
                  notes=notes, prefer=prefer, avoid=avoid, born_tick=self.ws.tick)
        self.agents[a.id] = a
        return a

    def alive(self) -> list[Agent]:
        return [a for a in self.agents.values() if a.alive]

    # ------------------------------------------------------------------- loop

    def start(self, tick: int = 0):
        self.ws.tick = tick
        self._last_progress = tick
        for _ in range(self.cfg.n_agents):
            self._new_agent()
        self.ws.log("swarm_start", agents=len(self.agents), models=",".join(self.cfg.models),
                    survival=self.economy.survival, treasury=self.economy.treasury)

    def round(self, tick: int):
        """One round: open needs, act, settle, then births and deaths."""
        self.ws.tick = tick
        self._maintain_needs()
        self._step()
        self._lifecycle()

    def finish(self, reason: str):
        self.ws.log("swarm_end", reason=reason, ready=self._ready_count(),
                    deaths=len(self.lineage.deaths), spawns=self.spawns, respawns=self.respawns,
                    treasury=self.economy.treasury)

    def run(self) -> list[Candidate]:
        self.start()
        reason = "max rounds"
        for tick in range(self.cfg.max_ticks):
            self.ws.tick = tick
            stop = self.stop_reason()
            if stop:
                reason = stop
                self.ws.log("stop", reason=stop)
                break
            self.round(tick)
        self.finish(reason)
        return self.ws.submission_candidates(self.cfg.max_submissions)

    def _ready_count(self) -> int:
        """Distinct method families with a ready candidate."""
        return len({c.family for c in self.ws.candidates.values() if c.status == "ready"})

    def stop_reason(self) -> str | None:
        if self.ws.budget.exhausted:
            return "budget"
        if self._ready_count() >= self.cfg.stop_when_ready:
            return "enough ready candidates"
        if not self.alive():
            return "population extinct"
        if self.economy.colony_mortal and self.economy.treasury <= 0:
            return "treasury exhausted"
        if self.ws.tick - self._last_progress >= self.cfg.stagnation_ticks:
            return f"no progress for {self.cfg.stagnation_ticks} rounds"
        return None

    def _maintain_needs(self):
        if self.index.count("needs_hypothesis"):
            return
        few = self.cfg.diversity_first and len(self.ws.families()) < self.cfg.min_families
        if few or not self.index.needs:
            self.index.open("needs_hypothesis", None, self.ws.tick, promise=0.5, shared=True)

    def _step(self):
        tick, plan, taken = self.ws.tick, [], set()
        agents = self.alive()
        self.rng.shuffle(agents)
        for agent in agents:
            needs = [n for n in self.index.open_needs(agent.id) if n.shared or n.id not in taken]
            need = choose(needs, agent.affinities, tick, self.rng)
            if need is not None:
                need.claimed_by.add(agent.id)
                if not need.shared:
                    taken.add(need.id)
            plan.append((agent, need))
        with ThreadPoolExecutor(max_workers=self.cfg.parallel) as pool:
            results = list(pool.map(lambda p: self._execute(*p), plan))
        for (agent, need), res in zip(plan, results):
            self._apply(agent, need, res)

    def _execute(self, agent: Agent, need: Need | None):
        if need is None:
            return None
        llm = self.llms[agent.model]
        cand = self.ws.candidates.get(need.candidate) if need.candidate else None
        if need.kind == "needs_hypothesis":
            return actions.hypothesize(self.ws, llm, agent.id, agent.notes,
                                       self.cfg.diversity_first, agent.prefer, agent.avoid)
        if need.kind == "needs_implementation":
            return actions.implement(self.ws, llm, agent.id, cand, agent.notes)
        if need.kind == "needs_simulation":
            return actions.simulate(self.ws, agent.id, cand)
        if need.kind == "needs_critique":
            return actions.critique(self.ws, llm, agent.id, cand)
        raise ValueError(need.kind)

    # ---------------------------------------------------------------- outcomes

    def _apply(self, agent: Agent, need: Need | None, res):
        tick = self.ws.tick
        role = need.role if need else "idle"
        self.economy.charge(agent, role, tick)
        agent.roles_played[role] += 1
        if need is None:
            return
        cand = self.ws.candidates.get(need.candidate) if need.candidate else None
        if need.kind == "needs_hypothesis":
            need.claimed_by.discard(agent.id)
            if res is None:
                agent.last_failure = "its hypothesis call failed"
                return
            if self.cfg.diversity_first and self._family_active(res.family):
                res.status = "broken"
                agent.last_failure = f"proposed {res.family}, which was already being pursued"
                self.ws.log("duplicate", who=agent.id, cand=res.id, family=res.family)
                return
            self.accepted.add(res.id)
            self._last_progress = tick
            agent.families_backed.add(res.family)
            self.index.open("needs_implementation", res.id, tick, promise=0.5)
            if not self.cfg.diversity_first or len(self.ws.families()) >= self.cfg.min_families:
                self.index.close(need.id)
            return
        self.index.close(need.id)
        if res is not None:
            self._last_progress = tick
        if need.kind == "needs_implementation":
            if res is None:
                agent.last_failure = f"failed to implement {cand.family}"
                self.index.open(need.kind, cand.id, tick, promise=need.promise)
                return
            agent.families_backed.add(res.family)
            self.index.open("needs_simulation", res.id, tick, promise=0.6)
        elif need.kind == "needs_simulation":
            self._after_simulation(agent, cand)
        elif need.kind == "needs_critique":
            self._after_critique(agent, cand, res)

    def _family_active(self, family: str) -> bool:
        """A family is active while an accepted lineage of it is ready or still has open work.
        A stalled family may be re-proposed as a fresh variant."""
        live = {n.candidate for n in self.index.needs.values() if n.candidate}
        for c in self.ws.candidates.values():
            if c.family != family:
                continue
            if c.status == "ready" or c.id in live:
                return True
        return False

    @staticmethod
    def _implementers(cand: Candidate) -> set[str]:
        """Nobody reviews their own code; everyone else in the chain may critique."""
        return {a for a, r in cand.chain if r == "implement"}

    def _implementer(self, cand: Candidate) -> Agent | None:
        ids = [a for a, r in cand.chain if r == "implement"]
        return self.agents.get(ids[-1]) if ids else None

    def _after_simulation(self, agent: Agent, cand: Candidate):
        tick, gap = self.ws.tick, cand.gap
        payout = self.economy.progress_payout(self.ws.parent_gap(cand), gap,
                                              self.ws.best_gap(exclude=cand.id))
        if payout > 0:
            self.economy.distribute(cand.chain, payout, self.agents, tick, f"progress:{cand.id}")
            for role, aid in {r: a for a, r in cand.chain}.items():
                self.lineage.record_success(aid, tick, cand.family, role,
                                            payout * self.cfg.economy.credit.get(role, 0), gap)
        if gap == 0.0:
            if self.cfg.critics_enabled:
                self.index.open("needs_critique", cand.id, tick, promise=1.0,
                                exclude=self._implementers(cand))
            else:
                self._ready(cand)
            return
        diag = self.ws.diagnostics(cand).splitlines()
        impl = self._implementer(cand)
        if impl is not None:
            impl.last_failure = f"{cand.family} candidate {cand.id} missed the claim: {diag[0][:200]}"
        if cand.attempts < self.cfg.max_attempts:
            self.index.open("needs_implementation", cand.id, tick, promise=max(0.05, 1 - gap))
        else:
            self.lineage.record_failure(cand.family, " | ".join(diag)[:300])
            self.ws.log("family_stalled", family=cand.family, cand=cand.id)

    def _after_critique(self, agent: Agent, cand: Candidate, rec: dict | None):
        tick = self.ws.tick
        critics = {k["critic"] for k in cand.critiques}
        if rec is None:
            self.index.open("needs_critique", cand.id, tick, promise=1.0,
                            exclude=self._implementers(cand) | critics)
            return
        if rec["confirmed"]:
            cand.status = "broken"
            impl = self._implementer(cand)
            self.economy.bounty(agent, impl, tick)
            if impl is not None:
                impl.last_failure = f"critic {agent.id} broke {cand.id} with {rec['stress_test']}"
            self.lineage.record_failure(cand.family, f"broken by stress test {rec['stress_test']}")
            if cand.attempts < self.cfg.max_attempts:
                self.index.open("needs_implementation", cand.id, tick, promise=0.8)
            return
        if rec["verdict"] == "break":
            agent.last_failure = f"its claimed break of {cand.id} did not reproduce"
        passes = sum(1 for k in cand.critiques if not k["confirmed"])
        if passes >= self.cfg.critiques_required:
            self._ready(cand)
        else:
            self.index.open("needs_critique", cand.id, tick, promise=1.0,
                            exclude=self._implementers(cand) | critics)

    def _ready(self, cand: Candidate):
        cand.status = "ready"
        chain = cand.chain + [(k["critic"], "critique") for k in cand.critiques if not k["confirmed"]]
        self.economy.distribute(chain, self.cfg.economy.ready_bonus, self.agents, self.ws.tick,
                                f"ready:{cand.id}")
        self.ws.log("ready", cand=cand.id, family=cand.family)

    # --------------------------------------------------------------- lifecycle

    def _lifecycle(self):
        tick = self.ws.tick
        self._pay_upkeep()
        for a in self.alive():
            if self.economy.is_dead(a):
                a.alive = False
                self.lineage.record_death(a, tick)
                self.ws.log("death", agent=a.id, gen=a.generation, reason=a.last_failure[:120])
        for a in sorted(self.alive(), key=lambda x: -x.energy):
            if len(self.alive()) >= self.cfg.max_agents:
                break
            if self.economy.can_spawn(a):
                child = self._new_agent(parent=a, energy=self.economy.pay_spawn(a, tick))
                self.spawns += 1
                self.ws.log("spawn", parent=a.id, child=child.id, gen=child.generation)
        while (len(self.alive()) < self.cfg.n_agents and self.respawns < self.cfg.max_respawns
               and not self.ws.budget.exhausted):
            # individual: respawns are free. both: the colony pays for each replacement.
            if self.economy.survival == "both" and not self.economy.colony_charge(
                    self.respawn_cost, "respawn", tick):
                self.ws.log("respawn_unfunded", treasury=round(self.economy.treasury, 3))
                break
            fresh = self._new_agent()
            self.respawns += 1
            self.ws.log("respawn", agent=fresh.id, gen=fresh.generation,
                        prefer=",".join(fresh.prefer), avoid=",".join(fresh.avoid))

    def _pay_upkeep(self):
        if self.economy.survival == "both" and self.upkeep > 0 and self.economy.cfg.enabled:
            due = self.upkeep * len(self.alive())
            self.economy.treasury -= due  # may go negative: the colony then dies
            self.economy.ledger.append({"tick": self.ws.tick, "agent": "colony", "to": "treasury",
                                        "delta": round(-due, 4), "why": "upkeep"})

    def stats(self) -> dict[str, Any]:
        return {"agents": [a.summary() for a in self.agents.values()],
                "survival": self.economy.survival, "treasury": self.economy.treasury,
                "deaths": len(self.lineage.deaths), "spawns": self.spawns,
                "respawns": self.respawns, "lineage": self.lineage.dump(),
                "ledger": self.economy.ledger, "open_needs": self.index.summary()}
