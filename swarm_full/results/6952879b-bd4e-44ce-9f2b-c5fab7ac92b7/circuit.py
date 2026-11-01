from qiskit import QuantumCircuit
import math


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    return v


def _as_angle(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError('angle must be a real number')
    if not math.isfinite(v):
        raise ValueError('angle must be finite')
    return float(v)


def build_circuit(instance):
    """Logical gate-set circuit for the encoded-qubit scheme (eq_2).

    instance: {'num_qubits': int in [1,12],
               'gates': [{'type': 'rx'|'rz'|'cphase'|'swap',
                          'qubits': [indices], 'angle': float (rx, rz only)}]}
    Qubit i is logical qubit i (walker position encoding); index 0 is least significant.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('num_qubits'), 'num_qubits')
    if n < 1 or n > 12:
        raise ValueError('num_qubits must be in [1, 12]')
    gates = instance.get('gates')
    if not isinstance(gates, list):
        raise ValueError('gates must be a list')
    if len(gates) > 500:
        raise ValueError('too many gates')
    qc = QuantumCircuit(n)
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError('each gate must be a dict')
        t = g.get('type')
        qs = g.get('qubits')
        if not isinstance(qs, list):
            raise ValueError('qubits must be a list')
        qs = [_as_int(q, 'qubit index') for q in qs]
        for q in qs:
            if q < 0 or q >= n:
                raise ValueError('qubit index out of range')
        if len(set(qs)) != len(qs):
            raise ValueError('qubit indices must be distinct')
        if t == 'rx' or t == 'rz':
            if len(qs) != 1:
                raise ValueError('rotation needs exactly one qubit')
            theta = _as_angle(g.get('angle'))
            # eq_2: R_X(theta)=exp(-i theta X/2), R_Z(phi)=exp(-i phi Z/2)
            if t == 'rx':
                qc.rx(theta, qs[0])
            else:
                qc.rz(theta, qs[0])
        elif t == 'cphase':
            if len(qs) != 2:
                raise ValueError('cphase needs exactly two qubits')
            # eq_2: CPHASE = diag(1,1,1,-1)
            qc.cp(math.pi, qs[0], qs[1])
        elif t == 'swap':
            if len(qs) != 2:
                raise ValueError('swap needs exactly two qubits')
            qc.swap(qs[0], qs[1])
        else:
            raise ValueError('unknown gate type')
    return qc
