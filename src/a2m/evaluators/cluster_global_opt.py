"""Materials: find the lowest-energy structure of a Lennard-Jones cluster.

The candidate returns coordinates; the trusted runner recomputes their energy, checks the
cluster has not broken apart, and compares with the known global minimum. A candidate cannot
report a good energy it did not achieve, because the runner never reads a number the candidate
produced - only the coordinates.
"""

from __future__ import annotations

import numpy as np

from a2m.backends import alchemi
from a2m.evaluators.base import CallEvaluator, failed
from a2m.skills import tool_module

lj = tool_module("materials", "lj")

INTERFACE = """\
Write one Python module that defines:

  search(spec: dict) -> list[list[float]]

spec = {"n": <number of atoms>, "seed": <int>, "time_budget_s": <float>}.

Return the positions of the n atoms as an (n, 3) nested list, in reduced Lennard-Jones units.
Return the best structure you found; the runner recomputes its energy itself and compares with
the known global minimum for that n, so only the coordinates matter.

Stay inside `time_budget_s` seconds of wall clock: the runner stops the process shortly after
that and the attempt scores zero. Use `seed` for any randomness so a run is reproducible. The
helpers in `a2m_task` are the same code the runner scores with.
"""


class ClusterGlobalOpt(CallEvaluator):
    name = "cluster_global_opt"
    domain = "materials"
    interface = INTERFACE
    entry = "search"
    tool = ("materials", "lj")

    def public_spec(self, n: int, seed: int, budget: float) -> dict:
        return {"n": int(n), "seed": int(seed), "time_budget_s": float(budget)}

    def _check(self, answer, n: int) -> tuple[float | None, str]:
        try:
            pos = np.asarray(answer, dtype=float)
        except (TypeError, ValueError):
            return None, "positions are not numeric"
        if pos.shape != (n, 3) or not np.all(np.isfinite(pos)):
            return None, f"expected a finite ({n}, 3) array, got {getattr(pos, 'shape', None)}"
        if not lj.is_connected(pos):
            return None, "the cluster has broken apart (atoms not all in contact)"
        return lj.energy(pos), ""

    def run_and_score(self, code, params, sandbox, card):
        n = int(params["n"])
        if n not in lj.GLOBAL_MINIMA:
            return {"ok": False, "error": f"no reference global minimum for n={n}"}
        target = lj.GLOBAL_MINIMA[n]
        tol = float(params.get("tolerance", 1e-3))
        budget = float(params.get("time_budget_s", 20.0))
        seeds = [int(s) for s in params.get("seeds", [0])]

        energies: list[float] = []
        notes: list[str] = []
        for seed in seeds:
            out = self.call(sandbox, code, [self.public_spec(n, seed, budget)], card,
                            timeout_s=int(budget) + 30)
            if not out["ok"]:
                return failed(out, f"search (n={n}, seed={seed})")
            energy, why = self._check(out["result"], n)
            if energy is None:
                return {"ok": False, "error": f"invalid structure (n={n}, seed={seed}): {why}"}
            energies.append(energy)
            notes.append(alchemi.cross_check(out["result"], energy))

        hits = sum(e <= target + tol for e in energies)
        best = min(energies)
        return {"ok": True, "metrics": {
            "success_rate": hits / len(energies),
            "best_energy": round(best, 6),
            "mean_energy_error": round(float(np.mean([e - target for e in energies])), 6),
            "best_energy_error": round(best - target, 6),
            "reference_minimum": target,
            "runs": len(energies),
            "n": n,
        }, "stats": {"energies": [round(e, 6) for e in energies],
                     "independent_check": sorted({x for x in notes if x})}}
