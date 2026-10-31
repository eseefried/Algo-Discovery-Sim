"""Quantum order finding (QOFA) circuit for Shor's algorithm.

build_circuit(instance) returns the unitary part of one QOFA run:
Hadamards on the control register, controlled modular multiplications
by a^(2^j) mod N (eq_3 / eq_4), and the inverse QFT on the control
register (eq_4).  Measurement and classical post-processing (eq_2, eq_5)
are left to the runner.

Layout: control qubits 0..t-1 (qubit j controls U_a^(2^j); qubit 0 is
the least significant bit of x and of the outcome m), work qubits
t..t+n-1 (integer y mod N, qubit t is the least significant bit).
Expected input state: |0>^t on control and |1> (integer one) on work.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('N', 'a', 't'):
        if key not in instance:
            raise ValueError('instance is missing key ' + key)
    big_n = _as_int(instance['N'], 'N')
    a = _as_int(instance['a'], 'a')
    t = _as_int(instance['t'], 't')
    if big_n < 3:
        raise ValueError('N must be at least 3')
    if not 1 < a < big_n:
        raise ValueError('a must satisfy 1 < a < N')
    if math.gcd(a, big_n) != 1:
        raise ValueError('a must be coprime to N (eq_1)')
    if t < 1:
        raise ValueError('t must be at least 1')
    n = (big_n - 1).bit_length()  # n = ceil(log2 N) work qubits
    if t + n > MAX_QUBITS:
        raise ValueError('t + ceil(log2 N) exceeds the qubit cap of %d' % MAX_QUBITS)
    if 'b' in instance:
        b = _as_int(instance['b'], 'b')
        if not 1 < b < big_n or (b * b) % big_n != a:
            raise ValueError('b must satisfy 1 < b < N and b^2 = a (mod N) (eq_5)')
    include_h = instance.get('include_hadamards', True)
    if not isinstance(include_h, bool):
        raise ValueError('include_hadamards must be a boolean')
    return big_n, a, t, n, include_h


def _mult_permutation(c, big_n, n):
    # eq_3: y -> c*y mod N for y < N, identity for N <= y < 2^n
    dim = 1 << n
    perm = list(range(dim))
    for y in range(big_n):
        perm[y] = (c * y) % big_n
    return perm


def _cycles_to_transpositions(perm):
    # cycle (c0 c1 ... ck-1) with perm[ci] = c(i+1) equals the time-ordered
    # sequence of transpositions (c0 c1), (c0 c2), ..., (c0 ck-1)
    seen = [False] * len(perm)
    pairs = []
    for start in range(len(perm)):
        if seen[start] or perm[start] == start:
            seen[start] = True
            continue
        cycle = []
        cur = start
        while not seen[cur]:
            seen[cur] = True
            cycle.append(cur)
            cur = perm[cur]
        for k in range(1, len(cycle)):
            pairs.append((cycle[0], cycle[k]))
    return pairs


def _controlled_transposition(qc, ctrl, work, x, y, n):
    # Controlled swap of basis states |x> and |y> of the work register.
    # V = CNOTs from pivot bit p to the other differing bits makes Vx, Vy
    # differ only at p; then a multi-controlled X (with ctrl added) on p
    # swaps exactly that pair; V is undone afterwards.
    diff = [i for i in range(n) if ((x >> i) & 1) != ((y >> i) & 1)]
    p = diff[0]
    others = diff[1:]
    xp = (x >> p) & 1
    for i in others:
        qc.cx(work[p], work[i])
    zero_ctrls = []
    for i in range(n):
        if i == p:
            continue
        bit = (x >> i) & 1
        if i in others:
            bit ^= xp
        if bit == 0:
            zero_ctrls.append(work[i])
    for q in zero_ctrls:
        qc.x(q)
    controls = [ctrl] + [work[i] for i in range(n) if i != p]
    qc.mcx(controls, work[p])
    for q in zero_ctrls:
        qc.x(q)
    for i in reversed(others):
        qc.cx(work[p], work[i])


def _controlled_mod_mult(qc, ctrl, work, c, big_n, n):
    # eq_3: controlled U_c with U_c|y> = |c y mod N> (y < N), identity otherwise
    perm = _mult_permutation(c, big_n, n)
    for x, y in _cycles_to_transpositions(perm):
        _controlled_transposition(qc, ctrl, work, x, y, n)


def build_circuit(instance):
    big_n, a, t, n, include_h = _validate(instance)
    control = QuantumRegister(t, 'ctrl')
    work = QuantumRegister(n, 'work')
    qc = QuantumCircuit(control, work, name='qofa_N%d_a%d' % (big_n, a))
    # eq_4: uniform superposition over exponents x on the control register
    if include_h:
        for j in range(t):
            qc.h(control[j])
    # eq_4: control qubit j (bit j of x) controls U_{a^(2^j) mod N},
    # so the work register ends in |a^x mod N> for input |1>
    for j in range(t):
        c = pow(a, 1 << j, big_n)
        if c != 1:
            _controlled_mod_mult(qc, control[j], work, c, big_n, n)
    # eq_4: inverse QFT on the control register (qubit 0 least significant)
    qc.append(QFTGate(t).inverse(), [control[j] for j in range(t)])
    return qc
