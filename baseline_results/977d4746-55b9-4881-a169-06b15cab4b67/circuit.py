"""Coined discrete-time quantum walk with ancilla-dilated per-step spin and spatial dephasing.

Registers (Qiskit little-endian, qubit 0 = least significant):
  pos[0..n-1]  : lattice site x mod 2^n in binary
  coin[0]      : spin qubit, |0> = up (moves +1), |1> = down (moves -1)
  env          : fresh environment ancillas per step (assumed |0>), traced out by the runner:
                 per step: [1 spin ancilla if p_s > 0] + [1 flag + n copy ancillas if p_x > 0]
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _check_int(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _check_prob(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number in [0, 1]")
    v = float(value)
    if math.isnan(v) or v < 0.0 or v > 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return v


def _apply_coin(qc, coin):
    # eq_1: Hadamard coin C on the spin qubit.
    qc.h(coin)


def _apply_shift(qc, pos, coin, n):
    # eq_2: spin-dependent shift S = |x+1><x| (coin=0) + |x-1><x| (coin=1), mod 2^n.
    # Implemented as a QFT adder: in the Fourier basis adding a to x multiplies
    # qubit l by exp(2*pi*i*a*2^l/2^n); a = +1 for coin |0>, a = -1 for coin |1>.
    pos_idx = [pos[l] for l in range(n)]
    qc.append(QFTGate(n), pos_idx)
    for l in range(n):
        ang = 2.0 * math.pi * float(2 ** l) / float(2 ** n)
        qc.p(ang, pos[l])  # +1 shift phase (unconditional)
        qc.cp(-2.0 * ang, coin, pos[l])  # flips to -1 shift when coin is |1>
    qc.append(QFTGate(n).inverse(), pos_idx)


def _apply_spin_dephasing(qc, coin, anc, p_s):
    # eq_4: E_s(rho) = (1-p_s) rho + p_s Z rho Z, via Stinespring dilation:
    # ancilla -> sqrt(1-p_s)|0> + sqrt(p_s)|1>, then CZ(anc, coin); tracing anc gives E_s.
    theta = 2.0 * math.asin(math.sqrt(p_s))
    qc.ry(theta, anc)
    qc.cz(anc, coin)


def _apply_spatial_dephasing(qc, pos, flag, copies, p_x, n):
    # eq_5: E_x(rho) = (1-p_x) rho + p_x sum_x |x><x| rho |x><x|, via dilation:
    # flag -> sqrt(1-p_x)|0> + sqrt(p_x)|1>; if flag=1 copy every position bit into a
    # fresh ancilla (Toffoli). Tracing flag and copies yields E_x exactly.
    theta = 2.0 * math.asin(math.sqrt(p_x))
    qc.ry(theta, flag)
    for l in range(n):
        qc.ccx(flag, pos[l], copies[l])


def build_circuit(instance):
    """Build the T-step decoherent coined quantum walk as a unitary circuit.

    instance keys: n (position qubits, >=1), T (steps, >=0), p_s (spin dephasing
    probability per step), p_x (spatial dephasing probability per step).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _check_int(instance.get("n"), "n", 1)
    steps = _check_int(instance.get("T"), "T", 0)
    p_s = _check_prob(instance.get("p_s", 0.0), "p_s")
    p_x = _check_prob(instance.get("p_x", 0.0), "p_x")

    use_s = p_s > 0.0
    use_x = p_x > 0.0
    anc_per_step = (1 if use_s else 0) + ((n + 1) if use_x else 0)
    n_env = steps * anc_per_step
    total = n + 1 + n_env
    if total > MAX_QUBITS:
        raise ValueError(
            f"instance needs {total} qubits (> {MAX_QUBITS}); reduce n, T, or disable a channel"
        )

    pos = QuantumRegister(n, "pos")
    coin_reg = QuantumRegister(1, "coin")
    if n_env > 0:
        env = QuantumRegister(n_env, "env")
        qc = QuantumCircuit(pos, coin_reg, env)
    else:
        env = None
        qc = QuantumCircuit(pos, coin_reg)
    coin = coin_reg[0]

    cursor = 0
    for _ in range(steps):
        # eq_3: W = S (1 x C); eq_6: rho -> E_x(E_s(W rho W^dag)) each step.
        _apply_coin(qc, coin)
        _apply_shift(qc, pos, coin, n)
        if use_s:
            _apply_spin_dephasing(qc, coin, env[cursor], p_s)
            cursor += 1
        if use_x:
            flag = env[cursor]
            copies = [env[cursor + 1 + l] for l in range(n)]
            _apply_spatial_dephasing(qc, pos, flag, copies, p_x, n)
            cursor += n + 1
    return qc
