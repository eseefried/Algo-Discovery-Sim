"""Ideal gate-level Grover search operator for a single marked basis state.

Implements eq_3 (uniform superposition |s>, phase oracle O_w, diffusion D,
Grover iterate G = D O_w) and eq_4 (default iteration count
r_opt = floor(pi/4 sqrt(N))) of the specification as a measurement-free
unitary circuit.  The pulse-level Ising spin-chain model (eq_1, eq_2), the
2*pi*k Rabi-frequency condition (eq_5) and the fidelity figure of merit
(eq_6) are NOT implemented here.

Qubit convention: specification spin k (k = 1..n, spin 1 = most significant
bit, x = sum_k x_k 2^(n-k)) is mapped to Qiskit qubit n - k, so that Qiskit
qubit 0 is the least significant bit.  A marked bitstring "x_1 x_2 ... x_n"
is therefore read with its leftmost character on the highest qubit index.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_ITERATIONS = 1024


def _parse_marked(marked, n):
    """Return the marked item w as an integer in [0, 2^n)."""
    if isinstance(marked, bool):
        raise ValueError("marked must be an int or a bitstring, not a bool")
    if isinstance(marked, int):
        if marked < 0 or marked >= 2 ** n:
            raise ValueError("marked integer out of range for n qubits")
        return marked
    if isinstance(marked, str):
        if len(marked) != n:
            raise ValueError("marked bitstring length must equal n")
        for c in marked:
            if c not in "01":
                raise ValueError("marked bitstring must contain only 0/1")
        return int(marked, 2)
    raise ValueError("marked must be an int or a bitstring")


def _phase_flip(qc, qubits, w):
    """eq_3 oracle: apply O_w = 1 - 2|w><w| on the given qubits.

    Qubits whose bit of w is 0 are X-conjugated so that the multi-controlled
    phase pi (multi-controlled Z) fires exactly on |w>.
    """
    n = len(qubits)
    flip = [qubits[q] for q in range(n) if ((w >> q) & 1) == 0]
    for q in flip:
        qc.x(q)
    qc.mcp(math.pi, [qubits[i] for i in range(n - 1)], qubits[n - 1])
    for q in flip:
        qc.x(q)


def _diffusion(qc, qubits):
    """eq_3 diffusion: D = 2|s><s| - 1 realised as H^n O_0 H^n (equals -D, a global phase)."""
    for q in qubits:
        qc.h(q)
    _phase_flip(qc, qubits, 0)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Build the ideal Grover search circuit.

    instance keys:
      n                      int, number of qubits (2 <= n <= 12)
      marked                 int in [0, 2^n) or bitstring of length n (spin 1 leftmost)
      iterations             optional non-negative int r; default eq_4 r_opt = floor(pi/4 sqrt(2^n))
      prepare_superposition  optional bool (default True): prepend H on every qubit (|0..0> -> |s>)
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an int")
    if n < 2 or n > MAX_QUBITS:
        raise ValueError("n must satisfy 2 <= n <= 12")
    if "marked" not in instance:
        raise ValueError("instance must contain 'marked'")
    w = _parse_marked(instance["marked"], n)
    big_n = 2 ** n
    iterations = instance.get("iterations")
    if iterations is None:
        # eq_4: r_opt = floor(pi/4 * sqrt(N))
        iterations = math.floor(math.pi / 4.0 * math.sqrt(big_n))
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise ValueError("iterations must be an int")
    if iterations < 0 or iterations > MAX_ITERATIONS:
        raise ValueError("iterations must be in [0, 1024]")
    prep = instance.get("prepare_superposition", True)
    if not isinstance(prep, bool):
        raise ValueError("prepare_superposition must be a bool")

    reg = QuantumRegister(n, "spin")
    qc = QuantumCircuit(reg, name="grover")
    qubits = list(range(n))

    # eq_3: |s> = H^n |0..0>
    if prep:
        for q in qubits:
            qc.h(q)

    # eq_3 / eq_4: apply G = D O_w  r times
    for _ in range(iterations):
        _phase_flip(qc, qubits, w)
        _diffusion(qc, qubits)

    return qc
