"""Grover-search baseline for triangle finding (scoped construction eq_4-eq_6).

The circuit implements k Grover iterates G = D * U_f on a triple-index register,
where U_f is realized by three compiled adjacency-matrix queries (eq_1) into
edge-bit ancillas, an AND-to-phase step (eq_2), and uncomputation.  The runner is
expected to prepare the uniform superposition on the triple-index register and
|000> on the edge bits.  This is NOT the paper's O~(n^{5/4}) algorithm; it is the
O(n^{3/2}) textbook baseline chosen as the minimal executable construction.

Qubit layout (qubit 0 = least significant bit):
  qubits 0..m-1      triple_index, bit i of the triple index t (m = ceil(log2 C(n,3)))
  qubits m..m+2      edge_bits: A[u,v], A[v,w], A[u,w] of triple t (ancillas, start in |0>)
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
NUM_EDGE_BITS = 3


def _check_int(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _parse_instance(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object")
    if "n" not in instance or "edges" not in instance:
        raise ValueError("instance requires keys 'n' and 'edges'")
    n = _check_int(instance["n"], "n", 4)
    edges = instance["edges"]
    if not isinstance(edges, (list, tuple)):
        raise ValueError("edges must be a list of pairs")
    adj = set()
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError("each edge must be a pair [u, v]")
        u = _check_int(e[0], "vertex", 0)
        v = _check_int(e[1], "vertex", 0)
        if u >= n or v >= n or u == v:
            raise ValueError("edge endpoints must be distinct vertices in range(n)")
        key = (min(u, v), max(u, v))
        if key in adj:
            raise ValueError("duplicate edge")
        adj.add(key)
    iterations = None
    if "iterations" in instance and instance["iterations"] is not None:
        iterations = _check_int(instance["iterations"], "iterations", 0)
    return n, adj, iterations


def _triples(n):
    # eq_6 ordering: lexicographic triples u < v < w, index t = position in this list.
    out = []
    for u in range(n):
        for v in range(u + 1, n):
            for w in range(v + 1, n):
                out.append((u, v, w))
    return out


def _pair(trip, j):
    u, v, w = trip
    if j == 0:
        return (u, v)
    if j == 1:
        return (v, w)
    return (u, w)


def _load_edge_bit(qc, idx, target, triples, adj, j):
    # eq_1: compiled query O_G |p_j(t)>|b> -> |p_j(t)>|b xor A[p_j(t)]>, controlled on |t>.
    # For each triple index t whose j-th pair is an edge, flip the target bit.
    # Index values t >= C(n,3) (padding of the register) never flip anything (f = 0).
    m = len(idx)
    for t, trip in enumerate(triples):
        if _pair(trip, j) not in adj:
            continue
        zeros = [idx[i] for i in range(m) if ((t >> i) & 1) == 0]
        for q in zeros:
            qc.x(q)
        qc.mcx(list(idx), target)
        for q in zeros:
            qc.x(q)


def _apply_oracle(qc, idx, edge, triples, adj):
    # eq_4 phase oracle U_f built from 3 queries (eq_1), AND-to-phase (eq_2), 3 uncompute queries.
    for j in range(NUM_EDGE_BITS):
        _load_edge_bit(qc, idx, edge[j], triples, adj, j)
    # eq_2: f = A[u,v] AND A[v,w] AND A[u,w]; apply phase (-1)^f via a CCZ on the edge bits.
    qc.mcp(math.pi, [edge[0], edge[1]], edge[2])
    for j in reversed(range(NUM_EDGE_BITS)):
        _load_edge_bit(qc, idx, edge[j], triples, adj, j)


def _apply_diffusion(qc, idx):
    # eq_4: 2|psi0><psi0| - I on triple_index (implemented up to a global phase of -1),
    # with |psi0> = H^{(x)m}|0> the uniform superposition over all 2^m index values.
    for q in idx:
        qc.h(q)
    for q in idx:
        qc.x(q)
    qc.mcp(math.pi, list(idx[:-1]), idx[-1])
    for q in idx:
        qc.x(q)
    for q in idx:
        qc.h(q)


def build_circuit(instance):
    """Return k Grover iterates for triangle search on the given graph instance.

    instance keys: 'n' (int >= 4), 'edges' (list of [u, v]), optional 'iterations'
    (int >= 0).  If 'iterations' is omitted it is set from eq_5 with N replaced by
    the padded search-space size 2^m and M = number of triangles (must be >= 1).
    """
    n, adj, iterations = _parse_instance(instance)
    triples = _triples(n)
    big_n = len(triples)
    m = (big_n - 1).bit_length()
    if m + NUM_EDGE_BITS > MAX_QUBITS:
        raise ValueError(
            f"instance needs {m + NUM_EDGE_BITS} qubits, exceeding the cap of {MAX_QUBITS}"
        )
    if iterations is None:
        # eq_5: k = floor((pi/4) * sqrt(N'/M)) with N' = 2^m (padded register).
        marked = 0
        for trip in triples:
            if _pair(trip, 0) in adj and _pair(trip, 1) in adj and _pair(trip, 2) in adj:
                marked += 1
        if marked == 0:
            raise ValueError("iterations must be supplied when the graph has no triangle")
        iterations = int(math.floor((math.pi / 4.0) * math.sqrt((2 ** m) / marked)))
    idx = QuantumRegister(m, "triple_index")
    edge = QuantumRegister(NUM_EDGE_BITS, "edge_bits")
    qc = QuantumCircuit(idx, edge, name="grover_triangle")
    for _ in range(iterations):
        _apply_oracle(qc, idx, edge, triples, adj)
        _apply_diffusion(qc, idx)
    return qc
