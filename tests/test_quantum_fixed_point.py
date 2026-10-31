"""The quantum fixed-point search task.

Two things are checked: that the reference reproduces the paper's closed-form success
probability (so the sealed reference is right, not merely passing), and that the obvious
substitute - plain Grover with the same query budget - fails, which is what makes the task
discriminating rather than a formality.
"""

import numpy as np
import pytest

from a2m.evaluators import get
from a2m.evaluators.fixed_point_search import gamma, lambda_floor
from a2m.llm import mock_corpus as mc
from a2m.scoring import claim_gap, meets_claim
from a2m.tasks import load_card, load_vault

TASK = "arxiv-1409.3305"


def paper_success_probability(big_l: int, delta: float, lam: float) -> float:
    """Eq. 1: P_L = 1 - delta^2 T_L(T_{1/L}(1/delta) sqrt(1-lambda))^2."""
    x = np.cosh(np.arccosh(1 / delta) / big_l) * np.sqrt(1 - lam)
    t_l = np.cos(big_l * np.arccos(x)) if abs(x) <= 1 else np.cosh(big_l * np.arccosh(x))
    return float(1 - delta**2 * t_l**2)


@pytest.fixture(scope="module")
def card():
    return load_card(TASK)


def _run(card, code, systems, sandbox):
    ev = get(card.evaluator)
    return {t.name: ev.evaluate(code, t.params, sandbox, card) for t in systems}


def test_reference_matches_the_papers_closed_form(card, sandbox):
    """Every simulated point must equal Eq. 1, not just clear the bound."""
    _, reference = load_vault(TASK)
    system = card.test_systems[0]
    result = _run(card, reference, [system], sandbox)[system.name]
    assert result["ok"], result
    big_l = system.params["L"]
    delta = system.params["delta"]
    for lam, probability in result["stats"]["by_lambda"].items():
        assert probability == pytest.approx(paper_success_probability(big_l, delta, lam),
                                            abs=2e-5), lam


def test_reference_meets_the_claim_on_visible_and_hidden(card, sandbox):
    vault, reference = load_vault(TASK)
    results = _run(card, reference, card.test_systems + vault.hidden_test_systems, sandbox)
    assert meets_claim(card.criteria, results), results
    for name, r in results.items():
        assert r["metrics"]["queries_over_budget"] == 0, name
        assert r["metrics"]["min_success_probability"] >= 1 - 0.2**2 - 1e-6 or "0.15" in name


def test_plain_grover_fails_the_fixed_point_requirement(card, sandbox):
    """The souffle problem: tuned to one marked fraction, it collapses at others."""
    results = _run(card, mc.FIXED_POINT_PLAIN_GROVER, card.test_systems, sandbox)
    assert not meets_claim(card.criteria, results)
    worst = min(r["metrics"]["min_success_probability"] for r in results.values())
    assert worst < 0.7, f"plain Grover should collapse somewhere, worst was {worst}"
    # it is not disqualified on cost: it spends exactly the same number of queries
    assert all(r["metrics"]["queries_over_budget"] == 0 for r in results.values())


def test_overspending_queries_is_caught(card, sandbox):
    greedy = mc.FIXED_POINT_CHEBYSHEV.replace(
        "    for j in range(len(alpha)):",
        "    qc.append(oracle(n, 0.1), q)\n    for j in range(len(alpha)):")
    results = _run(card, greedy, card.test_systems, sandbox)
    assert all(r["metrics"]["queries_over_budget"] == 1 for r in results.values())
    assert claim_gap(card.criteria, results) > 0


def test_guaranteed_range_matches_the_paper(card):
    """lambda >= 1 - gamma^2 with 1/gamma = T_{1/L}(1/delta)."""
    for big_l, delta in ((5, 0.2), (7, 0.15), (9, 0.1)):
        assert gamma(big_l, delta) == pytest.approx(
            1 / np.cosh(np.arccosh(1 / delta) / big_l))
        floor = lambda_floor(big_l, delta)
        assert 0 < floor < 1
        # at the floor the bound is exactly saturated
        assert paper_success_probability(big_l, delta, floor) == pytest.approx(
            1 - delta**2, abs=1e-9)
    # every tested marked fraction sits inside the guaranteed range
    system = load_card(TASK).test_systems[0]
    floor = lambda_floor(system.params["L"], system.params["delta"])
    assert all(m / 2**system.params["n"] >= floor for m in system.params["marked_counts"])


def test_a_measured_circuit_is_rejected(card, sandbox):
    measured = mc.FIXED_POINT_CHEBYSHEV.replace(
        "    return [qc]", "    qc.measure_all()\n    return [qc]")
    results = _run(card, measured, card.test_systems, sandbox)
    assert not any(r["ok"] for r in results.values())


def test_the_oracle_cannot_be_inspected(card, sandbox):
    """The black box is a placeholder with no definition until the runner substitutes it."""
    probing = mc.FIXED_POINT_CHEBYSHEV.replace(
        "    qc = QuantumCircuit(n)",
        "    assert oracle(n, 0.3).definition is None\n    qc = QuantumCircuit(n)")
    results = _run(card, probing, card.test_systems, sandbox)
    assert meets_claim(card.criteria, results), results
