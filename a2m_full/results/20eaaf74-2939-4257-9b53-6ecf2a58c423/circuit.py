from qiskit import QuantumCircuit, QuantumRegister
import math


def _real(x, name, strictly_positive):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + ' must be a real number')
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    if strictly_positive and x <= 0.0:
        raise ValueError(name + ' must be > 0')
    if (not strictly_positive) and x < 0.0:
        raise ValueError(name + ' must be >= 0')
    return x


def _integer(x, name, lo, hi):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError(name + ' must be an integer')
    if x < lo or x > hi:
        raise ValueError(name + ' must be in [' + str(lo) + ', ' + str(hi) + ']')
    return x


def _stage(qc, n, w, gamma, t, r):
    # eq_1/eq_4: (exp(i gamma A dt) exp(i |w><w| dt))^r, dt = t/r, A = sum_j X_j
    dt = t / r
    for _ in range(r):
        for j in range(n):
            # exp(i gamma dt X) = RX(-2 gamma dt)
            qc.rx(-2.0 * gamma * dt, j)
        for j in range(n):
            if not (w >> j) & 1:
                qc.x(j)
        # phase exp(i dt) on |1...1>, i.e. on |w> after conjugation
        qc.mcp(dt, list(range(n - 1)), n - 1)
        for j in range(n):
            if not (w >> j) & 1:
                qc.x(j)


def build_circuit(instance):
    """Two-stage Trotterized hypercube walk-search operation U = U2 U1 (eq_2).

    instance keys: n (3 or 4), w (marked vertex), gamma1, T1, gamma2, T2, r.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('n', 'w', 'gamma1', 'T1', 'gamma2', 'T2', 'r'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    n = _integer(instance['n'], 'n', 3, 4)
    w = _integer(instance['w'], 'w', 0, 2 ** n - 1)
    r = _integer(instance['r'], 'r', 1, 200)
    g1 = _real(instance['gamma1'], 'gamma1', True)
    g2 = _real(instance['gamma2'], 'gamma2', True)
    t1 = _real(instance['T1'], 'T1', False)
    t2 = _real(instance['T2'], 'T2', False)
    reg = QuantumRegister(n, 'v')
    qc = QuantumCircuit(reg, name='two_stage_walk_search')
    if t1 > 0.0:
        _stage(qc, n, w, g1, t1, r)
    if t2 > 0.0:
        _stage(qc, n, w, g2, t2, r)
    return qc
