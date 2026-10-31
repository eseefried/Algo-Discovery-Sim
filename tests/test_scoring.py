from a2m.schema import Criterion
from a2m.scoring import claim_gap, criterion_gap, meets_claim

GE = Criterion(metric="s", comparator=">=", target=1.0, tolerance=0.05)
LE = Criterion(metric="q", comparator="<=", target=2, scale=2.0)


def test_criterion_gap():
    assert criterion_gap(GE, 0.96) == 0.0
    assert abs(criterion_gap(GE, 0.5) - 0.45) < 1e-9
    assert criterion_gap(LE, 2) == 0.0 and criterion_gap(LE, 3) == 0.5
    assert criterion_gap(LE, 99) == 1.0 and criterion_gap(GE, None) == 1.0


def test_failed_run_counts_as_full_miss():
    res = {"a": {"ok": True, "metrics": {"s": 1.0, "q": 2}}, "b": {"ok": False, "error": "x"}}
    assert claim_gap([GE, LE], res) == 0.5
    assert meets_claim([GE, LE], res) is False


def test_meets_claim():
    res = {"a": {"ok": True, "metrics": {"s": 1.0, "q": 2}}}
    assert meets_claim([GE, LE], res) is True
    assert meets_claim([GE, LE], {}) is False
