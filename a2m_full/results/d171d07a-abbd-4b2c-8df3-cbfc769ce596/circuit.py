from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _as_int(v):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError('parameters must be integers')
    return v


def _cycles(m, N):
    # cycles of the permutation x -> m*x mod N on 0..N-1 (identity beyond N)
    seen = [False] * N
    out = []
    for s in range(N):
        if seen[s]:
            continue
        cyc = []
        x = s
        while not seen[x]:
            seen[x] = True
            cyc.append(x)
            x = (m * x) % N
        if len(cyc) > 1:
            out.append(cyc)
    return out


def _transposition(qc, ctrl, work, x, y):
    # controlled swap of basis states |x> and |y> on the work register
    n = len(work)
    d = x ^ y
    k = (d & -d).bit_length() - 1
    others = [j for j in range(n) if ((d >> j) & 1) and j != k]
    for j in others:
        qc.cx(work[k], work[j])
    lx = x
    if (x >> k) & 1:
        for j in others:
            lx ^= 1 << j
    ctrl_bits = [j for j in range(n) if j != k]
    zeros = [work[j] for j in ctrl_bits if not ((lx >> j) & 1)]
    for q in zeros:
        qc.x(q)
    qc.mcx([ctrl] + [work[j] for j in ctrl_bits], work[k])
    for q in zeros:
        qc.x(q)
    for j in reversed(others):
        qc.cx(work[k], work[j])


def _controlled_mult(qc, ctrl, work, m, N):
    # controlled |x> -> |m x mod N> (identity for x >= N)
    for cyc in _cycles(m, N):
        L = len(cyc)
        for i in range(L - 2, -1, -1):
            _transposition(qc, ctrl, work, cyc[i], cyc[i + 1])


def build_circuit(instance):
    """Order-finding phase estimation operation. instance: {'N':int,'a':int,'t':int (optional)}."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    N = _as_int(instance.get('N'))
    a = _as_int(instance.get('a'))
    if N < 3 or not (1 < a < N) or math.gcd(a, N) != 1:
        raise ValueError('need N>=3, 1<a<N, gcd(a,N)=1')
    n = (N - 1).bit_length()
    if n >= 12:
        raise ValueError('too many qubits')
    t = instance.get('t')
    if t is None:
        t = min(2 * n, 12 - n)
    t = _as_int(t)
    if t < 1 or t + n > 12:
        raise ValueError('invalid control register size')
    ctl = QuantumRegister(t, 'control')
    wrk = QuantumRegister(n, 'work')
    qc = QuantumCircuit(ctl, wrk)
    for j in range(t):
        qc.h(ctl[j])
    work = [wrk[i] for i in range(n)]
    for j in range(t):
        m = pow(a, 2 ** j, N)
        if m != 1:
            _controlled_mult(qc, ctl[j], work, m, N)
    qc.append(QFTGate(t).inverse(), list(range(t)))
    return qc
