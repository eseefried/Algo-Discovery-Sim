from qiskit import QuantumCircuit, QuantumRegister
import math


def _as_int(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    if value < lo or value > hi:
        raise ValueError(name + ' out of range')
    return value


def _coin(qc, p0, p1, c0, c1, w):
    # eq_2: C' = -(D on unmarked vertices, identity on marked), D = I - 2|s><s|, s = H^2|00>
    qc.h(c0)
    qc.h(c1)
    qc.x(c0)
    qc.x(c1)
    # phase flip on coin==00 (now coin==11) for every vertex
    qc.cz(c0, c1)
    # undo the flip when pos == w, so only unmarked vertices get D
    if (w & 1) == 0:
        qc.x(p0)
    if (w >> 1) == 0:
        qc.x(p1)
    qc.mcp(math.pi, [p0, p1, c0], c1)
    if (w & 1) == 0:
        qc.x(p0)
    if (w >> 1) == 0:
        qc.x(p1)
    qc.x(c0)
    qc.x(c1)
    qc.h(c0)
    qc.h(c1)
    # overall minus sign: C0 = -D, C1 = -I
    qc.global_phase += math.pi


def _shift(qc, p0, p1, c0, c1):
    # eq_3: |v,c> -> |v xor (c+1), c> for c in {0,1,2}; c=3 is the loop and is fixed
    # coin value c = c0 + 2*c1
    qc.mcx([c0, c1], p0, ctrl_state=0)  # c=0: xor 01
    qc.mcx([c0, c1], p1, ctrl_state=1)  # c=1: xor 10
    qc.mcx([c0, c1], p0, ctrl_state=2)  # c=2: xor 11
    qc.mcx([c0, c1], p1, ctrl_state=2)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key not in ('N', 'l', 'marked', 'steps'):
            raise ValueError('unknown parameter ' + str(key))
    _as_int(instance.get('N', 4), 'N', 4, 4)
    _as_int(instance.get('l', 1), 'l', 1, 1)
    w = _as_int(instance.get('marked', 0), 'marked', 0, 3)
    steps = _as_int(instance.get('steps', 1), 'steps', 0, 200)
    pos = QuantumRegister(2, 'pos')
    coin = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(pos, coin)
    p0, p1, c0, c1 = pos[0], pos[1], coin[0], coin[1]
    for _ in range(steps):
        _coin(qc, p0, p1, c0, c1, w)
        _shift(qc, p0, p1, c0, c1)
    return qc
