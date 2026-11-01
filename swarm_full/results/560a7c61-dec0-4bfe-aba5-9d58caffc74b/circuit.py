from qiskit import QuantumCircuit


def _build_part(n, gates):
    if not isinstance(gates, list) or len(gates) > 500:
        raise ValueError('gate list must be a list with at most 500 gates')
    table = {'h': (1, 0), 'x': (1, 0), 'y': (1, 0), 'z': (1, 0), 's': (1, 0), 'sdg': (1, 0), 't': (1, 0), 'tdg': (1, 0), 'rx': (1, 1), 'ry': (1, 1), 'rz': (1, 1), 'p': (1, 1), 'cx': (2, 0), 'cz': (2, 0), 'swap': (2, 0), 'cp': (2, 1)}
    qc = QuantumCircuit(n)
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError('each gate must be an object')
        name = g.get('name')
        if not isinstance(name, str) or name not in table:
            raise ValueError('unsupported gate name')
        nq, npar = table[name]
        qs = g.get('qubits')
        ps = g.get('params', [])
        if not isinstance(qs, list) or len(qs) != nq:
            raise ValueError('wrong number of qubits for gate ' + name)
        if not isinstance(ps, list) or len(ps) != npar:
            raise ValueError('wrong number of params for gate ' + name)
        for q in qs:
            if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
                raise ValueError('qubit index out of range')
        if len(set(qs)) != len(qs):
            raise ValueError('qubits must be distinct')
        vals = []
        for p in ps:
            if isinstance(p, bool) or not isinstance(p, (int, float)):
                raise ValueError('params must be real numbers')
            f = float(p)
            if f != f or f in (float('inf'), float('-inf')):
                raise ValueError('params must be finite')
            vals.append(f)
        if name == 'h':
            qc.h(qs[0])
        elif name == 'x':
            qc.x(qs[0])
        elif name == 'y':
            qc.y(qs[0])
        elif name == 'z':
            qc.z(qs[0])
        elif name == 's':
            qc.s(qs[0])
        elif name == 'sdg':
            qc.sdg(qs[0])
        elif name == 't':
            qc.t(qs[0])
        elif name == 'tdg':
            qc.tdg(qs[0])
        elif name == 'rx':
            qc.rx(vals[0], qs[0])
        elif name == 'ry':
            qc.ry(vals[0], qs[0])
        elif name == 'rz':
            qc.rz(vals[0], qs[0])
        elif name == 'p':
            qc.p(vals[0], qs[0])
        elif name == 'cx':
            qc.cx(qs[0], qs[1])
        elif name == 'cz':
            qc.cz(qs[0], qs[1])
        elif name == 'swap':
            qc.swap(qs[0], qs[1])
        elif name == 'cp':
            qc.cp(vals[0], qs[0], qs[1])
    return qc


def build_circuit(instance):
    """eq_3: miter circuit V^dagger U. Apply U, then inverse of V, on qubits 0..n-1."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in [1, 12]')
    u = _build_part(n, instance.get('U'))
    v = _build_part(n, instance.get('V'))
    qc = QuantumCircuit(n)
    qc.compose(u, qubits=list(range(n)), inplace=True)
    qc.compose(v.inverse(), qubits=list(range(n)), inplace=True)
    return qc
