"""Lennard-Jones clusters in reduced units: E = 4 sum_{i<j} (r^-12 - r^-6).

Shipped into the sandbox as `a2m_task` and imported by the trusted runner, so the objective a
candidate queries and the one the runner scores with are the same code. Public physics: the
task is the search strategy, not the potential.
"""

from __future__ import annotations

import numpy as np

# Global minima in reduced units. N=2, 5, 13 are Table 1 of Wales & Doye (cond-mat/9803344);
# the rest are reproduced by tests/test_domain_evaluators.py with independent restarts.
GLOBAL_MINIMA = {
    2: -1.000000, 3: -3.000000, 4: -6.000000, 5: -9.103852, 6: -12.712062,
    7: -16.505384, 8: -19.821489, 9: -24.113360, 10: -28.422532, 11: -32.765970,
    12: -37.967600, 13: -44.326801, 14: -47.845157, 15: -52.322627, 16: -56.815742,
    17: -61.317995, 18: -66.530949, 19: -72.659782, 20: -77.177043,
}


def energy(positions) -> float:
    """Total potential energy of an (N, 3) set of atom positions."""
    x = np.asarray(positions, dtype=float).reshape(-1, 3)
    diff = x[:, None, :] - x[None, :, :]
    r2 = np.einsum("ijk,ijk->ij", diff, diff)
    iu = np.triu_indices(len(x), 1)
    r2 = r2[iu]
    if np.any(r2 <= 0):
        return float("inf")
    inv6 = r2 ** -3.0
    return float(4.0 * np.sum(inv6 * inv6 - inv6))


def energy_forces(positions):
    """Energy and the (N, 3) forces, -dE/dx."""
    x = np.asarray(positions, dtype=float).reshape(-1, 3)
    diff = x[:, None, :] - x[None, :, :]
    r2 = np.einsum("ijk,ijk->ij", diff, diff)
    np.fill_diagonal(r2, np.inf)
    if np.any(r2 <= 0):
        return float("inf"), np.zeros_like(x)
    inv2 = 1.0 / r2
    inv6 = inv2 ** 3
    e = float(2.0 * np.sum(inv6 * inv6 - inv6))  # 4 * half the symmetric sum
    # dE/dr2 per pair = 4 * (-6 inv6^2 + 3 inv6) / r2 ; force = -dE/dx
    coef = 24.0 * inv2 * (2.0 * inv6 * inv6 - inv6)
    forces = np.einsum("ij,ijk->ik", coef, diff)
    return e, forces


def random_cluster(n: int, seed: int, radius: float = 5.5):
    """Atoms placed uniformly in a sphere, as in the paper's unseeded starts."""
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        p = rng.uniform(-radius, radius, 3)
        if np.dot(p, p) <= radius * radius:
            pts.append(p)
    return np.array(pts)


def is_connected(positions, cutoff: float = 1.6) -> bool:
    """Reject evaporated clusters: every atom must reach every other within `cutoff` hops."""
    x = np.asarray(positions, dtype=float).reshape(-1, 3)
    n = len(x)
    d = np.linalg.norm(x[:, None] - x[None], axis=-1)
    seen, stack = {0}, [0]
    while stack:
        i = stack.pop()
        for j in np.nonzero((d[i] <= cutoff) & (d[i] > 0))[0]:
            if int(j) not in seen:
                seen.add(int(j))
                stack.append(int(j))
    return len(seen) == n
