"""Native Nemotron proposals with a2m selection, energy, retries and lineage.

Sonnet plans, assembles specs, writes code and reviews. Nemotron receives ONLY
its training-format abstract/numbered-LaTeX prompt. Fitness is execution plus
model review, not a certificate of scientific correctness.
"""

import argparse
import json
import os
import time
from dataclasses import asdict, replace
from pathlib import Path
from uuid import uuid4

import httpx

from a2m import actions
from a2m.llm import prompts as P
from a2m.llm.client import LLM, Budget, BudgetExhausted, LLMError
from a2m.run import load_system
from a2m.swarm.matching import choose
from a2m.swarm.runtime import Swarm, SwarmConfig

from . import a2m_spec as spec_actions
from .config import Settings
from .external_spec import DATASET_ABSTRACTS, ExternalSpec
from .nemotron_equations import equation_key, generation_slot, messages, parse_block
from .schemas import MathSpecification
from .simulation_cli import simulate_source

PROFILES = [
    {"temperature": 0.0, "repetition_penalty": 1.12, "start": 1},
    {"temperature": 0.35, "repetition_penalty": 1.08, "start": 1},
    {"temperature": 0.6, "repetition_penalty": 1.18, "start": 9},
]
REVIEW_SCHEMA = {
    "type": "object", "properties": {
        "decision": {"type": "string", "enum": ["pass", "revise"]},
        "reason": {"type": "string"}, "stress_test": {"type": "string"}},
    "required": ["decision", "reason", "stress_test"], "additionalProperties": False,
}
HARNESS = """Actual execution contract: build_circuit(instance) returns a bound,
measurement-free Qiskit unitary built from standard gates. No a2m_task module,
opaque-oracle substitution, sealed tests or oracle query counter exists in this
worker. Explicit classical oracle parameters (a, b, marked states) may be compiled
into gates for functional simulation. Do not reject that solely because it is not
an opaque oracle. Equally, never certify black-box query complexity or claim the
parameters were hidden. Input preparation and output decoding must be documented.
Evaluate the stated algorithmic operation and coverage honestly; a circuit that
only solves a narrower task must disclose that limitation."""


def coordinator_system(abstract):
    return (spec_actions.SPEC_SYSTEM.format(domain=HARNESS, abstract=abstract)
            + "\nSpecification rules:\n" + spec_actions.SPEC_RULES)


class HybridBudget(Budget):
    """Separate virtual/compute limits from estimated paid API spend."""

    def __init__(self, max_usd, *, max_calls=40, max_seconds=1200):
        super().__init__(None, max_calls=max_calls, max_seconds=max_seconds)
        self.paid = Budget(max_usd)

    @property
    def exhausted(self):
        return super().exhausted or self.paid.exhausted

    def charge(self, model, inp, out, cache_read=0, *, local=False):
        super().charge(model, inp, out, cache_read, local=local)
        if not local:
            self.paid.charge(model, inp, out, cache_read)


