from qiskit import QuantumCircuit, QuantumRegister
import math


def _angles(x, name):
    if not isinstance(x, (list, tuple)) or len(x) == 0 or len(x) > 50:
        raise ValueError(name + ' must be a nonempty list of at most 50 reals')
    out = []
    for v in x:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(name + ' entries must be finite reals')
        out.append(float(v))
    return out


def build_circuit(instance):
    """QAOA MaxCut operation: prod_k U(B,beta_k) U(C,gamma_k). Input |+>^n is prepared by the runner."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in [1, 12]')
    raw_edges = instance.get('edges')
    if not isinstance(raw_edges, (list, tuple)) or len(raw_edges) > 66:
        raise ValueError('edges must be a list of at most 66 pairs')
    edges = []
    seen = set()
    for e in raw_edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        a, b = e
        if isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, int) or not isinstance(b, int):
            raise ValueError('edge endpoints must be integers')
        if a < 0 or b < 0 or a >= n or b >= n or a == b:
            raise ValueError('invalid edge endpoints')
        key = (min(a, b), max(a, b))
        if key in seen:
            raise ValueError('duplicate edge')
        seen.add(key)
        edges.append(key)
    gammas = _angles(instance.get('gammas'), 'gammas')
    betas = _angles(instance.get('betas'), 'betas')
    if len(gammas) != len(betas):
        raise ValueError('gammas and betas must have equal length p >= 1')
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    for g, b in zip(gammas, betas):
        # U(C,g) = prod_edges exp(-i g (1 - Z_j Z_k)/2) = exp(-i g/2) * exp(+i g/2 Z_j Z_k) = exp(-i g/2) * RZZ(-g)
        for (j, k) in edges:
            qc.rzz(-g, j, k)
            qc.global_phase -= g / 2.0
        # U(B,b) = prod_j exp(-i b X_j) = RX(2b)
        for j in range(n):
            qc.rx(2.0 * b, j)
    return qc
