"""The four research actions. Each returns a result or None (LLM failure); callers decide
what the outcome means (payouts, deaths, next needs)."""

from __future__ import annotations

import json
from typing import Any

from a2m.llm import prompts as P
from a2m.llm.client import LLM, BudgetExhausted, LLMError
from a2m.schema import Candidate, TestSystem
from a2m.scoring import claim_gap
from a2m.workspace import Workspace


def _call(ws: Workspace, llm: LLM, tag: str, prompt: str, schema: dict, meta: dict,
          who: str) -> dict | None:
    try:
        return llm.call(tag, P.render_system(ws.card), prompt, schema, meta)
    except BudgetExhausted:
        return None
    except LLMError as e:
        ws.log("llm_error", who=who, action=tag, error=str(e))
        return None


def hypothesize(ws: Workspace, llm: LLM, who: str, notes: str = "", diversity: bool = True,
                prefer: list[str] | None = None, avoid: list[str] | None = None) -> Candidate | None:
    existing = ws.families()
    out = _call(ws, llm, "hypothesize", P.hypothesize(existing, diversity, notes),
                P.HYPOTHESIZE_SCHEMA,
                {"evaluator": ws.card.evaluator, "existing_families": existing if diversity else [],
                 "prefer": prefer or [], "avoid": avoid or []}, who)
    if not out or not out.get("sketch"):
        return None
    family = (out.get("family") or "unnamed").strip().lower().replace(" ", "_")[:60]
    sketch = out["sketch"]
    if out.get("assumptions"):
        sketch += "\nAssumptions: " + "; ".join(out["assumptions"])
    cand = ws.new_candidate(family, sketch, who)
    ws.log("hypothesis", who=who, cand=cand.id, family=family)
    return cand


def implement(ws: Workspace, llm: LLM, who: str, base: Candidate, notes: str = "") -> Candidate | None:
    diag = ws.diagnostics(base) if base.code else ""
    out = _call(ws, llm, "implement",
                P.implement(base.family, base.sketch, base.code, diag, notes), P.IMPLEMENT_SCHEMA,
                {"evaluator": ws.card.evaluator, "family": base.family, "attempt": base.attempts},
                who)
    if not out or not out.get("code", "").strip():
        return None
    cand = ws.child(base) if base.code else base
    cand.code = out["code"]
    cand.attempts = base.attempts + 1
    cand.status = "implemented"
    cand.chain.append((who, "implement"))
    ws.log("implement", who=who, cand=cand.id, family=cand.family, attempt=cand.attempts)
    return cand


def simulate(ws: Workspace, who: str, cand: Candidate) -> float:
    gap = ws.simulate(cand)
    cand.chain.append((who, "simulate"))
    errs = [r.get("error", "")[:160] for r in cand.results.values() if not r.get("ok")]
    ws.log("simulate", who=who, cand=cand.id, family=cand.family, gap=round(gap, 4),
           status=cand.status, error=errs[0] if errs else "")
    return gap


def critique(ws: Workspace, llm: LLM, who: str, cand: Candidate) -> dict[str, Any] | None:
    keys = sorted(ws.card.test_systems[-1].params)
    prompt = P.CRITIQUE.format(family=cand.family, sketch=cand.sketch, code=cand.code,
                               results=json.dumps({k: v.get("metrics") for k, v in
                                                   cand.results.items()}, indent=1),
                               keys=", ".join(keys))
    out = _call(ws, llm, "critique", prompt, P.CRITIQUE_SCHEMA,
                {"stress_params": ws.stress_params()}, who)
    if not out:
        return None
    rec: dict[str, Any] = {"critic": who, "verdict": out["verdict"], "reason": out["reason"],
                           "stress_test": None, "confirmed": False}
    if out["verdict"] == "break":
        params = ws.validate_stress(out.get("stress_test", ""))
        if params is not None:
            res = ws.run_tests(cand.code, [TestSystem(name="stress", params=params)])["stress"]
            failed = claim_gap(ws.card.criteria, {"stress": res}) > 0
            if failed and "qubits; cap is" in str(res.get("error", "")):
                failed = False  # an oversized stress test is the critic's fault
            rec.update(stress_test=params, confirmed=failed,
                       stress_result=res.get("metrics") or res.get("error", "")[:300])
    cand.critiques.append(rec)
    ws.log("critique", who=who, cand=cand.id, verdict=rec["verdict"], confirmed=rec["confirmed"],
           reason=rec["reason"][:120])
    return rec
