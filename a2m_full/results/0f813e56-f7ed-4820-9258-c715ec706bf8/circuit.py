from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, YGate, ZGate, SGate, SdgGate, TGate, TdgGate, CXGate, CZGate, SwapGate, RXGate, RYGate, RZGate, PhaseGate
import math


def _make(name, ps):
    one = {'h': HGate, 'x': XGate, 'y': YGate, 'z': ZGate, 's': SGate, 'sdg': SdgGate, 't': TGate, 'tdg': TdgGate}
    two = {'cx': CXGate, 'cz': CZGate, 'swap': SwapGate}
    rot = {'rx': RXGate, 'ry': RYGate, 'rz': RZGate, 'p': PhaseGate}
    if name in one and len(ps) == 0:
        return one[name](), 1
    if name in two and len(ps) == 0:
        return two[name](), 2
    if name in rot and len(ps) == 1:
        return rot[name](float(ps[0])), 1
    raise ValueError('unsupported gate or wrong parameter count: %r' % (name,))


def _parse(ops, n):
    if not isinstance(ops, list) or len(ops) > 200:
        raise ValueError('gate list must be a list of at most 200 gates')
    out = []
    for op in ops:
        if not isinstance(op, dict):
            raise ValueError('each gate must be an object')
        name = op.get('name')
        qs = op.get('qubits', [])
        ps = op.get('params', [])
        if not isinstance(name, str) or not isinstance(qs, list) or not isinstance(ps, list):
            raise ValueError('malformed gate entry')
        for p in ps:
            if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p):
                raise ValueError('parameters must be finite numbers')
        if name == 'gphase':
            if len(ps) != 1 or len(qs) != 0:
                raise ValueError('gphase takes one parameter and no qubits')
            out.append((name, None, [], float(ps[0])))
            continue
        gate, nq = _make(name, ps)
        if len(qs) != nq or len(set(qs)) != nq:
            raise ValueError('wrong number of distinct qubits for gate')
        for q in qs:
            if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
                raise ValueError('qubit index out of range')
        out.append((name, gate, list(qs), 0.0))
    return out


def _apply(qc, op, anc, inverse):
    name, gate, qs, angle = op
    if name == 'gphase':
        qc.p(-angle if inverse else angle, anc)
        return
    g = gate.inverse() if inverse else gate
    qc.append(g.control(1), [anc] + qs)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 11:
        raise ValueError('n must be an integer in 1..11')
    readout = instance.get('readout', 'X')
    if readout not in ('X', 'Y'):
        raise ValueError('readout must be X or Y')
    u_ops = _parse(instance.get('U', []), n)
    v_ops = _parse(instance.get('V', []), n)
    anc = n
    qc = QuantumCircuit(n + 1)
    qc.h(anc)
    for op in u_ops:
        _apply(qc, op, anc, False)
    for op in reversed(v_ops):
        _apply(qc, op, anc, True)
    if readout == 'Y':
        qc.sdg(anc)
    qc.h(anc)
    return qc
