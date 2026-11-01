import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    t = instance.get('t')
    f = instance.get('f')
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError('n must be an integer')
    if isinstance(t, bool) or not isinstance(t, int):
        raise ValueError('t must be an integer')
    if n < 1 or t < 1 or t > 8 or n + 1 + t > 12:
        raise ValueError('need n>=1, 1<=t<=8, n+1+t<=12')
    if not isinstance(f, list) or len(f) != 2 ** n:
        raise ValueError('f must be a list of length 2^n')
    vals = []
    for v in f:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError('f entries must be numbers')
        if not math.isfinite(v) or v < 0 or v > 1:
            raise ValueError('f entries must lie in [0,1]')
        vals.append(float(v))
    return n, t, vals


def _prep(n, f):
    # eq_1: A|0> = N^-1/2 sum_x |x>(sqrt(1-f)|0> + sqrt(f)|1>)
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.h(i)
    for xv in range(2 ** n):
        if f[xv] > 0.0:
            theta = 2.0 * math.asin(math.sqrt(f[xv]))
            g = RYGate(theta).control(n, ctrl_state=xv)
            qc.append(g, list(range(n)) + [n])
    return qc


def _body(n, A):
    # eq_2 without the global -1: A S_0 A^-1 S_chi (circuit order: S_chi, A^-1, S_0, A)
    qc = QuantumCircuit(n + 1)
    allq = list(range(n + 1))
    qc.z(n)
    qc.append(A.inverse(), allq)
    for i in allq:
        qc.x(i)
    qc.h(n)
    qc.mcx(list(range(n)), n)
    qc.h(n)
    for i in allq:
        qc.x(i)
    qc.append(A, allq)
    return qc


def build_circuit(instance):
    n, t, f = _parse(instance)
    x = QuantumRegister(n, 'x')
    a = QuantumRegister(1, 'a')
    c = QuantumRegister(t, 'c')
    qc = QuantumCircuit(x, a, c)
    xa = list(range(n + 1))
    cnt = list(range(n + 1, n + 1 + t))
    A = _prep(n, f).to_gate(label='A')
    cbody = _body(n, A).to_gate(label='Qbody').control(1)
    for q in cnt:
        qc.h(q)
    qc.append(A, xa)
    # eq_3: phase estimation of Q; controlled-Q^(2^j) from counting qubit j
    for j in range(t):
        ctrl = cnt[j]
        for _ in range(2 ** j):
            qc.append(cbody, [ctrl] + xa)
            qc.p(math.pi, ctrl)  # the global -1 of Q becomes a phase on the control
    # eq_5: inverse QFT so that counting qubit j carries weight 2^j
    qc.append(QFTGate(t).inverse(), cnt)
    return qc
