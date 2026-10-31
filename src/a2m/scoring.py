"""Distance from a set of simulation results to the claim. 0 means the claim holds."""

from __future__ import annotations

from typing import Any

from a2m.schema import Criterion


def criterion_gap(c: Criterion, value: float | None) -> float:
    if value is None:
        return 1.0
    if c.comparator == ">=":
        violation = (c.target - c.tolerance) - value
    elif c.comparator == "<=":
        violation = value - (c.target + c.tolerance)
    else:
        violation = abs(value - c.target) - c.tolerance
    return min(1.0, max(0.0, violation) / c.scale)


def claim_gap(criteria: list[Criterion], results: dict[str, dict[str, Any]]) -> float:
    """Mean criterion gap over all test systems. A failed run counts as a full miss."""
    if not results:
        return 1.0
    gaps = []
    for outcome in results.values():
        metrics = outcome.get("metrics", {}) if outcome.get("ok") else {}
        gaps.extend(criterion_gap(c, metrics.get(c.metric)) for c in criteria)
    return sum(gaps) / len(gaps)


def meets_claim(criteria: list[Criterion], results: dict[str, dict[str, Any]]) -> bool:
    return bool(results) and all(bool(o.get("ok")) for o in results.values()) and bool(
        claim_gap(criteria, results) == 0.0
    )
