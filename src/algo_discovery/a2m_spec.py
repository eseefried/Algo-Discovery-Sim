"""The a2m swarm (src/a2m) writing math specifications instead of code, for the 96-paper benchmark.

The swarm runtime is a2m's, unchanged: pressure matching, the survival economy, payouts from
measured progress, deaths, respawns and lineage, configured by configs/systems/<variant>.yaml.
Only what an agent produces and what the runner measures are swapped:

  hypothesize  a2m's prompt and schema: a method family and sketch, from the abstract alone
  implement    a MathSpecification in the single agent's schema and rules
  simulate     deterministic spec checks; a spec that passes them is built by the black-box
               code stage and simulated in Docker/Aer. Gap 0 means it builds and runs.
  critique     a stress instance for the built circuit; a break counts only if the runner
               reproduces it (a2m's rule), and re-running the circuit costs no model call

The paper is never consulted: there is no claim card, so the runner measures only whether a
spec is well-formed and implementable. Every model call, including the runner's code-stage
call, is charged to one per-paper budget.
"""

import argparse
import json
import sys
import threading
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from anthropic import transform_schema
from pydantic import ValidationError

from a2m import actions as a2m_actions
from a2m import domains
from a2m.llm import prompts as P
from a2m.llm.client import LLM, Budget, BudgetExhausted, LLMError
from a2m.run import load_system
from a2m.schema import Candidate, ClaimCard
from a2m.swarm.runtime import Swarm, SwarmConfig
from a2m.workspace import Workspace

from .code_generation import generate_code, load_code_request
from .config import Settings
from .equations import GenerationError
from .external_spec import DATASET_ABSTRACTS, ExternalSpec, save_as_equation_run
from .prompt import SYSTEM_PROMPT
from .schemas import MathSpecification
from .simulation_cli import simulate_source

SOURCE = "a2m_swarm"

SPEC_SYSTEM = """\
You are a researcher in a team reconstructing a scientific method from a paper's abstract
alone. You have not read the paper and cannot look anything up. Work from the abstract and
your own knowledge. The team's output is a mathematical specification. A trusted runner checks
every specification and turns the ones that pass into a small quantum circuit that it builds
and simulates itself, so only a specification precise enough to implement will score.

{domain}

<abstract>
{abstract}
</abstract>"""

# The single agent's specification rules, addressed to a team member instead.
SINGLE_AGENT_OPENING = (
    "You are the single scientific reconstruction agent for a quantum-algorithm\nbaseline."
)
assert SINGLE_AGENT_OPENING in SYSTEM_PROMPT
SPEC_RULES = SYSTEM_PROMPT.replace(
    SINGLE_AGENT_OPENING, "You are one researcher in a team reconstructing a quantum algorithm."
)

IMPLEMENT = """\
Write the mathematical specification for this method family.

Method family: {family}
Sketch:
{sketch}
{previous}{notes}
Return the specification in `specification` and anything the next researcher should know in
`notes`."""

CRITIQUE = """\
Review this specification adversarially. The runner turned it into a circuit that builds and
simulates on the instance below.

Method family: {family}
<specification>
{spec}
</specification>
<runner_results>
instance: {instance}
simulation: {simulation}
</runner_results>

Would the construction fail on other valid instances, for example larger sizes or other
parameters within the qubit cap? If you think it breaks, give a stress test: a JSON object with
the same keys as the instance ({keys}). The runner rebuilds and simulates the circuit on it; a
break only counts if it fails there. If you find no concrete failure, return "pass" with an
empty stress_test."""

SIMULATION_SUMMARY_LIMIT = 600


def implement_schema() -> dict[str, Any]:
    spec = transform_schema(MathSpecification)
    defs = dict(spec.pop("$defs", {}))
    defs["MathSpecification"] = spec
    return {
        "$defs": defs,
        "type": "object",
        "properties": {
            "specification": {"$ref": "#/$defs/MathSpecification"},
            "notes": {"type": "string"},
        },
        "required": ["specification", "notes"],
        "additionalProperties": False,
    }


IMPLEMENT_SCHEMA = implement_schema()


