"""Dynamics: find the transition path between two stable states on an energy surface.

The candidate returns a path. The runner densely resamples it (so a coarse path cannot step
over a barrier unseen), takes its highest energy, and compares that with a barrier computed
independently of any path method: a bottleneck search on a fine grid, which returns the
lowest possible "highest energy" over all connecting paths.
"""

from __future__ import annotations

import heapq
from itertools import pairwise

import numpy as np
from scipy.optimize import minimize

from a2m.evaluators.base import CallEvaluator, failed
from a2m.skills import tool_module

p2 = tool_module("dynamics", "potential2d")

INTERFACE = """\
Write one Python module that defines:

  find_path(start: list, end: list, spec: dict) -> list[list[float]]

spec = {"n_images": <suggested number of points>, "seed": <int>, "time_budget_s": <float>}.

Return an ordered list of [x, y] points describing the path the system takes between the two
stable states `start` and `end`. The first point must be `start` and the last must be `end`.

The runner resamples your path densely before measuring it, so adding points only where the
energy happens to be low does not help: what counts is that the whole path stays as low as a
connecting path can. Energies and analytic gradients are available through `a2m_task`. Stay
inside `time_budget_s` seconds of wall clock.
"""


def _bottleneck_barrier(start, end, lo, hi, n: int) -> float:
    """Lowest achievable maximum energy over all paths from start to end, on an n x n grid.

    A maximin Dijkstra. Independent of any path-evolution method, so it is a fair reference.
    """
    xs = np.linspace(lo[0], hi[0], n)
    ys = np.linspace(lo[1], hi[1], n)
    grid = np.stack(np.meshgrid(xs, ys, indexing="ij"), axis=-1).reshape(-1, 2)
    v = p2.energy(grid).reshape(n, n)

    def nearest(p):
        return int(np.argmin(np.abs(xs - p[0]))), int(np.argmin(np.abs(ys - p[1])))

    s, t = nearest(start), nearest(end)
    best = np.full((n, n), np.inf)
    best[s] = v[s]
    seen = np.zeros((n, n), dtype=bool)
    queue = [(float(v[s]), s[0], s[1])]
    while queue:
        cost, i, j = heapq.heappop(queue)
        if seen[i, j]:
            continue
        seen[i, j] = True
        if (i, j) == t:
            return cost
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < n and not seen[a, b]:
                nxt = max(cost, float(v[a, b]))
                if nxt < best[a, b]:
                    best[a, b] = nxt
                    heapq.heappush(queue, (nxt, a, b))
    return float("inf")


def _refine_minimum(guess) -> np.ndarray:
    res = minimize(lambda p: float(p2.energy(p)[0]), np.asarray(guess, dtype=float),
                   jac=lambda p: p2.gradient(p)[0], method="L-BFGS-B",
                   options={"gtol": 1e-10, "ftol": 1e-16})
    return res.x


def _densify(path: np.ndarray, spacing: float) -> np.ndarray:
    """Resample so consecutive samples are no further apart than `spacing`."""
    out = [path[0]]
    for a, b in pairwise(path):
        steps = max(1, int(np.ceil(np.linalg.norm(b - a) / spacing)))
        for k in range(1, steps + 1):
            out.append(a + (b - a) * (k / steps))
    return np.array(out)


class TransitionPath(CallEvaluator):
    name = "transition_path"
    domain = "dynamics"
    interface = INTERFACE
    entry = "find_path"
    tool = ("dynamics", "potential2d")

    def __init__(self):
        self._barrier_cache: dict[tuple, float] = {}

    def reference_barrier(self, start, end, params) -> float:
        lo = tuple(params.get("grid_lo", (-1.6, -0.4)))
        hi = tuple(params.get("grid_hi", (1.1, 2.1)))
        n = int(params.get("grid_n", 701))
        key = (tuple(np.round(start, 6)), tuple(np.round(end, 6)), lo, hi, n)
        if key not in self._barrier_cache:
            self._barrier_cache[key] = _bottleneck_barrier(start, end, lo, hi, n)
        return self._barrier_cache[key]

    def run_and_score(self, code, params, sandbox, card):
        start = _refine_minimum(params.get("start", p2.MINIMUM_A))
        end = _refine_minimum(params.get("end", p2.MINIMUM_B))
        budget = float(params.get("time_budget_s", 30.0))
        spec = {"n_images": int(params.get("n_images", 30)), "seed": int(params.get("seed", 0)),
                "time_budget_s": budget}
        out = self.call(sandbox, code, [start.tolist(), end.tolist(), spec], card,
                        timeout_s=int(budget) + 30)
        if not out["ok"]:
            return failed(out, "find_path")

        try:
            path = np.asarray(out["result"], dtype=float)
        except (TypeError, ValueError):
            return {"ok": False, "error": "the path is not numeric"}
        if path.ndim != 2 or path.shape[1] != 2 or len(path) < 3:
            return {"ok": False, "error": f"expected an (M, 2) path with M >= 3, got "
                                          f"{getattr(path, 'shape', None)}"}
        if not np.all(np.isfinite(path)):
            return {"ok": False, "error": "the path contains non-finite values"}

        endpoint_error = float(max(np.linalg.norm(path[0] - start), np.linalg.norm(path[-1] - end)))
        dense = _densify(path, float(params.get("resample_spacing", 0.01)))
        path_max = float(p2.energy(dense).max())
        reference = self.reference_barrier(start, end, params)
        spacing = np.linalg.norm(np.diff(path, axis=0), axis=1)
        return {"ok": True, "metrics": {
            "barrier_error": round(path_max - reference, 4),
            "endpoint_error": round(endpoint_error, 4),
            "path_barrier": round(path_max, 4),
            "reference_barrier": round(reference, 4),
            "path_length": round(float(spacing.sum()), 4),
            "n_images": len(path),
        }, "stats": {"max_spacing": round(float(spacing.max()), 4),
                     "mean_spacing": round(float(spacing.mean()), 4),
                     "spacing_ratio": round(float(spacing.max() / max(spacing.mean(), 1e-12)), 3)}}
