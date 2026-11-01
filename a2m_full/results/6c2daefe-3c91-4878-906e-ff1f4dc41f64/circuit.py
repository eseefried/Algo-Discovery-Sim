import math
from qiskit import QuantumCircuit


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + " must be a real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def _angles(vals, count, name, clockwise_only):
    if not isinstance(vals, (list, tuple)) or len(vals) != count:
        raise ValueError(name + " must be a list of length " + str(count))
    out = []
    for v in vals:
        v = _num(v, name)
        if clockwise_only and not (0.0 <= v < 2.0 * math.pi):
            raise ValueError(name + " entries must lie in [0, 2pi) for clockwise-only")
        out.append(v)
    return out


def _append_rz(qc, angle):
    # Rz(a) segment about the z axis
    if angle != 0.0:
        qc.rz(angle, 0)


def _append_rn(qc, angle, theta):
    # eq_1: Rn(b) = Ry(theta) Rz(b) Ry(-theta); circuit order is the reverse of the matrix product
    if angle != 0.0:
        qc.ry(-theta, 0)
        qc.rz(angle, 0)
        qc.ry(theta, 0)


def build_circuit(instance):
    """Instance keys: theta in (0, pi/2], a (3 Rz angles), b (2 Rn angles),
    optional r > 0 (validated only), optional clockwise_only (bool)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    theta = _num(instance.get("theta"), "theta")
    if not (0.0 < theta <= math.pi / 2.0 + 1e-12):
        raise ValueError("theta must lie in (0, pi/2]")
    r = _num(instance.get("r", 1.0), "r")
    if r <= 0.0:
        raise ValueError("r must be positive")
    cw = instance.get("clockwise_only", False)
    if not isinstance(cw, bool):
        raise ValueError("clockwise_only must be a bool")
    a = _angles(instance.get("a"), 3, "a", cw)
    b = _angles(instance.get("b"), 2, "b", cw)
    qc = QuantumCircuit(1)
    # eq_2 in time order (first element applied first)
    _append_rz(qc, a[0])
    _append_rn(qc, b[0], theta)
    _append_rz(qc, a[1])
    _append_rn(qc, b[1], theta)
    _append_rz(qc, a[2])
    return qc
