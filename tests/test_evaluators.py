"""Known-correct implementations pass; deliberately wrong ones fail (offset, bit order, query
count, rotation sign, leaked carry)."""

import pytest

from a2m.evaluators import get
from a2m.llm import mock_corpus as mc
from a2m.scoring import claim_gap, meets_claim
from a2m.tasks import load_vault


def _run(card, code, systems=None):
    ev = get(card.evaluator)
    systems = systems or card.test_systems
    return {t.name: ev.evaluate(code, t.params, _run.sandbox, card) for t in systems}


@pytest.fixture(autouse=True)
def _bind(sandbox):
    _run.sandbox = sandbox


def test_affine_reference_passes_visible_and_hidden(affine_card):
    vault, ref = load_vault(affine_card.task_id)
    res = _run(affine_card, ref, affine_card.test_systems + vault.hidden_test_systems)
    assert meets_claim(affine_card.criteria, res), res
    assert all(r["metrics"]["oracle_queries"] == 2 for r in res.values())


@pytest.mark.parametrize("code,ok", [
    (mc.AFFINE_COHERENT, True),
    (mc.AFFINE_INDEPENDENT_F0, True),
    (mc.AFFINE_COHERENT_BITORDER_BUG, False),
    (mc.AFFINE_BV_ONLY, False),
    (mc.AFFINE_CLASSICAL, False),
])
def test_affine_variants(affine_card, code, ok):
    res = _run(affine_card, code)
    assert meets_claim(affine_card.criteria, res) is ok, res


def test_affine_offset_missing_scores_half(affine_card):
    res = _run(affine_card, mc.AFFINE_BV_ONLY)
    assert all(r["metrics"]["success_rate"] == 0.5 for r in res.values())


def test_classical_meets_accuracy_but_not_query_bound(affine_card):
    res = _run(affine_card, mc.AFFINE_CLASSICAL)
    assert all(r["metrics"]["success_rate"] == 1.0 for r in res.values())
    assert 0 < claim_gap(affine_card.criteria, res) < 1


def test_adder_reference_passes_visible_and_hidden(adder_card):
    vault, ref = load_vault(adder_card.task_id)
    res = _run(adder_card, ref, adder_card.test_systems + vault.hidden_test_systems)
    assert meets_claim(adder_card.criteria, res), res


@pytest.mark.parametrize("code,ok", [
    (mc.ADDER_QFT, True),
    (mc.ADDER_INCREMENT, True),
    (mc.ADDER_QFT_SIGN_BUG, False),
    (mc.ADDER_CARRY_QUBIT, False),
])
def test_adder_variants(adder_card, code, ok):
    res = _run(adder_card, code)
    assert meets_claim(adder_card.criteria, res) is ok, res


def test_candidate_cannot_see_oracle_secret(affine_card):
    peek = mc.AFFINE_COHERENT.replace(
        "    n = spec[\"n\"]\n    qc = QuantumCircuit(n + 1, n + 1)",
        "    n = spec[\"n\"]\n    assert oracle(n + 1).definition is None\n"
        "    qc = QuantumCircuit(n + 1, n + 1)", 1)
    res = _run(affine_card, peek)
    assert meets_claim(affine_card.criteria, res), res


def test_static_check_rejects_file_access(affine_card):
    bad = mc.AFFINE_COHERENT + "\nSECRET = open('/etc/hostname').read()\n"
    res = _run(affine_card, bad)
    assert not any(r["ok"] for r in res.values())
    assert "static check failed" in next(iter(res.values()))["error"]


def test_qubit_cap_enforced(affine_card):
    wide = mc.AFFINE_COHERENT.replace("QuantumCircuit(n + 1, n + 1)", "QuantumCircuit(n + 9, n + 1)")
    res = _run(affine_card, wide)
    assert not any(r["ok"] for r in res.values())
