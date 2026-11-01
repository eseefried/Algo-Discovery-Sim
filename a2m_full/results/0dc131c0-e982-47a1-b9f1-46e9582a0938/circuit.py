from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    depth = instance.get('depth')
    x = instance.get('x')
    tail = instance.get('tail_length')
    steps = instance.get('steps')
    if not _is_int(depth) or depth < 1 or depth > 3:
        raise ValueError('depth must be an integer in 1..3')
    if not isinstance(x, list) or len(x) != 2 ** depth:
        raise ValueError('x must be a list of length 2**depth')
    for b in x:
        if not _is_int(b) or b not in (0, 1):
            raise ValueError('x entries must be 0 or 1')
    if not _is_int(tail) or tail < 1 or tail > 32:
        raise ValueError('tail_length must be an integer in 1..32')
    if not _is_int(steps) or steps < 0 or steps > 40:
        raise ValueError('steps must be an integer in 0..40')
    return depth, x, tail, steps


def _bits(v, n):
    return [(v >> k) & 1 for k in range(n)]


def _pattern_x(qc, controls, values, target):
    # X on target when controls match the given bit values (self-inverse)
    for q, v in zip(controls, values):
        if v == 0:
            qc.x(q)
    qc.mcx(list(controls), target)
    for q, v in zip(controls, values):
        if v == 0:
            qc.x(q)


def _swap_states(qc, qubits, a_bits, b_bits):
    # exchange two computational basis states of the listed qubits
    n = len(qubits)
    diff = [k for k in range(n) if a_bits[k] != b_bits[k]]
    p = diff[0]
    rest = diff[1:]
    for k in rest:
        qc.cx(qubits[p], qubits[k])
    ctrl = []
    vals = []
    for k in range(n):
        if k == p:
            continue
        ctrl.append(qubits[k])
        vals.append(a_bits[k] ^ (a_bits[p] if k in rest else 0))
    _pattern_x(qc, ctrl, vals, qubits[p])
    for k in rest:
        qc.cx(qubits[p], qubits[k])


def _flag(qc, vq, anc, verts):
    # toggle anc on vertices in verts (apply twice to uncompute)
    for v in verts:
        _pattern_x(qc, vq, _bits(v, len(vq)), anc)


def _edges(depth, tail):
    m = 2 ** (depth + 1) - 1
    internal = 2 ** depth - 1
    edges = []
    for v in range(internal):
        edges.append(((v, 1), (2 * v + 1, 0)))
        edges.append(((v, 2), (2 * v + 2, 0)))
    edges.append(((0, 0), (m, 1)))
    for j in range(tail - 1):
        edges.append(((m + j, 0), (m + j + 1, 1)))
    return edges


def _step(qc, vq, cq, anc, depth, x, tail):
    nv = len(vq)
    m = 2 ** (depth + 1) - 1
    internal = 2 ** depth - 1
    alpha = 2.0 * math.asin(1.0 / math.sqrt(3.0))
    # eq_2: one leaf phase oracle call, (-1)^{x_i} on leaf i
    for i, b in enumerate(x):
        if b == 1:
            lb = _bits(internal + i, nv)
            _pattern_x(qc, vq, lb, anc)
            qc.z(anc)
            _pattern_x(qc, vq, lb, anc)
    # eq_3: Grover coin 2|phi><phi|-I on degree-3 vertices (internal nodes and root)
    _flag(qc, vq, anc, range(internal))
    qc.ch(cq[1], cq[0], ctrl_state=0)
    qc.ry(-alpha, cq[1])
    qc.z(anc)
    qc.x(cq[0])
    qc.x(cq[1])
    qc.mcp(math.pi, [anc, cq[0]], cq[1])
    qc.x(cq[0])
    qc.x(cq[1])
    qc.ry(alpha, cq[1])
    qc.ch(cq[1], cq[0], ctrl_state=0)
    _flag(qc, vq, anc, range(internal))
    # degree-2 tail vertices: coin swaps slots 0 and 1
    if tail > 1:
        _flag(qc, vq, anc, range(m, m + tail - 1))
        qc.x(cq[1])
        qc.ccx(anc, cq[1], cq[0])
        qc.x(cq[1])
        _flag(qc, vq, anc, range(m, m + tail - 1))
    # degree-1 vertices (leaves, tail end): identity coin
    # flip-flop shift along tree/tail edges
    qubits = list(vq) + list(cq)
    for (v, c), (u, d) in _edges(depth, tail):
        _swap_states(qc, qubits, _bits(v, nv) + _bits(c, 2), _bits(u, nv) + _bits(d, 2))


def build_circuit(instance):
    depth, x, tail, steps = _validate(instance)
    total_vertices = 2 ** (depth + 1) - 1 + tail
    nv = max(2, (total_vertices - 1).bit_length())
    if nv + 3 > 12:
        raise ValueError('too many qubits')
    vreg = QuantumRegister(nv, 'vertex')
    creg = QuantumRegister(2, 'coin')
    areg = QuantumRegister(1, 'anc')
    qc = QuantumCircuit(vreg, creg, areg)
    vq = list(vreg)
    cq = list(creg)
    for _ in range(steps):
        _step(qc, vq, cq, areg[0], depth, x, tail)
    return qc
