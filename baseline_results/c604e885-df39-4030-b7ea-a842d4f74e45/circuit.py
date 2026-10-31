"""Barrier-hindered coined quantum-walk search on the complete graph K_N.

Implements U_eps^t with U_eps = S_eps (I x C) Q  (eq_3, eq_4), where
  Q      = (I - 2|w><w|) x I            (eq_2, oracle on position register)
  C      = 2|s><s| - I                   (eq_2, Grover coin on coin register)
  S      = flip-flop shift |u>|v> -> |v>|u>  (eq_3)
  S_eps  = eps I + i sqrt(1-eps^2) S = exp(i theta S), cos theta = eps (eq_4)

Qubit layout: position register = qubits 0..n-1 (qubit k = bit k of u,
least significant first), coin register = qubits n..2n-1 (qubit n+k = bit k
of v). n = log2(N). Initial state |s>|s> (eq_1) and the position measurement
(eq_5) are supplied by the runner, not by this module.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    big_n = instance.get("N")
    if isinstance(big_n, bool) or not isinstance(big_n, int):
        raise ValueError("N must be an integer")
    if big_n < 2 or (big_n & (big_n - 1)) != 0:
        raise ValueError("N must be a power of two >= 2")
    n = big_n.bit_length() - 1
    if 2 * n > MAX_QUBITS:
        raise ValueError("2*log2(N) exceeds the qubit cap of %d" % MAX_QUBITS)
    w = instance.get("marked")
    if isinstance(w, bool) or not isinstance(w, int) or w < 0 or w >= big_n:
        raise ValueError("marked must be an integer in [0, N)")
    eps = instance.get("epsilon")
    if isinstance(eps, bool) or not isinstance(eps, (int, float)):
        raise ValueError("epsilon must be a real number")
    eps = float(eps)
    if not math.isfinite(eps) or eps < 0.0 or eps > 1.0:
        raise ValueError("epsilon must lie in [0, 1]")
    steps = instance.get("steps")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    return big_n, n, w, eps, steps


def _oracle(qc, pos, w, n):
    """eq_2: Q = (I_N - 2|w><w|) x I_N, phase flip when position == w."""
    for k in range(n):
        if not (w >> k) & 1:
            qc.x(pos[k])
    if n == 1:
        qc.z(pos[0])
    else:
        qc.mcp(math.pi, pos[:-1], pos[-1])
    for k in range(n):
        if not (w >> k) & 1:
            qc.x(pos[k])


def _coin(qc, coin, n):
    """eq_2: Grover coin C = 2|s><s| - I = -(H^n X^n MCZ X^n H^n) on the coin register."""
    qc.h(coin)
    qc.x(coin)
    if n == 1:
        qc.z(coin[0])
    else:
        qc.mcp(math.pi, coin[:-1], coin[-1])
    qc.x(coin)
    qc.h(coin)
    qc.global_phase += math.pi  # overall minus sign of C


def _barrier_shift(qc, pos, coin, n, theta):
    """eq_4 (and eq_3 at theta = pi/2): S_eps = exp(i theta S) = cos(theta) I + i sin(theta) S.

    S = prod_k SWAP(pos[k], coin[k]). Each SWAP = V_k^dag CZ_k V_k with
    V_k = H(pos[k]) * CX(pos[k] -> coin[k]), so S = V^dag (prod_k CZ_k) V and
    prod_k CZ_k = (-1)^{XOR_k (a_k b_k)}. Hence
      exp(i theta prod CZ_k) = e^{i theta} * exp(-2 i theta * XOR_k y_k),  y_k = a_k b_k,
    and XOR_k y_k = sum_{S nonempty} (-2)^{|S|-1} prod_{k in S} y_k, each term
    being a multi-controlled phase on the 2|S| qubits of the pairs in S.
    """
    # basis change V
    for k in range(n):
        qc.cx(pos[k], coin[k])
        qc.h(pos[k])
    # diagonal phase exp(i theta prod_k CZ_k)
    qc.global_phase += theta
    for mask in range(1, 1 << n):
        qubits = []
        size = 0
        for k in range(n):
            if (mask >> k) & 1:
                qubits.append(pos[k])
                qubits.append(coin[k])
                size += 1
        angle = -2.0 * theta * ((-2.0) ** (size - 1))
        qc.mcp(angle, qubits[:-1], qubits[-1])
    # undo basis change V^dag
    for k in range(n):
        qc.h(pos[k])
        qc.cx(pos[k], coin[k])


def build_circuit(instance):
    """Return the unitary U_eps^t (eq_3/eq_4) on 2*log2(N) qubits, no prep, no measurement."""
    big_n, n, w, eps, steps = _validate(instance)
    pos_reg = QuantumRegister(n, "pos")
    coin_reg = QuantumRegister(n, "coin")
    qc = QuantumCircuit(pos_reg, coin_reg, name="barrier_walk_search_N%d" % big_n)
    pos = list(range(n))
    coin = list(range(n, 2 * n))
    theta = math.acos(eps)  # eq_4: cos(theta) = eps, sin(theta) = sqrt(1 - eps^2)
    for _ in range(steps):
        _oracle(qc, pos, w, n)          # Q   (eq_2)
        _coin(qc, coin, n)              # I x C (eq_2)
        _barrier_shift(qc, pos, coin, n, theta)  # S_eps (eq_4); S when eps = 0 (eq_3)
    return qc
