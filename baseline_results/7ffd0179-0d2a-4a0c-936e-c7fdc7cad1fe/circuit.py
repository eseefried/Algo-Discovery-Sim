"""Trugenberger-style Hamming-distance classifier core (eq_2, eq_3, eq_4).

The returned circuit is the unitary part of the classifier only. The runner
prepares the input state of eq_1:
    (1/sqrt N) sum_k |x>_I |x^k>_M |y^k>_Y (|0>+|1>)_c / sqrt 2
and performs the measurements / postselection of eq_4 and eq_5 afterwards.

Qubit layout (Qiskit index 0 = least significant bit):
    inp[0..n-1]      input register I, pattern bit j (j=1..n) in inp[j-1]
    mem[0..n-1]      memory register M, training bit j in mem[j-1]
    cls[0..m-1]      class register Y (m = num_class_qubits, idle here)
    anc[0]           ancilla c (control qubit of Trugenberger's routine)
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _read_int(instance, key, lower, upper):
    """Read a required integer instance parameter in [lower, upper]."""
    if key not in instance:
        raise ValueError("missing instance key '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("instance key '%s' must be an integer" % key)
    if value < lower or value > upper:
        raise ValueError(
            "instance key '%s' must lie in [%d, %d], got %d" % (key, lower, upper, value)
        )
    return value


def build_circuit(instance):
    """Build the Hamming-distance classifier operation for a given instance.

    instance keys:
        n                 number of bits per pattern (>= 1)
        num_class_qubits  size of the class register (>= 1; 1 = binary labels)
    Total qubits 2*n + num_class_qubits + 1 must not exceed 12.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    allowed = {"n", "num_class_qubits"}
    for key in instance:
        if key not in allowed:
            raise ValueError("unknown instance key '%s'" % key)

    n = _read_int(instance, "n", 1, MAX_QUBITS)
    m = _read_int(instance, "num_class_qubits", 1, MAX_QUBITS)
    total = 2 * n + m + 1
    if total > MAX_QUBITS:
        raise ValueError(
            "2*n + num_class_qubits + 1 = %d exceeds the cap of %d qubits" % (total, MAX_QUBITS)
        )

    inp = QuantumRegister(n, "inp")
    mem = QuantumRegister(n, "mem")
    cls = QuantumRegister(m, "cls")
    anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(inp, mem, cls, anc, name="hamming_classifier")

    # eq_2: CNOT_{I_j -> M_j} for every j, so mem holds x XOR x^k and its
    # Hamming weight equals the Hamming distance d_k.
    for j in range(n):
        qc.cx(inp[j], mem[j])

    # eq_3: U = exp(-i theta Z_c (x) sum_j |1><1|_j), theta = pi/(2n).
    # For each memory qubit j, the factor exp(-i theta Z_c (x) |1><1|_j) acts
    # as diag(e^{-i theta}, e^{+i theta}) on the ancilla when mem[j] = 1 and as
    # identity otherwise.  This equals  P(-theta) on mem[j]  followed by
    # CP(2 theta) with control mem[j] and target anc[0]:
    #   mem=1, c=0 : e^{-i theta}            mem=1, c=1 : e^{-i theta} e^{2 i theta} = e^{i theta}
    # All factors commute, so the product over j realises U exactly.
    theta = math.pi / (2.0 * n)
    for j in range(n):
        qc.p(-theta, mem[j])
        qc.cp(2.0 * theta, mem[j], anc[0])

    # eq_4: Hadamard on the ancilla, turning the relative phase
    # e^{-/+ i theta_k} into amplitudes cos(theta_k)|0>_c - i sin(theta_k)|1>_c.
    # The measurement / postselection on c = 0 is done by the runner.
    qc.h(anc[0])

    return qc
