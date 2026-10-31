"""Discrete-time quantum walk on a cycle of N = 2^n sites with a final coin operator.

Implements eq_1 (conditional shift), eq_2 (U = S (C x I), t steps), eq_4 (final coin C_f)
and the identity-coin perfect-state-transfer instance eq_5. The unknown coin state
(eq_3) is prepared by the runner on qubit 0; the walker position is encoded as an
n-bit integer on qubits 1..n (qubit 1 = least significant bit).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _apply_coin(qc, coin_qubit, name):
    """Apply a named coin operator to the coin qubit (C in eq_2 or C_f in eq_4)."""
    if name == "identity":
        return
    if name == "flip":
        qc.x(coin_qubit)
        return
    if name == "hadamard":
        qc.h(coin_qubit)
        return
    raise ValueError("coin must be one of 'identity', 'flip', 'hadamard'")


def _check_int(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + " must be an integer")
    if value < minimum:
        raise ValueError(name + " must be >= " + str(minimum))
    return value


def build_circuit(instance):
    """Return the walk operation (C_f x I) U^t on 1 + log2(N) qubits.

    instance keys:
      N          : number of sites on the circle, a power of two >= 2
      steps      : number of walk steps t >= 1
      coin       : driving coin C, 'identity' | 'flip' | 'hadamard'
      final_coin : final coin C_f, 'identity' | 'flip' | 'hadamard'
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("N", "steps", "coin", "final_coin"):
        if key not in instance:
            raise ValueError("missing instance key: " + key)
    n_sites = _check_int(instance["N"], "N", 2)
    if n_sites & (n_sites - 1) != 0:
        raise ValueError("N must be a power of two (binary position encoding)")
    steps = _check_int(instance["steps"], "steps", 1)
    if steps > 1024:
        raise ValueError("steps must be <= 1024")
    coin_name = instance["coin"]
    final_name = instance["final_coin"]
    for name in (coin_name, final_name):
        if name not in ("identity", "flip", "hadamard"):
            raise ValueError("coin operators must be 'identity', 'flip' or 'hadamard'")
    n_pos = n_sites.bit_length() - 1
    if 1 + n_pos > 12:
        raise ValueError("total qubits (1 + log2 N) must not exceed 12")

    coin = QuantumRegister(1, "coin")
    pos = QuantumRegister(n_pos, "pos")
    qc = QuantumCircuit(coin, pos, name="dtqw_pst")
    pos_idx = list(range(1, 1 + n_pos))

    # eq_1 / eq_2: shift S realised in the Fourier basis. The coin C acts on a
    # different register than the QFT, so one QFT / inverse-QFT pair encloses all
    # t steps. In the Fourier basis, adding a to x multiplies qubit m by
    # exp(i * a * 2*pi*2^m / N). Coin |1> -> +1 (angle +theta_m), coin |0> -> -1
    # (angle -theta_m): implemented as p(-theta_m) followed by cp(2 theta_m).
    qc.append(QFTGate(n_pos), pos_idx)
    for _step in range(steps):
        _apply_coin(qc, coin[0], coin_name)  # eq_2: coin C before the shift
        for m in range(n_pos):
            theta = math.pi * float(2 ** (m + 1)) / float(n_sites)
            qc.p(-theta, pos[m])
            qc.cp(2.0 * theta, coin[0], pos[m])
    qc.append(QFTGate(n_pos).inverse(), pos_idx)

    # eq_4 / eq_5: state-independent final coin operator C_f (identity for the
    # identity-coin antipodal-transfer instance).
    _apply_coin(qc, coin[0], final_name)
    return qc