def spec_card(arxiv_id: str, abstract: str) -> ClaimCard:
    """A claim card carrying only the abstract: no claim, criteria or tests from the paper."""
    return ClaimCard(
        task_id=f"arxiv-{arxiv_id}",
        domain="quantum",
        evaluator="spec_blackbox",
        abstract=abstract,
        claim="Reconstruct the method this abstract describes as a mathematical specification "
        "precise enough to build and simulate as a small quantum circuit.",
        criteria=[],
        interface="A MathSpecification object (see the specification rules).",
        test_systems=[],
        allowed_imports=[],
        notes="Abstract-only benchmark condition; the runner measures implementability only.",
    )


def check_spec(raw: str, abstract: str) -> tuple[float, list[str], MathSpecification | None]:
    """Deterministic, abstract-only checks. Returns (gap before building, issues, spec)."""
    try:
        spec = MathSpecification.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        return 1.0, [f"schema or consistency check failed: {str(exc)[:300]}"], None
    try:
        spec.validate_evidence(abstract)
    except ValueError as exc:
        return 0.9, [str(exc)], spec
    checks = {
        "status must be specified or partial": spec.status in {"specified", "partial"},
        "at least one equation": bool(spec.equations),
        "at least one register": bool(spec.registers),
        "every algorithm step cites an equation": bool(spec.steps)
        and all(step.equation_ids for step in spec.steps),
        "an initial state": bool(spec.initial_state),
        "a measurement or classical postprocessing": bool(
            spec.measurement or spec.classical_postprocessing
        ),
        "abstract-sourced equations quote the abstract": all(
            e.abstract_quote for e in spec.equations if e.provenance.startswith("abstract_")
        ),
    }
    issues = [name for name, ok in checks.items() if not ok]
    if issues:
        return 0.3 + 0.5 * len(issues) / len(checks), [f"missing: {i}" for i in issues], spec
    return 0.3, [], spec


