from qiskit import QuantumCircuit, QuantumRegister
import math


def _int_param(instance, key, default, minimum):
    value = instance.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(key + " must be an integer >= " + str(minimum))
    return value


def build_circuit(instance):
    """Distance-phase interference operation.

    Layout: pattern 0..n-1, input n..2n-1, ancilla 2n, optional class 2n+1...
    Expects ancilla in |+> on entry (prepared by the runner).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int_param(instance, "n", None, 1)
    c = _int_param(instance, "class_qubits", 0, 0)
    if 2 * n + 1 + c > 12:
        raise ValueError("total qubits exceed 12")
    pattern = QuantumRegister(n, "pattern")
    inp = QuantumRegister(n, "input")
    anc = QuantumRegister(1, "ancilla")
    if c > 0:
        cls = QuantumRegister(c, "class")
        qc = QuantumCircuit(pattern, inp, anc, cls)
    else:
        qc = QuantumCircuit(pattern, inp, anc)
    theta = math.pi / n
    # eq_2: pattern_j <- x^k_j XOR x_j
    for j in range(n):
        qc.cx(inp[j], pattern[j])
    # eq_3: ancilla-controlled phase, relative phase pi*d_H/n on ancilla=1 branch
    for j in range(n):
        qc.cp(theta, anc[0], pattern[j])
    # uncompute XOR
    for j in range(n):
        qc.cx(inp[j], pattern[j])
    # eq_4: interference on the ancilla
    qc.h(anc[0])
    return qc
