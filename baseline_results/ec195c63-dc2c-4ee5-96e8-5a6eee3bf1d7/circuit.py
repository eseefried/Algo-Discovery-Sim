"""Exact bit-flip oracle U_f for a classical Boolean function f (instance: OR_n).

Scoped construction (eq_1, eq_4; building blocks eq_2, eq_3):
    U_f = (I (x) H_y) . D_f . (I (x) H_y),   D_f |x,y> = (-1)^{y f(x)} |x,y>.
Writing g(z) = y*f(x), z = (x, y), the real function pi*g has a Walsh expansion
    pi*g(z) = sum_S a_S chi_S(z),   chi_S(z) = (-1)^{z . S},
so D_f = prod_S exp(i a_S chi_S).  Every factor is realised by
  * a parity gate (CNOT fan-in of the qubits in S into an ancilla); the parity
    gate is the Hadamard-conjugate of the unbounded fan-out gate F_m of eq_2,
  * an R_Z rotation diag(e^{i a_S}, e^{-i a_S}) on the ancilla (eq_3),
  * the uncomputing parity gate (ancilla returned to |0>).
All factors commute.  In the fan-out + R_Z depth model they may be applied in
parallel on 2^(n+1) ancillas (constant depth); here they are serialised in
batches over `num_ancilla` ancillas because of the 12-qubit cap, so the Qiskit
depth of the returned circuit is NOT constant.

Qubit layout: qubits 0..n-1 = input register x (x_j on qubit n-j, so the string
x_1...x_n reads as the big-endian bitstring of the register), qubit n = target
y, qubits n+1..n+num_ancilla = ancillas (must be supplied in |0>).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
TOL = 1e-12


def _read_int(instance, key, fallback):
    if key in instance:
        value = instance[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(key + ' must be an integer')
        return value
    return fallback


def _truth_table(instance, n):
    """eq_4: f = OR_n (default) or an explicit truth table of any f."""
    size = 1 << n
    function = instance['function'] if 'function' in instance else 'or'
    if function == 'or':
        # OR_n(x) = 1 - [|x| = 0]: only the all-zero string maps to 0.
        return [0 if i == 0 else 1 for i in range(size)]
    if function == 'truth_table':
        if 'truth_table' not in instance:
            raise ValueError('truth_table required when function == truth_table')
        table = instance['truth_table']
        if not isinstance(table, (list, tuple)) or len(table) != size:
            raise ValueError('truth_table must have 2**n entries')
        out = []
        for v in table:
            if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
                raise ValueError('truth_table entries must be 0 or 1')
            out.append(v)
        return out
    raise ValueError('function must be or or truth_table')


def _walsh_coefficients(table, n):
    """Return a_S, S a bitmask over qubits 0..n, with pi*y*f(x) = sum_S a_S chi_S(z)."""
    m = n + 1
    size = 1 << m
    mask_x = (1 << n) - 1
    a = [0.0] * size
    for z in range(size):
        y = (z >> n) & 1
        x = z & mask_x
        a[z] = math.pi * y * table[x]
    h = 1
    while h < size:
        for i in range(0, size, 2 * h):
            for j in range(i, i + h):
                u = a[j]
                v = a[j + h]
                a[j] = u + v
                a[j + h] = u - v
        h *= 2
    return [c / size for c in a]


def _bits(mask):
    out = []
    q = 0
    while mask:
        if mask & 1:
            out.append(q)
        mask >>= 1
        q += 1
    return out


def build_circuit(instance):
    """Build the exact oracle U_f |x>|y>|0..0> = |x>|y xor f(x)>|0..0> (eq_1)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _read_int(instance, 'n', None)
    if n is None or n < 1:
        raise ValueError('n must be a positive integer')
    k = _read_int(instance, 'num_ancilla', 1)
    if k < 1:
        raise ValueError('num_ancilla must be >= 1')
    total = n + 1 + k
    if total > MAX_QUBITS:
        raise ValueError('n + 1 + num_ancilla must not exceed 12')
    table = _truth_table(instance, n)
    coeffs = _walsh_coefficients(table, n)

    x = QuantumRegister(n, 'x')
    y = QuantumRegister(1, 'y')
    anc = QuantumRegister(k, 'a')
    qc = QuantumCircuit(x, y, anc, name='U_f')
    data = list(x) + [y[0]]  # qubit index q in a mask S refers to data[q]

    # eq_1: X^{f(x)} on y = H Z^{f(x)} H ; the middle part is the diagonal D_f.
    qc.h(y[0])
    # S = empty set: global phase exp(i a_0).
    qc.global_phase += coeffs[0]
    terms = [(s, coeffs[s]) for s in range(1, len(coeffs)) if abs(coeffs[s]) > TOL]
    # Commuting parity-phase factors; batches of size k are the serialised
    # version of what the fan-out model does in a single parallel layer.
    for start in range(0, len(terms), k):
        batch = terms[start:start + k]
        # eq_2 (parity gate = H-conjugated fan-out): compute z.S into ancilla t.
        for t, (s, _c) in enumerate(batch):
            for q in _bits(s):
                qc.cx(data[q], anc[t])
        # eq_3: R_Z on the parity ancilla, rz(-2a) = diag(e^{ia}, e^{-ia}) = exp(i a chi_S).
        for t, (_s, c) in enumerate(batch):
            qc.rz(-2.0 * c, anc[t])
        # Uncompute the parity (ancilla back to |0>).
        for t, (s, _c) in enumerate(batch):
            for q in reversed(_bits(s)):
                qc.cx(data[q], anc[t])
    qc.h(y[0])
    return qc
