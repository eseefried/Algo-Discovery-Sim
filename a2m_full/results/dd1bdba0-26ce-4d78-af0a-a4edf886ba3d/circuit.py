import math
from qiskit import QuantumCircuit, QuantumRegister


def _angle(op, key):
    v = op.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError('angle ' + key + ' must be a finite real number')
    return float(v)


def _qubits(op, k, n):
    q = op.get('qubits')
    if not isinstance(q, list) or len(q) != k:
        raise ValueError('qubits must be a list of length ' + str(k))
    for x in q:
        if isinstance(x, bool) or not isinstance(x, int) or x < 0 or x >= n:
            raise ValueError('qubit index out of range')
    if len(set(q)) != k:
        raise ValueError('qubit indices must be distinct')
    return q


def build_circuit(instance):
    """Apply an ordered list of gates {rx, rz, cp, swap} to n qubits."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    ops = instance.get('ops')
    if not isinstance(ops, list) or len(ops) > 2000:
        raise ValueError('ops must be a list of at most 2000 operations')
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    for op in ops:
        if not isinstance(op, dict):
            raise ValueError('each op must be an object')
        g = op.get('gate')
        if g == 'rz':
            # eq_1: Rz(theta) = exp(-i theta Z/2)
            (a,) = _qubits(op, 1, n)
            qc.rz(_angle(op, 'theta'), a)
        elif g == 'rx':
            # eq_2: Rx(theta) = exp(-i theta X/2)
            (a,) = _qubits(op, 1, n)
            qc.rx(_angle(op, 'theta'), a)
        elif g == 'cp':
            # eq_3: CP(phi) = diag(1,1,1,exp(i phi))
            a, b = _qubits(op, 2, n)
            qc.cp(_angle(op, 'phi'), a, b)
        elif g == 'swap':
            # eq_4: SWAP|a,b> = |b,a>
            a, b = _qubits(op, 2, n)
            qc.swap(a, b)
        else:
            raise ValueError('unknown gate')
    return qc
