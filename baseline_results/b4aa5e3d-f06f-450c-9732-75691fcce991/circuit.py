"""Lackadaisical quantum walk search on the complete graph K_N.

One step U = S C Q (eq_5) of the discrete-time coined walk with l self-loops
per vertex, phase-flip marking of one vertex (eq_3), Grover coin on the
d = N-1+l dimensional coin space (eq_2) and a flip-flop shift in which
self-loop directions act as identity (eq_4).

Restriction (disclosed in the artifact): N and d = N-1+l must both be powers
of two and l >= 1, so that the coin register is exactly d-dimensional and the
modular arithmetic of the shift is exact with standard gates.

Qubit layout: qubits 0..n_v-1 hold the vertex label v (little-endian),
qubits n_v..n_v+n_c-1 hold the coin/direction index c (little-endian).
Direction encoding used here: c in {1,...,N-1} is the edge to (v+c) mod N;
c = 0 and c in {N,...,d-1} are the l self-loops.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _is_pow2(x):
    return x >= 1 and (x & (x - 1)) == 0


def _as_int(instance, key):
    if key not in instance:
        raise ValueError("missing instance key: " + key)
    val = instance[key]
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError("instance key must be an integer: " + key)
    return val


def _mcx(qc, controls, target):
    if len(controls) == 0:
        qc.x(target)
    else:
        qc.mcx(list(controls), target)


def _mcp(qc, angle, controls, target):
    if len(controls) == 0:
        qc.p(angle, target)
    elif len(controls) == 1:
        qc.cp(angle, controls[0], target)
    else:
        qc.mcp(angle, list(controls), target)


def _phase_flip(qc, vq, marked):
    """eq_3: Q = (I_N - 2|a><a|) (x) I_d acting on the vertex register."""
    n_v = len(vq)
    zeros = [vq[i] for i in range(n_v) if ((marked >> i) & 1) == 0]
    for q in zeros:
        qc.x(q)
    _mcp(qc, math.pi, vq[:-1], vq[-1])
    for q in zeros:
        qc.x(q)


def _grover_coin(qc, cq):
    """eq_2: C_0 = 2|s_c><s_c| - I_d on the coin register (d = 2**n_c).

    H^n (X^n MCZ X^n) H^n equals -(2|s><s| - I); the global phase pi is
    recorded on the circuit so the implemented operator is exactly C_0.
    """
    for q in cq:
        qc.h(q)
    for q in cq:
        qc.x(q)
    _mcp(qc, math.pi, cq[:-1], cq[-1])
    for q in cq:
        qc.x(q)
    for q in cq:
        qc.h(q)
    qc.global_phase = qc.global_phase + math.pi


def _shift(qc, vq, cq):
    """eq_4 (relabelled encoding): flip-flop shift with self-loops.

    For c < N (high coin bits all zero): v -> (v + c) mod N, c -> (-c) mod N.
    This is the identity on c = 0 (a self-loop) and the flip-flop move for
    c in {1,...,N-1}. For c >= N (self-loops) nothing happens.
    """
    n_v = len(vq)
    low = list(cq[:n_v])
    high = list(cq[n_v:])
    # control on high coin bits being zero: flip them so controls are |1>
    for q in high:
        qc.x(q)
    # Draper adder: v += c (mod 2**n_v) using QFTGate on the vertex register
    qc.append(QFTGate(n_v), vq)
    for j in range(n_v):
        for i in range(n_v):
            if i + j < n_v:
                angle = 2.0 * math.pi * float(2 ** (i + j)) / float(2 ** n_v)
                _mcp(qc, angle, high + [low[j]], vq[i])
    qc.append(QFTGate(n_v).inverse(), vq)
    # negation c -> -c mod 2**n_v : bitwise complement then increment
    for j in range(n_v):
        _mcx(qc, high, low[j])
    for i in range(n_v - 1, 0, -1):
        _mcx(qc, high + low[:i], low[i])
    _mcx(qc, high, low[0])
    for q in high:
        qc.x(q)


def build_circuit(instance):
    """Return the unitary U**steps with U = S C Q (eq_5) on vertex+coin qubits.

    instance keys: N (vertices, power of two), l (self-loops, >= 1, with
    N-1+l a power of two), marked (marked vertex a), steps (walk steps >= 1).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n_vert = _as_int(instance, "N")
    loops = _as_int(instance, "l")
    marked = _as_int(instance, "marked")
    steps = _as_int(instance, "steps")
    if n_vert < 2 or not _is_pow2(n_vert):
        raise ValueError("N must be a power of two >= 2")
    if loops < 1:
        raise ValueError("l must be >= 1 (coin value 0 encodes a self-loop)")
    d = n_vert - 1 + loops
    if not _is_pow2(d):
        raise ValueError("d = N-1+l must be a power of two")
    if marked < 0 or marked >= n_vert:
        raise ValueError("marked vertex out of range")
    if steps < 1:
        raise ValueError("steps must be >= 1")
    n_v = int(round(math.log2(n_vert)))
    n_c = int(round(math.log2(d)))
    if n_v + n_c > MAX_QUBITS:
        raise ValueError("instance needs more than 12 qubits")
    vreg = QuantumRegister(n_v, "vertex")
    creg = QuantumRegister(n_c, "coin")
    qc = QuantumCircuit(vreg, creg)
    vq = list(vreg)
    cq = list(creg)
    for _ in range(steps):
        _phase_flip(qc, vq, marked)
        _grover_coin(qc, cq)
        _shift(qc, vq, cq)
    return qc
