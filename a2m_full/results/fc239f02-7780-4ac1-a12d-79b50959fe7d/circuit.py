from __future__ import annotations

import math

from qiskit import QuantumCircuit


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_qubits')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('num_qubits must be an integer in 1..12')
    t = instance.get('time')
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or t <= 0:
        raise ValueError('time must be a positive finite number')
    r = instance.get('steps')
    if isinstance(r, bool) or not isinstance(r, int) or r < 1 or r > 200:
        raise ValueError('steps must be an integer in 1..200')
    terms = instance.get('terms')
    if not isinstance(terms, list) or len(terms) < 1 or len(terms) > 200:
        raise ValueError('terms must be a list of 1..200 entries')
    parsed = []
    for term in terms:
        if not isinstance(term, dict):
            raise ValueError('each term must be a dict')
        c = term.get('coeff')
        p = term.get('pauli')
        if isinstance(c, bool) or not isinstance(c, (int, float)) or not math.isfinite(c):
            raise ValueError('coeff must be a finite real number')
        if not isinstance(p, str) or len(p) != n or any(ch not in 'IXYZ' for ch in p):
            raise ValueError('pauli must be a string of length num_qubits over IXYZ')
        parsed.append((float(c), p))
    if r * 2 * len(parsed) > 20000:
        raise ValueError('circuit too large')
    return n, float(t), r, parsed


def _pauli_rotation(qc, pauli, angle):
    # Implements exp(-i * angle/2 * P) = basis change, CX ladder, Rz(angle), uncompute.
    # Character i of the Pauli string acts on qubit i (little-endian).
    support = [i for i, ch in enumerate(pauli) if ch != 'I']
    if not support:
        qc.global_phase -= angle / 2.0
        return
    for i in support:
        ch = pauli[i]
        if ch == 'X':
            qc.h(i)
        elif ch == 'Y':
            qc.sdg(i)
            qc.h(i)
    target = support[-1]
    for i in support[:-1]:
        qc.cx(i, target)
    qc.rz(angle, target)
    for i in reversed(support[:-1]):
        qc.cx(i, target)
    for i in support:
        ch = pauli[i]
        if ch == 'X':
            qc.h(i)
        elif ch == 'Y':
            qc.h(i)
            qc.s(i)


def build_circuit(instance):
    """Second-order Trotter circuit S_2(t/r)^r for H = sum_j c_j P_j (eq_2)."""
    n, t, r, terms = _validate(instance)
    dt = t / r
    qc = QuantumCircuit(n, name='trotter2')
    for _ in range(r):
        # Time order: A_1..A_L then A_L..A_1, with A_j = exp(-i c_j P_j dt/2).
        # Each rotation is Rz(2*c_j*dt/2) = Rz(c_j*dt).
        for c, p in terms:
            _pauli_rotation(qc, p, c * dt)
        for c, p in reversed(terms):
            _pauli_rotation(qc, p, c * dt)
    return qc
