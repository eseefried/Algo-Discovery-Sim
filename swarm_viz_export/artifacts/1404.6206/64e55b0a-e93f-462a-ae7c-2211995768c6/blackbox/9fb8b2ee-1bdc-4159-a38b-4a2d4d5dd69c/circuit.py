from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def build_circuit(instance):
    """Bell-like basis generator U = CNOT-fanout(f) * (H^{(x)m} (x) I).

    instance keys:
      n: total qubits (2..12)
      m: number of Hadamard control qubits (1 <= m <= n-1)
      f_matrix (optional): (n-m) x m 0/1 matrix; target j is XORed with the
        parity of controls i having f_matrix[j][i] == 1. Default: every target
        receives the parity of all controls (eq_4 for n=3, m=2).
    Layout: qubits 0..m-1 are controls c, qubits m..n-1 are targets t.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('n'), 'n')
    m = _as_int(instance.get('m'), 'm')
    if n < 2 or n > 12:
        raise ValueError('n must be in [2, 12]')
    if m < 1 or m > n - 1:
        raise ValueError('m must satisfy 1 <= m <= n-1')
    k = n - m
    mat = instance.get('f_matrix')
    if mat is None:
        mat = [[1] * m for _ in range(k)]
    if not isinstance(mat, (list, tuple)) or len(mat) != k:
        raise ValueError('f_matrix must have n-m rows')
    clean = []
    for row in mat:
        if not isinstance(row, (list, tuple)) or len(row) != m:
            raise ValueError('each f_matrix row must have m entries')
        r = []
        for e in row:
            e = _as_int(e, 'f_matrix entry')
            if e not in (0, 1):
                raise ValueError('f_matrix entries must be 0 or 1')
            r.append(e)
        clean.append(r)
    c = QuantumRegister(m, 'c')
    t = QuantumRegister(k, 't')
    qc = QuantumCircuit(c, t)
    # H on control qubits: H^{(x)m}|a> = 2^{-m/2} sum_c (-1)^{a.c}|c>
    for i in range(m):
        qc.h(c[i])
    # CNOT fan-out implementing |c>|y> -> |c>|y xor f(c)>
    for j in range(k):
        for i in range(m):
            if clean[j][i]:
                qc.cx(c[i], t[j])
    return qc
