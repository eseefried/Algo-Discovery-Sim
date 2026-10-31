"""Collective survival. Several colonies (each a Swarm) share one dollar budget. A colony lives
on a treasury; colonies that run dry, die out, or stall are removed, and new colonies are
founded from the genome and history of the survivors.

Survival modes (configs/systems/swarm_*.yaml):
  collective  agents are immortal; every cost and payout goes through the colony treasury
  both        agents live on their own energy and die; the colony taxes their earnings and
              pays for respawns and upkeep, and dies when its treasury is exhausted
  individual  agents die, colonies do not (use with selection: false as the control for
              "several colonies, no colony-level selection")
"""

from __future__ import annotations

import dataclasses
import json
import math
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from a2m import domains
from a2m.llm.client import LLM
from a2m.schema import Candidate
from a2m.swarm.economy import SURVIVAL_MODES
from a2m.swarm.runtime import Swarm, SwarmConfig
from a2m.workspace import Workspace, select

FINISHED = ("budget", "enough ready candidates")


@dataclass
class Genome:
    """What colony-level selection acts on. Agents inherit it at birth."""

    role_bias: dict[str, float]
    min_families: int
    max_attempts: int
    critiques_required: int

    @classmethod
    def default(cls, cfg: SwarmConfig, domain: str = "quantum") -> Genome:
        """Seed a colony from its field's profile; the system config still wins where set."""
        profile = domains.get(domain)
        g = profile.colony_genome
        return cls(dict(profile.role_bias),
                   int(g.get("min_families", cfg.min_families)),
                   int(g.get("max_attempts", cfg.max_attempts)),
                   int(g.get("critiques_required", cfg.critiques_required)))

    def mutate(self, rng: random.Random, noise: float) -> Genome:
        def step(v: int, lo: int, hi: int) -> int:
            return min(hi, max(lo, v + rng.choice((-1, 0, 0, 1))))

        return Genome(
            {r: round(min(4.0, max(0.25, b * math.exp(rng.gauss(0, noise)))), 3)
             for r, b in self.role_bias.items()},
            step(self.min_families, 1, 5), step(self.max_attempts, 1, 5),
            step(self.critiques_required, 0, 2))

    def apply(self, cfg: SwarmConfig) -> SwarmConfig:
        return dataclasses.replace(cfg, min_families=self.min_families,
                                   max_attempts=self.max_attempts,
                                   critiques_required=self.critiques_required,
                                   critics_enabled=cfg.critics_enabled and self.critiques_required > 0)


@dataclass
class ColonyConfig:
    survival: str = "collective"
    n_colonies: int = 3
    selection: bool = True          # False: colonies never die or reproduce (control)
    max_rounds: int = 25
    initial_treasury: float = 24.0  # also the grant for a replacement colony
    tax: float = 0.3                # both: share of agent earnings paid to the colony
    respawn_cost: float = 3.0       # both: colony pays to replace a dead agent
    upkeep: float = 0.1             # both: per living agent per round
    found_threshold: float = 48.0   # a colony this rich founds a daughter
    found_cost: float = 24.0        # paid by the parent, becomes the daughter's treasury
    max_foundings: int = 6
    max_colonies: int = 4
    genome_noise: float = 0.3
    stop_when_ready: int = 2
    max_submissions: int = 3
    parallel_colonies: bool = True


@dataclass
class ColoniesConfig:
    swarm: SwarmConfig = field(default_factory=SwarmConfig)
    colony: ColonyConfig = field(default_factory=ColonyConfig)

    @property
    def models(self) -> list[str]:
        return self.swarm.models

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ColoniesConfig:
        colony = dict(d.get("colony", {}))
        colony.setdefault("survival", d.get("survival", "collective"))
        if colony["survival"] not in SURVIVAL_MODES:
            raise ValueError(f"survival must be one of {SURVIVAL_MODES}")
        return cls(SwarmConfig.from_dict(d.get("swarm", {})), ColonyConfig(**colony))


