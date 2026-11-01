from __future__ import annotations
import math
from qiskit import QuantumCircuit


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _mcz(qc, qubits):
    # multi-controlled Z on the given qubits (phase -1 on all-ones)
    if len(qubits) == 1:
        qc.z(qubits[0])
        return
    t = qubits[-1]
    qc.h(t)
    qc.mcx(list(qubits[:-1]), t)
    qc.h(t)


def _oracle(qc, n, ctrl, w):
    # Lambda_C(O_w): O_w = I - 2|w><w| on S, applied only when C=1 (eq_2)
    zeros = [i for i in range(n) if not ((w >> i) & 1)]
    for i in zeros:
        qc.x(i)
    _mcz(qc, list(range(n)) + [ctrl])
    for i in zeros:
        qc.x(i)


def _diffusion(qc, n):
    # D = 2|s><s| - I on S (eq_2); H X mcz X H = I - 2|s><s| = -D, so add global phase pi
    for i in range(n):
        qc.h(i)
        qc.x(i)
    _mcz(qc, list(range(n)))
    for i in range(n):
        qc.x(i)
        qc.h(i)
    qc.global_phase += math.pi


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    w = instance.get('w')
    theta = instance.get('theta')
    tau = instance.get('tau')
    k = instance.get('k')
    if not _is_int(n) or n < 1 or n > 10:
        raise ValueError('n must be an integer in [1,10]')
    if not _is_int(w) or w < 0 or w >= 2 ** n:
        raise ValueError('w must be an integer in [0, 2^n)')
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError('theta must be a finite real number')
    if tau is not None and (not _is_int(tau) or tau < 1):
        raise ValueError('tau must be a positive integer or null')
    if not _is_int(k) or k < 0 or k > 1000:
        raise ValueError('k must be an integer in [0,1000]')
    m = (k // tau) if tau is not None else 0
    total = n + 1 + m
    if total > 12:
        raise ValueError('total qubits exceed 12')
    qc = QuantumCircuit(total)
    ctrl = n
    rec = 0
    for j in range(1, k + 1):
        _oracle(qc, n, ctrl, w)
        qc.ry(float(theta), ctrl)
        _diffusion(qc, n)
        if tau is not None and j % tau == 0:
            # deferred Z measurement of C, no reset (eq_3)
            qc.cx(ctrl, n + 1 + rec)
            rec += 1
    return qc
