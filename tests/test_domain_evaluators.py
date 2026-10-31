"""Cross-domain evaluators: a correct method passes and a plausible wrong one fails.

Each domain gets the same treatment the quantum tasks already had - the sealed reference is
checked against something independent of it, and the obvious substitute is shown to fail, so
a passing score means the method worked rather than the test being lenient.
"""

import numpy as np
import pytest
from scipy.optimize import minimize

from a2m.backends import alchemi
from a2m.evaluators import get
from a2m.llm import mock_corpus as mc
from a2m.scoring import claim_gap, meets_claim
from a2m.skills import tool_module
from a2m.tasks import load_card

lj = tool_module("materials", "lj")
chem = tool_module("chemistry", "chem")
rna = tool_module("biology", "rna")
p2 = tool_module("dynamics", "potential2d")

MATERIALS = "arxiv-cond-mat-9803344"
CHEMISTRY = "arxiv-1909.11655"
BIOLOGY = "arxiv-2010.02141"
DYNAMICS = "arxiv-cond-mat-0205527"


def evaluate(task, code, params, sandbox):
    card = load_card(task)
    result = get(card.evaluator).evaluate(code, params, sandbox, card)
    return card, result


def passes(card, result):
    return meets_claim(card.criteria, {"t": result})


# ------------------------------------------------------------------ independent references


@pytest.mark.parametrize("n", [5, 7, 9, 13])
def test_lj_global_minima_reproduce_by_multistart(n):
    """The tabulated minima the materials task scores against, re-derived here."""
    def value_and_grad(flat):
        energy, forces = lj.energy_forces(flat.reshape(-1, 3))
        return energy, -forces.ravel()

    def relax(seed):
        x0 = lj.random_cluster(n, seed, radius=1.3 * n ** (1 / 3))
        res = minimize(value_and_grad, x0.ravel(), jac=True, method="L-BFGS-B",
                       options={"maxiter": 3000, "ftol": 1e-14, "gtol": 1e-8})
        return float(res.fun)

    best = min(relax(s) for s in range(400))
    assert best == pytest.approx(lj.GLOBAL_MINIMA[n], abs=1e-5)


def test_lj_forces_match_finite_differences():
    x = lj.random_cluster(6, 3)
    _, forces = lj.energy_forces(x)
    step = 1e-6
    for i in range(len(x)):
        for k in range(3):
            up, down = x.copy(), x.copy()
            up[i, k] += step
            down[i, k] -= step
            numeric = -(lj.energy(up) - lj.energy(down)) / (2 * step)
            assert forces[i, k] == pytest.approx(numeric, abs=1e-4)


@pytest.mark.skipif(not alchemi.available(), reason="NVIDIA ALCHEMI Toolkit not installed")
def test_alchemi_agrees_with_the_runners_own_energy():
    for n in (7, 13):
        x = lj.random_cluster(n, 1)
        assert alchemi.energy(x) == pytest.approx(lj.energy(x), rel=1e-9)
        assert alchemi.cross_check(x, lj.energy(x)) == "alchemi:agrees"


def test_dynamics_reference_barrier_is_grid_independent():
    """The scored barrier comes from a bottleneck search, not from any path method."""
    evaluator = get("transition_path")
    start, end = np.array(p2.MINIMUM_A), np.array(p2.MINIMUM_B)
    coarse = evaluator.reference_barrier(start, end, {"grid_n": 351})
    fine = evaluator.reference_barrier(start, end, {"grid_n": 701})
    assert fine == pytest.approx(coarse, abs=0.01)
    assert fine == pytest.approx(-40.66, abs=0.05)   # the known Mueller-Brown saddle


def test_rna_best_binder_scores_near_one():
    target = rna.random_target(50, 11)
    normalizer = rna.normalizer_for(target, 14)
    assert rna.fitness(rna.best_binder(target, 14), target, normalizer) == pytest.approx(1.0)
    assert rna.fitness(rna.random_target(14, 3), target, normalizer) < 0.6


def test_penalized_logp_rejects_invalid_molecules():
    assert chem.score("not a molecule") == float("-inf")
    assert chem.is_valid("CCO") and not chem.is_valid("C(((")
    assert chem.similarity("CCO", "CCO") == pytest.approx(1.0)
    assert chem.similarity("CCO", "c1ccccc1") < 0.2


# --------------------------------------------------------------------- materials: search


def test_basin_hopping_finds_the_global_minimum(sandbox):
    card, result = evaluate(MATERIALS, mc.CLUSTER_BASIN_HOPPING,
                            {"n": 7, "seeds": [0, 1], "time_budget_s": 8}, sandbox)
    assert result["ok"], result
    assert result["metrics"]["success_rate"] == 1.0
    assert passes(card, result)


def test_a_broken_up_cluster_is_rejected(sandbox):
    scattered = '''
def search(spec):
    return [[8.0 * i, 0.0, 0.0] for i in range(spec["n"])]
'''
    _, result = evaluate(MATERIALS, scattered,
                            {"n": 7, "seeds": [0], "time_budget_s": 5}, sandbox)
    assert not result["ok"] and "broken apart" in result["error"]


