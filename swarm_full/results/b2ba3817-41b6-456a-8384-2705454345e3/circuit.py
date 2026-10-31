import math
from qiskit import QuantumCircuit


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + ' must be a real number')
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    return x


def _int(x, name):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError(name + ' must be an integer')
    return x


def _oracle_phase(qc, n, marked, angle):
    # applies exp(+i*angle*|w><w|): phase e^{i angle} on basis state |marked>
    zeros = [q for q in range(n) if not (marked >> q) & 1]
    for q in zeros:
        qc.x(q)
    if n == 1:
        qc.p(angle, 0)
    else:
        qc.mcp(angle, list(range(n - 1)), n - 1)
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    """First-order Lie-Trotter approximation of exp(-i t H), H = gamma*(D-A) - |w><w|
    on the hypercube graph (eq_1). Qubit q is bit q of the vertex label."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance.get('n'), 'n')
    if n < 1 or n > 12:
        raise ValueError('n must be in 1..12')
    gamma = _num(instance.get('gamma'), 'gamma')
    t = _num(instance.get('time'), 'time')
    if gamma < 0 or t < 0:
        raise ValueError('gamma and time must be nonnegative')
    marked = _int(instance.get('marked'), 'marked')
    if marked < 0 or marked >= 2 ** n:
        raise ValueError('marked must be in 0..2^n-1')
    r = _int(instance.get('trotter_steps'), 'trotter_steps')
    if r < 1 or r > 2000:
        raise ValueError('trotter_steps must be in 1..2000')
    qc = QuantumCircuit(n, name='ctqw_search_hypercube')
    dt = t / r
    # graph term: gamma*(n*I - sum_i X_i); exp(-i dt gamma (-X)) = RX(-2 gamma dt)
    for _ in range(r):
        for q in range(n):
            qc.rx(-2.0 * gamma * dt, q)
        _oracle_phase(qc, n, marked, dt)
    # constant shift gamma*n*I contributes global phase exp(-i gamma n t)
    qc.global_phase = -gamma * n * t
    return qc
