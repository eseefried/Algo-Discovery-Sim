from qiskit import QuantumCircuit, QuantumRegister


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _memory(qc, index, data, db, n, m):
    # U_M (eq_2): |x>|y> -> |x>|y XOR D_x>; every gate is self-inverse, so the same routine uncomputes.
    for x, v in enumerate(db):
        for b in range(m):
            if (v >> b) & 1:
                zeros = [index[i] for i in range(n) if not (x >> i) & 1]
                for q in zeros:
                    qc.x(q)
                qc.mcx(list(index), data[b])
                for q in zeros:
                    qc.x(q)


def _mark(qc, data, flag, target, m):
    # predicate g(D) = [D == target] (eq_3), XORed onto the flag qubit
    zeros = [data[i] for i in range(m) if not (target >> i) & 1]
    for q in zeros:
        qc.x(q)
    qc.mcx(list(data), flag[0])
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    """Grover database oracle. instance: {n, m, database (2^n ints < 2^m), target (int < 2^m)}."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    m = instance.get('m')
    db = instance.get('database')
    target = instance.get('target')
    if not _is_int(n) or not _is_int(m) or n < 1 or m < 1:
        raise ValueError('n and m must be positive integers')
    if n + m + 1 > 12:
        raise ValueError('total qubits n+m+1 must be at most 12')
    if not isinstance(db, list) or len(db) != 2 ** n:
        raise ValueError('database must be a list of length 2^n')
    for v in db:
        if not _is_int(v) or v < 0 or v >= 2 ** m:
            raise ValueError('database entries must be integers in [0, 2^m)')
    if not _is_int(target) or target < 0 or target >= 2 ** m:
        raise ValueError('target must be an integer in [0, 2^m)')
    index = QuantumRegister(n, 'index')
    data = QuantumRegister(m, 'data')
    flag = QuantumRegister(1, 'flag')
    qc = QuantumCircuit(index, data, flag)
    _memory(qc, index, data, db, n, m)
    _mark(qc, data, flag, target, m)
    _memory(qc, index, data, db, n, m)
    return qc
