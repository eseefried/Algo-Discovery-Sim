"""QFT-domain controlled weighted sum (inner product of a quantum bit vector with classical weights).

Operation implemented (spec eq_3, built from eq_1 and eq_2):
    |x_1 ... x_m>_inp (x) |a>_acc  ->  |x_1 ... x_m>_inp (x) |(a + sum_j w_j x_j) mod 2^n>_acc

Register layout (Qiskit index 0 = least significant bit):
    qubits 0 .. n-1      : accumulator 'acc', acc[k] has weight 2^k (acc[0] is the LSB)
    qubits n .. n+m-1    : inputs 'inp', inp[j] holds bit x_{j+1} (weight w_{j+1} = weights[j])

Convention note: the specification writes the Fourier factor index l big-endian with phase
2*pi*a/2^l. Under Qiskit's QFTGate convention the qubit with weight 2^k carries phase
2*pi*a*2^k/2^n = 2*pi*a/2^(n-k), i.e. l = n - k. Angles below use the Qiskit form.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _validate(instance):
    """Validate the instance dict and return (n, weights)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    allowed = {"n", "weights"}
    extra = set(instance.keys()) - allowed
    if extra:
        raise ValueError("unknown instance keys: " + ", ".join(sorted(str(k) for k in extra)))
    if "n" not in instance or "weights" not in instance:
        raise ValueError("instance must contain 'n' (accumulator size) and 'weights' (list of ints)")
    n = instance["n"]
    weights = instance["weights"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer")
    if not isinstance(weights, (list, tuple)) or len(weights) < 1:
        raise ValueError("'weights' must be a non-empty list of integers")
    ws = []
    for w in weights:
        if isinstance(w, bool) or not isinstance(w, int):
            raise ValueError("each weight must be an integer")
        ws.append(int(w))
    m = len(ws)
    if n + m > MAX_QUBITS:
        raise ValueError(
            "total qubits n + m = %d exceeds the cap of %d" % (n + m, MAX_QUBITS)
        )
    return n, ws


def _controlled_phase_add(qc, control, acc, weight, n):
    """eq_2 (controlled): add classical 'weight' to the Fourier-encoded accumulator
    when 'control' is |1>.  Phi(w) = (x)_k diag(1, exp(2*pi*i*w*2^k/2^n)) on acc[k];
    controlling every factor on the same qubit gives C[Phi(w)].  Rotations whose
    angle is a multiple of 2*pi are dropped (exact, since the phase is 2^n-periodic)."""
    modulus = 1 << n
    wm = weight % modulus  # negative weights act as subtraction mod 2^n
    if wm == 0:
        return
    for k in range(n):
        num = (wm * (1 << k)) % modulus
        if num == 0:
            continue
        angle = 2.0 * math.pi * num / modulus
        qc.cp(angle, control, acc[k])


def build_circuit(instance):
    """Return the controlled-weighted-sum operation as a unitary QuantumCircuit.

    instance = {"n": <accumulator qubits>, "weights": [w_1, ..., w_m]}
    """
    n, weights = _validate(instance)
    m = len(weights)
    acc = QuantumRegister(n, "acc")
    inp = QuantumRegister(m, "inp")
    qc = QuantumCircuit(acc, inp, name="ctrl_weighted_sum")
    acc_idx = list(range(n))

    # eq_1: move the accumulator to the Fourier basis (QFT|a>).
    qc.append(QFTGate(n), acc_idx)

    # eq_3: product over inputs j of C_{x_j}[Phi(w_j)]; the blocks are diagonal and
    # commute, so the accumulator receives sum_j w_j x_j (mod 2^n).
    for j in range(m):
        _controlled_phase_add(qc, inp[j], acc, weights[j], n)

    # eq_1 (inverse): back to the computational basis |(a + S) mod 2^n>.
    qc.append(QFTGate(n).inverse(), acc_idx)
    return qc
