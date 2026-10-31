"""Sealed judge. The only component that reads the vault. It reruns submitted code and the
paper's reference on visible and hidden tests, checks for loopholes, and grades method match
against a rubric written from the paper before any run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from a2m.evaluators import get as get_evaluator
from a2m.llm import prompts as P
from a2m.llm.client import LLM, Budget, BudgetExhausted, LLMError
from a2m.run import load_defaults, make_sandbox
from a2m.sandbox.static import scan
from a2m.schema import Candidate, JudgeReport, Submission
from a2m.scoring import meets_claim
from a2m.tasks import load_card, load_vault

STRUCT_KEYS = ("oracle_queries", "num_qubits", "num_circuits", "two_qubit_gates", "depth")


class VaultError(RuntimeError):
    pass


def _similar(a: float, b: float) -> float:
    a, b = float(a), float(b)
    if a == b:
        return 1.0
    return min(a, b) / max(a, b) if max(a, b) > 0 else 0.0


def structural_similarity(cand: dict[str, dict], ref: dict[str, dict]) -> float:
    sims = []
    for name, r in ref.items():
        c = cand.get(name, {})
        if not (r.get("ok") and c.get("ok")):
            continue
        sims += [_similar(c["stats"][k], r["stats"][k]) for k in STRUCT_KEYS
                 if k in c.get("stats", {}) and k in r.get("stats", {})]
    return round(sum(sims) / len(sims), 4) if sims else 0.0


def loopholes(cand: Candidate, results: dict[str, dict], allowed: list[str]) -> list[str]:
    found = [f"static: {p}" for p in scan(cand.code, allowed)]
    for name, r in results.items():
        for s in r.get("stats", {}).get("opaque_shortcuts", []):
            found.append(f"{name}: opaque shortcut gate '{s}' (hard-codes the target operation)")
    return sorted(set(found))


def _numbers(results: dict[str, dict]) -> dict[str, dict[str, Any]]:
    return {k: (v.get("metrics") if v.get("ok") else {"error": v.get("error", "")[:300]})
            for k, v in results.items()}


class SealedJudge:
    def __init__(self, llm_mode: str = "anthropic", models: list[str] | None = None,
                 sandbox_profile: str | None = None, verbose: bool = True):
        self.defaults = load_defaults()
        j = self.defaults.get("judge", {})
        self.models = models or j.get("models", ["claude-opus-5-5", "claude-sonnet-5-5"])
        self.budget = Budget(j.get("max_usd", 2.0))
        self.judges = [LLM(m, self.budget, llm_mode, effort=j.get("effort", "high"), mock_seed=i)
                       for i, m in enumerate(self.models)]
        self.recovered_t = j.get("recovered_threshold", 0.7)
        self.alt_t = j.get("alternative_threshold", 0.5)
        self.sandbox = make_sandbox(self.defaults, sandbox_profile, False)
        self.verbose = verbose
        self._ref_cache: dict[str, dict] = {}

    def _say(self, msg: str):
        if self.verbose:
            print(f"[judge] {msg}", flush=True)

    def _reference(self, task_id: str, card, vault, ref_code: str) -> dict[str, dict]:
        if task_id not in self._ref_cache:
            ev = get_evaluator(card.evaluator)
            res = {t.name: ev.evaluate(ref_code, t.params, self.sandbox, card.allowed_imports,
                                       card.qubit_cap)
                   for t in card.test_systems + vault.hidden_test_systems}
            if not meets_claim(card.criteria, res):
                raise VaultError(f"{task_id}: reference does not meet its own claim: "
                                 f"{json.dumps(_numbers(res))[:500]}")
            self._ref_cache[task_id] = res
        return self._ref_cache[task_id]

    def _rubric(self, cand: Candidate, vault) -> tuple[float, dict[str, dict[str, float]], list[str]]:
        scores: dict[str, dict[str, float]] = {}
        review = []
        total = wsum = 0.0
        for item in vault.rubric:
            per: dict[str, float] = {}
            prompt = P.JUDGE_RUBRIC.format(item=item.text, sketch=cand.sketch, code=cand.code)
            for j in self.judges:
                try:
                    out = j.call("judge_rubric", P.JUDGE_SYSTEM, prompt, P.JUDGE_SCHEMA,
                                 {"keywords": item.keywords, "sketch": cand.sketch,
                                  "code": cand.code})
                    per[j.label + f"#{len(per)}"] = float(out["score"])
                except (LLMError, BudgetExhausted, KeyError, ValueError) as e:
                    self._say(f"rubric {item.id} judge {j.label} failed: {e}")
            text = (cand.sketch + "\n" + cand.code).lower()
            lexical = float(any(k.lower() in text for k in item.keywords)) if item.keywords else 0.0
            if per:
                vals = list(per.values())
                if max(vals) - min(vals) >= 0.5:
                    review.append(f"rubric {item.id}: judges disagree {vals}")
                total += item.weight * sum(vals) / len(vals)
                wsum += item.weight
            else:
                review.append(f"rubric {item.id}: no judge produced a score")
            scores[item.id] = {**per, "lexical": lexical}
        return (round(total / wsum, 4) if wsum else 0.0), scores, review

    def judge(self, run_dir: Path) -> JudgeReport:
        run_dir = Path(run_dir).resolve()
        sub = Submission.model_validate_json((run_dir / "submission.json").read_text())
        card = load_card(sub.task_id)
        vault, ref_code = load_vault(sub.task_id)
        ev = get_evaluator(card.evaluator)
        systems = card.test_systems + vault.hidden_test_systems
        ref = self._reference(sub.task_id, card, vault, ref_code)
        self._say(f"{sub.run_id}: {len(sub.candidates)} submitted candidate(s)")

        evaluated = []
        for cand in sub.candidates:
            res = {t.name: ev.evaluate(cand.code, t.params, self.sandbox, card.allowed_imports,
                                       card.qubit_cap) for t in systems}
            holes = loopholes(cand, res, card.allowed_imports)
            reproduced = meets_claim(card.criteria, res) and not holes
            mm, rubric, review = self._rubric(cand, vault)
            evaluated.append({"candidate": cand, "results": res, "loopholes": holes,
                              "claim_reproduced": reproduced, "method_match": mm,
                              "rubric": rubric, "review": review,
                              "structural": structural_similarity(res, ref)})
            self._say(f"  {cand.id} family={cand.family} reproduced={reproduced} "
                      f"method_match={mm:.2f} structural={evaluated[-1]['structural']:.2f}")

        primary = evaluated[0] if evaluated else None
        if primary is None:
            report = JudgeReport(
                run_id=sub.run_id, task_id=sub.task_id, system=sub.system, seed=sub.seed,
                candidate_id=None, claim_reproduced=False, method_match=0.0,
                method_recovered=False, valid_alternative=False, structural_similarity=0.0,
                loopholes=[], human_review=["no candidate submitted"], rubric_scores={},
                candidate_numbers={}, reference_numbers=_numbers(ref),
                paper_numbers=vault.reported_numbers, usage=sub.usage)
        else:
            mm, ok = primary["method_match"], primary["claim_reproduced"]
            review = list(primary["review"])
            alt = ok and mm < self.alt_t
            if alt:
                review.append("valid alternative: claim reproduced by a different method")
            elif ok and mm < self.recovered_t:
                review.append("partial method match; check by hand")
            report = JudgeReport(
                run_id=sub.run_id, task_id=sub.task_id, system=sub.system, seed=sub.seed,
                candidate_id=primary["candidate"].id, claim_reproduced=ok, method_match=mm,
                method_recovered=ok and mm >= self.recovered_t,
                any_method_recovered=any(e["claim_reproduced"] and e["method_match"]
                                         >= self.recovered_t for e in evaluated),
                valid_alternative=alt,
                structural_similarity=primary["structural"], loopholes=primary["loopholes"],
                human_review=review, rubric_scores=primary["rubric"],
                candidate_numbers=_numbers(primary["results"]), reference_numbers=_numbers(ref),
                paper_numbers=vault.reported_numbers, usage=sub.usage,
                all_candidates=[{"id": e["candidate"].id, "family": e["candidate"].family,
                                 "claim_reproduced": e["claim_reproduced"],
                                 "method_match": e["method_match"],
                                 "structural_similarity": e["structural"],
                                 "loopholes": e["loopholes"]} for e in evaluated])
        report_dict = report.model_dump()
        report_dict["judge_usage"] = self.budget.snapshot()
        report_dict["reference_family"] = vault.reference_family
        (run_dir / "judge.json").write_text(json.dumps(report_dict, indent=2, default=str))
        (run_dir / "judge.md").write_text(render_markdown(report, vault.reference_family))
        return report


def render_markdown(r: JudgeReport, ref_family: str) -> str:
    lines = [f"# Judge report: {r.run_id}", "",
             f"- task: `{r.task_id}`  system: `{r.system}`  seed: {r.seed}",
             f"- primary candidate: `{r.candidate_id}`",
             f"- **claim reproduced: {r.claim_reproduced}**",
             (f"- **method match: {r.method_match:.2f}** (recovered: {r.method_recovered}; "
              f"valid alternative: {r.valid_alternative}); reference family `{ref_family}`"),
             f"- structural similarity to reference: {r.structural_similarity:.2f}",
             (f"- spend: ${r.usage.get('usd', 0):.4f} over {r.usage.get('calls', 0)} calls, "
              f"{r.usage.get('wall_seconds', 0)} s"), ""]
    if r.loopholes:
        lines += ["## Loopholes", *[f"- {x}" for x in r.loopholes], ""]
    if r.human_review:
        lines += ["## Needs human review", *[f"- {x}" for x in r.human_review], ""]
    lines += ["## Rubric", "| item | scores |", "|---|---|"]
    lines += [f"| {k} | {json.dumps(v)} |" for k, v in r.rubric_scores.items()]
    lines += ["", "## Numbers (candidate vs reference)", "| test | candidate | reference |",
              "|---|---|---|"]
    for k in r.reference_numbers:
        lines.append(f"| {k} | `{json.dumps(r.candidate_numbers.get(k))}` | "
                     f"`{json.dumps(r.reference_numbers[k])}` |")
    lines += ["", f"Paper reports: `{json.dumps(r.paper_numbers)}`", ""]
    if r.all_candidates:
        lines += ["## All submitted candidates", "| id | family | reproduced | method match |",
                  "|---|---|---|---|"]
        lines += [f"| {c['id']} | {c['family']} | {c['claim_reproduced']} | "
                  f"{c['method_match']:.2f} |" for c in r.all_candidates]
    return "\n".join(lines) + "\n"
