from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    m = instance.get('m')
    f = instance.get('f_values')
    if not _is_int(n) or not _is_int(m):
        raise ValueError('n and m must be integers')
    if n < 1 or m < 1:
        raise ValueError('n and m must be >= 1')
    if n + m + 1 > 12:
        raise ValueError('total qubits n+m+1 must be <= 12')
    if not isinstance(f, (list, tuple)) or len(f) != 2 ** n:
        raise ValueError('f_values must be a list of length 2**n')
    angles = []
    for v in f:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError('f values must be real numbers')
        v = float(v)
        if not math.isfinite(v) or v < 0.0 or v > 1.0:
            raise ValueError('f values must lie in [0,1]')
        angles.append(2.0 * math.asin(math.sqrt(v)))
    return n, m, angles


def _prep_A(n, angles):
    # eq_2: A|0>|0> = N^-1/2 sum_x |x>(sqrt(1-f)|0> + sqrt(f)|1>)
    a = QuantumCircuit(n + 1, name='A')
    for q in range(n):
        a.h(q)
    for x, t in enumerate(angles):
        if t != 0.0:
            a.append(RYGate(t).control(n, ctrl_state=x), list(range(n)) + [n])
    return a


def _grover_gate(n, a_circ):
    # eq_4: Q' = A S_0 A^dagger S_chi (the overall -1 is applied separately as Z on the control)
    a_gate = a_circ.to_gate()
    q = QuantumCircuit(n + 1, name='Qp')
    allq = list(range(n + 1))
    q.z(n)  # S_chi: flip sign of flag=1
    q.append(a_gate.inverse(), allq)
    for i in allq:
        q.x(i)
    q.h(n)
    q.mcx(list(range(n)), n)
    q.h(n)
    for i in allq:
        q.x(i)  # S_0: flip sign of |0...0>
    q.append(a_gate, allq)
    return q.to_gate()


def build_circuit(instance):
    n, m, angles = _parse(instance)
    phase = QuantumRegister(m, 'phase')
    xr = QuantumRegister(n, 'x')
    flag = QuantumRegister(1, 'flag')
    qc = QuantumCircuit(phase, xr, flag)
    xq = list(range(m, m + n))
    fq = m + n
    a_circ = _prep_A(n, angles)
    qc.append(a_circ.to_gate(), xq + [fq])
    for j in range(m):
        qc.h(j)
    cq = _grover_gate(n, a_circ).control(1)
    for j in range(m):
        for _ in range(2 ** j):
            qc.append(cq, [j] + xq + [fq])
    # Q = -Q': controlled (-1) is Z on the control qubit; (-1)^(2^j) = 1 for j >= 1
    qc.z(0)
    qc.append(QFTGate(m).inverse(), list(range(m)))
    return qc
