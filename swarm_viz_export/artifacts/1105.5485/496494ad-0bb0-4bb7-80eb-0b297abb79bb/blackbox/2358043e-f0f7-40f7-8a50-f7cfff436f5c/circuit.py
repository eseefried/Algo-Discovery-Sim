import math
from qiskit import QuantumCircuit


def _cond_gate(qc, controls, bits, target, kind, angle):
    for q, b in zip(controls, bits):
        if b == 0:
            qc.x(q)
    if kind == 'x':
        if len(controls) == 0:
            qc.x(target)
        elif len(controls) == 1:
            qc.cx(controls[0], target)
        else:
            qc.mcx(list(controls), target)
    else:
        qc.mcp(angle, list(controls), target)
    for q, b in zip(controls, bits):
        if b == 0:
            qc.x(q)


def _shift(qc, ctrl, ctrl_bits, t, sign):
    # Shift target level by sign (+1 or -1) mod 3, controlled on ctrl==ctrl_bits.
    t0, t1 = t[0], t[1]

    def swap01():
        _cond_gate(qc, list(ctrl) + [t1], list(ctrl_bits) + [0], t0, 'x', 0.0)

    def swap12():
        qc.cx(t1, t0)
        _cond_gate(qc, list(ctrl) + [t0], list(ctrl_bits) + [1], t1, 'x', 0.0)
        qc.cx(t1, t0)

    if sign == 1:
        swap12()
        swap01()
    else:
        swap01()
        swap12()


def _cx3(qc, c, t, sign):
    # |a,b> -> |a, b + sign*a mod 3>
    _shift(qc, c, [1, 0], t, sign)
    _shift(qc, c, [0, 1], t, -sign)


def _cz3(qc, qa, qb, sign):
    for a in (1, 2):
        for b in (1, 2):
            k = (a * b) % 3
            angle = sign * 2.0 * math.pi * k / 3.0
            bits_a = [a & 1, a >> 1]
            bits_b = [b & 1, b >> 1]
            ctrls = [qa[0], qa[1], qb[0]]
            bits = bits_a + [bits_b[0]]
            # extra condition on qb[1]: fold into target via X conjugation
            if bits_b[1] == 0:
                qc.x(qb[1])
            _cond_gate(qc, ctrls, bits, qb[1], 'p', angle)
            if bits_b[1] == 0:
                qc.x(qb[1])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gate = instance.get('gate', 'cx3')
    control = instance.get('control', 'a')
    inverse = instance.get('inverse', False)
    if gate not in ('cz3', 'cx3', 'swap3'):
        raise ValueError('gate must be cz3, cx3 or swap3')
    if control not in ('a', 'b'):
        raise ValueError('control must be a or b')
    if not isinstance(inverse, bool):
        raise ValueError('inverse must be boolean')
    qc = QuantumCircuit(4, name=gate)
    qa = [0, 1]
    qb = [2, 3]
    sign = -1 if inverse else 1
    if gate == 'cz3':
        _cz3(qc, qa, qb, sign)
    elif gate == 'cx3':
        if control == 'a':
            _cx3(qc, qa, qb, sign)
        else:
            _cx3(qc, qb, qa, sign)
    else:
        _cx3(qc, qa, qb, 1)
        _cx3(qc, qb, qa, -1)
        _cx3(qc, qa, qb, 1)
        # negation |j> -> |-j> on qutrit a: exchange levels 1 and 2
        qc.swap(qa[0], qa[1])
    return qc
