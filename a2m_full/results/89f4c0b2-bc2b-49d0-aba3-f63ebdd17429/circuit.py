from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Diagonal Hermitian gate diag((-1)^f(x)) as a product of multi-controlled Z gates.

    instance: {"n": int in 1..12, "truth_table": list of 2^n bits, index x little-endian}.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n must be an integer in 1..12")
    tt = instance.get("truth_table")
    size = 1 << n
    if not isinstance(tt, (list, tuple)) or len(tt) != size:
        raise ValueError("truth_table must have length 2^n")
    # eq_1: entries are signs (-1)^f(x); b[x] = f(x)
    b = []
    for v in tt:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError("truth_table entries must be 0 or 1")
        b.append(v)
    # eq_3/eq_4: fast binary Moebius transform, c_S = xor_{x subset S} f(x)
    for i in range(n):
        bit = 1 << i
        for x in range(size):
            if x & bit:
                b[x] ^= b[x ^ bit]
    q = QuantumRegister(n, "q")
    qc = QuantumCircuit(q)
    # constant ANF term c_empty gives global phase (-1)^c_empty
    if b[0]:
        qc.global_phase = math.pi
    # eq_2/eq_5: one MCZ_S per nonempty S with c_S = 1 (all diagonal, commute)
    for s in range(1, size):
        if b[s]:
            qubits = [i for i in range(n) if (s >> i) & 1]
            if len(qubits) == 1:
                qc.z(q[qubits[0]])
            elif len(qubits) == 2:
                qc.cz(q[qubits[0]], q[qubits[1]])
            else:
                target = qubits[-1]
                controls = [q[j] for j in qubits[:-1]]
                qc.h(q[target])
                qc.mcx(controls, q[target])
                qc.h(q[target])
    return qc