class NativeProposer:
    def __init__(self, budget, directory, base_url):
        self.budget, self.directory, self.base_url = budget, directory, base_url
        self.serial = 0

    def propose(self, abstract, profile, seed, who):
        self.budget.check()
        self.serial += 1
        directory = self.directory / f"{self.serial:03}-{who}"
        directory.mkdir(parents=True)
        body = {"model": "nemotron-quantum", "messages": messages(abstract, profile["start"]),
                "max_tokens": 2048, "response_format": {"type": "text"},
                "max_time_seconds": 240, "seed": seed,
                "temperature": profile["temperature"],
                "repetition_penalty": profile["repetition_penalty"]}
        (directory / "request.json").write_text(json.dumps(body, indent=2))
        headers = {"Authorization": "Bearer " + os.environ["NEMOTRON_API_KEY"]} if os.getenv("NEMOTRON_API_KEY") else {}
        try:
            with httpx.Client(timeout=300, headers=headers) as client, generation_slot():
                self.budget.check()
                response = client.post(self.base_url.rstrip("/") + "/chat/completions", json=body)
            (directory / "response.txt").write_text(response.text)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            self.budget.charge("nemotron-quantum", 0, 0, local=True)
            raise LLMError(f"Native proposal request failed: {type(exc).__name__}") from exc
        usage = payload.get("usage") or {}
        self.budget.charge("nemotron-quantum", usage.get("prompt_tokens", 0),
                           usage.get("completion_tokens", 0), local=True)
        choice = payload["choices"][0]
        text = choice["message"]["content"]
        (directory / "equations.txt").write_text(text)
        if choice["finish_reason"] != "stop":
            raise LLMError("Native equation output truncated.")
        eqs, complete = parse_block(text, profile["start"])
        return {"equations": eqs, "complete": complete, "artifacts": str(directory),
                "unique_equations": len({equation_key(e["latex"]) for e in eqs}),
                "profile": dict(profile), "seed": seed}


