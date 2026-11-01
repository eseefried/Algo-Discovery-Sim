import json
from types import SimpleNamespace

import pytest

from a2m.llm.client import Budget
from algo_discovery import a2m_spec
from algo_discovery.simulation import SimulationCase, SimulationReport

ARXIV_ID = "1411.5949"
QUOTE = "Quantum Fourier Transform"
SPEC = {
    "status": "partial",
    "problem": "Add two registers with the QFT.",
    "reconstruction_scope": "Two 2-qubit registers.",
    "symbols": [{"symbol": "a", "meaning": "addend", "domain": "integers mod 4"}],
    "equations": [
        {
            "id": "eq_1",
            "label": "QFT adder",
            "latex": r"|a\rangle|b\rangle \mapsto |a\rangle|a+b \bmod 4\rangle",
            "description": "In-place addition.",
            "provenance": "abstract_inferred",
            "abstract_quote": QUOTE,
            "justification": "The abstract names QFT arithmetic.",
            "assumptions": [],
        }
    ],
    "registers": [{"name": "a", "size": "2", "role": "addend"}],
    "initial_state": "|a>|b>",
    "steps": [{"description": "QFT, phases, inverse QFT.", "equation_ids": ["eq_1"]}],
    "measurement": "Measure b.",
    "classical_postprocessing": None,
    "assumptions": ["Two qubits per register."],
    "missing_information": [],
}


class FakeLLM:
    """Answers each a2m role; charges the shared budget like the real client."""

    def __init__(self, budget, critique="pass"):
        self.budget, self.critique, self.calls = budget, critique, []

    def call(self, tag, system, prompt, schema, meta=None):
        self.budget.check()
        self.budget.charge("claude-sonnet-5-5", 1000, 500)
        self.calls.append((tag, system, prompt))
        if tag == "hypothesize":
            return {
                "family": f"qft_adder_{len(self.calls)}",
                "sketch": "QFT then phases.",
                "assumptions": [],
            }
        if tag == "implement":
            return {"specification": SPEC, "notes": ""}
        return {
            "verdict": self.critique,
            "reason": "checked",
            "stress_test": json.dumps({"n": 9}) if self.critique == "break" else "",
        }


@pytest.fixture
def runner(monkeypatch):
    """Stub the black-box code stage and the Docker/Aer simulation."""
    monkeypatch.setenv("CLAUDE_HACKATHON_API", "test-key")
    seen = {"code_calls": 0, "sim_instances": []}

    def generate_code(request, settings):
        seen["code_calls"] += 1
        directory = settings.artifact_dir / f"code{seen['code_calls']}"
        directory.mkdir(parents=True)
        (directory / "instance.json").write_text('{"n": 2}')
        return SimpleNamespace(
            run_id=directory.name,
            usage=SimpleNamespace(
                input_tokens=500,
                output_tokens=300,
                cache_creation_input_tokens=0,
                cache_read_input_tokens=0,
            ),
            artifact=SimpleNamespace(
                status="generated", source_python="def build_circuit(i): ...", summary="adder"
            ),
            static_checks_passed=True,
            validation=SimpleNamespace(status="build_passed", detail="ok"),
        )

    def simulate_source(source, instance, reference, *args, **kwargs):
        seen["sim_instances"].append(instance)
        ok = instance.get("n", 0) <= 4
        case = SimulationCase(
            input={"basis_state": 0},
            initial_basis_state=0,
            counts={"00": 1},
            probabilities={"00": 1.0},
        )
        return "{}", SimulationReport(
            status="simulated" if ok else "failed",
            detail="ok" if ok else "wrong output",
            cases_run=1,
            num_qubits=4,
            cases=[case],
        )

    monkeypatch.setattr(a2m_spec, "generate_code", generate_code)
    monkeypatch.setattr(a2m_spec, "simulate_source", simulate_source)
    return seen


def run(tmp_path, critique="pass", budget_usd=0.15):
    budget = Budget(budget_usd)
    llm = FakeLLM(budget, critique)
    original = a2m_spec.Budget
    a2m_spec.Budget = lambda _usd: budget
    try:
        summary = a2m_spec.run(
            ARXIV_ID,
            tmp_path,
            budget_usd=budget_usd,
            model="claude-sonnet-5-5",
            effort="medium",
            code_model="claude-sonnet-5-5",
            code_effort="high",
            llms={"claude-sonnet-5-5": llm},
            verbose=False,
        )
    finally:
        a2m_spec.Budget = original
    return summary, llm, budget


