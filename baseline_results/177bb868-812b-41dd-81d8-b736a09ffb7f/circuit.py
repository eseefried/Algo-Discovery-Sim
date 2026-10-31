"""Coined quantum walk on the N-cycle with a parameterised (placeholder) coin.

Registers (Qiskit little-endian, qubit 0 least significant):
  position : qubits 0 .. n-1, n = ceil(log2 N), vertex x in Z_N as unsigned binary (eq_1)
  coin     : qubit n (eq_1)

One step (eq_3): U = S (I_N (x) C) with C = u(theta, phi, lam) on the coin qubit and
S the conditional shift (eq_2): coin=0 -> x+1 mod N, coin=1 -> x-1 mod N.
The circuit returned is U^steps (no state preparation, no measurement).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_STEPS = 1024
ALLOWED_KEYS = ("N", "steps", "coin")
COIN_KEYS = ("theta", "phi", "lam")


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _as_angle(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    val = float(value)
    if not math.isfinite(val):
        raise ValueError(f"{name} must be finite")
    return val


def _controlled_increment_mod_n(n_pos, cycle_size):
    """eq_2: controlled |x> -> |(x+1) mod N> on qubits 0..n_pos-1, control = qubit n_pos.

    Step A: binary increment mod 2^n (MCX ladder), active only when the control is 1.
    Step B (only if N is not a power of two): swap the basis states |N> and |0> on the
    position register (controlled), so that N-1 -> N -> 0 realises the modular wrap.
    The unused states x >= N are permuted among themselves, so the map stays unitary.
    """
    qc = QuantumCircuit(n_pos + 1, name="inc_mod_N")
    pos = list(range(n_pos))
    ctrl = n_pos
    # Step A: controlled increment modulo 2^n
    for i in range(n_pos - 1, 0, -1):
        qc.mcx([ctrl] + pos[:i], pos[i])
    qc.cx(ctrl, pos[0])
    # Step B: controlled swap of |N> and |0> for non-power-of-two N
    if cycle_size != (1 << n_pos):
        ones = [b for b in range(n_pos) if (cycle_size >> b) & 1]
        zeros = [b for b in range(n_pos) if not ((cycle_size >> b) & 1)]
        head = ones[0]
        others = ones[1:]
        for b in others:
            qc.cx(pos[head], pos[b])
        open_ctrls = others + zeros
        for b in open_ctrls:
            qc.x(pos[b])
        qc.mcx([ctrl] + [pos[b] for b in open_ctrls], pos[head])
        for b in open_ctrls:
            qc.x(pos[b])
        for b in reversed(others):
            qc.cx(pos[head], pos[b])
    return qc


def build_circuit(instance):
    """Return the unitary U^steps of the coined walk on the N-cycle (eq_3).

    instance = {"N": int >= 3, "steps": int >= 0,
                "coin": {"theta": float, "phi": float, "lam": float}}
    The coin dict gives the Euler angles of the generic U(2) coin gate u(theta, phi, lam),
    standing in for the unknown memory-dependent coin C(lambda).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in instance:
        if key not in ALLOWED_KEYS:
            raise ValueError(f"unknown instance key: {key}")
    for key in ALLOWED_KEYS:
        if key not in instance:
            raise ValueError(f"missing instance key: {key}")
    cycle_size = _as_int(instance["N"], "N")
    if cycle_size < 3:
        raise ValueError("N must be at least 3")
    steps = _as_int(instance["steps"], "steps")
    if steps < 0 or steps > MAX_STEPS:
        raise ValueError(f"steps must be in [0, {MAX_STEPS}]")
    coin = instance["coin"]
    if not isinstance(coin, dict):
        raise ValueError("coin must be a dict with keys theta, phi, lam")
    for key in coin:
        if key not in COIN_KEYS:
            raise ValueError(f"unknown coin key: {key}")
    for key in COIN_KEYS:
        if key not in coin:
            raise ValueError(f"missing coin key: {key}")
    theta = _as_angle(coin["theta"], "theta")
    phi = _as_angle(coin["phi"], "phi")
    lam = _as_angle(coin["lam"], "lam")

    n_pos = (cycle_size - 1).bit_length()  # n = ceil(log2 N), eq_1
    if n_pos + 1 > MAX_QUBITS:
        raise ValueError(f"N={cycle_size} needs {n_pos + 1} qubits, exceeds cap {MAX_QUBITS}")

    # eq_1: position register (little-endian vertex label) then coin register
    position = QuantumRegister(n_pos, "position")
    coin_reg = QuantumRegister(1, "coin")
    qc = QuantumCircuit(position, coin_reg, name=f"cycle_walk_N{cycle_size}_t{steps}")

    inc = _controlled_increment_mod_n(n_pos, cycle_size)  # eq_2, +1 when control = 1
    dec = inc.inverse()                                   # eq_2, -1 when control = 1
    targets = list(range(n_pos)) + [n_pos]
    coin_q = coin_reg[0]

    for _ in range(steps):
        # eq_3: coin flip C (placeholder generic U(2) for C(lambda))
        qc.u(theta, phi, lam, coin_q)
        # eq_2 / eq_3: shift S. coin = 0 -> x+1 (open control via X conjugation)
        qc.x(coin_q)
        qc.compose(inc, qubits=targets, inplace=True)
        qc.x(coin_q)
        # coin = 1 -> x-1
        qc.compose(dec, qubits=targets, inplace=True)
    return qc
