from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _angles(values, name):
    if not isinstance(values, (list, tuple)) or len(values) < 1 or len(values) > 20:
        raise ValueError(name + ' must be a list of 1..20 reals')
    out = []
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(name + ' entries must be finite reals')
        out.append(float(v))
    return out


def build_circuit(instance):
    """QAOA operation for MaxCut: prod_{l=1..p} exp(-i beta_l B) exp(-i gamma_l C).
    C = sum_{(u,v) in E} (1 - Z_u Z_v)/2 (eq_1), B = sum_j X_j (eq_4).
    The |+>^n input state is NOT prepared here (runner prepares inputs)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    raw_edges = instance.get('edges')
    if not isinstance(raw_edges, (list, tuple)) or len(raw_edges) < 1 or len(raw_edges) > 66:
        raise ValueError('edges must be a non-empty list of vertex pairs')
    edges = []
    seen = set()
    for e in raw_edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        u, v = e
        if not _is_int(u) or not _is_int(v) or u < 0 or v < 0 or u >= n or v >= n:
            raise ValueError('edge endpoint out of range')
        if u == v:
            raise ValueError('self loops not allowed')
        key = (min(u, v), max(u, v))
        if key in seen:
            raise ValueError('duplicate edge')
        seen.add(key)
        edges.append(key)
    gammas = _angles(instance.get('gammas'), 'gammas')
    betas = _angles(instance.get('betas'), 'betas')
    if len(gammas) != len(betas):
        raise ValueError('gammas and betas must have equal length p')
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    m = len(edges)
    for g, b in zip(gammas, betas):
        # exp(-i g (1-ZZ)/2) = exp(-i g/2) * exp(+i g ZZ/2) = global phase * RZZ(-g)
        for (u, v) in edges:
            qc.rzz(-g, u, v)
        qc.global_phase += -g * m / 2.0
        # exp(-i b X) = RX(2 b)
        for j in range(n):
            qc.rx(2.0 * b, j)
    return qc
