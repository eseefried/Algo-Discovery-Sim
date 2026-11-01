from qiskit import QuantumCircuit, QuantumRegister
import math


def _anf(table):
    a = [int(v) for v in table]
    for i in range(3):
        bit = 1 << i
        for m in range(8):
            if m & bit:
                a[m] ^= a[m ^ bit]
    return a


def build_circuit(instance):
    """Phase oracle U_f|x>=(-1)^f(x)|x> on 3 qubits; qubit i holds bit i of x.

    instance: {"truth_table": [f(0),...,f(7)]} with x = x0 + 2*x1 + 4*x2.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    table = instance.get("truth_table")
    if not isinstance(table, (list, tuple)) or len(table) != 8:
        raise ValueError("truth_table must be a list of 8 bits")
    bits = []
    for v in table:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError("truth_table entries must be 0 or 1")
        bits.append(v)
    s = 8 - 2 * sum(bits)
    if s not in (8, -8, 0):
        raise ValueError("f violates the Deutsch-Jozsa promise (constant or balanced)")
    q = QuantumRegister(3, "q")
    qc = QuantumCircuit(q, name="U_f")
    coeffs = _anf(bits)
    for m in range(8):
        if not coeffs[m]:
            continue
        idx = [i for i in range(3) if (m >> i) & 1]
        if len(idx) == 0:
            qc.global_phase += math.pi
        elif len(idx) == 1:
            qc.z(q[idx[0]])
        elif len(idx) == 2:
            qc.cz(q[idx[0]], q[idx[1]])
        else:
            qc.ccz(q[idx[0]], q[idx[1]], q[idx[2]])
    return qc
