from qiskit import QuantumCircuit, QuantumRegister
import math


def _triples(n):
    out = []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                out.append((a, b, c))
    return out


def _parse_edges(raw, n):
    if not isinstance(raw, list):
        raise ValueError('edges must be a list of [u,v] pairs')
    edges = set()
    for e in raw:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        u, v = e
        if isinstance(u, bool) or isinstance(v, bool) or not isinstance(u, int) or not isinstance(v, int):
            raise ValueError('edge endpoints must be integers')
        if u < 0 or v < 0 or u >= n or v >= n or u == v:
            raise ValueError('invalid edge')
        edges.add((min(u, v), max(u, v)))
    return edges


def _oracle_edge_load(qc, m, tri, edges):
    # eq_4: query x_ab, x_bc, x_ac for each triple index t and write into ancillas m, m+1, m+2
    ctrls = list(range(m))
    for t, (a, b, c) in enumerate(tri):
        pairs = ((a, b), (b, c), (a, c))
        for j in range(3):
            if pairs[j] in edges:
                qc.mcx(ctrls, m + j, ctrl_state=t)


def _diffusion(qc, m):
    # eq_5: reflection about uniform superposition on the m-qubit index register
    for q in range(m):
        qc.h(q)
        qc.x(q)
    if m == 1:
        qc.z(0)
    else:
        qc.h(m - 1)
        qc.mcx(list(range(m - 1)), m - 1)
        qc.h(m - 1)
    for q in range(m):
        qc.x(q)
        qc.h(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 3 or n > 13:
        raise ValueError('n must be an integer in [3, 13]')
    k = instance.get('iterations')
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 64:
        raise ValueError('iterations must be an integer in [0, 64]')
    edges = _parse_edges(instance.get('edges'), n)
    num_tri = n * (n - 1) * (n - 2) // 6
    m = max(1, (num_tri - 1).bit_length())
    if m + 3 > 12:
        raise ValueError('too many qubits')
    tri = _triples(n)
    treg = QuantumRegister(m, 'triple')
    ereg = QuantumRegister(3, 'edge')
    qc = QuantumCircuit(treg, ereg)
    for _ in range(k):
        _oracle_edge_load(qc, m, tri, edges)
        qc.ccz(m, m + 1, m + 2)
        _oracle_edge_load(qc, m, tri, edges)
        _diffusion(qc, m)
    return qc
