from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate
import math
import numpy as np


def _get(inst, key, lo, hi):
    v = inst.get(key)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError('invalid or missing parameter ' + key)
    return v


def _inc(qc, reg, ctrl, forward):
    # +1 (forward) or -1 (inverse) mod 2^len(reg), controlled on ctrl being 1
    n = len(reg)
    order = range(n - 1, -1, -1) if forward else range(n)
    for i in order:
        qc.mcx([ctrl] + list(reg[:i]), reg[i])


def _shift(qc, reg, ctrl):
    # eq_2: coin 0 -> +1, coin 1 -> -1 (mod 2^n)
    qc.x(ctrl)
    _inc(qc, reg, ctrl, True)
    qc.x(ctrl)
    _inc(qc, reg, ctrl, False)


def _coin(qc, pos, targets, theta, N):
    # eq_1: multiplexed exp(-i theta Y) = Ry(2 theta), controlled on the site index
    for a, t in enumerate(targets):
        for s in range(N * N):
            g = RYGate(2.0 * float(theta[a][s])).control(len(pos), ctrl_state=s)
            qc.append(g, list(pos) + [t])


def _swap_states(qc, a, b):
    # transposition of two basis states given as {qubit: bit} over the same qubit set
    diff = [q for q in a if a[q] != b[q]]
    p = diff[0]
    others = diff[1:]
    for q in others:
        qc.cx(p, q)
    ap = dict(a)
    for q in others:
        ap[q] = a[q] ^ a[p]
    ctrls = [q for q in a if q != p]
    zeros = [q for q in ctrls if ap[q] == 0]
    for q in zeros:
        qc.x(q)
    qc.mcx(ctrls, p)
    for q in zeros:
        qc.x(q)
    for q in reversed(others):
        qc.cx(p, q)


def _reflect(qc, n, cxq, row, xs, xe):
    # eq_3: applied right after the x shift. For each cut link (x,x+1) on the row,
    # swap |x+1,c=0> and |x,c=1> so the walker that tried to cross is returned to its
    # origin site with flipped coin. The y coin qubit is untouched.
    for x in range(xs, xe):
        a = {}
        b = {}
        for i in range(n):
            a[i] = (x >> i) & 1
            b[i] = ((x + 1) >> i) & 1
            a[n + i] = (row >> i) & 1
            b[n + i] = (row >> i) & 1
        a[cxq] = 1
        b[cxq] = 0
        _swap_states(qc, a, b)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _get(instance, 'n_bits', 2, 3)
    T = _get(instance, 'steps', 1, 32)
    seed = _get(instance, 'seed', 0, 2 ** 31 - 1)
    cut = instance.get('cut')
    if not isinstance(cut, bool):
        raise ValueError('cut must be a bool')
    N = 1 << n
    row = _get(instance, 'cut_row', 0, N - 1)
    xs = _get(instance, 'cut_x_start', 0, N - 2)
    xe = _get(instance, 'cut_x_end', 1, N - 1)
    if xe <= xs:
        raise ValueError('cut_x_end must exceed cut_x_start')
    qx = QuantumRegister(n, 'x')
    qy = QuantumRegister(n, 'y')
    qcn = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(qx, qy, qcn)
    xr = list(range(n))
    yr = list(range(n, 2 * n))
    pos = xr + yr
    cxq = 2 * n
    cyq = 2 * n + 1
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0.0, 2.0 * math.pi, size=(2, N * N))
    for _ in range(T):
        _coin(qc, pos, [cxq, cyq], theta, N)
        _shift(qc, xr, cxq)
        if cut:
            _reflect(qc, n, cxq, row, xs, xe)
        _shift(qc, yr, cyq)
    return qc
