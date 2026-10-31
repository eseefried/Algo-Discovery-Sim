"""Pressure-scored matching: each agent picks the open need with the most pressure for its
role affinities. Sampling is softmax, so agents spread out instead of piling on one need."""

from __future__ import annotations

import math
import random

from a2m.swarm.index import Need

URGENCY = {"needs_simulation": 1.4, "needs_critique": 1.2, "needs_implementation": 1.0,
           "needs_hypothesis": 0.8}


def pressure(n: Need, tick: int) -> float:
    age = max(0, tick - n.created)
    return URGENCY.get(n.kind, 1.0) * (1 + 0.15 * age) * (0.3 + n.promise) / (1 + len(n.claimed_by))


def choose(needs: list[Need], affinities: dict[str, float], tick: int, rng: random.Random,
           temperature: float = 0.35) -> Need | None:
    if not needs:
        return None
    scores = [pressure(n, tick) * affinities.get(n.role, 0.5) for n in needs]
    top = max(scores)
    weights = [math.exp((s - top) / max(temperature, 1e-6)) for s in scores]
    return rng.choices(needs, weights=weights, k=1)[0]
