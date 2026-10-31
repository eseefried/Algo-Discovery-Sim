"""Coined discrete-time quantum walk U^t on the cycle C_N (N = 2^n).

Operation only: implements U = S (I_N (x) C) repeated ``steps`` times, where
C is the degree-2 Grover coin (= Pauli X) or, optionally, the Hadamard coin,
and S is the flip-flop shift S|v>|c> = |v + (-1)^c mod N>|c xor 1>.

Qubit layout (Qiskit qubit 0 = least significant bit):
    qubit 0           : coin c (0 -> toward v+1, 1 -> toward v-1)
    qubits 1 .. n     : position v in binary, qubit 1 = v_0 (LSB of v)
so that the computational-basis index of |v>|c> is 2*v + c.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_STEPS = 1024
ALLOWED_COINS = ("grover", "hadamard")


def _require_int(instance, key):
    """Fetch a non-boolean integer entry from the instance dict or raise."""
    if key not in instance:
        raise ValueError("instance is missing required key '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("instance['%s'] must be an integer" % key)
    return value


def _controlled_increment(qc, controls, position):
    """Add 1 mod 2^n to ``position`` (position[0] = LSB) when all ``controls`` are 1.

    Standard cascade of multi-controlled X gates, most significant target first.
    """
    n = len(position)
    for i in range(n - 1, -1, -1):
        ctrls = list(controls) + [position[j] for j in range(i)]
        target = position[i]
        if len(ctrls) == 0:
            qc.x(target)
        elif len(ctrls) == 1:
            qc.cx(ctrls[0], target)
        else:
            qc.mcx(ctrls, target)


def _apply_coin(qc, coin, coin_name):
    """eq_2: coin operator on the coin qubit at every node (node independent).

    'grover'   : G_2 = (2/2) J_2 - I_2 = X
    'hadamard' : H (degree-2 Fourier coin), optional extension
    """
    if coin_name == "grover":
        qc.x(coin)
    elif coin_name == "hadamard":
        qc.h(coin)
    else:
        raise ValueError("unknown coin '%s'" % coin_name)


def _flip_flop_shift(qc, coin, position):
    """eq_3: S|v>|c> = |v + (-1)^c mod N>|c xor 1> with N = 2^n.

    c = 0 : increment v mod N (coin control conjugated by X to act on |0>)
    c = 1 : decrement v mod N, realised as X^(x)n . increment . X^(x)n
    then flip the coin so it points back along the traversed edge.
    """
    # c = 0 branch: increment
    qc.x(coin)
    _controlled_increment(qc, [coin], position)
    qc.x(coin)
    # c = 1 branch: decrement (bitwise complement conjugation of increment)
    for q in position:
        qc.x(q)
    _controlled_increment(qc, [coin], position)
    for q in position:
        qc.x(q)
    # arc reversal: c -> c xor 1
    qc.x(coin)


def build_circuit(instance):
    """Return the DTQW operator U^steps on C_N as a QuantumCircuit.

    instance keys:
        'N'     : number of cycle nodes, a power of two with 4 <= N <= 2048
        'steps' : number of walk steps t, 0 <= t <= 1024
        'coin'  : 'grover' (Pauli X, the degree-2 Grover coin) or 'hadamard'
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n_nodes = _require_int(instance, "N")
    steps = _require_int(instance, "steps")
    if "coin" not in instance:
        raise ValueError("instance is missing required key 'coin'")
    coin_name = instance["coin"]
    if not isinstance(coin_name, str) or coin_name not in ALLOWED_COINS:
        raise ValueError("instance['coin'] must be one of %s" % (ALLOWED_COINS,))
    if n_nodes < 4:
        raise ValueError("N must be at least 4")
    if n_nodes & (n_nodes - 1) != 0:
        raise ValueError("N must be a power of two (binary modular increment)")
    if steps < 0 or steps > MAX_STEPS:
        raise ValueError("steps must satisfy 0 <= steps <= %d" % MAX_STEPS)
    n_pos = int(round(math.log2(n_nodes)))
    if (1 << n_pos) != n_nodes:
        raise ValueError("N must be a power of two")
    total_qubits = n_pos + 1
    if total_qubits > MAX_QUBITS:
        raise ValueError("instance needs %d qubits, cap is %d" % (total_qubits, MAX_QUBITS))

    # eq_1: |v>|c> with coin as least significant qubit, position above it
    coin_reg = QuantumRegister(1, "coin")
    pos_reg = QuantumRegister(n_pos, "pos")
    qc = QuantumCircuit(coin_reg, pos_reg, name="dtqw_C%d_t%d" % (n_nodes, steps))
    coin = coin_reg[0]
    position = [pos_reg[i] for i in range(n_pos)]

    # eq_4: U = S (I (x) C), applied ``steps`` times
    for _ in range(steps):
        _apply_coin(qc, coin, coin_name)
        _flip_flop_shift(qc, coin, position)
    return qc
