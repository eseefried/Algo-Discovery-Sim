from qiskit import QuantumCircuit, QuantumRegister
import math


def _shift_gate(power):
    """Qutrit shift X^power on 2 qubits (value=q0+2*q1): 0->1->2->0, 3 fixed."""
    sub = QuantumCircuit(2)
    sub.swap(0, 1)  # exchanges values 1 and 2
    sub.cx(1, 0, ctrl_state=0)  # exchanges values 0 and 1
    if power == 2:
        sub = sub.inverse()
    return sub.to_gate(label='X^%d' % power)


def _phase_on_state(qc, bits, angle):
    """Apply exp(i*angle) to the 4-qubit basis state whose bits (q0..q3) are given."""
    for q in range(4):
        if bits[q] == 0:
            qc.x(q)
    qc.mcp(angle, [0, 1, 2], 3)
    for q in range(4):
        if bits[q] == 0:
            qc.x(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gate = instance.get('gate', 'TCX')
    inverse = instance.get('inverse', False)
    if gate not in ('TCX', 'TCZ'):
        raise ValueError('gate must be TCX or TCZ')
    if not isinstance(inverse, bool):
        raise ValueError('inverse must be a bool')
    qc = QuantumCircuit(QuantumRegister(2, 'ctrl'), QuantumRegister(2, 'targ'))
    if gate == 'TCX':
        # eq_1: sum_c |c><c| (x) X^c
        for c in (1, 2):
            g = _shift_gate(c).control(2, ctrl_state=c)
            qc.append(g, [0, 1, 2, 3])
    else:
        # eq_2: sum_c |c><c| (x) Z^c, i.e. phase omega^(c*t) on |c,t>
        for c in (1, 2):
            for t in (1, 2):
                k = (c * t) % 3
                if k:
                    bits = [c & 1, c >> 1, t & 1, t >> 1]
                    _phase_on_state(qc, bits, 2 * math.pi * k / 3)
    if inverse:
        qc = qc.inverse()
    return qc
