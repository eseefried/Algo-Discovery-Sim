import math
from qiskit import QuantumCircuit, QuantumRegister


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _load(qc, index, data, db, n, m):
    # eq_1: U_D = product over addresses i and set bits j of C^n_i X_j (self-inverse)
    idx = list(index)
    for i, word in enumerate(db):
        if word == 0:
            continue
        zeros = [idx[k] for k in range(n) if not ((i >> k) & 1)]
        for q in zeros:
            qc.x(q)
        for j in range(m):
            if (word >> j) & 1:
                qc.mcx(idx, data[j])
        for q in zeros:
            qc.x(q)


def _mark(qc, data, flag, target, m):
    # eq_2: compare data register to w via X conjugation, MCX onto flag (phase kickback if flag is |->)
    zeros = [data[j] for j in range(m) if not ((target >> j) & 1)]
    for q in zeros:
        qc.x(q)
    qc.mcx(list(data), flag[0])
    for q in zeros:
        qc.x(q)


def _oracle(qc, index, data, flag, db, target, n, m):
    # eq_3: O = U_D Mark_w U_D
    _load(qc, index, data, db, n, m)
    _mark(qc, data, flag, target, m)
    _load(qc, index, data, db, n, m)


def _diffusion(qc, index, n):
    # eq_4: H^n X^n C^{n-1}Z X^n H^n = -(2|s><s| - I); global phase pi restores the sign
    idx = list(index)
    for q in idx:
        qc.h(q)
    for q in idx:
        qc.x(q)
    if n == 1:
        qc.z(idx[0])
    else:
        qc.h(idx[-1])
        qc.mcx(idx[:-1], idx[-1])
        qc.h(idx[-1])
    for q in idx:
        qc.x(q)
    for q in idx:
        qc.h(q)
    qc.global_phase += math.pi


def build_circuit(instance):
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
    N = 1 << n
    if not isinstance(db, list) or len(db) != N:
        raise ValueError('database must be a list of length 2^n')
    for word in db:
        if not _is_int(word) or word < 0 or word >= (1 << m):
            raise ValueError('database words must be integers in [0, 2^m)')
    if not _is_int(target) or target < 0 or target >= (1 << m):
        raise ValueError('target must be an integer in [0, 2^m)')
    M = sum(1 for word in db if word == target)
    if M < 1 or M >= N:
        raise ValueError('number of matching addresses must satisfy 1 <= M < N')
    R = instance.get('iterations')
    if R is None:
        # eq_5: R = floor(pi/4 sqrt(N/M))
        R = int(math.floor(math.pi / 4.0 * math.sqrt(N / M)))
    if not _is_int(R) or R < 0 or R > 1000:
        raise ValueError('iterations must be an integer in [0, 1000]')
    index = QuantumRegister(n, 'index')
    data = QuantumRegister(m, 'data')
    flag = QuantumRegister(1, 'flag')
    qc = QuantumCircuit(index, data, flag)
    for _ in range(R):
        _oracle(qc, index, data, flag, db, target, n, m)
        _diffusion(qc, index, n)
    return qc
