import math
from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Decompose D=diag((-1)^f(x)) into multiple-controlled Z gates.

    instance: {"n": int in 1..12, "f": list of 2^n bits}; f[x] is the truth table,
    where qubit i is bit i of x (qubit 0 least significant).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n must be an integer in 1..12")
    size = 1 << n
    f = instance.get("f")
    if not isinstance(f, (list, tuple)) or len(f) != size:
        raise ValueError("f must be a list of length 2^n")
    a = []
    for v in f:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError("f entries must be 0 or 1")
        a.append(v)
    # eq_2: GF(2) Moebius transform -> algebraic normal form coefficients c_S = a[mask(S)]
    for i in range(n):
        bit = 1 << i
        for x in range(size):
            if x & bit:
                a[x] ^= a[x ^ bit]
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    # eq_2: apply Z_S for each subset S with c_S = 1 (gates commute)
    for mask in range(1, size):
        if a[mask]:
            qubits = [i for i in range(n) if (mask >> i) & 1]
            if len(qubits) == 1:
                qc.z(qubits[0])
            elif len(qubits) == 2:
                qc.cz(qubits[0], qubits[1])
            else:
                t = qubits[-1]
                qc.h(t)
                qc.mcx(qubits[:-1], t)
                qc.h(t)
    # empty subset: constant term f(0)=1 is a global phase of -1
    if a[0]:
        qc.global_phase = math.pi
    return qc
