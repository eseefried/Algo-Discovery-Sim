import math
from qiskit import QuantumCircuit, QuantumRegister


def _mcx(qc, ctrls, bits, t):
    cs = sum(b << i for i, b in enumerate(bits))
    qc.mcx(list(ctrls), t, ctrl_state=cs)


def _phase(qc, qs, bits):
    # phase -1 on the basis pattern bits over qubits qs
    t = qs[-1]
    if bits[-1] == 0:
        qc.x(t)
    qc.h(t)
    _mcx(qc, qs[:-1], bits[:-1], t)
    qc.h(t)
    if bits[-1] == 0:
        qc.x(t)


def _coin(qc, v, slots):
    # eq_2 coin C_v on used slots of vertex v, controlled on vertex == v
    vq = [2, 3, 4]
    vb = [(v >> i) & 1 for i in range(3)]
    d = len(slots)
    if d == 1:
        _phase(qc, [0, 1] + vq, [0, 0] + vb)
    elif d == 2:
        if slots[1] == 1:
            _mcx(qc, [1] + vq, [0] + vb, 0)
        else:
            _mcx(qc, [0] + vq, [0] + vb, 1)
    else:
        th = 2.0 * math.asin(1.0 / math.sqrt(3.0))
        qc.ry(th, 1)
        qc.ch(1, 0, ctrl_state=0)
        for sb in ([1, 0], [0, 1], [1, 1]):
            _phase(qc, [0, 1] + vq, sb + vb)
        qc.ch(1, 0, ctrl_state=0)
        qc.ry(-th, 1)
        _phase(qc, [0, 1] + vq, [1, 1] + vb)


def _swap(qc, a, b):
    # exchange basis states |a> and |b> of the 5 qubits
    dbits = [i for i in range(5) if ((a ^ b) >> i) & 1]
    p = dbits[0]
    others = dbits[1:]
    for q in others:
        qc.cx(p, q)
    ap = a
    if (a >> p) & 1:
        for q in others:
            ap ^= 1 << q
    ctl = [i for i in range(5) if i != p]
    _mcx(qc, ctl, [(ap >> i) & 1 for i in ctl], p)
    for q in others:
        qc.cx(p, q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    x = instance.get('x')
    if not isinstance(x, (list, tuple)) or len(x) != 4:
        raise ValueError('x must be a list of 4 bits')
    for b in x:
        if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
            raise ValueError('x entries must be 0 or 1')
    steps = instance.get('steps', 4)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 32:
        raise ValueError('steps must be an integer in 1..32')
    slot = QuantumRegister(2, 'slot')
    vert = QuantumRegister(3, 'vertex')
    qc = QuantumCircuit(slot, vert)
    # vertices: 0 tail, 1 root, 2 and 3 internal, 4..7 leaves (leaf 4+i present iff x[i]=1)
    s2 = [0] + ([1] if x[0] else []) + ([2] if x[1] else [])
    s3 = [0] + ([1] if x[2] else []) + ([2] if x[3] else [])
    coins = [(0, [0]), (1, [0, 1, 2]), (2, s2), (3, s3)]
    edges = [((0, 0), (1, 0)), ((1, 1), (2, 0)), ((1, 2), (3, 0))]
    for i, (par, sl) in enumerate([(2, 1), (2, 2), (3, 1), (3, 2)]):
        if x[i]:
            coins.append((4 + i, [0]))
            edges.append(((par, sl), (4 + i, 0)))
    for _ in range(steps):
        for v, sl in coins:
            _coin(qc, v, sl)
        for (u, su), (w, sw) in edges:
            _swap(qc, 4 * u + su, 4 * w + sw)
    return qc
