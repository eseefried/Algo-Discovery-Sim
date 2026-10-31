"""Reference: basin-hopping (Wales & Doye, cond-mat/9803344, Secs. 2-3).

The energy surface is transformed into E~(X) = E(local minimum reached from X), a set of
interpenetrating staircases that leaves the global minimum unchanged. A canonical Monte Carlo
walk at T = 0.8 then runs on E~: displace every coordinate, minimize, accept or reject on the
*minimized* energies, and reset the coordinates to the minimum after a successful step. Step
size is tuned to a 0.5 acceptance ratio; surface atoms with the highest pair energy are moved
to a random point on the cluster surface (the paper's angular moves).
"""

import time

import numpy as np
from scipy.optimize import minimize

import a2m_task

TEMPERATURE = 0.8          # paper: reduced temperature of the MC walk
TARGET_ACCEPT = 0.5        # paper: step size tuned to this acceptance ratio
ANGULAR_FRACTION = 0.42    # paper: alpha, tuned to a 0.5 angular-move acceptance ratio


def _relax(x):
    """Local minimization: the transformation E -> E~ that defines the staircase surface."""
    def fun(flat):
        e, f = a2m_task.energy_forces(flat.reshape(-1, 3))
        return e, -f.ravel()

    res = minimize(fun, x.ravel(), jac=True, method="L-BFGS-B",
                   options={"maxiter": 2000, "ftol": 1e-14, "gtol": 1e-8})
    return float(res.fun), res.x.reshape(-1, 3)


def _pair_energies(x):
    d = np.linalg.norm(x[:, None] - x[None], axis=-1)
    np.fill_diagonal(d, np.inf)
    inv6 = d ** -6.0
    return (4.0 * (inv6 * inv6 - inv6)).sum(axis=1)


def _angular_move(x, rng):
    """Move the worst-bound atom to a random point on the cluster surface."""
    pair = _pair_energies(x)
    if pair.max() <= ANGULAR_FRACTION * pair.min():
        return None
    i = int(np.argmax(pair))
    centre = x.mean(axis=0)
    radius = float(np.linalg.norm(x - centre, axis=1).max())
    theta = rng.uniform(0, np.pi)
    phi = rng.uniform(0, 2 * np.pi)
    y = x.copy()
    y[i] = centre + radius * np.array([np.sin(theta) * np.cos(phi),
                                       np.sin(theta) * np.sin(phi), np.cos(theta)])
    return y


def search(spec):
    n, seed = int(spec["n"]), int(spec["seed"])
    deadline = time.time() + float(spec["time_budget_s"]) * 0.9
    rng = np.random.default_rng(seed)

    current_e, current_x = _relax(a2m_task.random_cluster(n, seed))
    best_e, best_x = current_e, current_x.copy()
    step, accepted, attempted = 0.38, 0, 0

    while time.time() < deadline:
        trial = _angular_move(current_x, rng)
        if trial is None:
            trial = current_x + rng.uniform(-1.0, 1.0, current_x.shape) * step
        energy, relaxed = _relax(trial)
        attempted += 1
        # Metropolis on the transformed (minimized) energies, not the raw ones.
        if energy < current_e or rng.random() < np.exp(-(energy - current_e) / TEMPERATURE):
            current_e, current_x = energy, relaxed  # reset coordinates to the minimum
            accepted += 1
            if energy < best_e:
                best_e, best_x = energy, relaxed.copy()
        if attempted % 20 == 0:  # keep the acceptance ratio near 0.5
            step *= 1.1 if accepted / attempted > TARGET_ACCEPT else 0.9
            step = float(np.clip(step, 0.05, 1.5))
            accepted = attempted = 0

    return best_x.tolist()