class SpecWorkspace(Workspace):
    """a2m's Workspace with the code evaluator replaced by spec checks and the black box."""

    def __init__(
        self,
        card: ClaimCard,
        budget: Budget,
        run_dir: Path,
        settings: Settings,
        verbose: bool = True,
    ):
        # Workspace.__init__ looks up a code evaluator, which a spec task does not have; the
        # remaining state is set up exactly as it does.
        import itertools

        self.card, self.sandbox, self.budget, self.run_dir = card, None, budget, run_dir
        self.evaluator = None
        self.settings = settings
        self.candidates: dict[str, Candidate] = {}
        self.verbose, self.prefix = verbose, ""
        self.tick = 0
        self.t0 = time.time()
        self._ids = itertools.count(1)
        self._lock = threading.Lock()
        self._code_lock = threading.Lock()
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "candidates").mkdir(exist_ok=True)
        self._events = open(run_dir / "events.jsonl", "a")  # noqa: SIM115 - open for the run

    def simulate(self, cand: Candidate) -> float:
        gap, issues, spec = check_spec(cand.code, self.card.abstract)
        result: dict[str, Any] = {"ok": not issues, "metrics": {"gap": gap}, "issues": issues}
        if not issues:
            gap, build = self.build(spec)
            result.update(build, metrics={"gap": gap, **build["metrics"]})
            result["ok"] = gap == 0.0
            if gap:
                result["error"] = build["detail"]
        else:
            result["error"] = "; ".join(issues)
        cand.results = {"spec": result}
        cand.gap = gap
        cand.status = "passing" if gap == 0.0 else "failing"
        (self.run_dir / "candidates" / f"{cand.id}.json").write_text(cand.code)
        return gap

    def build(self, spec: MathSpecification) -> tuple[float, dict[str, Any]]:
        # Local workers share one paid runner allowance. Admit builds serially so
        # a whole parallel agent round cannot each overshoot that allowance.
        if getattr(self, "code_budget", None) is not None:
            with self._code_lock:
                return self._build(spec)
        return self._build(spec)

    def _build(self, spec: MathSpecification) -> tuple[float, dict[str, Any]]:
        """Black-box code stage + Docker build + Aer simulation of one spec."""
        if self.budget.exhausted:
            return 0.3, {"metrics": {}, "detail": "build test skipped: budget exhausted"}
        code_budget = getattr(self, "code_budget", None)
        if code_budget is not None and code_budget.exhausted:
            return 0.3, {"metrics": {}, "detail": "build test skipped: paid code budget exhausted"}
        external = ExternalSpec(source=SOURCE, abstract=self.card.abstract, specification=spec)
        try:
            equations = save_as_equation_run(external, self.settings)
            request = load_code_request(
                self.settings.artifact_dir / equations.run_id / "result.json",
                validate_circuit=True,
            )
            code = generate_code(request, self.settings)
        except GenerationError as exc:
            return 0.25, {"metrics": {}, "detail": f"code stage failed: {exc}"[:400]}
        except (ValidationError, ValueError) as exc:
            return 0.25, {"metrics": {}, "detail": f"code stage rejected spec: {exc}"[:400]}
        u = code.usage
        self.budget.charge(
            self.settings.model,
            u.input_tokens + u.cache_creation_input_tokens,
            u.output_tokens,
            u.cache_read_input_tokens,
            local=self.settings.backend == "local",
        )
        if code_budget is not None:
            code_budget.charge(self.settings.model,
                               u.input_tokens + u.cache_creation_input_tokens,
                               u.output_tokens, u.cache_read_input_tokens)
        base = {"code_run_id": code.run_id, "code_status": code.artifact.status}
        if code.artifact.status != "generated":
            return 0.25, {
                **base,
                "metrics": {},
                "detail": f"code stage abstained ({code.artifact.status}): "
                + code.artifact.summary[:300],
            }
        if not code.static_checks_passed or code.validation.status != "build_passed":
            return 0.15, {
                **base,
                "metrics": {},
                "detail": f"circuit did not build: {code.validation.detail[:300]}",
            }
        instance = json.loads(
            (self.settings.artifact_dir / code.run_id / "instance.json").read_text()
        )
        _, report = simulate_source(code.artifact.source_python, instance, "none")
        metrics = {"num_qubits": report.num_qubits, "cases_run": report.cases_run}
        detail = report.detail if report.status != "simulated" else "built and simulated"
        build = {
            **base,
            "metrics": metrics,
            "detail": detail,
            "instance": instance,
            "source": code.artifact.source_python,
            "simulation": json.dumps([c.probabilities for c in report.cases])[
                :SIMULATION_SUMMARY_LIMIT
            ],
        }
        return (0.0 if report.status == "simulated" else 0.1), build

    def diagnostics(self, cand: Candidate) -> str:
        r = cand.results.get("spec", {})
        lines = list(r.get("issues", [])) or [r.get("detail", "")]
        for c in cand.critiques:
            if c.get("confirmed"):
                lines.append(f"stress instance {c['stress_test']} failed: {c.get('stress_result')}")
        return "\n".join(line for line in lines if line)


def _system(ws: SpecWorkspace, rules: bool = False) -> str:
    profile = domains.get(ws.card.domain)
    # The field's summary and conventions; the sandbox helper list does not apply to specs.
    domain = f"Field: {profile.domain}. {profile.summary}\n\nConventions in this field:\n" + (
        profile.conventions
    )
    text = SPEC_SYSTEM.format(domain=domain, abstract=ws.card.abstract)
    return text + ("\n\nSpecification rules:\n" + SPEC_RULES if rules else "")


def _call(ws, llm: LLM, tag: str, system: str, prompt: str, schema: dict, who: str):
    try:
        return llm.call(tag, system, P.role_line(ws.card, tag) + prompt, schema, {})
    except BudgetExhausted:
        return None
    except LLMError as exc:
        ws.log("llm_error", who=who, action=tag, error=str(exc))
        return None


