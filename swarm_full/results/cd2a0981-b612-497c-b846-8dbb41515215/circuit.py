import math
from qiskit import QuantumCircuit


def _num(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(name + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(name + ' must be finite')
    return v


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(name + ' out of range')
    return v


def _mark_phase(qc, n, w, angle):
    # Applies exp(i*angle*|w><w|): phase e^{i angle} on basis state |w> only.
    zeros = [k for k in range(n) if not (w >> k) & 1]
    for k in zeros:
        qc.x(k)
    if n == 1:
        qc.p(angle, 0)
    else:
        qc.mcp(angle, list(range(n - 1)), n - 1)
    for k in zeros:
        qc.x(k)


def _mix(qc, n, theta):
    # exp(i*gamma*dt*sum_j(-X_j)) = prod_j RX(2*gamma*dt); theta is the RX angle
    for k in range(n):
        qc.rx(theta, k)


def build_circuit(instance):
    """Trotterized exp(-iHt), H=-gamma*L-|w><w|, L the n-cube Laplacian."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance.get('n'), 'n', 1, 12)
    w = _int(instance.get('marked'), 'marked', 0, 2 ** n - 1)
    gamma = _num(instance.get('gamma'), 'gamma')
    t = _num(instance.get('time'), 't')
    if gamma <= 0.0:
        raise ValueError('gamma must be positive')
    if t < 0.0:
        raise ValueError('time must be nonnegative')
    steps = _int(instance.get('steps'), 'steps', 1, 2000)
    order = _int(instance.get('order', 1), 'order', 1, 2)
    dt = t / steps
    qc = QuantumCircuit(n, name='hypercube_ctqw_search')
    # constant part of gamma*L: exp(i*gamma*t*n) global phase
    qc.global_phase += gamma * n * t
    for _ in range(steps):
        if order == 1:
            _mix(qc, n, 2.0 * gamma * dt)
            _mark_phase(qc, n, w, dt)
        else:
            _mix(qc, n, gamma * dt)
            _mark_phase(qc, n, w, dt)
            _mix(qc, n, gamma * dt)
    return qc
