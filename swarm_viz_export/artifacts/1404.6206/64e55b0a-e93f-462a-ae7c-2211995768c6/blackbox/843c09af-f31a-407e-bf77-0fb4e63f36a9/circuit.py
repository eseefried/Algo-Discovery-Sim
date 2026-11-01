from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def build_circuit(instance):
    """Bell-like basis generator W = (controlled-X layer) * (H on m controls).

    instance keys: n (total qubits, 2..12), m (1<=m<n, Hadamard controls),
    variant ('xor' or 'and').
    Qubits 0..m-1 are controls c1..cm; qubits m..n-1 are targets.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('n', 3), 'n')
    m = _as_int(instance.get('m', 2), 'm')
    variant = instance.get('variant', 'xor')
    if n < 2 or n > 12:
        raise ValueError('n must be in 2..12')
    if m < 1 or m >= n:
        raise ValueError('m must satisfy 1 <= m < n')
    if variant not in ('xor', 'and'):
        raise ValueError("variant must be 'xor' or 'and'")
    c = QuantumRegister(m, 'c')
    t = QuantumRegister(n - m, 't')
    qc = QuantumCircuit(c, t)
    # eq_2 right factor: H on the m control qubits
    for i in range(m):
        qc.h(c[i])
    # eq_2 left factor: sum_c |c><c| (x) X^{f(c)} on each target
    for tq in t:
        if variant == 'xor':
            # eq_4 f_A: CNOT fan-out, target gets parity of controls
            for cq in c:
                qc.cx(cq, tq)
        else:
            # eq_4 f_B / eq_5: multi-controlled X, target flips iff all controls are 1
            if m == 1:
                qc.cx(c[0], tq)
            else:
                qc.mcx(list(c), tq)
    return qc