def hypothesize(ws, llm, who, notes="", diversity=True, prefer=None, avoid=None):
    prompt = P.hypothesize(ws.families(), diversity, notes)
    target = "could achieve the claim through the interface"
    assert target in prompt
    prompt = prompt.replace(target, "could be the method this abstract describes")
    out = _call(ws, llm, "hypothesize", _system(ws), prompt, P.HYPOTHESIZE_SCHEMA, who)
    if not out or not out.get("sketch"):
        return None
    family = (out.get("family") or "unnamed").strip().lower().replace(" ", "_")[:60]
    sketch = out["sketch"]
    if out.get("assumptions"):
        sketch += "\nAssumptions: " + "; ".join(out["assumptions"])
    cand = ws.new_candidate(family, sketch, who)
    ws.log("hypothesis", who=who, cand=cand.id, family=family)
    return cand


def implement(ws, llm, who, base: Candidate, notes=""):
    previous = ""
    if base.code:
        previous = (
            f"\nA previous specification did not pass the runner.\n<previous_spec>\n"
            f"{base.code}\n</previous_spec>\n<runner_diagnostics>\n{ws.diagnostics(base)}"
            "\n</runner_diagnostics>\nFix the cause.\n"
        )
    prompt = IMPLEMENT.format(
        family=base.family, sketch=base.sketch, previous=previous, notes=P._notes_block(notes)
    )
    out = _call(ws, llm, "implement", _system(ws, rules=True), prompt, IMPLEMENT_SCHEMA, who)
    if not out or not out.get("specification"):
        return None
    cand = ws.child(base) if base.code else base
    cand.code = json.dumps(out["specification"], ensure_ascii=False)
    cand.attempts = base.attempts + 1
    cand.status = "implemented"
    cand.chain.append((who, "implement"))
    ws.log("implement", who=who, cand=cand.id, family=cand.family, attempt=cand.attempts)
    return cand


def critique(ws, llm, who, cand: Candidate) -> dict[str, Any] | None:
    build = cand.results.get("spec", {})
    instance = build.get("instance") or {}
    prompt = CRITIQUE.format(
        family=cand.family,
        spec=cand.code,
        instance=json.dumps(instance),
        simulation=build.get("simulation", ""),
        keys=", ".join(sorted(instance)),
    )
    out = _call(ws, llm, "critique", _system(ws), prompt, P.CRITIQUE_SCHEMA, who)
    if not out:
        return None
    rec: dict[str, Any] = {
        "critic": who,
        "verdict": out["verdict"],
        "reason": out["reason"],
        "stress_test": None,
        "confirmed": False,
    }
    if out["verdict"] == "break":
        try:
            params = json.loads(out.get("stress_test") or "null")
        except json.JSONDecodeError:
            params = None
        if isinstance(params, dict) and params and set(params) <= set(instance):
            stress = {**instance, **params}
            _, report = simulate_source(build["source"], stress, "none")
            # Rejecting invalid parameters with ValueError is correct behaviour, as is a size
            # over the cap: the critic's fault, not a break.
            fault = "ValueError" in report.detail or "limits" in report.detail
            rec.update(
                stress_test=stress,
                stress_result=report.detail[:300],
                confirmed=report.status != "simulated" and not fault,
            )
    cand.critiques.append(rec)
    ws.log(
        "critique",
        who=who,
        cand=cand.id,
        verdict=rec["verdict"],
        confirmed=rec["confirmed"],
        reason=rec["reason"][:120],
    )
    return rec


class SpecSwarm(Swarm):
    """a2m's swarm with spec-writing actions; matching, economy and lineage are inherited."""

    def _execute(self, agent, need):
        if need is None:
            return None
        llm = self.llms[agent.model]
        cand = self.ws.candidates.get(need.candidate) if need.candidate else None
        if need.kind == "needs_hypothesis":
            return hypothesize(
                self.ws,
                llm,
                agent.id,
                agent.notes,
                self.cfg.diversity_first,
                agent.prefer,
                agent.avoid,
            )
        if need.kind == "needs_implementation":
            return implement(self.ws, llm, agent.id, cand, agent.notes)
        if need.kind == "needs_simulation":
            return a2m_actions.simulate(self.ws, agent.id, cand)
        if need.kind == "needs_critique":
            return critique(self.ws, llm, agent.id, cand)
        raise ValueError(need.kind)


