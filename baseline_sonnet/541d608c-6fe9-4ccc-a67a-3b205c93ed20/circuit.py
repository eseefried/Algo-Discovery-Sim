from qiskit import QuantumCircuit
import math


def _ccz(qc, a, b, c):
    """Conventional CCZ: CP_bc(pi/2) CX_ab CP_bc(-pi/2) CX_ab CP_ac(pi/2).
    Phase exponent (units pi/2): c*(b - (a xor b) + a) = 2abc -> (-1)^(abc)."""
    qc.cp(math.pi / 2, b, c)
    qc.cx(a, b)
    qc.cp(-math.pi / 2, b, c)
    qc.cx(a, b)
    qc.cp(math.pi / 2, a, c)


def _toffoli(qc, a, b, c):
    """Toffoli = H_c CCZ H_c."""
    qc.h(c)
    _ccz(qc, a, b, c)
    qc.h(c)


def build_circuit(instance):
    """instance: {'gate': 'ccz'|'toffoli'|'fredkin', 'n_qubits': int 3..12, 'qubits': [a,b,c]}.
    ccz: symmetric phase on |111> of a,b,c. toffoli: controls a,b, target c.
    fredkin: control a, swaps b and c."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gate = instance.get('gate')
    if gate not in ('ccz', 'toffoli', 'fredkin'):
        raise ValueError('gate must be ccz, toffoli or fredkin')
    n = instance.get('n_qubits', 3)
    if isinstance(n, bool) or not isinstance(n, int) or n < 3 or n > 12:
        raise ValueError('n_qubits must be an integer in [3, 12]')
    qs = instance.get('qubits', [0, 1, 2])
    if not isinstance(qs, list) or len(qs) != 3:
        raise ValueError('qubits must be a list of three indices')
    for q in qs:
        if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
            raise ValueError('qubit index out of range')
    if len(set(qs)) != 3:
        raise ValueError('qubit indices must be distinct')
    a, b, c = qs
    qc = QuantumCircuit(n, name=gate)
    if gate == 'ccz':
        _ccz(qc, a, b, c)
    elif gate == 'toffoli':
        _toffoli(qc, a, b, c)
    else:
        qc.cx(c, b)
        _toffoli(qc, a, b, c)
        qc.cx(c, b)
    return qc
