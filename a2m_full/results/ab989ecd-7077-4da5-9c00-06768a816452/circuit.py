from qiskit import QuantumCircuit
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def build_circuit(instance):
    """Trotterized AQC evolution U_M...U_1, U_k = exp(-i(1-s_k)H_B dt) exp(-i s_k H_P dt).
    H_B=-sum X_i. H_P=sum over clauses (x_a+x_b+x_c-1)^2 = 1 - (Za+Zb+Zc)/2 + (ZaZb+ZaZc+ZbZc)/2 per clause.
    Qubit i is variable x_i (bit i of the basis index). Input state must be prepared by the runner."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not _is_int(n) or n < 3 or n > 12:
        raise ValueError('n must be an integer in [3, 12]')
    clauses = instance.get('clauses')
    if not isinstance(clauses, list) or len(clauses) < 1 or len(clauses) > 50:
        raise ValueError('clauses must be a list of 1..50 triples')
    parsed = []
    for cl in clauses:
        if not isinstance(cl, (list, tuple)) or len(cl) != 3:
            raise ValueError('each clause must have 3 variable indices')
        if not all(_is_int(v) and 0 <= v < n for v in cl):
            raise ValueError('clause index out of range')
        if len(set(cl)) != 3:
            raise ValueError('clause indices must be distinct')
        parsed.append((cl[0], cl[1], cl[2]))
    M = instance.get('M')
    if not _is_int(M) or M < 1 or M > 200:
        raise ValueError('M must be an integer in [1, 200]')
    T = instance.get('T')
    if not _is_num(T) or T <= 0 or T > 1000:
        raise ValueError('T must be a positive finite number <= 1000')
    mode = instance.get('schedule', 'linear')
    if mode == 'linear':
        sched = [(k + 0.5) / M for k in range(M)]
    elif mode == 'explicit':
        sv = instance.get('s_values')
        if not isinstance(sv, list) or len(sv) != M:
            raise ValueError('s_values must be a list of length M')
        if not all(_is_num(v) and 0.0 <= v <= 1.0 for v in sv):
            raise ValueError('s_values must lie in [0, 1]')
        sched = [float(v) for v in sv]
    else:
        raise ValueError('schedule must be linear or explicit')
    h = [0.0] * n
    J = {}
    const = 0.0
    for a, b, c in parsed:
        const += 1.0
        for q in (a, b, c):
            h[q] -= 0.5
        for p in ((a, b), (a, c), (b, c)):
            key = (min(p), max(p))
            J[key] = J.get(key, 0.0) + 0.5
    qc = QuantumCircuit(n)
    dt = float(T) / M
    for sk in sched:
        th = sk * dt
        qc.global_phase = qc.global_phase - th * const
        for q in range(n):
            if h[q] != 0.0:
                qc.rz(2.0 * th * h[q], q)
        for key in sorted(J.keys()):
            if J[key] != 0.0:
                qc.rzz(2.0 * th * J[key], key[0], key[1])
        for q in range(n):
            qc.rx(-2.0 * (1.0 - sk) * dt, q)
    return qc
