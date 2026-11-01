import math
from qiskit import QuantumCircuit, QuantumRegister


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    if v < lo or v > hi:
        raise ValueError(name + " out of range [" + str(lo) + ", " + str(hi) + "]")
    return v


def _mcz(qc, n):
    # phase -1 on |1...1>: multi-controlled Z (n >= 2)
    qc.mcp(math.pi, list(range(n - 1)), n - 1)


def build_circuit(instance):
    """Grover iterate G^r on n qubits; qubit i holds bit i of x (little-endian)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int(instance.get("n_qubits"), "n_qubits", 2, 12)
    w = _int(instance.get("marked"), "marked", 0, 2 ** n - 1)
    r = _int(instance.get("iterations", 1), "iterations", 0, 64)
    qr = QuantumRegister(n, "s")
    qc = QuantumCircuit(qr, name="grover_iterate")
    zeros = [i for i in range(n) if not (w >> i) & 1]
    for _ in range(r):
        # oracle I - 2|w><w| (eq_2)
        for i in zeros:
            qc.x(qr[i])
        _mcz(qc, n)
        for i in zeros:
            qc.x(qr[i])
        # diffusion 2|s><s| - I = -(H X MCZ X H) (eq_2)
        for i in range(n):
            qc.h(qr[i])
        for i in range(n):
            qc.x(qr[i])
        _mcz(qc, n)
        for i in range(n):
            qc.x(qr[i])
        for i in range(n):
            qc.h(qr[i])
        qc.global_phase = qc.global_phase + math.pi
    return qc
