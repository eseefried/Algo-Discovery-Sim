from qiskit import QuantumCircuit
import math


def _ccz(qc, a, b, c):
    # eq_1: CCZ = (-1)^{abc} via conventional 5 two-qubit gate circuit
    qc.cp(math.pi / 2, b, c)
    qc.cx(a, b)
    qc.cp(-math.pi / 2, b, c)
    qc.cx(a, b)
    qc.cp(math.pi / 2, a, c)


def _ccx(qc, a, b, c):
    qc.h(c)
    _ccz(qc, a, b, c)
    qc.h(c)


def build_circuit(instance):
    """Build CCZ or Fredkin on a register of num_qubits qubits.

    instance keys: gate ('ccz' or 'fredkin'), num_qubits (3..12, default 3),
    qubits (three distinct indices, default [0,1,2]). For fredkin the order is
    [control, target1, target2].
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gate = instance.get('gate')
    if gate not in ('ccz', 'fredkin'):
        raise ValueError("gate must be 'ccz' or 'fredkin'")
    n = instance.get('num_qubits', 3)
    if isinstance(n, bool) or not isinstance(n, int) or n < 3 or n > 12:
        raise ValueError('num_qubits must be an integer in [3, 12]')
    qubits = instance.get('qubits', [0, 1, 2])
    if not isinstance(qubits, list) or len(qubits) != 3:
        raise ValueError('qubits must be a list of three indices')
    for q in qubits:
        if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
            raise ValueError('qubit index out of range')
    if len(set(qubits)) != 3:
        raise ValueError('qubit indices must be distinct')
    a, b, c = qubits
    qc = QuantumCircuit(n)
    if gate == 'ccz':
        _ccz(qc, a, b, c)
    else:
        # eq_2: controlled swap of b and c conditioned on a
        qc.cx(c, b)
        _ccx(qc, a, b, c)
        qc.cx(c, b)
    return qc
