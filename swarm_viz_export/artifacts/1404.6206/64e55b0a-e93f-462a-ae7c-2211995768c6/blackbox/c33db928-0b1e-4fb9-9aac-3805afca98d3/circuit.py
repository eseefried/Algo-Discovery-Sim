from qiskit import QuantumCircuit, QuantumRegister


def _int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    return v


def build_circuit(instance):
    """Return V = CNOT_A (H^m (x) I). Qubits 0..m-1 are sup, qubits m..n-1 are tgt."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "m" not in instance or "A" not in instance:
        raise ValueError("instance needs n, m, A")
    n = _int(instance["n"], "n")
    m = _int(instance["m"], "m")
    if m < 1 or n < m + 1 or n > 12:
        raise ValueError("require 1 <= m, m+1 <= n <= 12")
    k = n - m
    A = instance["A"]
    if not isinstance(A, (list, tuple)) or len(A) != k:
        raise ValueError("A must have n-m rows")
    rows = []
    for r in A:
        if not isinstance(r, (list, tuple)) or len(r) != m:
            raise ValueError("each row of A must have m entries")
        row = []
        for e in r:
            if isinstance(e, bool):
                e = int(e)
            if not isinstance(e, int) or e not in (0, 1):
                raise ValueError("A entries must be 0 or 1")
            row.append(e)
        rows.append(row)
    sup = QuantumRegister(m, "sup")
    tgt = QuantumRegister(k, "tgt")
    qc = QuantumCircuit(sup, tgt)
    # eq_3/eq_1: H on |s> gives sum_x (-1)^{s.x}|x>
    for j in range(m):
        qc.h(sup[j])
    # eq_3/eq_1: CNOT_A maps |x>|t> to |x>|Ax xor t>
    for i in range(k):
        for j in range(m):
            if rows[i][j] == 1:
                qc.cx(sup[j], tgt[i])
    return qc
