import math
from qiskit import QuantumCircuit, QuantumRegister


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _edge_query(qc, xs, ys, target, pairs):
    # eq_1: O_G|x,y,b> = |x,y,b xor A[x][y]> compiled for the instance graph
    controls = list(xs) + list(ys)
    for (a, b) in pairs:
        flips = []
        for i, q in enumerate(xs):
            if not (a >> i) & 1:
                flips.append(q)
        for i, q in enumerate(ys):
            if not (b >> i) & 1:
                flips.append(q)
        for q in flips:
            qc.x(q)
        qc.mcx(controls, target)
        for q in flips:
            qc.x(q)


def _phase_oracle(qc, U, V, W, E, pairs):
    # eq_2/eq_3: compute edge bits, phase flip if all three set, uncompute
    groups = [(U, V), (V, W), (U, W)]
    for j, (xs, ys) in enumerate(groups):
        _edge_query(qc, xs, ys, E[j], pairs)
    qc.ccz(E[0], E[1], E[2])
    for j, (xs, ys) in enumerate(groups):
        _edge_query(qc, xs, ys, E[j], pairs)


def _diffusion(qc, reg):
    # eq_4: reflection about uniform superposition (up to global phase)
    for q in reg:
        qc.h(q)
    for q in reg:
        qc.x(q)
    qc.h(reg[-1])
    qc.mcx(reg[:-1], reg[-1])
    qc.h(reg[-1])
    for q in reg:
        qc.x(q)
    for q in reg:
        qc.h(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not _is_int(n) or n < 3 or n > 8:
        raise ValueError('n must be an integer in 3..8')
    edges = instance.get('edges')
    if not isinstance(edges, (list, tuple)):
        raise ValueError('edges must be a list of [a,b] pairs')
    und = set()
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        a, b = e
        if not _is_int(a) or not _is_int(b) or a < 0 or b < 0 or a >= n or b >= n or a == b:
            raise ValueError('invalid edge')
        und.add((min(a, b), max(a, b)))
    pairs = []
    for (a, b) in sorted(und):
        pairs.append((a, b))
        pairs.append((b, a))
    m = max(1, (n - 1).bit_length())
    if 3 * m + 3 > 12:
        raise ValueError('too many qubits')
    adj = [[0] * n for _ in range(n)]
    for (a, b) in und:
        adj[a][b] = 1
        adj[b][a] = 1
    k = instance.get('iterations')
    if k is None:
        t = 0
        for a in range(n):
            for b in range(a + 1, n):
                for c in range(b + 1, n):
                    if adj[a][b] and adj[b][c] and adj[a][c]:
                        t += 1
        if t == 0:
            raise ValueError('no triangle: give iterations explicitly')
        M = 6 * t
        N = 2 ** (3 * m)
        theta = math.asin(math.sqrt(M / N))
        k = max(0, int(round(math.pi / (4.0 * theta) - 0.5)))
    if not _is_int(k) or k < 0 or k > 64:
        raise ValueError('iterations must be an integer in 0..64')
    ru = QuantumRegister(m, 'u')
    rv = QuantumRegister(m, 'v')
    rw = QuantumRegister(m, 'w')
    re = QuantumRegister(3, 'e')
    qc = QuantumCircuit(ru, rv, rw, re)
    U = list(ru)
    V = list(rv)
    W = list(rw)
    E = list(re)
    for _ in range(k):
        _phase_oracle(qc, U, V, W, E, pairs)
        _diffusion(qc, U + V + W)
    return qc
