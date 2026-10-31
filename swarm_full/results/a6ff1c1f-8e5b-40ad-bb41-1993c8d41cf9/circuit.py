from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RXGate
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_vertex_qubits')
    m = instance.get('num_phase_qubits')
    steps = instance.get('trotter_steps')
    t = instance.get('time')
    edges = instance.get('edges')
    if not (_is_int(n) and _is_int(m) and _is_int(steps)):
        raise ValueError('num_vertex_qubits, num_phase_qubits, trotter_steps must be integers')
    if n < 1 or m < 1 or n + m > 12:
        raise ValueError('need n>=1, m>=1 and n+m<=12')
    if steps < 1 or steps > 64:
        raise ValueError('trotter_steps must be in 1..64')
    if not _is_num(t):
        raise ValueError('time must be a finite real number')
    if not isinstance(edges, list) or len(edges) < 1 or len(edges) > 64:
        raise ValueError('edges must be a list of 1..64 entries')
    clean = []
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 3:
            raise ValueError('each edge must be [a, b, weight]')
        a, b, w = e
        if not (_is_int(a) and _is_int(b)):
            raise ValueError('edge endpoints must be integers')
        if a < 0 or b < 0 or a >= 2 ** n or b >= 2 ** n or a == b:
            raise ValueError('invalid edge endpoints')
        if not _is_num(w):
            raise ValueError('edge weight must be a finite real number')
        clean.append((a, b, float(w)))
    return n, m, steps, float(t), clean


def _check_bipartite(edges):
    adj = {}
    for a, b, _ in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    color = {}
    for s in adj:
        if s in color:
            continue
        color[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    stack.append(v)
                elif color[v] == color[u]:
                    raise ValueError('graph is not bipartite')


def _controlled_edge(qc, ctrl, vq, a, b, theta):
    # Implements controlled exp(i*phi*(|a><b|+|b><a|)) with theta=-2*phi (RX(theta)=exp(-i theta X/2)).
    n = len(vq)
    diff = a ^ b
    bits = [i for i in range(n) if (diff >> i) & 1]
    p = bits[0]
    others = bits[1:]
    for d in others:
        qc.cx(vq[p], vq[d])
    ap = (a >> p) & 1
    flips = []
    controls = [ctrl]
    for q in range(n):
        if q == p:
            continue
        bit = (a >> q) & 1
        if q in others:
            bit ^= ap
        if bit == 0:
            flips.append(vq[q])
        controls.append(vq[q])
    for f in flips:
        qc.x(f)
    qc.append(RXGate(theta).control(len(controls)), controls + [vq[p]])
    for f in flips:
        qc.x(f)
    for d in reversed(others):
        qc.cx(vq[p], vq[d])


def build_circuit(instance):
    """Trotterized phase estimation of exp(iAt) for a weighted bipartite graph.

    Qubits: vertex register 0..n-1 (little endian vertex label), phase register n..n+m-1.
    Phase qubit k controls U^(2^k); output integer j on the phase register ~ eigenphase j/2^m of U.
    """
    n, m, steps, t, edges = _parse(instance)
    _check_bipartite(edges)
    vreg = QuantumRegister(n, 'vertex')
    preg = QuantumRegister(m, 'phase')
    qc = QuantumCircuit(vreg, preg)
    vq = list(range(n))
    pq = list(range(n, n + m))
    for q in pq:
        qc.h(q)
    for k in range(m):
        tau = t * (2 ** k) / steps
        for _ in range(steps):
            for a, b, w in edges:
                _controlled_edge(qc, pq[k], vq, a, b, -2.0 * w * tau)
    qc.append(QFTGate(m).inverse(), pq)
    return qc
