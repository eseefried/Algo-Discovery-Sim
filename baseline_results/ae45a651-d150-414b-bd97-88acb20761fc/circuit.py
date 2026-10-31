'''Discrete-time coined quantum-walk search operator U^t = (S C)^t on a 4-regular
circulant graph (vertices Z_n, offsets +-1 and +-m), with the marked vertex w encoded
directly in the circuit (no black-box oracle).  Exposes build_circuit(instance).

Layout (Qiskit little-endian): position register pos[0..npos-1] holds the vertex label
x in binary (pos[j] is bit 2^j); coin register coin[0] (= c0) and coin[1] (= c1) holds
the direction c = c0 + 2*c1 with displacements (+1, -1, +m, -m) for c = 0, 1, 2, 3.
'''
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12
COIN_SIZE = 2
MAX_STEPS = 10000


def _require_int(instance, key, minimum):
    if key not in instance:
        raise ValueError('missing instance key: ' + key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError('instance key must be an integer: ' + key)
    if value < minimum:
        raise ValueError('instance key below minimum: ' + key)
    return value


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _require_int(instance, 'n', 8)
    if n & (n - 1) != 0:
        raise ValueError('n must be a power of two')
    npos = n.bit_length() - 1
    if npos + COIN_SIZE > MAX_QUBITS:
        raise ValueError('too many qubits: n <= 1024 required')
    m = _require_int(instance, 'm', 2)
    if not (1 < m < n // 2):
        raise ValueError('m must satisfy 1 < m < n/2')
    w = _require_int(instance, 'w', 0)
    if w >= n:
        raise ValueError('w must satisfy 0 <= w < n')
    t = _require_int(instance, 't', 0)
    if t > MAX_STEPS:
        raise ValueError('t too large')
    return n, npos, m, w, t


def _grover_coin(qc, coin):
    # eq_4 (unmarked part): C_0 = 2|s><s| - I = -(H H)(X X) CZ (X X)(H H) on the coin.
    # The leading minus sign is an unconditional global phase, tracked exactly.
    qc.h(coin[0])
    qc.h(coin[1])
    qc.x(coin[0])
    qc.x(coin[1])
    qc.cz(coin[0], coin[1])
    qc.x(coin[0])
    qc.x(coin[1])
    qc.h(coin[0])
    qc.h(coin[1])
    qc.global_phase += math.pi


def _marked_correction(qc, coin, pos, npos, w):
    # eq_4 (marked part, oracle-free): on |x> = |w> apply C_1 C_0^{-1} = -C_0 = I - 2|s><s|
    # = (H H)(X X) CZ (X X)(H H); controlled on x = w this is (H H)(X X) [multi-controlled Z
    # with controls = all position qubits (zero bits of w flipped by X) and coin[0],
    # target coin[1]] (X X)(H H).  Composition with _grover_coin gives
    # C = C_0 (x) (I - |w><w|) + C_1 (x) |w><w| exactly.
    for j in range(npos):
        if ((w >> j) & 1) == 0:
            qc.x(pos[j])
    qc.h(coin[0])
    qc.h(coin[1])
    qc.x(coin[0])
    qc.x(coin[1])
    controls = [pos[j] for j in range(npos)] + [coin[0]]
    qc.mcp(math.pi, controls, coin[1])
    qc.x(coin[0])
    qc.x(coin[1])
    qc.h(coin[0])
    qc.h(coin[1])
    for j in range(npos):
        if ((w >> j) & 1) == 0:
            qc.x(pos[j])


def _shift(qc, coin, pos, npos, n, m):
    # eq_3 with the eq_1 graph: |c>|x> -> |c>|x + delta_c mod n>, delta = (+1, -1, +m, -m)
    # for c = c0 + 2*c1.  Write delta_c = a + b*c0 + e*c1 + f*c0*c1 with
    # a = 1, b = -2, e = m - 1, f = 2 - 2m and add each term in the QFT basis:
    # after QFTGate, adding k to x multiplies the Fourier bit j by exp(2*pi*i*k*2^j/n).
    a = 1
    b = -2
    e = m - 1
    f = 2 - 2 * m
    targets = [pos[j] for j in range(npos)]
    qc.append(QFTGate(npos), targets)
    for j in range(npos):
        base = 2.0 * math.pi * float(2 ** j) / float(n)
        qc.p(base * a, pos[j])
        qc.cp(base * b, coin[0], pos[j])
        qc.cp(base * e, coin[1], pos[j])
        qc.mcp(base * f, [coin[0], coin[1]], pos[j])
    qc.append(QFTGate(npos).inverse(), targets)


def build_circuit(instance):
    '''Return the unitary U^t = (S C)^t (eq_5) as a measurement-free QuantumCircuit.'''
    n, npos, m, w, t = _validate(instance)
    pos = QuantumRegister(npos, 'pos')
    coin = QuantumRegister(COIN_SIZE, 'coin')
    qc = QuantumCircuit(pos, coin, name='qw_search_steps')
    for _ in range(t):
        # eq_5: one step U = S C (coin first, then shift)
        _grover_coin(qc, coin)
        _marked_correction(qc, coin, pos, npos, w)
        _shift(qc, coin, pos, npos, n, m)
    return qc
