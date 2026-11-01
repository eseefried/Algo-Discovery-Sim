import json

import httpx
import pytest

from a2m.swarm.runtime import SwarmConfig
from algo_discovery import native_swarm as N
from algo_discovery.a2m_spec import spec_card
from algo_discovery.config import Settings
from algo_discovery.nemotron_equations import messages

ABSTRACT = "We apply a Hadamard gate to a single qubit and measure its output."
SPEC = {
    "status": "specified", "problem": "Apply Hadamard", "reconstruction_scope": "One qubit",
    "symbols": [], "equations": [{"id": "eq_1", "label": "H", "latex": "H",
        "description": "Hadamard", "provenance": "standard_background", "abstract_quote": None,
        "justification": "Definition", "assumptions": []}],
    "registers": [{"name": "q", "size": "1", "role": "input"}],
    "initial_state": "|0>", "steps": [{"description": "Apply H", "equation_ids": ["eq_1"]}],
    "measurement": "Measure q", "classical_postprocessing": None,
    "assumptions": [], "missing_information": [],
}


class Coordinator:
    def __init__(self, budget):
        self.budget, self.hypotheses = budget, 0
        self.tags = []

    def call(self, tag, system, prompt, schema, meta=None):
        self.budget.check()
        self.tags.append(tag)
        self.budget.charge("claude-sonnet-5-5", 100, 30)
        if tag == "hypothesize":
            self.hypotheses += 1
            return {"family": f"family{self.hypotheses}", "sketch": "Apply H", "assumptions": []}
        if tag == "implement":
            return {"specification": SPEC, "notes": "Added standard gate definition."}
        return {"decision": "pass", "reason": "Scope and implementation agree.", "stress_test": ""}


class Proposer:
    def __init__(self, budget):
        self.budget = budget

    def propose(self, abstract, profile, seed, who):
        self.budget.check()
        self.budget.charge("nemotron-quantum", 100, 30, local=True)
        return {"equations": [{"index": 1, "latex": "H"}], "complete": True}


@pytest.fixture
def setup(tmp_path):
    budget = N.HybridBudget(1, max_calls=100, max_seconds=60)
    settings = Settings(api_key="test", artifact_dir=tmp_path / "code")
    ws = N.NativeWorkspace(spec_card("1411.5949", ABSTRACT), budget, tmp_path / "run", settings, verbose=False)
    cfg = SwarmConfig.from_dict(N.load_system("nemotron_native_swarm"))
    cfg.models = ["nemotron-quantum"]
    swarm = N.NativeSwarm(ws, Coordinator(budget), Proposer(budget), cfg, 0)
    yield ws, swarm
    ws.close()


def test_failed_candidates_retry_cull_and_respawn_without_earning(setup, monkeypatch):
    ws, swarm = setup
    monkeypatch.setattr(ws, "build", lambda spec: (1.0, {
        "metrics": {}, "detail": "code stage abstained", "code_status": "insufficient_information"}))
    swarm.run()
    assert any(c.attempts >= 2 for c in ws.candidates.values())
    assert swarm.lineage.deaths and swarm.respawns > 0
    assert not swarm.lineage.successes
    assert all(a.earned == 0 for a in swarm.agents.values())
    assert not any(c.status == "ready" for c in ws.candidates.values())


def test_replacements_clone_a_successful_parent_and_mutate_one_gene(setup):
    _ws, swarm = setup
    swarm.start()
    donor, victim = swarm.agents["a01"], swarm.agents["a02"]
    donor.earned, donor.spent = 3, 1
    victim.energy = -1
    swarm._lifecycle()
    child = swarm.agents["a04"]
    assert child.parent == donor.id and child.generation == donor.generation + 1
    assert sum(swarm.genotypes[child.id][k] != swarm.genotypes[donor.id][k]
               for k in swarm.genotypes[child.id]) == 1
    assert len(swarm.alive()) == 3


def test_model_objection_never_counts_as_pass_or_verified_counterexample(setup):
    ws, swarm = setup
    swarm.start()
    cand = ws.new_candidate("qft", "sketch", "a01")
    cand.chain.append(("a01", "implement"))
    cand.attempts, cand.gap, cand.status = 1, 0, "passing"
    swarm._after_simulation(swarm.agents["a02"], cand)
    assert not swarm.lineage.successes  # No reward for execution before review.
    rec = {"critic": "a02", "verdict": "break", "confirmed": False, "reason": "Missing affine offset"}
    cand.critiques.append(rec)
    swarm._after_critique(swarm.agents["a02"], cand, rec)
    assert cand.status == "failing" and cand.gap == 1
    assert not swarm.lineage.successes
    assert any(n.kind == "needs_implementation" for n in swarm.index.needs.values())
    assert "Missing affine offset" in ws.diagnostics(cand)


def test_native_model_receives_only_training_format_and_costs_no_api_usd(tmp_path, monkeypatch):
    monkeypatch.setenv("NEMOTRON_GPU_LOCK", str(tmp_path / "gpu.lock"))
    seen = []

    def reply(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {
            "content": "(9) H=I\n<END_EQUATIONS>"}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 20}})

    client = httpx.Client(transport=httpx.MockTransport(reply))
    monkeypatch.setattr(N.httpx, "Client", lambda **kw: client)
    budget = N.HybridBudget(1)
    proposer = N.NativeProposer(budget, tmp_path, "http://localhost:8000/v1")
    profile = {"temperature": 0.6, "repetition_penalty": 1.18, "start": 9}
    out = proposer.propose(ABSTRACT, profile, 4, "a01")
    assert seen[0]["messages"] == messages(ABSTRACT, 9)
    assert seen[0]["response_format"] == {"type": "text"}
    assert out["complete"] and budget.paid.usd == 0 and budget.calls == 1


def test_paid_usage_counted_once_in_both_ledgers():
    budget = N.HybridBudget(1)
    budget.charge("nemotron-quantum", 1000, 1000, local=True)
    assert budget.usd == budget.paid.usd == 0
    budget.charge("claude-sonnet-5-5", 1000, 100)
    assert budget.usd == pytest.approx(0.003)
    assert budget.paid.usd == pytest.approx(budget.usd)
    assert budget.calls == 2 and budget.paid.calls == 1


def test_execution_and_independent_review_produce_ready_candidate_and_rewards(setup, monkeypatch):
    ws, swarm = setup
    monkeypatch.setattr(ws, "build", lambda spec: (0.0, {
        "metrics": {"num_qubits": 1, "cases_run": 1}, "detail": "built and simulated",
        "instance": {"n": 1}, "source": "def build_circuit(instance): ..."}))
    swarm.run()
    assert any(c.status == "ready" for c in ws.candidates.values())
    assert swarm.lineage.successes
    assert any(a.earned > 0 for a in swarm.agents.values())
    assert swarm.coordinator.tags.count("implement") == 1  # Validate first result before producing more branches.
    assert swarm.agents[swarm.reviewer_id].roles_played["implement"] == 0
    for cand in ws.candidates.values():
        if cand.status == "ready":
            assert cand.critiques and all(c["verdict"] == "pass" for c in cand.critiques)
            assert all(c["critic"] not in swarm._implementers(cand) for c in cand.critiques)


def test_coordinator_contract_matches_actual_worker_instead_of_sealed_harness():
    system = N.coordinator_system(ABSTRACT)
    assert "No a2m_task module" in system
    assert "may be compiled" in system
    assert "never certify black-box query complexity" in system
    assert "runner only substitutes placeholders" not in system
