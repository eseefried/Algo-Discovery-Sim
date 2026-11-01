from qiskit import QuantumCircuit
import math


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be a finite real number')
    return float(x)


def _rotate(qc, axis, alpha, theta):
    # eq_1: R_k(alpha) = exp(-i alpha/2 n_k.sigma); n_1 = z, n_2 = (sin theta, 0, cos theta)
    if axis == 1:
        qc.rz(alpha, 0)
    else:
        # R_2(alpha) = Ry(theta) Rz(alpha) Ry(-theta); circuit order is rightmost factor first
        qc.ry(-theta, 0)
        qc.rz(alpha, 0)
        qc.ry(theta, 0)


def build_circuit(instance):
    """Instance keys: theta in (0,pi), angles (list of reals, alpha_1 applied first),
    first_axis (1 or 2), clockwise_only (bool; if true all angles must be >= 0)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    theta = _num(instance.get('theta'), 'theta')
    if not (0.0 < theta < math.pi):
        raise ValueError('theta must lie strictly in (0, pi)')
    angles = instance.get('angles')
    if not isinstance(angles, (list, tuple)) or len(angles) > 64:
        raise ValueError('angles must be a list of at most 64 reals')
    alphas = [_num(a, 'angle') for a in angles]
    first_axis = instance.get('first_axis')
    if isinstance(first_axis, bool) or first_axis not in (1, 2):
        raise ValueError('first_axis must be 1 or 2')
    cw = instance.get('clockwise_only')
    if not isinstance(cw, bool):
        raise ValueError('clockwise_only must be a bool')
    if cw and any(a < 0.0 for a in alphas):
        raise ValueError('clockwise-only sequences need nonnegative angles')
    qc = QuantumCircuit(1, name='two_axis_su2')
    # eq_2: segment 1 acts first (rightmost factor); axes alternate
    for j, a in enumerate(alphas):
        axis = first_axis if j % 2 == 0 else 3 - first_axis
        _rotate(qc, axis, a, theta)
    return qc
