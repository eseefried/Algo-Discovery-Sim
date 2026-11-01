from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    try:
        a = np.array(instance.get('adjacency'), dtype=float)
    except Exception:
        raise ValueError('adjacency must be a numeric square matrix')
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError('adjacency must be square')
    n = a.shape[0]
    if n < 2 or n > 8:
        raise ValueError('number of vertices must be in 2..8')
    if not np.all(np.isfinite(a)) or not np.all((a == 0) | (a == 1)):
        raise ValueError('adjacency entries must be 0 or 1')
    if not np.array_equal(a, a.T) or np.any(np.diag(a) != 0):
        raise ValueError('adjacency must be symmetric with zero diagonal')
    t = instance.get('time')
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t):
        raise ValueError('time must be a finite real number')
    steps = instance.get('trotter_steps', 1)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 100:
        raise ValueError('trotter_steps must be an integer in 1..100')
    order = instance.get('order', 2)
    if isinstance(order, bool) or order not in (1, 2):
        raise ValueError('order must be 1 or 2')
    return a, float(t), steps, order


def _pauli_terms(a):
    # Classical Pauli decomposition A = sum_P c_P P of the zero-padded adjacency matrix.
    n = a.shape[0]
    m = max(1, int(math.ceil(math.log2(n))))
    d = 2 ** m
    big = np.zeros((d, d))
    big[:n, :n] = a
    mats = [np.eye(2), np.array([[0, 1], [1, 0]], dtype=complex),
            np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
    terms = []
    for code in range(1, 4 ** m):
        digits = [(code // (4 ** k)) % 4 for k in range(m)]
        mat = np.array([[1.0]], dtype=complex)
        for k in range(m - 1, -1, -1):
            mat = np.kron(mat, mats[digits[k]])
        c = float(np.real(np.trace(mat @ big))) / d
        if abs(c) > 1e-12:
            terms.append((digits, c))
    return m, terms


def _rot(qc, qubits, digits, theta):
    # exp(-i theta P) for Pauli string P; digits[k] in {0:I,1:X,2:Y,3:Z} on qubits[k].
    act = [(q, dg) for q, dg in zip(qubits, digits) if dg]
    if not act:
        return
    for q, dg in act:
        if dg == 1:
            qc.h(q)
        elif dg == 2:
            qc.sdg(q)
            qc.h(q)
    for i in range(len(act) - 1):
        qc.cx(act[i][0], act[i + 1][0])
    qc.rz(2.0 * theta, act[-1][0])
    for i in range(len(act) - 2, -1, -1):
        qc.cx(act[i][0], act[i + 1][0])
    for q, dg in act:
        if dg == 1:
            qc.h(q)
        elif dg == 2:
            qc.h(q)
            qc.s(q)


def _evolve(qc, qubits, terms, t, steps, order):
    # Product-formula approximation of exp(-i A t) on one position register.
    dt = t / steps
    for _ in range(steps):
        if order == 1:
            for digits, c in terms:
                _rot(qc, qubits, digits, c * dt)
        else:
            for digits, c in terms:
                _rot(qc, qubits, digits, c * dt / 2.0)
            for digits, c in reversed(terms):
                _rot(qc, qubits, digits, c * dt / 2.0)


def build_circuit(instance):
    """Two-fermion CTQW operation exp(-i (A x I + I x A) t) on registers r1, r2."""
    a, t, steps, order = _validate(instance)
    m, terms = _pauli_terms(a)
    r1 = QuantumRegister(m, 'r1')
    r2 = QuantumRegister(m, 'r2')
    qc = QuantumCircuit(r1, r2)
    q1 = list(range(m))
    q2 = list(range(m, 2 * m))
    # H2 = A (x) I + I (x) A; the two terms commute, so exp(-iH2 t) = exp(-iAt)_r1 exp(-iAt)_r2.
    _evolve(qc, q1, terms, t, steps, order)
    _evolve(qc, q2, terms, t, steps, order)
    return qc
