"""Palindromic reversible circuits (self-inverse functions as conjugates of one Toffoli gate).

Gate library: NOT (X), CNOT (CX), multiple-controlled Toffoli (MCX); all are involutions.
A palindrome G = (g_1, ..., g_m, T, g_m, ..., g_1) with g_1 applied first realizes
f = H^{-1} o T o H with H = g_m o ... o g_1 (eq_2, eq_3).
Qubit index q (0-based, Qiskit little-endian) is circuit line q+1 of the specification;
basis state x = sum_q x_q 2^q (eq_1 encoding).
"""
from __future__ import annotations

import math
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _check_int(value, name, low, high):
    """Validate that value is a plain int within [low, high]."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < low or value > high:
        raise ValueError(f"{name}={value} out of range [{low}, {high}]")
    return value


def _normalize_gate(gate, n):
    """Validate a gate dict {'controls': [...], 'target': q} and return (tuple(controls), target)."""
    if not isinstance(gate, dict):
        raise ValueError("gate must be a dict with keys 'controls' and 'target'")
    if "target" not in gate or "controls" not in gate:
        raise ValueError("gate must have keys 'controls' and 'target'")
    target = _check_int(gate["target"], "target", 0, n - 1)
    controls_raw = gate["controls"]
    if not isinstance(controls_raw, list):
        raise ValueError("controls must be a list")
    controls = []
    for c in controls_raw:
        controls.append(_check_int(c, "control", 0, n - 1))
    if len(set(controls)) != len(controls):
        raise ValueError("controls must be distinct")
    if target in controls:
        raise ValueError("target must not be a control")
    return (tuple(controls), target)


def _apply_toffoli(qc, controls, target):
    """Apply T_c (eq_4): c=0 -> X, c=1 -> CX, c=2 -> CCX, c>=3 -> MCX. All involutive."""
    c = len(controls)
    if c == 0:
        qc.x(target)
    elif c == 1:
        qc.cx(controls[0], target)
    elif c == 2:
        qc.ccx(controls[0], controls[1], target)
    else:
        qc.mcx(list(controls), target)


def _synthesize_transposition(n, a, b):
    """Build (half, middle) so that the palindrome realizes the transposition (a b) (eq_6).

    d = a xor b; target p = highest differing bit; middle gate = Toffoli with all other
    lines as positive controls (swaps 2^n-1 and 2^n-1-2^p, t=1, eq_4).
    half (applied first, g_1 ... g_m): an X layer followed by CNOTs from p into the other
    bits of d, mapping {a, b} onto the two states swapped by the middle gate.
    """
    d = a ^ b
    p = d.bit_length() - 1
    half = []
    for q in range(n):
        if q == p:
            continue
        a_q = (a >> q) & 1
        a_p = (a >> p) & 1
        in_d = (d >> q) & 1
        # after the CNOT layer bit q of the image of a equals a_q ^ m_q ^ (a_p if in_d);
        # choose m_q so that this bit is 1.
        m_q = 1 ^ a_q ^ (a_p if in_d else 0)
        if m_q:
            half.append(((), q))
    for q in range(n):
        if q != p and ((d >> q) & 1):
            half.append(((p,), q))
    controls = tuple(q for q in range(n) if q != p)
    middle = (controls, p)
    return half, middle


def build_circuit(instance):
    """Return the palindromic circuit for the given instance.

    instance keys:
      'n'    : number of lines (1..12)
      'mode' : 'transposition' (keys 'a', 'b': basis states to swap, a != b)
               or 'explicit' (keys 'half': list of gate dicts g_1..g_m, 'middle': gate dict)
    Gate dicts are {'controls': [qubits], 'target': qubit} with 0-based qubit indices.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "mode" not in instance:
        raise ValueError("instance requires keys 'n' and 'mode'")
    n = _check_int(instance["n"], "n", 1, MAX_QUBITS)
    mode = instance["mode"]
    if mode == "transposition":
        if "a" not in instance or "b" not in instance:
            raise ValueError("transposition mode requires keys 'a' and 'b'")
        a = _check_int(instance["a"], "a", 0, 2 ** n - 1)
        b = _check_int(instance["b"], "b", 0, 2 ** n - 1)
        if a == b:
            raise ValueError("a and b must differ (f must be a genuine transposition)")
        half, middle = _synthesize_transposition(n, a, b)
    elif mode == "explicit":
        if "half" not in instance or "middle" not in instance:
            raise ValueError("explicit mode requires keys 'half' and 'middle'")
        half_raw = instance["half"]
        if not isinstance(half_raw, list):
            raise ValueError("half must be a list of gate dicts")
        half = [_normalize_gate(g, n) for g in half_raw]
        middle = _normalize_gate(instance["middle"], n)
    else:
        raise ValueError("mode must be 'transposition' or 'explicit'")

    lines = QuantumRegister(n, "lines")
    qc = QuantumCircuit(lines, name="palindrome")
    # eq_2 / eq_3: first half g_1..g_m (applied first), middle gate, mirrored half g_m..g_1.
    for controls, target in half:
        _apply_toffoli(qc, controls, target)
    _apply_toffoli(qc, middle[0], middle[1])
    for controls, target in reversed(half):
        _apply_toffoli(qc, controls, target)
    return qc
