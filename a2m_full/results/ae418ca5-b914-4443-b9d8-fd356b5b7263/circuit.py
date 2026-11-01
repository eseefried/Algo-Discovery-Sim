from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _pair_cz(qc, n):
    # (-1)^(k(k-1)/2) for k excitations = product of CZ over all pairs
    for i in range(n):
        for j in range(i + 1, n):
            qc.cz(i, j)


def _exact_evolution(qc, n):
    # eq_2: exact many-body mirror transfer (free-fermion / Jordan-Wigner argument).
    # One-excitation sector: |j> -> (-i)^(n-1) |n-1-j> (spin-(n-1)/2 rotation by pi about x).
    # Many-body: mode reversal gives a sign (-1)^C(k,2) for k excitations -> CZ on all pairs.
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    _pair_cz(qc, n)
    alpha = -math.pi * (n - 1) / 2.0
    for q in range(n):
        qc.p(alpha, q)


def _trotter_evolution(qc, n, steps):
    # eq_1 and eq_3: H = 1/2 sum J_j (XX+YY); bond gate = RXX(theta) RYY(theta), theta = J_j * tau
    tau = (math.pi / 2.0) / steps
    for _ in range(steps):
        for j in range(1, n):
            theta = math.sqrt(j * (n - j)) * tau
            qc.rxx(theta, j - 1, j)
            qc.ryy(theta, j - 1, j)


def _undo_diagonal(qc, n):
    # eq_4: remove the CZ-pair sign and the uniform phase, leaving pure site reversal
    _pair_cz(qc, n)
    alpha = math.pi * (n - 1) / 2.0
    for q in range(n):
        qc.p(alpha, q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_sites', 4)
    method = instance.get('method', 'exact')
    steps = instance.get('trotter_steps', 8)
    corrected = instance.get('corrected', False)
    if not _is_int(n) or n < 2 or n > 12:
        raise ValueError('n_sites must be an integer in [2, 12]')
    if method not in ('exact', 'trotter'):
        raise ValueError('method must be exact or trotter')
    if not _is_int(steps) or steps < 1 or steps > 200:
        raise ValueError('trotter_steps must be an integer in [1, 200]')
    if not isinstance(corrected, bool):
        raise ValueError('corrected must be a bool')
    qc = QuantumCircuit(QuantumRegister(n, 'site'))
    if method == 'exact':
        _exact_evolution(qc, n)
    else:
        _trotter_evolution(qc, n, steps)
    if corrected:
        _undo_diagonal(qc, n)
    return qc
