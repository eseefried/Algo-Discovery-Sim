"""Noiseless parity-learning (Bernstein-Vazirani) operation for the quantum example oracle.

Qubit layout (Qiskit index 0 = least significant bit):
    qubits 0 .. n-1 : data register D, qubit i holds x_i
    qubit  n        : label register L

Stages selectable through instance["stage"]:
    "oracle"  : U_s : |x>_D |b>_L -> |x>_D |b xor s.x>_L            (eq_1)
    "example" : H^{(x)n} on D, then U_s ; maps |0^n>|0> -> |psi_s>    (eq_2)
    "full"    : "example" followed by H on all n+1 qubits            (eq_4)
                maps |0^n>|0> -> (|0^n>|0> + |s>|1>)/sqrt(2)
The depolarizing channel (eq_3) is not unitary and is NOT part of this circuit.
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
STAGES = ("oracle", "example", "full")


def _validate(instance):
    """Validate the instance dictionary and return (n, s, stage)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "s" not in instance:
        raise ValueError("instance must contain keys 'n' and 's'")
    n = instance["n"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1:
        raise ValueError("n must be at least 1")
    if n + 1 > MAX_QUBITS:
        raise ValueError("n + 1 qubits exceeds the cap of %d qubits" % MAX_QUBITS)
    s_raw = instance["s"]
    if not isinstance(s_raw, (list, tuple)):
        raise ValueError("s must be a list of 0/1 integers")
    if len(s_raw) != n:
        raise ValueError("s must have length n")
    s = []
    for v in s_raw:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError("entries of s must be the integers 0 or 1")
        s.append(v)
    stage = instance.get("stage", "full")
    if not isinstance(stage, str) or stage not in STAGES:
        raise ValueError("stage must be one of %s" % (STAGES,))
    for key in instance:
        if key not in ("n", "s", "stage"):
            raise ValueError("unknown instance key: %r" % (key,))
    return n, s, stage


def build_circuit(instance):
    """Build the noiseless parity-learning operation described in the module docstring."""
    n, s, stage = _validate(instance)
    data = QuantumRegister(n, "d")
    label = QuantumRegister(1, "l")
    qc = QuantumCircuit(data, label, name="parity_learn_%s" % stage)

    # eq_2: uniform superposition over inputs x on the data register.
    if stage in ("example", "full"):
        for i in range(n):
            qc.h(data[i])

    # eq_1: parity oracle U_s, label <- label xor (s . x mod 2),
    # implemented as one CNOT from every data qubit i with s_i = 1.
    for i in range(n):
        if s[i] == 1:
            qc.cx(data[i], label[0])

    # eq_4: learner's Hadamard layer on all n+1 qubits (Bernstein-Vazirani transform).
    if stage == "full":
        for i in range(n):
            qc.h(data[i])
        qc.h(label[0])

    return qc
