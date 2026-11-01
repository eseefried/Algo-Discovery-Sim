from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Nonlocal CNOT (logical 0 -> logical 1) over a chain of m Bell links, deferred-measurement form.

    Qubits: 0 = control a, 1 = target b, path qubits 2..2m+1; link j uses (2+2j, 3+2j).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object')
    m = instance.get('m')
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError('m must be an integer')
    if m < 1 or 2 + 2 * m > 12:
        raise ValueError('m must satisfy 1 <= m <= 5')
    logical = QuantumRegister(2, 'logical')
    path = QuantumRegister(2 * m, 'path')
    qc = QuantumCircuit(logical, path)
    a = 0
    b = 1
    ea = 2
    eb = 2 * m + 1
    # eq_1: Bell pair on every link, all in parallel
    for j in range(m):
        qc.h(2 + 2 * j)
        qc.cx(2 + 2 * j, 3 + 2 * j)
    # eq_2: entanglement swapping at each junction; Bell measurement = CNOT(q->r), H(q).
    # Outcome (s on q, c on r) leaves X^c Z^s on the far end; the deferred correction is coherent.
    for j in range(1, m):
        q = 1 + 2 * j
        r = 2 + 2 * j
        qc.cx(q, r)
        qc.h(q)
        qc.cx(r, eb)
        qc.cz(q, eb)
    # eq_3: nonlocal CNOT through the (corrected) Bell pair (ea, eb), measurements deferred
    qc.cx(a, ea)
    qc.cx(ea, eb)
    qc.cx(eb, b)
    qc.h(eb)
    qc.cz(eb, a)
    return qc
