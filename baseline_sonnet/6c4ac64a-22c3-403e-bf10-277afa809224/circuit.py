import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import PhaseGate


def _shift(inverse):
    """Qutrit X (eq_1) on 2 qubits: 0->1->2->0, 3 fixed. Value = q0 + 2*q1."""
    s = QuantumCircuit(2, name='X3inv' if inverse else 'X3')
    if not inverse:
        s.swap(0, 1)  # |01> <-> |10>  (values 1 <-> 2)
        s.cx(1, 0, ctrl_state=0)  # |00> <-> |01>  (values 0 <-> 1)
    else:
        s.cx(1, 0, ctrl_state=0)
        s.swap(0, 1)
    return s


def build_circuit(instance):
    """Build TCX or TCZ on control qubits [0,1] and target qubits [2,3]."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gate = instance.get('gate', None)
    if gate not in ('TCX', 'TCZ'):
        raise ValueError('gate must be TCX or TCZ')
    inverse = instance.get('inverse', False)
    if not isinstance(inverse, bool):
        raise ValueError('inverse must be a bool')
    ctrl = QuantumRegister(2, 'ctrl')
    tgt = QuantumRegister(2, 'tgt')
    qc = QuantumCircuit(ctrl, tgt, name=gate)
    if gate == 'TCX':
        # eq_2: control value c applies X^c to target
        g1 = _shift(inverse).to_gate()
        g2 = _shift(not inverse).to_gate()  # X^2 = X^-1
        qc.append(g1.control(2, ctrl_state=1), [0, 1, 2, 3])  # c=1
        qc.append(g2.control(2, ctrl_state=2), [0, 1, 2, 3])  # c=2
    else:
        # eq_3: phase w^(c*t) on basis |c,t>
        sign = -1.0 if inverse else 1.0
        for c in (1, 2):
            for t in (1, 2):
                k = (c * t) % 3
                if k == 0:
                    continue
                angle = sign * 2.0 * math.pi * k / 3.0
                bits = [c & 1, (c >> 1) & 1, t & 1, (t >> 1) & 1]
                tidx = 2 if bits[2] == 1 else 3
                controls = [i for i in range(4) if i != tidx]
                cs = 0
                for j, i in enumerate(controls):
                    cs |= bits[i] << j
                qc.append(PhaseGate(angle).control(3, ctrl_state=cs), controls + [tidx])
    return qc
