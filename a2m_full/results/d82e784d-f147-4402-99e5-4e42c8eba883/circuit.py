import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError('angles must be finite real numbers')
    return float(x)


def _vertex(v, n):
    if isinstance(v, bool) or not isinstance(v, int) or v < 0 or v >= n:
        raise ValueError('edge endpoint out of range')
    return v


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 12:
        raise ValueError('n must be an integer in [2, 12]')
    raw = instance.get('edges')
    if not isinstance(raw, (list, tuple)) or len(raw) == 0:
        raise ValueError('edges must be a non-empty list')
    seen = set()
    edges = []
    for e in raw:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        a = _vertex(e[0], n)
        b = _vertex(e[1], n)
        if a == b:
            raise ValueError('self loops not allowed')
        key = (min(a, b), max(a, b))
        if key in seen:
            raise ValueError('duplicate edge')
        seen.add(key)
        edges.append(key)
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    if len(set(deg)) != 1:
        raise ValueError('graph must be regular')
    gammas = instance.get('gammas')
    betas = instance.get('betas')
    if not isinstance(gammas, (list, tuple)) or not isinstance(betas, (list, tuple)):
        raise ValueError('gammas and betas must be lists')
    if len(gammas) != len(betas) or len(gammas) < 1 or len(gammas) > 3:
        raise ValueError('need 1..3 layers with equal numbers of gammas and betas')
    gammas = [_num(g) for g in gammas]
    betas = [_num(b) for b in betas]
    return n, edges, gammas, betas


def build_circuit(instance):
    """QAOA MaxCut operator prod_{l=p..1} exp(-i beta_l B) exp(-i gamma_l C).

    The |+>^n input is prepared by the runner; no Hadamards are applied here.
    """
    n, edges, gammas, betas = _parse(instance)
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    for g, b in zip(gammas, betas):
        # eq_1/eq_3: exp(-i g (1-Z_i Z_j)/2) = exp(-i g/2) * RZZ(-g)_{ij}
        for a, c in edges:
            qc.rzz(-g, qr[a], qr[c])
        qc.global_phase = qc.global_phase - g * len(edges) / 2.0
        # eq_2/eq_3: mixer exp(-i b X_i) = RX(2b)
        for i in range(n):
            qc.rx(2.0 * b, qr[i])
    return qc
