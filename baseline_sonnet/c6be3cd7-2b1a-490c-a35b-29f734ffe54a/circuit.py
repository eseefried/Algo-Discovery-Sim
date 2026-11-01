from qiskit import QuantumCircuit, QuantumRegister
import math


def _apply(qc, n, ops):
    """Append gate dicts {gate, qubits, params} to qc (eq_3 operands U, V)."""
    if not isinstance(ops, list) or len(ops) > 200:
        raise ValueError('gate list must be a list of at most 200 ops')
    table = {
        'h': (1, 0, qc.h), 'x': (1, 0, qc.x), 'y': (1, 0, qc.y),
        'z': (1, 0, qc.z), 's': (1, 0, qc.s), 'sdg': (1, 0, qc.sdg),
        't': (1, 0, qc.t), 'tdg': (1, 0, qc.tdg), 'sx': (1, 0, qc.sx),
        'rx': (1, 1, qc.rx), 'ry': (1, 1, qc.ry), 'rz': (1, 1, qc.rz),
        'p': (1, 1, qc.p), 'cx': (2, 0, qc.cx), 'cz': (2, 0, qc.cz),
        'swap': (2, 0, qc.swap), 'cp': (2, 1, qc.cp),
    }
    for op in ops:
        if not isinstance(op, dict):
            raise ValueError('each op must be an object')
        name = op.get('gate')
        qs = op.get('qubits')
        ps = op.get('params', [])
        if not isinstance(name, str) or name not in table:
            raise ValueError('unsupported gate')
        nq, np_, fn = table[name]
        if not isinstance(qs, list) or len(qs) != nq:
            raise ValueError('wrong number of qubits')
        for q in qs:
            if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
                raise ValueError('qubit index out of range')
        if len(set(qs)) != len(qs):
            raise ValueError('repeated qubit')
        if not isinstance(ps, list) or len(ps) != np_:
            raise ValueError('wrong number of params')
        vals = []
        for p in ps:
            if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p):
                raise ValueError('invalid parameter')
            vals.append(float(p))
        fn(*vals, *qs)


def build_circuit(instance):
    """Return the miter V^dagger U (eq_3): U first, then V inverse."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    uc = QuantumCircuit(n)
    vc = QuantumCircuit(n)
    _apply(uc, n, instance.get('u', []))
    _apply(vc, n, instance.get('v', []))
    qc = QuantumCircuit(QuantumRegister(n, 'q'))
    qc.compose(uc, inplace=True)
    qc.compose(vc.inverse(), inplace=True)
    return qc
