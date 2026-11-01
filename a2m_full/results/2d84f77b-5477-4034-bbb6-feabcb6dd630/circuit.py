from qiskit import QuantumCircuit, QuantumRegister
import math


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(name + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(name + ' must be finite')
    return v


def build_circuit(instance):
    '''CTQW search operator on the periodic 2x2-cell honeycomb (cube graph).
    Site index = 4*sublattice + 2*y + x, qubit0=x, qubit1=y, qubit2=sublattice.
    Edge colours (perfect matchings) are XOR with masks 0b100, 0b101, 0b110:
    A(x,y)-B(x,y), A(x,y)-B(x-1,y), A(x,y)-B(x,y-1).'''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gamma = _real(instance.get('gamma'), 'gamma')
    epsilon = _real(instance.get('epsilon'), 'epsilon')
    dt = _real(instance.get('dt'), 'dt')
    if dt <= 0:
        raise ValueError('dt must be positive')
    steps = instance.get('steps')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 500:
        raise ValueError('steps must be an integer in 1..500')
    marked = instance.get('marked_sites')
    if not isinstance(marked, list) or len(marked) < 1 or len(marked) > 8:
        raise ValueError('marked_sites must be a list of 1..8 sites')
    for w in marked:
        if isinstance(w, bool) or not isinstance(w, int) or w < 0 or w > 7:
            raise ValueError('marked site must be an integer in 0..7')
    if len(set(marked)) != len(marked):
        raise ValueError('marked_sites must be distinct')
    pos = QuantumRegister(3, 'pos')
    qc = QuantumCircuit(pos)
    masks = ([2], [2, 0], [2, 1])
    for _ in range(steps):
        # eq_3 hopping layers: exp(i*gamma*dt*X_mask) = rx(-2*gamma*dt) on parity qubit
        for m in masks:
            c = m[0]
            for t in m[1:]:
                qc.cx(c, t)
            qc.rx(-2.0 * gamma * dt, c)
            for t in reversed(m[1:]):
                qc.cx(c, t)
        # eq_1/eq_3 marking: exp(i*epsilon*dt|w><w|) as multi-controlled phase
        for w in marked:
            zeros = [q for q in range(3) if not (w >> q) & 1]
            for q in zeros:
                qc.x(q)
            qc.mcp(epsilon * dt, [0, 1], 2)
            for q in zeros:
                qc.x(q)
    return qc