def best_spec(ws: SpecWorkspace) -> tuple[Candidate | None, MathSpecification | None]:
    """The swarm's own ranking, first candidate whose spec passes the abstract checks.
    Specs written but never simulated (the budget ran out) come after every tested one."""
    tested = ws.ranked()
    untested = [c for c in ws.candidates.values() if c.code and c not in tested]
    ordered = tested + sorted(untested, key=lambda c: c.id)
    for cand in ordered:
        _, issues, spec = check_spec(cand.code, ws.card.abstract)
        if spec is not None and not issues:
            return cand, spec
    for cand in ordered:
        _, _, spec = check_spec(cand.code, ws.card.abstract)
        if spec is not None and spec.status in {"specified", "partial"}:
            return cand, spec
    return None, None


def run(
    arxiv_id: str,
    out: Path,
    *,
    budget_usd: float,
    model: str,
    effort: str,
    code_model: str,
    code_effort: str,
    variant: str = "swarm",
    seed: int = 0,
    llms: dict[str, LLM] | None = None,
    verbose: bool = True,
    backend: str = "anthropic",
    base_url: str | None = None,
    max_calls: int = 100,
    token_budget: int | None = None,
    max_seconds: float = 1800,
    code_budget_usd: float = 0.15,
    code_backend: str | None = None,
    code_base_url: str | None = None,
    local_parallel: int = 1,
    local_max_output_tokens: int = 4096,
) -> dict[str, Any]:
    if backend not in {"anthropic", "local"}:
        raise ValueError("backend must be anthropic or local")
    code_backend = code_backend or "anthropic"
    if code_backend not in {"anthropic", "local"}:
        raise ValueError("code backend must be anthropic or local")
    if max_calls <= 0 or max_seconds <= 0 or (token_budget is not None and token_budget <= 0):
        raise ValueError("execution limits must be positive")
    if local_parallel < 1 or not 1 <= local_max_output_tokens <= 16384:
        raise ValueError("local parallelism must be positive and output tokens between 1 and 16384")
    abstract = (DATASET_ABSTRACTS / f"arxiv-{arxiv_id}.txt").read_text(encoding="utf-8")
    run_dir = out / "runs" / arxiv_id
    # Keep historical paid runs unchanged. Local inference has resource limits, not prices.
    budget = (Budget(None, token_budget, max_calls=max_calls, max_seconds=max_seconds)
              if backend == "local" else Budget(budget_usd))
    settings = replace(
        Settings.from_env(backend=code_backend, model=code_model,
                          base_url=code_base_url or (base_url if code_backend == "local" else None)),
        model=code_model,
        effort=code_effort,
        max_tokens=16384,
        artifact_dir=run_dir / "blackbox",
    )
    sys_cfg = load_system(variant)
    cfg = SwarmConfig.from_dict(
        {k: v for k, v in sys_cfg.items() if k not in {"system"}} | {"models": [model]}
    )
    if backend == "local":
        # The simple GPU server serializes generation. Submit one action at a time
        # so each request's timeout measures generation rather than queue wait.
        cfg.parallel = local_parallel
    if llms is None:
        llms = {
            model: LLM(model, budget, backend, effort=effort,
                       max_tokens=local_max_output_tokens if backend == "local" else 16000,
                       mock_seed=seed, base_url=base_url)
        }
    ws = SpecWorkspace(spec_card(arxiv_id, abstract), budget, run_dir, settings, verbose)
    ws.code_budget = Budget(code_budget_usd) if backend == "local" and code_backend == "anthropic" else None
    swarm = SpecSwarm(ws, llms, cfg, seed)
    started = time.time()
    swarm.run()
    cand, spec = best_spec(ws)
    summary: dict[str, Any] = {
        "arxiv_id": arxiv_id,
        "status": "completed" if spec else "failed",
        "specification_status": spec.status if spec else None,
        "candidate": cand.id if cand else None,
        "candidate_gap": cand.gap if cand else None,
        "families": ws.families(),
        "candidates_total": len(ws.candidates),
        "input_tokens": budget.input_tokens,
        "output_tokens": budget.output_tokens,
        "usd": round(budget.usd, 4),
        "budget_usd": budget.max_usd,
        "execution_budget": budget.snapshot(),
        "code_budget": ws.code_budget.snapshot() if ws.code_budget is not None else None,
        "calls": budget.calls,
        "wall_seconds": round(time.time() - started, 1),
        "settings": {
            "variant": variant,
            "backend": backend,
            "agent_parallelism": cfg.parallel,
            "agent_max_output_tokens": local_max_output_tokens if backend == "local" else 16000,
            "model": model,
            "effort": effort,
            "runner_code_model": code_model,
            "runner_code_backend": code_backend,
            "runner_code_effort": code_effort,
            "seed": seed,
        },
        "swarm": {k: v for k, v in swarm.stats().items() if k not in {"ledger", "lineage"}},
    }
    if spec is None:
        summary["error"] = "no candidate produced a valid specification"
    else:
        spec_path = out / "specs" / f"{arxiv_id}.json"
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        external = ExternalSpec(source=SOURCE, arxiv_id=arxiv_id, specification=spec)
        spec_path.write_text(external.model_dump_json(indent=2) + "\n", encoding="utf-8")
        summary["specification"] = str(spec_path)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (run_dir / "all_candidates.json").write_text(
        json.dumps([c.model_dump() for c in ws.candidates.values()], indent=2)
    )
    ws.close()
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="a2m swarm writing a math spec for one paper.")
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--out", type=Path, default=Path("a2m_full"))
    parser.add_argument("--budget", type=float, default=0.15, help="Anthropic mode: USD per paper, all calls")
    parser.add_argument("--backend", choices=["anthropic", "local"], default="anthropic")
    parser.add_argument("--base-url", help="Local OpenAI-compatible URL, including /v1")
    parser.add_argument("--max-calls", type=int, default=100, help="Local run call limit, including code calls")
    parser.add_argument("--token-budget", type=int, help="Local run input+output token limit")
    parser.add_argument("--max-seconds", type=float, default=1800, help="Local run deadline, checked between actions")
    parser.add_argument("--code-budget", type=float, default=0.15, help="Local mode: USD cap for paid code calls only")
    parser.add_argument("--code-backend", choices=["anthropic", "local"], default="anthropic", help="Shared Anthropic code stage by default")
    parser.add_argument("--code-base-url", help="Separate local code server URL, if needed")
    parser.add_argument("--local-parallel", type=int, default=1, help="Concurrent local agent requests (default 1)")
    parser.add_argument("--local-max-output-tokens", type=int, default=4096, help="Local tokens per response")
    parser.add_argument("--model", help="Served local model name, or Anthropic model ID")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--code-model", help="Defaults to Sonnet; with local code, the swarm model")
    parser.add_argument("--code-effort", default="high")
    parser.add_argument("--variant", default="swarm", help="configs/systems/<variant>.yaml")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    try:
        summary = run(
            args.arxiv_id,
            args.out,
            budget_usd=args.budget,
            model=args.model or ("nemotron-quantum" if args.backend == "local" else "claude-sonnet-5-5"),
            effort=args.effort,
            code_model=args.code_model or (
                (args.model or "nemotron-quantum")
                if args.code_backend == "local" else "claude-sonnet-5-5"),
            code_effort=args.code_effort,
            variant=args.variant,
            seed=args.seed,
            verbose=not args.quiet,
            backend=args.backend,
            base_url=args.base_url,
            max_calls=args.max_calls,
            token_budget=args.token_budget,
            max_seconds=args.max_seconds,
            code_budget_usd=args.code_budget,
            code_backend=args.code_backend,
            code_base_url=args.code_base_url,
            local_parallel=args.local_parallel,
            local_max_output_tokens=args.local_max_output_tokens,
        )
    except (OSError, ValueError, LLMError) as exc:
        print("a2m spec run failed: " + str(exc)[:400], file=sys.stderr)
        return 1
    print(json.dumps({k: v for k, v in summary.items() if k != "swarm"}, indent=2))
    return 0 if summary["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