@dataclass
class Colony:
    id: str
    swarm: Swarm
    ws: Workspace
    genome: Genome
    parent: str | None
    founded: int
    alive: bool = True
    finished: str | None = None   # stopped without dying (budget, success, dormant)
    died: int | None = None
    cause: str = ""

    @property
    def treasury(self) -> float | None:
        return self.swarm.economy.treasury

    def best_gap(self) -> float:
        return min((c.gap for c in self.ws.candidates.values() if c.results), default=1.0)

    def ready_families(self) -> list[str]:
        return sorted({c.family for c in self.ws.candidates.values() if c.status == "ready"})

    def summary(self) -> dict[str, Any]:
        st = self.swarm
        return {"id": self.id, "parent": self.parent, "founded": self.founded,
                "alive": self.alive, "finished": self.finished, "died": self.died,
                "cause": self.cause, "treasury": None if self.treasury is None
                else round(self.treasury, 3), "genome": dataclasses.asdict(self.genome),
                "agents_born": len(st.agents), "agent_deaths": len(st.lineage.deaths),
                "respawns": st.respawns, "spawns": st.spawns,
                "families": self.ws.families(), "ready_families": self.ready_families(),
                "best_gap": round(self.best_gap(), 4), "candidates": len(self.ws.candidates)}


@dataclass
class ColonyDeath:
    colony: str
    round: int
    cause: str
    families: list[str]
    best_gap: float
    genome: dict[str, Any]