def test_swarm_writes_a_spec_that_the_runner_built(tmp_path, runner):
    summary, llm, budget = run(tmp_path)
    assert summary["status"] == "completed" and summary["candidate_gap"] == 0.0
    saved = json.loads((tmp_path / "specs" / f"{ARXIV_ID}.json").read_text())
    assert saved["source"] == "a2m_swarm" and saved["arxiv_id"] == ARXIV_ID
    assert saved["specification"]["equations"][0]["id"] == "eq_1"
    tags = {tag for tag, _, _ in llm.calls}
    assert {"hypothesize", "implement", "critique"} <= tags
    # The runner's code-stage calls are charged to the same per-paper budget.
    assert runner["code_calls"] >= 1
    assert budget.calls == len(llm.calls) + runner["code_calls"]
    assert summary["usd"] <= 0.15 + 0.02  # one in-flight round may finish past the cap


def test_prompts_carry_the_abstract_and_spec_rules_but_never_the_paper(tmp_path, runner):
    _, llm, _ = run(tmp_path)
    abstract = (a2m_spec.DATASET_ABSTRACTS / f"arxiv-{ARXIV_ID}.txt").read_text()
    for tag, system, prompt in llm.calls:
        assert abstract in system
        assert "papers/" not in system + prompt and "equations/" not in system + prompt
        if tag == "implement":
            assert "Label EVERY equation with provenance" in system
            assert "single scientific reconstruction agent" not in system


def test_confirmed_break_needs_the_runner_to_reproduce_it(tmp_path, runner):
    run(tmp_path, critique="break")
    stressed = [i for i in runner["sim_instances"] if i.get("n") == 9]
    assert stressed, "the critic's stress instance was rebuilt and simulated"
    candidates = json.loads((tmp_path / "runs" / ARXIV_ID / "all_candidates.json").read_text())
    critiques = [k for c in candidates for k in c["critiques"]]
    assert any(k["confirmed"] for k in critiques)


@pytest.mark.parametrize(
    ("change", "gap_floor"),
    [
        ({"status": "insufficient_information", "missing_information": ["x"]}, 0.3),
        ({"equations": [SPEC["equations"][0] | {"abstract_quote": "not in the abstract"}]}, 0.9),
    ],
)
def test_spec_checks_rank_bad_specs_above_zero(change, gap_floor):
    abstract = (a2m_spec.DATASET_ABSTRACTS / f"arxiv-{ARXIV_ID}.txt").read_text()
    gap, issues, _ = a2m_spec.check_spec(json.dumps(SPEC | change), abstract)
    assert gap >= gap_floor and issues
    gap, issues, _ = a2m_spec.check_spec(json.dumps(SPEC), abstract)
    assert gap == 0.3 and not issues  # passes the checks; only the build test can reach 0


@pytest.mark.parametrize("code_budget", [0.0, 0.001])
def test_local_swarm_has_execution_limits_and_separate_paid_cap(tmp_path, runner, monkeypatch, code_budget):
    # Real local transport is tested separately. Here exercise the full spec swarm loop.
    monkeypatch.setattr(a2m_spec, "LLM", lambda model, budget, *a, **kw: FakeLLM(budget))
    summary = a2m_spec.run(
        ARXIV_ID, tmp_path, backend="local", budget_usd=0.0,
        model="nemotron-quantum", effort="medium", code_model="claude-sonnet-5-5",
        code_effort="high", max_calls=30, code_budget_usd=code_budget, verbose=False,
        code_backend="anthropic",
    )
    assert summary["status"] == "completed"
    assert summary["budget_usd"] is None
    assert summary["execution_budget"]["max_calls"] == 30
    assert summary["calls"] > 1  # zero dollar budget does not stop local workers
    assert summary["settings"]["backend"] == "local"
    assert summary["settings"]["agent_parallelism"] == 1
    assert summary["settings"]["agent_max_output_tokens"] == 4096
    assert runner["code_calls"] == (0 if code_budget == 0 else 1)
