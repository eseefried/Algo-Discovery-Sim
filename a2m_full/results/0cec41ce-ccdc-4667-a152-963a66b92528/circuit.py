from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def build_circuit(instance):
    """Hamming-distance phase/interference operation.

    instance: {"n": pattern bits, "m": label bits (identity on them), "query": list of n bits}
    Layout: p = qubits 0..n-1 (p_j is qubit j), c = next m qubits, a = last qubit.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    m = instance.get("m")
    x = instance.get("query")
    if not _is_int(n) or not _is_int(m):
        raise ValueError("n and m must be integers")
    if n < 1 or m < 0:
        raise ValueError("need n>=1 and m>=0")
    if n + m + 1 > 12:
        raise ValueError("total qubits exceed 12")
    if not isinstance(x, list) or len(x) != n:
        raise ValueError("query must be a list of n bits")
    for b in x:
        if not _is_int(b) or b not in (0, 1):
            raise ValueError("query entries must be 0 or 1")

    p = QuantumRegister(n, "p")
    regs = [p]
    if m > 0:
        c = QuantumRegister(m, "c")
        regs.append(c)
    a = QuantumRegister(1, "a")
    regs.append(a)
    qc = QuantumCircuit(*regs)

    # eq_2: XOR query into pattern register; qubit j is 1 where pattern disagrees with query
    for j in range(n):
        if x[j] == 1:
            qc.x(p[j])

    # eq_3: ancilla superposition, then phase exp(-i*pi*d/n) on the a=1 branch
    qc.h(a[0])
    for j in range(n):
        qc.cp(-math.pi / n, a[0], p[j])

    # eq_4: interference so that P(a=0|k)=cos^2(pi d_k/(2n))
    qc.h(a[0])
    return qc