def test_a_wrong_shaped_answer_is_rejected(sandbox):
    _, result = evaluate(MATERIALS, "def search(spec):\n    return [[0.0, 0.0]]\n",
                            {"n": 7, "seeds": [0], "time_budget_s": 5}, sandbox)
    assert not result["ok"] and "(7, 3)" in result["error"]


# -------------------------------------------------------------------- chemistry: molecules


def test_constrained_search_improves_and_stays_similar(sandbox):
    params = {"starts": ["CC(=O)Oc1ccccc1C(=O)O"], "similarity_threshold": 0.6,
              "n_return": 10, "seed": 0, "time_budget_s": 25}
    card, result = evaluate(CHEMISTRY, mc.CHEM_GA, params, sandbox)
    assert result["ok"], result
    assert result["metrics"]["mean_improvement"] >= 1.0
    assert result["metrics"]["constraint_rate"] == 1.0
    assert passes(card, result)


def test_blind_chain_extension_fails_the_similarity_constraint(sandbox):
    """The reason the visible system uses the tighter threshold."""
    params = {"starts": ["CC(=O)Oc1ccccc1C(=O)O"], "similarity_threshold": 0.6,
              "n_return": 10, "seed": 0, "time_budget_s": 25}
    card, result = evaluate(CHEMISTRY, mc.CHEM_APPEND_CARBONS, params, sandbox)
    assert result["ok"], result
    assert result["metrics"]["constraint_rate"] < 1.0
    assert not passes(card, result)


# ------------------------------------------------------------------------ biology: design


def test_model_guided_search_beats_random_within_the_same_budget(sandbox):
    params = {"length": 14, "target_length": 50, "target_seed": 11, "rounds": 6,
              "batch_size": 60, "seed": 0}
    _, guided = evaluate(BIOLOGY, mc.RNA_THRESHOLD_GREEDY, params, sandbox)
    _, random_batches = evaluate(BIOLOGY, mc.RNA_RANDOM, params, sandbox)
    assert guided["ok"] and random_batches["ok"]
    assert guided["metrics"]["best_fitness"] > random_batches["metrics"]["best_fitness"]
    assert guided["metrics"]["measurements_used"] == random_batches["metrics"]["measurements_used"]


def test_the_measurement_budget_is_enforced(sandbox):
    greedy_overspender = '''
def propose(measured, spec):
    a, L = spec["alphabet"], spec["length"]
    import numpy as np
    rng = np.random.default_rng(spec["round_index"])
    n = spec["batch_size"] * 5                       # asks for five times the budget
    return ["".join(a[i] for i in rng.integers(len(a), size=L)) for _ in range(n)]
'''
    params = {"length": 14, "target_length": 50, "target_seed": 11, "rounds": 3,
              "batch_size": 40, "seed": 0}
    _, result = evaluate(BIOLOGY, greedy_overspender, params, sandbox)
    assert result["ok"], result
    assert result["metrics"]["measurements_used"] == 120      # 3 rounds x 40, not 600
    assert result["metrics"]["over_batch"] == 480


def test_invalid_sequences_are_counted_and_dropped(sandbox):
    sloppy = '''
def propose(measured, spec):
    return ["XXXX"] * spec["batch_size"]
'''
    params = {"length": 14, "target_length": 50, "target_seed": 11, "rounds": 2,
              "batch_size": 10, "seed": 0}
    _, result = evaluate(BIOLOGY, sloppy, params, sandbox)
    assert not result["ok"] and "no valid sequence" in result["error"]


# ---------------------------------------------------------------------- dynamics: paths


def test_normal_force_string_recovers_the_barrier(sandbox):
    params = {"n_images": 24, "seed": 0, "time_budget_s": 15}
    card, result = evaluate(DYNAMICS, mc.STRING_NORMAL_FORCE, params, sandbox)
    assert result["ok"], result
    assert abs(result["metrics"]["barrier_error"]) < 0.1
    assert passes(card, result)


def test_plain_descent_collapses_the_path(sandbox):
    """Without projecting out the tangential force the images fall into the minima."""
    params = {"n_images": 24, "seed": 0, "time_budget_s": 15}
    card, result = evaluate(DYNAMICS, mc.STRING_PLAIN_DESCENT, params, sandbox)
    assert result["ok"], result
    assert result["metrics"]["barrier_error"] > 1.0
    assert not passes(card, result)


def test_a_coarse_path_cannot_hide_the_barrier(sandbox):
    """A two-point path is densely resampled before the barrier is measured."""
    shortcut = '''
def find_path(start, end, spec):
    mid = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
    return [list(start), mid, list(end)]
'''
    params = {"n_images": 24, "seed": 0, "time_budget_s": 10}
    card, result = evaluate(DYNAMICS, shortcut, params, sandbox)
    assert result["ok"], result
    assert result["metrics"]["barrier_error"] > 1.0
    assert not passes(card, result)


def test_moving_the_endpoints_is_caught(sandbox):
    drifting = mc.STRING_NORMAL_FORCE.replace(
        "    path[0], path[-1] = start, end\n", "")
    params = {"n_images": 24, "seed": 0, "time_budget_s": 10}
    card, result = evaluate(DYNAMICS, drifting, params, sandbox)
    assert result["ok"], result
    assert claim_gap(card.criteria, {"t": result}) >= 0.0
