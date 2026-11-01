from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def build_circuit(instance):
    """Toffoli: |a,b,c> -> |a,b,c xor (a and b)> (eq_1).

    instance keys: num_qubits (3..12, default 3), controls (two distinct indices,
    default [0, 1]), target (index, default 2), decompose (bool, default False).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('num_qubits', 3), 'num_qubits')
    if n < 3 or n > 12:
        raise ValueError('num_qubits must be in [3, 12]')
    controls = instance.get('controls', [0, 1])
    if not isinstance(controls, (list, tuple)) or len(controls) != 2:
        raise ValueError('controls must contain exactly two indices')
    a = _as_int(controls[0], 'control')
    b = _as_int(controls[1], 'control')
    t = _as_int(instance.get('target', 2), 'target')
    for q in (a, b, t):
        if q < 0 or q >= n:
            raise ValueError('qubit index out of range')
    if len({a, b, t}) != 3:
        raise ValueError('controls and target must be distinct')
    decompose = instance.get('decompose', False)
    if not isinstance(decompose, bool):
        raise ValueError('decompose must be a bool')
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    if not decompose:
        qc.ccx(a, b, t)
    else:
        qc.h(t)
        qc.cx(b, t)
        qc.tdg(t)
        qc.cx(a, t)
        qc.t(t)
        qc.cx(b, t)
        qc.tdg(t)
        qc.cx(a, t)
        qc.t(b)
        qc.t(t)
        qc.h(t)
        qc.cx(a, b)
        qc.t(a)
        qc.tdg(b)
        qc.cx(a, b)
    return qc