class Colonies:
    name = "colonies"

    def __init__(self, ws: Workspace, llms: dict[str, LLM], cfg: ColoniesConfig, seed: int):
        self.ws, self.llms, self.cfg = ws, llms, cfg
        self.c = cfg.colony
        self.rng = random.Random(seed)
        self.colonies: list[Colony] = []
        self.deaths: list[ColonyDeath] = []
        self.foundings = 0
        self._k = 0

    # ------------------------------------------------------------ founding

    def _feedback(self, parent: Colony | None) -> str:
        lines = []
        for d in self.deaths[-3:]:
            fams = ", ".join(d.families) or "nothing"
            lines.append(f"- Colony {d.colony} died at round {d.round} ({d.cause}) after "
                         f"pursuing {fams}; best gap {d.best_gap:.2f}.")
        if parent is not None:
            ready = ", ".join(parent.ready_families())
            lines.append(f"- Founded from colony {parent.id}"
                         + (f", which has ready candidates in: {ready}." if ready else "."))
            inherited = parent.swarm.lineage.feedback()
            if inherited:
                lines.append("Lessons inherited from that colony:\n" + inherited)
        return "\n".join(lines)

    def _found(self, parent: Colony | None, treasury: float, tick: int,
               genome: Genome | None = None) -> Colony:
        self._k += 1
        cid = f"k{self._k}"
        if genome is None:
            base = parent.genome if parent else Genome.default(self.cfg.swarm,
                                                               self.ws.card.domain)
            # the first colony keeps the default genome; the others vary it
            genome = base if (parent is None and self._k == 1) else base.mutate(
                self.rng, self.c.genome_noise)
        sub = Workspace(self.ws.card, self.ws.sandbox, self.ws.budget,
                        self.ws.run_dir / "colonies" / cid, self.ws.verbose, prefix=f"{cid}-")
        mortal_colony = self.c.survival != "individual"
        swarm = Swarm(sub, self.llms, genome.apply(self.cfg.swarm), self.rng.randrange(1 << 30),
                      colony_id=f"{cid}-", survival=self.c.survival,
                      treasury=treasury if mortal_colony else None, tax=self.c.tax,
                      respawn_cost=self.c.respawn_cost, upkeep=self.c.upkeep,
                      role_bias=genome.role_bias, inherited_notes=self._feedback(parent))
        swarm.start(tick)
        col = Colony(cid, swarm, sub, genome, parent.id if parent else None, tick)
        self.colonies.append(col)
        self.ws.log("colony_founded", colony=cid, parent=col.parent,
                    treasury=treasury if mortal_colony else None, genome=dataclasses.asdict(genome))
        return col

    # --------------------------------------------------------------- loop

    def alive(self) -> list[Colony]:
        return [c for c in self.colonies if c.alive]

    def _active(self) -> list[Colony]:
        return [c for c in self.colonies if c.alive and c.finished is None]

    def _ready_total(self) -> int:
        return len({f for c in self.colonies for f in c.ready_families()})

    def _end(self, col: Colony, reason: str, tick: int):
        if reason in FINISHED or not self.c.selection:
            col.finished = reason if reason in FINISHED else f"dormant: {reason}"
            self.ws.log("colony_stopped", colony=col.id, reason=col.finished)
        else:
            col.alive, col.died, col.cause = False, tick, reason
            self.deaths.append(ColonyDeath(col.id, tick, reason, col.ws.families(),
                                           round(col.best_gap(), 4), dataclasses.asdict(col.genome)))
            self.ws.log("colony_death", colony=col.id, cause=reason,
                        best_gap=round(col.best_gap(), 4), families=",".join(col.ws.families()))
        col.swarm.finish(reason)

    def _select(self, tick: int, newly_dead: int):
        """Replace dead colonies from the fittest survivor, and let rich colonies reproduce."""
        if not self.c.selection or self.ws.budget.exhausted:
            return

        def fitness(c: Colony):
            return (len(c.ready_families()), -c.best_gap(), c.treasury or 0.0)

        for _ in range(newly_dead):
            if self.foundings >= self.c.max_foundings or len(self.alive()) >= self.c.max_colonies:
                break
            living = [c for c in self.alive() if c.finished is None] or self.alive()
            if living:
                parent = max(living, key=fitness)
                self._found(parent, self.c.initial_treasury, tick)
            else:  # extinction: refound from the best dead genome
                best = min(self.deaths, key=lambda d: d.best_gap)
                self._found(None, self.c.initial_treasury, tick,
                            Genome(**best.genome).mutate(self.rng, self.c.genome_noise))
            self.foundings += 1
        for col in sorted(self._active(), key=lambda c: -(c.treasury or 0.0)):
            if self.foundings >= self.c.max_foundings or len(self.alive()) >= self.c.max_colonies:
                break
            if (col.treasury or 0.0) >= self.c.found_threshold and col.swarm.economy.colony_charge(
                    self.c.found_cost, "found_daughter", tick):
                self._found(col, self.c.found_cost, tick)
                self.foundings += 1

    def run(self) -> list[Candidate]:
        ws = self.ws
        for _ in range(self.c.n_colonies):
            self._found(None, self.c.initial_treasury, 0)
        reason = "max rounds"
        for tick in range(self.c.max_rounds):
            ws.tick = tick
            if ws.budget.exhausted:
                reason = "budget"
                break
            if self._ready_total() >= self.c.stop_when_ready:
                reason = "enough ready candidates"
                break
            active = []
            for col in self._active():
                stop = col.swarm.stop_reason()
                if stop:
                    self._end(col, stop, tick)
                else:
                    active.append(col)
            if active:
                if self.c.parallel_colonies and len(active) > 1:
                    with ThreadPoolExecutor(max_workers=len(active)) as pool:
                        list(pool.map(lambda c, t=tick: c.swarm.round(t), active))
                else:
                    for col in active:
                        col.swarm.round(tick)
            dead = 0
            for col in active:  # a treasury can run dry during the round
                stop = col.swarm.stop_reason()
                if stop and stop not in FINISHED and self.c.selection:
                    self._end(col, stop, tick)
                    dead += 1
            dead += sum(1 for c in self.colonies if c.died == tick and c not in active)
            self._select(tick, dead)
            if not self._active():
                reason = "no active colonies"
                break
        for col in self._active():
            col.finished = reason
            col.swarm.finish(reason)
        ws.log("colonies_end", reason=reason, colonies=len(self.colonies),
               colony_deaths=len(self.deaths), foundings=self.foundings,
               ready_families=self._ready_total())
        for col in self.colonies:
            ws.candidates.update(col.ws.candidates)
            (col.ws.run_dir / "stats.json").write_text(
                json.dumps(col.swarm.stats(), indent=1, default=str))
            col.ws.close()
        return select(ws.candidates.values(), self.c.max_submissions)

    def stats(self) -> dict[str, Any]:
        return {"survival": self.c.survival, "selection": self.c.selection,
                "colonies": [c.summary() for c in self.colonies],
                "colony_deaths": len(self.deaths), "foundings": self.foundings,
                "colony_lineage": [dataclasses.asdict(d) for d in self.deaths],
                "deaths": sum(len(c.swarm.lineage.deaths) for c in self.colonies),
                "respawns": sum(c.swarm.respawns for c in self.colonies),
                "spawns": sum(c.swarm.spawns for c in self.colonies)}
