"""Chemistry: improve a molecule's penalized logP while keeping it similar to the original.

The similarity constraint is what makes this a search problem rather than a loophole: the
unconstrained objective is maximised by absurd structures such as a long carbon chain, which
any method can emit without reasoning. Requiring every answer to stay within a Tanimoto
distance of its starting molecule removes that escape and keeps the measured quantity the
method itself.

The candidate returns SMILES; the trusted runner re-parses, re-scores and re-checks similarity
with the same code the sandbox exposed, so nothing a candidate reports about its own molecules
is used.
"""

from __future__ import annotations

from a2m.evaluators.base import CallEvaluator, failed
from a2m.skills import tool_module

chem = tool_module("chemistry", "chem")

INTERFACE = """\
Write one Python module that defines:

  run(spec: dict) -> list[str]

spec = {"start": <SMILES>, "similarity_threshold": <float>, "n_return": <int>,
        "seed": <int>, "time_budget_s": <float>}.

Return up to `n_return` SMILES strings: molecules that score better than `start` under
`a2m_task.score` while staying chemically similar to it. A returned molecule counts only if

    a2m_task.similarity(molecule, start) >= spec["similarity_threshold"]

The runner re-parses, re-scores and re-checks similarity itself, and ignores anything your
code reports. Invalid strings, duplicates and molecules that miss the similarity threshold are
all wasted. Stay inside `time_budget_s` seconds of wall clock and use `seed` for randomness.
"""


class MoleculeOpt(CallEvaluator):
    name = "molecule_opt"
    domain = "chemistry"
    interface = INTERFACE
    entry = "run"
    tool = ("chemistry", "chem")

    def _one(self, code, start: str, params: dict, sandbox, card) -> dict:
        threshold = float(params["similarity_threshold"])
        n_return = int(params.get("n_return", 10))
        budget = float(params.get("time_budget_s", 60.0))
        spec = {"start": start, "similarity_threshold": threshold, "n_return": n_return,
                "seed": int(params.get("seed", 0)), "time_budget_s": budget}
        out = self.call(sandbox, code, [spec], card, timeout_s=int(budget) + 60)
        if not out["ok"]:
            return {"error": failed(out, f"run ({start})")}

        answer = out["result"]
        if not isinstance(answer, list):
            return {"error": {"ok": False, "error": "run() must return a list of SMILES"}}
        returned = answer[:n_return]
        base = chem.score(start)

        valid, satisfying = [], []
        for item in returned:
            canonical = chem.canonical(item) if isinstance(item, str) else None
            if canonical is None:
                continue
            valid.append(canonical)
            if chem.similarity(canonical, start) >= threshold:
                satisfying.append(canonical)
        scores = [chem.score(s) for s in satisfying]
        best = max(scores, default=float("-inf"))
        return {"base": base, "best": best, "returned": len(returned), "valid": len(valid),
                "satisfying": len(set(satisfying)),
                "improvement": (best - base) if scores else 0.0,
                "over_limit": max(0, len(answer) - n_return)}

    def run_and_score(self, code, params, sandbox, card):
        starts = list(params["starts"])
        results = []
        for start in starts:
            r = self._one(code, start, params, sandbox, card)
            if "error" in r:
                return r["error"]
            results.append(r)

        improvements = [r["improvement"] for r in results]
        returned = sum(r["returned"] for r in results) or 1
        solved = sum(r["satisfying"] > 0 and r["improvement"] > 0 for r in results)
        return {"ok": True, "metrics": {
            "mean_improvement": round(sum(improvements) / len(improvements), 4),
            "worst_improvement": round(min(improvements), 4),
            "success_rate": round(solved / len(results), 4),
            "validity": round(sum(r["valid"] for r in results) / returned, 4),
            "constraint_rate": round(sum(r["satisfying"] for r in results) / returned, 4),
            "molecules": len(starts),
            "over_limit": sum(r["over_limit"] for r in results),
        }, "stats": {"per_start": [
            {"start": s, "base_score": round(r["base"], 3),
             "best_score": None if r["best"] == float("-inf") else round(r["best"], 3),
             "improvement": round(r["improvement"], 3), "satisfying": r["satisfying"]}
            for s, r in zip(starts, results)]}}
