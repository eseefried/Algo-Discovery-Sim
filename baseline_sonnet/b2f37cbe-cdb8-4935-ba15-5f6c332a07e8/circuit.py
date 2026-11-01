import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, np.integer)):
        raise ValueError(name + ' must be an integer')
    return int(v)


def _coin(qc, cq):
    # Grover coin G = 2|s><s| - I = -(H H)(I - 2|00><00|)(H H); eq_1 coin factor
    qc.h(cq[0])
    qc.h(cq[1])
    qc.x(cq[0])
    qc.x(cq[1])
    qc.cz(cq[0], cq[1])
    qc.x(cq[0])
    qc.x(cq[1])
    qc.h(cq[0])
    qc.h(cq[1])
    qc.global_phase += math.pi


def _disorder(qc, pos, L, phases):
    # eq_2: diagonal phase e^{i theta_x} on each site, identity on coin
    n = len(pos)
    for s in range(L * L):
        th = phases[s]
        if th == 0.0:
            continue
        zeros = [pos[i] for i in range(n) if not (s >> i) & 1]
        for q in zeros:
            qc.x(q)
        qc.mcp(th, pos[:-1], pos[-1])
        for q in zeros:
            qc.x(q)


def _basis_swap(qc, qubits, a, b):
    # exchange computational basis states |a> and |b| using CX + multi-controlled X
    n = len(qubits)
    d = [i for i in range(n) if ((a ^ b) >> i) & 1]
    p = d[0]
    pa = (a >> p) & 1
    for j in d[1:]:
        qc.cx(qubits[p], qubits[j])
    controls = []
    cs = 0
    for i in range(n):
        if i == p:
            continue
        bit = (a >> i) & 1
        if i in d:
            bit ^= pa
        cs |= bit << len(controls)
        controls.append(qubits[i])
    qc.mcx(controls, qubits[p], ctrl_state=cs)
    for j in d[1:]:
        qc.cx(qubits[p], qubits[j])


def _cut_swaps(qc, allq, m, L, cuts):
    # eq_3 (cut part): swap |x,R> <-> |x+e,L> across each cut link before the plain shift
    for (x, y, ax) in cuts:
        if ax == 0:
            a = x + L * y + L * L * 0
            b = ((x + 1) % L) + L * y + L * L * 1
        else:
            a = x + L * y + L * L * 2
            b = x + L * ((y + 1) % L) + L * L * 3
        _basis_swap(qc, allq, a, b)


def _shift(qc, m, xq, yq, cq):
    # eq_3 (hop part): coin 0:+x, 1:-x, 2:+y, 3:-y with modular increment/decrement
    for reg, cinc, cdec in ((xq, 0, 1), (yq, 2, 3)):
        for k in range(m - 1, -1, -1):
            qc.mcx(cq + reg[:k], reg[k], ctrl_state=cinc | (((1 << k) - 1) << 2))
        for k in range(m - 1, -1, -1):
            qc.mcx(cq + reg[:k], reg[k], ctrl_state=cdec)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    L = _as_int(instance.get('L', 4), 'L')
    if L not in (2, 4, 8):
        raise ValueError('L must be 2, 4 or 8')
    m = int(round(math.log2(L)))
    if 2 * m + 2 > 12:
        raise ValueError('too many qubits')
    T = _as_int(instance.get('steps', 1), 'steps')
    if T < 0 or T > 16:
        raise ValueError('steps must be in 0..16')
    ph = instance.get('disorder_phases', None)
    if ph is None:
        phases = [0.0] * (L * L)
    else:
        if not isinstance(ph, (list, tuple)) or len(ph) != L * L:
            raise ValueError('disorder_phases must have length L*L')
        phases = []
        for v in ph:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError('invalid phase')
            phases.append(float(v))
    raw = instance.get('cut_links', [])
    if not isinstance(raw, (list, tuple)):
        raise ValueError('cut_links must be a list')
    cutset = set()
    for c in raw:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            raise ValueError('cut link must be [x, y, axis]')
        x = _as_int(c[0], 'x')
        y = _as_int(c[1], 'y')
        ax = _as_int(c[2], 'axis')
        if not (0 <= x < L and 0 <= y < L and ax in (0, 1)):
            raise ValueError('cut link out of range')
        cutset.add((x, y, ax))
    cuts = sorted(cutset)
    xr = QuantumRegister(m, 'x')
    yr = QuantumRegister(m, 'y')
    cr = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(xr, yr, cr)
    xq = list(range(m))
    yq = list(range(m, 2 * m))
    cq = [2 * m, 2 * m + 1]
    allq = xq + yq + cq
    pos = xq + yq
    for _ in range(T):  # eq_1 / eq_4: U^T with U = S D (I x C)
        _coin(qc, cq)
        _disorder(qc, pos, L, phases)
        _cut_swaps(qc, allq, m, L, cuts)
        _shift(qc, m, xq, yq, cq)
    return qc
