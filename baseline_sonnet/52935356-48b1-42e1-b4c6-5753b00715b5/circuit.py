import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError('numeric value required')
    return float(x)


def _int(x):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError('integer required')
    return x


def build_circuit(instance):
    """Randomized-Trotter fast-signal-assisted AQC for EC3 (eq_1, eq_2, eq_3, eq_5).

    instance: n (3..12), clauses (list of distinct-index triples), T>0, N (1..200),
    signals: list of N entries [qubit, 'x'|'y'|'z', amplitude xi_k].
    Qubit i carries bit z_i of the clause labels. Input state is prepared by the runner.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = _int(instance.get('n'))
    if n < 3 or n > 12:
        raise ValueError('n must be in 3..12')
    T = _num(instance.get('T'))
    if T <= 0:
        raise ValueError('T must be positive')
    N = _int(instance.get('N'))
    if N < 1 or N > 200:
        raise ValueError('N must be in 1..200')
    raw = instance.get('clauses')
    if not isinstance(raw, list) or len(raw) == 0 or len(raw) > 40:
        raise ValueError('clauses must be a non-empty list')
    clauses = []
    for c in raw:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            raise ValueError('each clause needs 3 indices')
        t = tuple(_int(v) for v in c)
        if len(set(t)) != 3 or min(t) < 0 or max(t) >= n:
            raise ValueError('invalid clause indices')
        clauses.append(t)
    sig = instance.get('signals')
    if not isinstance(sig, list) or len(sig) != N:
        raise ValueError('signals must be a list of length N')
    parsed = []
    for e in sig:
        if not isinstance(e, (list, tuple)) or len(e) != 3:
            raise ValueError('signal entry must be [qubit, axis, amplitude]')
        j = _int(e[0])
        ax = e[1]
        if j < 0 or j >= n or ax not in ('x', 'y', 'z'):
            raise ValueError('invalid signal entry')
        parsed.append((j, ax, _num(e[2])))

    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q)
    dt = T / N
    for k in range(1, N + 1):
        s = k / N
        # driver exp(-i dt (1-s) H_B), H_B = -sum X_i  -> RX(-2 dt (1-s))
        for i in range(n):
            qc.rx(-2.0 * dt * (1.0 - s), q[i])
        # EC3 penalty (z_a+z_b+z_c-1)^2 = 1 - (Za+Zb+Zc)/2 + (ZaZb+ZaZc+ZbZc)/2
        for (a, b, c) in clauses:
            for v in (a, b, c):
                qc.rz(-dt * s, q[v])
            qc.rzz(dt * s, q[a], q[b])
            qc.rzz(dt * s, q[a], q[c])
            qc.rzz(dt * s, q[b], q[c])
        # fast signal exp(-i dt xi sigma_j) = R_sigma(2 dt xi)
        j, ax, xi = parsed[k - 1]
        ang = 2.0 * dt * xi
        if ax == 'x':
            qc.rx(ang, q[j])
        elif ax == 'y':
            qc.ry(ang, q[j])
        else:
            qc.rz(ang, q[j])
    return qc