class NativeWorkspace(spec_actions.SpecWorkspace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_budget = None  # All paid stages share HybridBudget.paid exactly once.
        self.evidence = {}

    def simulate(self, cand):
        gap = super().simulate(cand)
        if gap > 0:
            # No rewards for parsing a spec or receiving a code-stage abstention.
            cand.gap = 1.0
            cand.results["spec"]["metrics"]["gap"] = 1.0
        return cand.gap

    def diagnostics(self, cand):
        text = super().diagnostics(cand)
        reviews = [c["reason"] for c in cand.critiques if c.get("verdict") == "break"]
        return "\n".join([text, *reviews]).strip()


class NativeSwarm(Swarm):
    def __init__(self, workspace, coordinator, proposer, cfg, seed):
        super().__init__(workspace, {"nemotron-quantum": coordinator}, cfg, seed)
        self.coordinator, self.proposer, self.seed = coordinator, proposer, seed
        self.genotypes = {}
        self.reviewer_id = None

    def _new_agent(self, parent=None, energy=None):
        if parent is None:
            donors = [a for a in self.agents.values() if a.earned > 0]
            if donors:
                parent = max(donors, key=lambda a: a.earned / max(a.spent, 1))
        agent = super()._new_agent(parent, energy)
        if parent is not None:
            profile = dict(self.genotypes[parent.id])
            gene = self.rng.choice(list(profile))
            choices = {"temperature": [0.0, 0.2, 0.35, 0.6],
                       "repetition_penalty": [1.05, 1.08, 1.12, 1.18, 1.22],
                       "start": [1, 9, 17]}[gene]
            profile[gene] = self.rng.choice([value for value in choices if value != profile[gene]])
        else:
            profile = dict(PROFILES[(len(self.agents) - 1) % len(PROFILES)])
        self.genotypes[agent.id] = profile
        if ((self.reviewer_id is None and len(self.agents) == self.cfg.n_agents)
                or (self.reviewer_id is not None and not self.agents[self.reviewer_id].alive)):
            self.reviewer_id = agent.id
        self.ws.log("genotype", agent=agent.id, parent=agent.parent, generation=agent.generation,
                    profile=profile)
        return agent

    def _call(self, tag, prompt, schema, who):
        self.ws.log("model_start", who=who, action=tag, provider="sonnet")
        try:
            return self.coordinator.call(tag, coordinator_system(self.ws.card.abstract), prompt, schema, {})
        except BudgetExhausted:
            return None
        except LLMError as exc:
            self.ws.log("llm_error", who=who, action=tag, error=str(exc))
            return None

    def _step(self):
        # Settle each action immediately, so simulation/review can precede more
        # proposal generation. Reserve one agent outside all implementation chains.
        agents = self.alive()
        self.rng.shuffle(agents)
        for agent in agents:
            if self.stop_reason():
                break
            self._maintain_needs()
            needs = list(self.index.open_needs(agent.id))
            if agent.id == self.reviewer_id:
                needs = [n for n in needs if n.kind != "needs_implementation"]
            few = self.cfg.diversity_first and len(self.ws.families()) < self.cfg.min_families
            if self.index.count("needs_critique"):
                needs = [n for n in needs if n.kind == "needs_critique"]
            elif self.index.count("needs_simulation"):
                needs = [n for n in needs if n.kind == "needs_simulation"]
            elif few:
                needs = [n for n in needs if n.kind == "needs_hypothesis"]
            elif any(n.kind == "needs_implementation" for n in needs):
                needs = [n for n in needs if n.kind == "needs_implementation"]
            need = choose(needs, agent.affinities, self.ws.tick, self.rng)
            if need:
                need.claimed_by.add(agent.id)
            result = self._execute(agent, need)
            self._apply(agent, need, result)

    def _execute(self, agent, need):
        if need is None:
            return None
        cand = self.ws.candidates.get(need.candidate) if need.candidate else None
        if need.kind == "needs_hypothesis":
            prompt = P.hypothesize(self.ws.families(), self.cfg.diversity_first, agent.notes)
            out = self._call("hypothesize", prompt, P.HYPOTHESIZE_SCHEMA, agent.id)
            if not out or not out.get("sketch"):
                return None
            family = out["family"].strip().lower().replace(" ", "_")[:60]
            cand = self.ws.new_candidate(family, out["sketch"], agent.id)
            self.ws.log("hypothesis", who=agent.id, cand=cand.id, family=family)
            return cand
        if need.kind == "needs_implementation":
            return self._implement(agent, cand)
        if need.kind == "needs_simulation":
            return actions.simulate(self.ws, agent.id, cand)
        if need.kind == "needs_critique":
            return self._review(agent, cand)
        raise ValueError(need.kind)

    def _implement(self, agent, base):
        cand = self.ws.child(base) if base.code else base
        cand.attempts = base.attempts + 1
        cand.chain.append((agent.id, "implement"))
        cand.status = "implemented"
        self.ws.log("native_start", who=agent.id, cand=cand.id, profile=self.genotypes[agent.id])
        try:
            prediction = self.proposer.propose(self.ws.card.abstract, self.genotypes[agent.id],
                                               self.seed + self._n * 100 + self.ws.tick, agent.id)
            self.ws.evidence[cand.id] = prediction
            previous = self.ws.diagnostics(base) if base.results else ""
            prompt = (
                "Assemble an implementable MathSpecification from this method plan and an "
                "equation-specialist's unverified predictions. You may reject wrong predictions "
                "and derive missing standard steps using background knowledge, but disclose "
                "corrections and additions in notes and label provenance honestly. Supply "
                "registers, encoding, steps and measurement. Preserve the abstract's substantive "
                "goal; do not replace it with an unrelated easy operation merely to pass a build. "
                "Never claim the paper was read. Return insufficient_information when necessary.\n"
                f"Method family: {base.family}\nSketch: {base.sketch}\n"
                f"Native predictions: {json.dumps(prediction['equations'])}\n"
                f"Previous spec: {base.code[:20000] if base.results else ''}\n"
                f"Runner/reviewer feedback: {previous[:6000]}\nLineage feedback: {agent.notes}"
            )
            out = self._call("implement", prompt, spec_actions.IMPLEMENT_SCHEMA, agent.id)
            if out is None:
                raise LLMError("Coordinator did not return a complete specification.")
            cand.code = json.dumps(out["specification"])
            self.ws.evidence[cand.id]["coordinator_notes"] = out.get("notes", "")
            native_keys = {equation_key(e["latex"]) for e in prediction["equations"]}
            assembled = out["specification"].get("equations", [])
            retained = sum(equation_key(e["latex"]) in native_keys for e in assembled)
            self.ws.evidence[cand.id].update(
                assembled_equations=len(assembled), native_equations_retained_by_text=retained,
                coordinator_added_or_rewritten_equations=len(assembled) - retained)
        except (BudgetExhausted, LLMError, ValueError, KeyError, TypeError, IndexError) as exc:
            cand.code = json.dumps({"failed_native_or_assembly": str(exc)[:400]})
            agent.last_failure = str(exc)[:400]
            self.ws.log("implementation_failure", who=agent.id, cand=cand.id, error=str(exc)[:400])
        self.ws.log("implement", who=agent.id, cand=cand.id, attempt=cand.attempts)
        return cand

    def _review(self, agent, cand):
        if agent.id in self._implementers(cand):
            raise ValueError("An implementer cannot review its own candidate.")
        built = cand.results["spec"]
        source = built.get("source", "")
        prompt = (
            "Independently review the ACTUAL generated circuit against the abstract and spec. "
            "Return pass only if it faithfully implements its stated scope without hiding "
            "a missing central requirement, nonsensical equations, or a trivial substitute. "
            "Otherwise return revise with actionable reasons. A simulated circuit is not "
            "proof of algorithm correctness. Optionally give a valid larger instance as "
            "a JSON string in stress_test (or an empty string); use only existing keys.\n"
            f"Specification: {cand.code}\nActual source:\n{source}\n"
            f"Instance: {json.dumps(built.get('instance'))}\nExecution: {built.get('detail')}"
        )
        out = self._call("critique", prompt, REVIEW_SCHEMA, agent.id)
        if out is None:
            return None
        rec = {"critic": agent.id, "verdict": "pass" if out["decision"] == "pass" else "break",
               "reason": out["reason"], "confirmed": False, "stress_test": None,
               "review_basis": "model_judgment"}
        if out.get("stress_test"):
            try:
                instance = built["instance"]
                patch = json.loads(out["stress_test"])
                if isinstance(patch, dict) and patch and set(patch) <= set(instance):
                    stress = {**instance, **patch}
                    _, result = simulate_source(source, stress, "none")
                    rec.update(stress_test=stress, stress_result=result.detail[:400])
                    rec["confirmed"] = result.status == "failed" and not any(
                        word in result.detail for word in ("ValueError", "limits", "cap"))
                    if rec["confirmed"]:
                        rec.update(verdict="break", review_basis="reproduced_execution_failure")
            except (ValueError, TypeError, KeyError):
                rec["stress_invalid"] = True
        cand.critiques.append(rec)
        self.ws.log("critique", who=agent.id, cand=cand.id, verdict=rec["verdict"],
                    confirmed=rec["confirmed"], reason=rec["reason"][:300])
        return rec

    def _after_critique(self, agent, cand, rec):
        if rec and rec["verdict"] == "break" and not rec["confirmed"]:
            # A model objection is not a verified counterexample or a passing review.
            cand.status, cand.gap = "failing", 1.0
            self.lineage.record_failure(cand.family, "Reviewer requested revision: " + rec["reason"][:250])
            implementer = self._implementer(cand)
            if implementer:
                implementer.last_failure = rec["reason"][:300]
            if cand.attempts < self.cfg.max_attempts:
                self.index.open("needs_implementation", cand.id, self.ws.tick, promise=1.0)
            self.ws.log("review_revision", cand=cand.id, reason=rec["reason"][:300])
            return
        return super()._after_critique(agent, cand, rec)

    def _after_simulation(self, agent, cand):
        if cand.gap == 0 and self.cfg.critics_enabled:
            # Execution is provisional: defer financial rewards until review passes.
            self.index.open("needs_critique", cand.id, self.ws.tick, promise=1.0,
                            exclude=self._implementers(cand))
            self.ws.log("execution_pass_review_pending", cand=cand.id)
            return
        return super()._after_simulation(agent, cand)

    def _ready(self, cand):
        payout = self.economy.progress_payout(self.ws.parent_gap(cand), cand.gap,
                                              self.ws.best_gap(exclude=cand.id))
        self.economy.distribute(cand.chain, payout, self.agents, self.ws.tick,
                                f"reviewed_progress:{cand.id}")
        if payout > 0:
            for role, aid in {r: a for a, r in cand.chain}.items():
                self.lineage.record_success(aid, self.ws.tick, cand.family, role,
                                            payout * self.cfg.economy.credit.get(role, 0), cand.gap)
        return super()._ready(cand)


def run(paper, out, *, max_usd=0.5, max_calls=40, max_seconds=1200, seed=0,
        coordinator=None, proposer=None, config=None):
    abstract = (DATASET_ABSTRACTS / f"arxiv-{paper}.txt").read_text()
    directory = out / "runs" / paper / str(uuid4())
    budget = HybridBudget(max_usd, max_calls=max_calls, max_seconds=max_seconds)
    settings = replace(Settings.from_env(backend="anthropic", model="claude-sonnet-5-5"),
                       effort="high", max_tokens=16384, artifact_dir=directory / "blackbox")
    ws = NativeWorkspace(spec_actions.spec_card(paper, abstract), budget, directory, settings)
    coordinator = coordinator or LLM("claude-sonnet-5-5", budget, effort="medium", max_tokens=8192)
    proposer = proposer or NativeProposer(budget, directory / "native",
                                         os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1"))
    cfg = SwarmConfig.from_dict(config or load_system("nemotron_native_swarm"))
    cfg.models, cfg.parallel = ["nemotron-quantum"], 1
    swarm = NativeSwarm(ws, coordinator, proposer, cfg, seed)
    started = time.monotonic()
    try:
        swarm.run()
        ready = [c for c in ws.ranked() if c.status == "ready"]
        summary = {"paper": paper, "system": "hybrid_native_equation_swarm",
                   "status": "ready" if ready else "no_reviewed_candidate",
                   "fitness": "Docker/Aer execution plus independent-agent model review; not certified scientific correctness",
                   "selected_candidate": ready[0].id if ready else None,
                   "directory": str(directory), "wall_seconds": round(time.monotonic() - started, 2),
                   "budget": budget.snapshot(), "paid_budget": budget.paid.snapshot(),
                   "swarm": swarm.stats(), "genotypes": swarm.genotypes,
                   "config": asdict(cfg), "seed": seed,
                   "execution_policy": "settle_each_action_prioritize_validation_reserved_reviewer",
                   "coordinator_model": "claude-sonnet-5-5", "code_model": "claude-sonnet-5-5/high"}
        (directory / "summary.json").write_text(json.dumps(summary, indent=2))
        (directory / "all_candidates.json").write_text(json.dumps([c.model_dump() for c in ws.candidates.values()], indent=2))
        (directory / "native_evidence.json").write_text(json.dumps(ws.evidence, indent=2))
        if ready:
            chosen = ready[0]
            spec = ExternalSpec(source="hybrid_native_swarm", arxiv_id=paper,
                                specification=MathSpecification.model_validate_json(chosen.code))
            (directory / "selected_spec.json").write_text(spec.model_dump_json(indent=2))
            summary["selected_code_artifacts"] = str(settings.artifact_dir / chosen.results["spec"]["code_run_id"])
            (directory / "summary.json").write_text(json.dumps(summary, indent=2))
        return summary
    finally:
        ws.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--out", type=Path, default=Path("artifacts/native_swarm"))
    parser.add_argument("--max-usd", type=float, default=0.5)
    parser.add_argument("--max-calls", type=int, default=40)
    parser.add_argument("--max-seconds", type=float, default=1200)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.arxiv_id, args.out, max_usd=args.max_usd,
                 max_calls=args.max_calls, max_seconds=args.max_seconds, seed=args.seed)
    print(json.dumps({k: v for k, v in result.items() if k not in {"swarm", "genotypes"}}, indent=2))
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
