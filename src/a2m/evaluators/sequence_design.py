"""Biology: design RNA sequences that bind a hidden target, under a measurement budget.

This is the one non-quantum domain with a genuinely hidden oracle. The binding target never
enters the sandbox: the candidate proposes a batch of sequences each round, the runner
measures them with ViennaRNA in the parent process, and hands back only the fitness values.
The measurement budget is therefore exact - a candidate cannot buy information off the books.
"""

from __future__ import annotations

from a2m.evaluators.base import CallEvaluator, failed
from a2m.skills import tool_module

rna = tool_module("biology", "rna")

INTERFACE = """\
Write one Python module that defines:

  propose(measured: list, spec: dict) -> list[str]

The runner calls `propose` once per round and measures the batch you return against a hidden
target, then calls you again with everything measured so far.

  measured = [[sequence, fitness], ...]   every measurement so far, best fitness is about 1.0
  spec = {"length": int, "alphabet": "ACGU", "batch_size": int, "rounds": int,
          "round_index": int, "seed": int}

Return exactly `batch_size` sequences of exactly `length` characters over `alphabet`.
Anything longer is truncated to `batch_size`; invalid strings are dropped and wasted.
Re-proposing a sequence that was already measured wastes budget too. The first round is called
with an empty list. You get no other access to the target: measurements are the only
information about it, and the total is `rounds * batch_size`.

You are called fresh each round, so recompute any state you need from `measured`.
"""


class SequenceDesign(CallEvaluator):
    name = "sequence_design"
    domain = "biology"
    interface = INTERFACE
    entry = "propose"
    tool = None             # the oracle stays in the parent; nothing is shipped in

    def run_and_score(self, code, params, sandbox, card):
        length = int(params["length"])
        rounds = int(params["rounds"])
        batch = int(params["batch_size"])
        target = rna.random_target(int(params["target_length"]), int(params["target_seed"]))
        normalizer = rna.normalizer_for(target, length)

        measured: list[list] = []
        seen: dict[str, float] = {}
        invalid = wasted = overflow = 0
        for r in range(rounds):
            spec = {"length": length, "alphabet": rna.ALPHABET, "batch_size": batch,
                    "rounds": rounds, "round_index": r, "seed": int(params.get("seed", 0))}
            out = self.call(sandbox, code, [measured, spec], card)
            if not out["ok"]:
                return failed(out, f"propose (round {r})")
            proposed = out["result"]
            if not isinstance(proposed, list):
                return {"ok": False, "error": f"round {r}: propose() must return a list"}
            overflow += max(0, len(proposed) - batch)
            for seq in proposed[:batch]:
                if not rna.is_valid(seq, length):
                    invalid += 1
                    continue
                if seq in seen:
                    wasted += 1
                    measured.append([seq, seen[seq]])
                    continue
                fit = rna.fitness(seq, target, normalizer)
                seen[seq] = fit
                measured.append([seq, fit])

        if not seen:
            return {"ok": False, "error": "no valid sequence was ever proposed"}
        best = max(seen.values())
        return {"ok": True, "metrics": {
            "best_fitness": round(best, 4),
            "mean_top10": round(sum(sorted(seen.values(), reverse=True)[:10])
                                / min(10, len(seen)), 4),
            "measurements_used": len(measured),
            "distinct_measured": len(seen),
            "invalid_proposed": invalid,
            "repeat_proposed": wasted,
            "over_batch": overflow,
            "rounds": rounds,
        }, "stats": {"budget": rounds * batch,
                     "best_possible": 1.0,
                     "best_sequence_length": length}}
