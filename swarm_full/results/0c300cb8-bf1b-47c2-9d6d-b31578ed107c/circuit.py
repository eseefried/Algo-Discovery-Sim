from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Hamming-distance interference operation (Trugenberger-style template).

    Layout: input qubits 0..n-1, memory qubits n..2n-1, control qubit 2n.
    instance: {"n": int in 1..5, "uncompute_xor": bool (optional, default True)}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or 2 * n + 1 > 12:
        raise ValueError("n must satisfy 1 <= n <= 5")
    unc = instance.get("uncompute_xor", True)
    if not isinstance(unc, bool):
        raise ValueError("uncompute_xor must be a bool")
    inp = QuantumRegister(n, "input")
    mem = QuantumRegister(n, "memory")
    ctl = QuantumRegister(1, "control")
    qc = QuantumCircuit(inp, mem, ctl)
    c = ctl[0]
    # control into superposition
    qc.h(c)
    # eq_1: memory <- x XOR p, bitwise differences
    for i in range(n):
        qc.cx(inp[i], mem[i])
    # eq_1: phase exp(i*pi*d_H/n) on the control=1 branch, d_H = number of 1s in memory
    for i in range(n):
        qc.cp(math.pi / n, c, mem[i])
    if unc:
        for i in range(n):
            qc.cx(inp[i], mem[i])
    # interference: P(control=0) = cos^2(pi*d_H/(2n))
    qc.h(c)
    return qc
