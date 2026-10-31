"""Discrete-time coined quantum walk search with k walk steps per oracle query.

Implements U_k^q = (W^k Q_w)^q on an n-dimensional hypercube (N = 2^n vertices,
degree d = n), following the reconstruction specification:
  eq_1: Q_w = (I_N - 2|w><w|) (x) I_d          (oracle, phase flip on marked vertex)
  eq_2: W = S (I_N (x) C), C = 2|s_c><s_c| - I_d, S|x,c> = |x xor e_c, c>
  eq_3: U_k = W^k Q_w, applied q times (q counted oracle queries)
The initial state |psi_0> of eq_3 and the measurement of eq_5 are NOT part of
the returned operation; the runner prepares inputs and measures.

Register layout (little-endian):
  qubits 0 .. n-1          : vertex register, qubit j = bit j of vertex label x
  qubits n .. n+m-1        : coin register, m = log2(n), little-endian direction c
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_WALK_STEPS = 4096


def _as_int(instance, key):
    if key not in instance:
        raise ValueError("missing instance parameter: " + key)
    val = instance[key]
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError("instance parameter must be an integer: " + key)
    return val


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    n = _as_int(instance, "n")
    w = _as_int(instance, "w")
    k = _as_int(instance, "k")
    q = _as_int(instance, "q")
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n (hypercube dimension = coin dimension d) must be a power of two >= 2")
    m = int(round(math.log2(n)))
    if (1 << m) != n:
        raise ValueError("n must be an exact power of two")
    if n + m > MAX_QUBITS:
        raise ValueError("total qubits n + log2(n) exceeds cap of %d" % MAX_QUBITS)
    if w < 0 or w >= (1 << n):
        raise ValueError("marked vertex w must satisfy 0 <= w < 2^n")
    if k < 1:
        raise ValueError("k (walk steps per query) must be >= 1")
    if q < 0:
        raise ValueError("q (number of queries) must be >= 0")
    if k * q > MAX_WALK_STEPS:
        raise ValueError("k*q too large (max %d total walk steps)" % MAX_WALK_STEPS)
    return n, m, w, k, q


def _reflect_zero(qc, qubits):
    """Apply I - 2|0...0><0...0| on the given qubits (multi-controlled Z conjugated by X)."""
    for qb in qubits:
        qc.x(qb)
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        qc.h(qubits[-1])
        qc.mcx(list(qubits[:-1]), qubits[-1])
        qc.h(qubits[-1])
    for qb in qubits:
        qc.x(qb)


def _oracle(qc, vertex, n, w):
    """eq_1: Q_w = (I_N - 2|w><w|) (x) I_d, acting only on the vertex register."""
    flips = [vertex[j] for j in range(n) if ((w >> j) & 1) == 1]
    # Map |w> -> |0...0>, reflect about |0...0>, map back.
    for qb in flips:
        qc.x(qb)
    _reflect_zero(qc, [vertex[j] for j in range(n)])
    for qb in flips:
        qc.x(qb)


def _grover_coin(qc, coin, m):
    """eq_2 coin: C = 2|s_c><s_c| - I_d = -( H^m (I - 2|0><0|) H^m ); global phase pi fixes the sign."""
    cq = [coin[j] for j in range(m)]
    for qb in cq:
        qc.h(qb)
    _reflect_zero(qc, cq)
    for qb in cq:
        qc.h(qb)
    qc.global_phase += math.pi


def _shift(qc, vertex, coin, n, m):
    """eq_2 shift: S|x,c> = |x xor e_c, c> (flip vertex bit c, controlled on coin = c)."""
    cq = [coin[j] for j in range(m)]
    for c in range(n):
        zeros = [cq[j] for j in range(m) if ((c >> j) & 1) == 0]
        for qb in zeros:
            qc.x(qb)
        qc.mcx(cq, vertex[c])
        for qb in zeros:
            qc.x(qb)


def _walk_step(qc, vertex, coin, n, m):
    """eq_2: W = S (I_N (x) C): coin first, then shift."""
    _grover_coin(qc, coin, m)
    _shift(qc, vertex, coin, n, m)


def build_circuit(instance):
    """Return the unitary U_k^q = (W^k Q_w)^q (eq_3) as a measurement-free QuantumCircuit.

    instance keys: n (hypercube dimension, power of two >= 2), w (marked vertex),
    k (walk steps per query, >= 1), q (number of counted oracle queries, >= 0).
    """
    n, m, w, k, q = _validate(instance)
    vertex = QuantumRegister(n, "vertex")
    coin = QuantumRegister(m, "coin")
    qc = QuantumCircuit(vertex, coin, name="walk_search_k%d_q%d" % (k, q))
    for _ in range(q):
        # eq_3: one counted query Q_w followed by k uncounted walk steps W^k
        _oracle(qc, vertex, n, w)
        for _step in range(k):
            _walk_step(qc, vertex, coin, n, m)
    return qc
