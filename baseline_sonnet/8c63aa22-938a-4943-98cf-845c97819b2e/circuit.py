from qiskit import QuantumCircuit, QuantumRegister


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    perm = instance.get('permutation')
    if not isinstance(perm, (list, tuple)) or len(perm) != 4:
        raise ValueError('permutation must be a list of length 4')
    for v in perm:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('permutation entries must be integers')
    if sorted(perm) != [0, 1, 2, 3]:
        raise ValueError('permutation must be a permutation of 0..3')
    return [int(v) for v in perm]


def _single_bit_swap(qc, a, b):
    # swap basis states a and b that differ in exactly one bit
    d = a ^ b
    t = 0 if d == 1 else 1
    c = 1 - t
    v = (a >> c) & 1
    if v == 0:
        qc.x(c)
    qc.cx(c, t)
    if v == 0:
        qc.x(c)


def _transposition(qc, a, b):
    # exchange basis states |a> and |b> (eq_1 building block)
    d = a ^ b
    if d == 3:
        qc.cx(0, 1)
        a2 = a ^ ((a & 1) << 1)
        b2 = b ^ ((b & 1) << 1)
        _single_bit_swap(qc, a2, b2)
        qc.cx(0, 1)
    else:
        _single_bit_swap(qc, a, b)


def build_circuit(instance):
    """Return a circuit with U|j> = |sigma(j)>, j = 2*q1 + q0 (qubit 0 least significant)."""
    sigma = _validate(instance)
    qr = QuantumRegister(2, 'ququart')
    qc = QuantumCircuit(qr)
    cur = [0, 1, 2, 3]
    for j in range(4):
        x = cur[j]
        y = sigma[j]
        if x != y:
            _transposition(qc, x, y)
            for k in range(4):
                if cur[k] == x:
                    cur[k] = y
                elif cur[k] == y:
                    cur[k] = x
    return qc
