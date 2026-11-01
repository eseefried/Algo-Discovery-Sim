import math
from qiskit import QuantumCircuit


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + " must be a real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def build_circuit(instance):
    """Alternating two-axis SU(2) rotation sequence on one qubit.

    instance: {"alpha": float in (0, pi), "segments": [{"axis": 1|2, "angle": float}, ...],
               "allow_counterclockwise": bool (optional, default True)}
    Segments are listed in time order (first applied first).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    alpha = _num(instance.get("alpha"), "alpha")
    if not (0.0 < alpha < math.pi):
        raise ValueError("alpha must lie in (0, pi)")
    segs = instance.get("segments")
    if not isinstance(segs, list) or len(segs) < 1 or len(segs) > 50:
        raise ValueError("segments must be a list of 1..50 entries")
    ccw = instance.get("allow_counterclockwise", True)
    if not isinstance(ccw, bool):
        raise ValueError("allow_counterclockwise must be bool")
    qc = QuantumCircuit(1, name="two_axis_sequence")
    prev = None
    for s in segs:
        if not isinstance(s, dict):
            raise ValueError("each segment must be a dict")
        axis = s.get("axis")
        if isinstance(axis, bool) or axis not in (1, 2):
            raise ValueError("axis must be 1 or 2")
        theta = _num(s.get("angle"), "angle")
        if axis == prev:
            raise ValueError("consecutive segments must use alternating axes")
        if (not ccw) and theta < 0.0:
            raise ValueError("negative angle not allowed when clockwise-only")
        prev = axis
        if axis == 1:
            # eq_1 with n1 = z: R_1(theta) = exp(-i theta Z / 2)
            qc.rz(theta, 0)
        else:
            # eq_1 with n2 = Ry(alpha) z: R_2(theta) = Ry(alpha) Rz(theta) Ry(-alpha)
            qc.ry(-alpha, 0)
            qc.rz(theta, 0)
            qc.ry(alpha, 0)
    return qc
