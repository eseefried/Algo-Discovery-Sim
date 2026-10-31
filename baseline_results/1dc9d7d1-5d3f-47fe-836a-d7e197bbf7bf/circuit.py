"""Refined three-qubit Deutsch-Jozsa algorithm with f-controlled phase oracle.

The oracle U_f|x> = (-1)^{f(x)}|x> (eq_1) is decomposed through the algebraic
normal form of f (eq_3) into sigma_z, CZ and two-target CZ gates (eq_4, eq_5),
optionally sandwiched between Hadamard layers (eq_2). Paper qubit i (1-indexed,
leftmost in |x_1 x_2 x_3>) is Qiskit qubit n - i so that the Qiskit integer
label equals x = 4 x_1 + 2 x_2 + x_3.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
ALLOWED_KEYS = ("n", "anf", "truth_table", "include_hadamards", "merge_two_target", "enforce_promise")


def _bit(value, name):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int) and value in (0, 1):
        return value
    raise ValueError("%s must be 0 or 1" % name)


def _flag(instance, key, fallback):
    if key not in instance:
        return fallback
    value = instance[key]
    if not isinstance(value, bool):
        raise ValueError("%s must be a boolean" % key)
    return value


def _label(i, n):
    if isinstance(i, bool) or not isinstance(i, int) or i < 1 or i > n:
        raise ValueError("qubit label %r outside 1..%d" % (i, n))
    return i


def _anf_from_truth_table(table, n):
    """eq_3: GF(2) Moebius transform of the truth table; index x has bit (n-i) = x_i."""
    size = 1 << n
    if not isinstance(table, (list, tuple)) or len(table) != size:
        raise ValueError("truth_table must have length 2^n")
    coeff = [_bit(v, "truth_table entry") for v in table]
    for b in range(n):
        for m in range(size):
            if m & (1 << b):
                coeff[m] ^= coeff[m ^ (1 << b)]
    constant = coeff[0]
    linear = []
    quadratic = []
    for m in range(1, size):
        if coeff[m] == 0:
            continue
        labels = [n - b for b in range(n) if m & (1 << b)]
        if len(labels) == 1:
            linear.append(labels[0])
        elif len(labels) == 2:
            quadratic.append((min(labels), max(labels)))
        else:
            raise ValueError("f has an ANF monomial of degree >= 3; not realizable with Z, CZ and two-target CZ gates (eq_3)")
    return constant, sorted(linear), sorted(quadratic)


def _anf_from_dict(anf, n):
    """eq_3: ANF coefficients given directly (constant a0, linear labels, quadratic pairs)."""
    if not isinstance(anf, dict):
        raise ValueError("anf must be a dict")
    for key in anf:
        if key not in ("constant", "linear", "quadratic"):
            raise ValueError("unknown anf key %r" % key)
    constant = _bit(anf.get("constant", 0), "constant")
    linear_in = anf.get("linear", [])
    quadratic_in = anf.get("quadratic", [])
    if not isinstance(linear_in, (list, tuple)) or not isinstance(quadratic_in, (list, tuple)):
        raise ValueError("linear and quadratic must be lists")
    linear = sorted(set(_label(i, n) for i in linear_in))
    if len(linear) != len(linear_in):
        raise ValueError("duplicate linear terms")
    quadratic = []
    for pair in quadratic_in:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("quadratic terms must be pairs of qubit labels")
        i, j = _label(pair[0], n), _label(pair[1], n)
        if i == j:
            raise ValueError("quadratic term needs two distinct qubits")
        quadratic.append((min(i, j), max(i, j)))
    if len(set(quadratic)) != len(quadratic):
        raise ValueError("duplicate quadratic terms")
    return constant, linear, sorted(quadratic)


def _check_promise(constant, linear, quadratic, n):
    """eq_2 promise: f must be constant or balanced."""
    ones = 0
    for x in range(1 << n):
        bits = [(x >> (n - i)) & 1 for i in range(1, n + 1)]
        value = constant
        for i in linear:
            value ^= bits[i - 1]
        for i, j in quadratic:
            value ^= bits[i - 1] & bits[j - 1]
        ones += value
    if ones not in (0, 1 << n, 1 << (n - 1)):
        raise ValueError("f is neither constant nor balanced")


def _two_target_cz_gate():
    """eq_5: CZ_{c;t1 t2} = CZ_{c t1} CZ_{c t2}; gate qubit 0 is the control, 1 and 2 the targets."""
    sub = QuantumCircuit(3, name="CZ_c;t1t2")
    sub.cz(0, 1)
    sub.cz(0, 2)
    return sub.to_gate(label="CZ_c;t1t2")


def _append_oracle(qc, qr, n, constant, linear, quadratic, merge):
    """eq_1 / eq_4: U_f = (-1)^{a0} prod_i Z_i^{a_i} prod_{i<j} CZ_ij^{a_ij} (all factors commute)."""
    qc.global_phase += math.pi * constant
    for i in linear:
        qc.z(qr[n - i])
    remaining = list(quadratic)
    if merge:
        for c in range(1, n + 1):
            incident = [p for p in remaining if c in p]
            while len(incident) >= 2:
                p1 = incident.pop(0)
                p2 = incident.pop(0)
                remaining.remove(p1)
                remaining.remove(p2)
                t1 = p1[0] if p1[1] == c else p1[1]
                t2 = p2[0] if p2[1] == c else p2[1]
                qc.append(_two_target_cz_gate(), [qr[n - c], qr[n - t1], qr[n - t2]])
    for i, j in remaining:
        qc.cz(qr[n - i], qr[n - j])


def build_circuit(instance):
    """Return the refined DJ operation H^{xn} U_f H^{xn} (eq_2) or the bare oracle U_f."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in instance:
        if key not in ALLOWED_KEYS:
            raise ValueError("unknown instance key %r" % key)
    n = instance.get("n", 3)
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > MAX_QUBITS:
        raise ValueError("n must be an integer in 1..%d" % MAX_QUBITS)
    if ("anf" in instance) == ("truth_table" in instance):
        raise ValueError("provide exactly one of anf or truth_table")
    if "anf" in instance:
        constant, linear, quadratic = _anf_from_dict(instance["anf"], n)
    else:
        constant, linear, quadratic = _anf_from_truth_table(instance["truth_table"], n)
    include_h = _flag(instance, "include_hadamards", True)
    merge = _flag(instance, "merge_two_target", True)
    if _flag(instance, "enforce_promise", False):
        _check_promise(constant, linear, quadratic, n)
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr, name="refined_DJ")
    if include_h:
        qc.h(qr)  # eq_2: first Hadamard layer
    _append_oracle(qc, qr, n, constant, linear, quadratic, merge)
    if include_h:
        qc.h(qr)  # eq_2: second Hadamard layer (measurement left to the runner)
    return qc
