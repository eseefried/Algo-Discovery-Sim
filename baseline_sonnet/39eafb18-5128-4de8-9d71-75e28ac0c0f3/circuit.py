import math

from qiskit import QuantumCircuit


def _int_param(instance, key, low, high):
    if not isinstance(instance, dict) or key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < low or v > high:
        raise ValueError(key + ' out of range')
    return v


def _mcz(qc, qubits):
    # multi-controlled Z on all listed qubits: I - 2|1..1><1..1|
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        t = qubits[-1]
        qc.h(t)
        qc.mcx(list(qubits[:-1]), t)
        qc.h(t)


def _oracle(qc, n, w):
    # eq_3: O = I - 2|w><w| (phase oracle on the marked vertex)
    zeros = [q for q in range(n) if not (w >> q) & 1]
    for q in zeros:
        qc.x(q)
    _mcz(qc, list(range(n)))
    for q in zeros:
        qc.x(q)


def _walk_step(qc, n):
    # W = 2|s><s| - I = -(H^n X^n (I-2|0><0|) X^n H^n); global phase pi supplies the minus sign
    for q in range(n):
        qc.h(q)
        qc.x(q)
    _mcz(qc, list(range(n)))
    for q in range(n):
        qc.x(q)
        qc.h(q)
    qc.global_phase = qc.global_phase + math.pi


def build_circuit(instance):
    """Build U=(W^m O)^k. instance keys: n_qubits (1..12), marked (0..2^n-1), m (1..64), k (0..64)."""
    n = _int_param(instance, 'n_qubits', 1, 12)
    w = _int_param(instance, 'marked', 0, 2 ** n - 1)
    m = _int_param(instance, 'm', 1, 64)
    k = _int_param(instance, 'k', 0, 64)
    qc = QuantumCircuit(n, name='dtqw_search')
    for _ in range(k):
        # eq_2: each round applies O first, then W^m (operator order W^m O)
        _oracle(qc, n, w)
        for _ in range(m):
            _walk_step(qc, n)
    return qc
