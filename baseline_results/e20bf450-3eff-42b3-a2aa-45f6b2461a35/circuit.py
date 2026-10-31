"""Level-one QAOA cost+mixer unitary for bounded-occurrence Max E3LIN2.

Instance (JSON object):
  n          : number of boolean variables / qubits (1..12)
  equations  : list of [a, b, c, r]; a,b,c distinct 1-indexed variables, r in {0,1}
               meaning x_a + x_b + x_c = r (mod 2), sign d_e = (-1)^r (eq_1)
  gamma      : cost angle (real)
  beta       : mixer angle (real)
  D          : optional max-occurrence bound to enforce (positive int)
  prepare_plus_state : optional bool (default False). If True a Hadamard layer is
               prepended so the circuit maps |0>^n to the full QAOA state of eq_3;
               by default the runner is expected to supply |+>^n.

Qubit layout: variable x_j (j = 1..n) lives on Qiskit qubit j-1. Qiskit qubit 0 is
the least significant bit, so a measured bitstring reads x_n ... x_2 x_1 left to right.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    return value


def _as_angle(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    angle = float(value)
    if not math.isfinite(angle):
        raise ValueError(f"{name} must be finite")
    return angle


def _parse_equations(raw, n):
    """Validate equations and return list of (a, b, c, d) with 0-indexed qubits.

    Implements the sign convention d_e = (-1)^{r_e} of eq_1.
    """
    if not isinstance(raw, (list, tuple)) or len(raw) == 0:
        raise ValueError("equations must be a non-empty list")
    parsed = []
    for idx, eq in enumerate(raw):
        if not isinstance(eq, (list, tuple)) or len(eq) != 4:
            raise ValueError(f"equation {idx} must be [a, b, c, r]")
        a = _as_int(eq[0], f"equation {idx} variable a")
        b = _as_int(eq[1], f"equation {idx} variable b")
        c = _as_int(eq[2], f"equation {idx} variable c")
        r = _as_int(eq[3], f"equation {idx} parity r")
        for v in (a, b, c):
            if v < 1 or v > n:
                raise ValueError(f"equation {idx}: variable {v} out of range 1..{n}")
        if len({a, b, c}) != 3:
            raise ValueError(f"equation {idx}: variables must be distinct (E3LIN2)")
        if r not in (0, 1):
            raise ValueError(f"equation {idx}: parity r must be 0 or 1")
        d = 1 - 2 * r  # d_e = (-1)^{r_e}
        parsed.append((a - 1, b - 1, c - 1, d))
    return parsed


def _check_occurrence(parsed, n, bound):
    counts = [0] * n
    for a, b, c, _d in parsed:
        counts[a] += 1
        counts[b] += 1
        counts[c] += 1
    if bound is not None and max(counts) > bound:
        raise ValueError(
            f"a variable occurs in {max(counts)} equations, exceeding D={bound}"
        )


def _apply_cost_unitary(qc, qubits, parsed, gamma):
    """exp(-i gamma C) with C = sum_e (1 + d_e Z_a Z_b Z_c)/2  (eq_2, eq_3).

    Each term exp(-i (gamma/2) d_e Z_a Z_b Z_c) is realized by computing the parity
    onto qubit c with a CX ladder, applying Rz(gamma*d_e) = exp(-i gamma d_e Z/2),
    and uncomputing. The constant m/2 is kept as an exact global phase.
    """
    m = len(parsed)
    qc.global_phase -= gamma * m / 2.0
    for a, b, c, d in parsed:
        qc.cx(qubits[a], qubits[c])
        qc.cx(qubits[b], qubits[c])
        qc.rz(gamma * d, qubits[c])
        qc.cx(qubits[b], qubits[c])
        qc.cx(qubits[a], qubits[c])


def _apply_mixer_unitary(qc, qubits, beta):
    """exp(-i beta B) with B = sum_j X_j, i.e. Rx(2 beta) on every qubit (eq_3)."""
    for q in qubits:
        qc.rx(2.0 * beta, q)


def build_circuit(instance):
    """Return the level-one QAOA unitary exp(-i beta B) exp(-i gamma C) (eq_3)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    if "n" not in instance or "equations" not in instance:
        raise ValueError("instance requires keys 'n' and 'equations'")
    if "gamma" not in instance or "beta" not in instance:
        raise ValueError("instance requires keys 'gamma' and 'beta'")
    n = _as_int(instance["n"], "n")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError(f"n must be in 1..{MAX_QUBITS}, got {n}")
    gamma = _as_angle(instance["gamma"], "gamma")
    beta = _as_angle(instance["beta"], "beta")
    parsed = _parse_equations(instance["equations"], n)
    bound = None
    if "D" in instance and instance["D"] is not None:
        bound = _as_int(instance["D"], "D")
        if bound < 1:
            raise ValueError("D must be a positive integer")
    _check_occurrence(parsed, n, bound)
    prepare = False
    if "prepare_plus_state" in instance:
        prepare = instance["prepare_plus_state"]
        if not isinstance(prepare, bool):
            raise ValueError("prepare_plus_state must be a boolean")

    qreg = QuantumRegister(n, "q")
    qc = QuantumCircuit(qreg, name="qaoa_p1_e3lin2")
    qubits = [qreg[i] for i in range(n)]
    if prepare:
        # Optional |+>^n layer of eq_3; off by default (runner prepares input).
        for q in qubits:
            qc.h(q)
    _apply_cost_unitary(qc, qubits, parsed, gamma)
    _apply_mixer_unitary(qc, qubits, beta)
    return qc
