import math
from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Diagonal Hermitian gate -> product of multiple-controlled Z gates.

    instance: {"n": int in [1,12], and exactly one of
               "f": list of 2^n bits, or "signs": list of 2^n entries in {+1,-1}}
    Entry index x is the computational-basis integer (Qiskit qubit 0 = LSB).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n must be an integer in [1, 12]")
    size = 1 << n
    has_f = "f" in instance
    has_s = "signs" in instance
    if has_f == has_s:
        raise ValueError("provide exactly one of 'f' or 'signs'")
    raw = instance["f"] if has_f else instance["signs"]
    if not isinstance(raw, list) or len(raw) != size:
        raise ValueError("diagonal data must be a list of length 2^n")
    f = []
    for v in raw:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError("entries must be integers")
        if has_f:
            if v not in (0, 1):
                raise ValueError("f entries must be 0 or 1")
            f.append(v)
        else:
            if v not in (1, -1):
                raise ValueError("signs must be +1 or -1 (Hermitian unitary diagonal)")
            f.append(0 if v == 1 else 1)
    # GF(2) solve in the MCZ basis: a[mask] = c_S (Moebius transform)
    a = list(f)
    for i in range(n):
        bit = 1 << i
        for x in range(size):
            if x & bit:
                a[x] ^= a[x ^ bit]
    q = QuantumRegister(n, "q")
    qc = QuantumCircuit(q)
    if a[0] == 1:
        qc.global_phase = math.pi  # f(0)=1 -> global factor -1
    for mask in range(1, size):
        if a[mask] == 0:
            continue
        qubits = [i for i in range(n) if (mask >> i) & 1]
        if len(qubits) == 1:
            qc.z(qubits[0])
        elif len(qubits) == 2:
            qc.cz(qubits[0], qubits[1])
        else:
            target = qubits[-1]
            qc.h(target)
            qc.mcx(qubits[:-1], target)
            qc.h(target)
    return qc
