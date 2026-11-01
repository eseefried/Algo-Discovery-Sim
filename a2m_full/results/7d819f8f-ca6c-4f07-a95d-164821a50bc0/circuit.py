from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    costs = instance.get('costs')
    if not isinstance(costs, (list, tuple)):
        raise ValueError('costs must be a list')
    n = len(costs)
    if n < 2 or n > 8:
        raise ValueError('number of candidates n must satisfy 2<=n<=8')
    for c in costs:
        if isinstance(c, bool) or not isinstance(c, int) or c < 0:
            raise ValueError('costs must be nonnegative integers')
    tau = instance.get('threshold')
    if isinstance(tau, bool) or not isinstance(tau, int) or tau < 0:
        raise ValueError('threshold must be a nonnegative integer')
    k = instance.get('iterations')
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 64:
        raise ValueError('iterations must be an integer in 0..64')
    return [int(c) for c in costs], int(tau), int(k)


def _mcz(qc, idx):
    # Z on the all-ones basis state of the index register.
    if len(idx) == 1:
        qc.z(idx[0])
    else:
        qc.mcp(math.pi, list(idx[:-1]), idx[-1])


def _oracle(qc, idx, marked):
    # eq_2: O_tau|w> = (-1)^[c(w)<tau]|w>, compiled from the table.
    q = len(idx)
    for w in marked:
        zeros = [i for i in range(q) if not (w >> i) & 1]
        for i in zeros:
            qc.x(idx[i])
        _mcz(qc, idx)
        for i in zeros:
            qc.x(idx[i])


def _diffusion(qc, idx):
    # eq_3: 2|s><s| - I = -(H X MCZ X H); the -1 is restored as global phase.
    for i in range(len(idx)):
        qc.h(idx[i])
    for i in range(len(idx)):
        qc.x(idx[i])
    _mcz(qc, idx)
    for i in range(len(idx)):
        qc.x(idx[i])
    for i in range(len(idx)):
        qc.h(idx[i])
    qc.global_phase += math.pi


def build_circuit(instance):
    costs, tau, k = _validate(instance)
    n = len(costs)
    q = max(1, math.ceil(math.log2(n)))
    if q > 12:
        raise ValueError('too many qubits')
    marked = [w for w in range(n) if costs[w] < tau]
    idx = QuantumRegister(q, 'idx')
    qc = QuantumCircuit(idx)
    for _ in range(k):
        _oracle(qc, idx, marked)
        _diffusion(qc, idx)
    return qc
