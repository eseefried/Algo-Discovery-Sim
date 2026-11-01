import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + ' must be a real number')
    f = float(x)
    if not math.isfinite(f):
        raise ValueError(name + ' must be finite')
    return f


def _zeeman(qc, a1, a2, dt):
    # exp(-i dt (a1 Z1 + a2 Z2)); RZ(theta)=exp(-i theta Z/2)
    qc.rz(2.0 * a1 * dt, 0)
    qc.rz(2.0 * a2 * dt, 1)


def _exchange(qc, j, dt):
    # exp(-i dt J/4 (XX+YY+ZZ)); RPP(theta)=exp(-i theta PP/2) -> theta=J dt/2
    theta = j * dt / 2.0
    qc.rxx(theta, 0, 1)
    qc.ryy(theta, 0, 1)
    qc.rzz(theta, 0, 1)


def build_circuit(instance):
    """Trotterized U(T) for piecewise-constant B(t) (eq_1, eq_3). hbar=1.
    instance keys: g1, g2, j, mu_b (optional, default 1.0), trotter_steps (int per segment),
    segments: list of {"b": field amplitude, "duration": time >= 0}."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    g1 = _num(instance.get('g1'), 'g1')
    g2 = _num(instance.get('g2'), 'g2')
    j = _num(instance.get('j'), 'j')
    mu_b = _num(instance.get('mu_b', 1.0), 'mu_b')
    if g1 <= 0 or g2 <= 0 or mu_b <= 0:
        raise ValueError('g1, g2, mu_b must be positive')
    n = instance.get('trotter_steps')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 200:
        raise ValueError('trotter_steps must be an integer in [1, 200]')
    segs = instance.get('segments')
    if not isinstance(segs, list) or len(segs) < 1 or len(segs) > 64:
        raise ValueError('segments must be a list of 1..64 items')
    parsed = []
    for s in segs:
        if not isinstance(s, dict):
            raise ValueError('each segment must be a dict')
        b = _num(s.get('b'), 'b')
        d = _num(s.get('duration'), 'duration')
        if d < 0:
            raise ValueError('duration must be nonnegative')
        parsed.append((b, d))
    if n * len(parsed) > 4000:
        raise ValueError('circuit too large')
    q1 = QuantumRegister(1, 'q1')
    q2 = QuantumRegister(1, 'q2')
    qc = QuantumCircuit(q1, q2)
    for b, d in parsed:
        dt = d / n
        a1 = mu_b * b * g1 / 2.0
        a2 = mu_b * b * g2 / 2.0
        for _ in range(n):
            _zeeman(qc, a1, a2, dt / 2.0)
            _exchange(qc, j, dt)
            _zeeman(qc, a1, a2, dt / 2.0)
    return qc
