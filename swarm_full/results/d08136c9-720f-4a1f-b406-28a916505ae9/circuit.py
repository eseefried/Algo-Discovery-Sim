import math
from qiskit import QuantumCircuit, QuantumRegister


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    shape = instance.get('shape')
    if not isinstance(shape, list) or len(shape) < 2 or len(shape) > 12:
        raise ValueError('shape must be a list of >=2 positive ints (k>=2)')
    n = 1
    for s in shape:
        if isinstance(s, bool) or not isinstance(s, int) or s < 1:
            raise ValueError('shape entries must be positive ints')
        n *= s
        if 2 * n > 12:
            raise ValueError('total qubits 2*prod(shape) must be <= 12')
    op = instance.get('operation', 'x')
    if op not in ('x', 'z', 'p'):
        raise ValueError("operation must be 'x', 'z' or 'p'")
    angle = instance.get('angle', 0.0)
    if isinstance(angle, bool) or not isinstance(angle, (int, float)):
        raise ValueError('angle must be a number')
    angle = float(angle)
    if not math.isfinite(angle):
        raise ValueError('angle must be finite')
    return shape, n, op, angle


def _coords(idx, shape):
    out = []
    for s in shape:
        out.append(idx % s)
        idx //= s
    return out


def _spread_edges(shape, n):
    # Spanning tree: parent of a site lowers its first nonzero coordinate by 1.
    # Edges are ordered by Manhattan distance from the origin (eq_2 depth structure).
    strides = []
    st = 1
    for s in shape:
        strides.append(st)
        st *= s
    maxd = 0
    for s in shape:
        maxd += s - 1
    edges = []
    for d in range(1, maxd + 1):
        for idx in range(1, n):
            c = _coords(idx, shape)
            if sum(c) != d:
                continue
            j = 0
            while c[j] == 0:
                j += 1
            edges.append((idx - strides[j], idx))
    return edges


def build_circuit(instance):
    shape, n, op, angle = _parse(instance)
    t = QuantumRegister(n, 't')
    c = QuantumRegister(n, 'c')
    qc = QuantumCircuit(t, c)
    edges = _spread_edges(shape, n)
    # spread control copy over the grid with nearest-neighbor CNOTs (eq_2)
    for p, ch in edges:
        qc.cx(c[p], c[ch])
    # local controlled operation on each site's target (fanout, eq_3)
    for idx in range(n):
        if op == 'x':
            qc.cx(c[idx], t[idx])
        elif op == 'z':
            qc.cz(c[idx], t[idx])
        else:
            qc.cp(angle, c[idx], t[idx])
    # uncompute the copies
    for p, ch in reversed(edges):
        qc.cx(c[p], c[ch])
    return qc
