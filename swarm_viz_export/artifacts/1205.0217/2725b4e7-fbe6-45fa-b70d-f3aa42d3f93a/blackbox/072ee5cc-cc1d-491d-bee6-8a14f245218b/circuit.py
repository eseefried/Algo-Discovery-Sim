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
    """Ideal piecewise-constant evolution, H_k=(J_k/2)Z+(h/2)X (eq_1, eq_2).

    instance: {"h": float>0, "J_max": float>0, "segments": [[J_k, tau_k], ...]}
    with 0<=J_k<=J_max, tau_k>=0, 1..64 segments.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    h = _num(instance.get("h"), "h")
    jmax = _num(instance.get("J_max"), "J_max")
    if h <= 0.0:
        raise ValueError("h must be positive")
    if jmax <= 0.0:
        raise ValueError("J_max must be positive")
    segs = instance.get("segments")
    if not isinstance(segs, (list, tuple)) or len(segs) < 1 or len(segs) > 64:
        raise ValueError("segments must be a list of 1..64 pairs")
    parsed = []
    for seg in segs:
        if not isinstance(seg, (list, tuple)) or len(seg) != 2:
            raise ValueError("each segment must be [J, tau]")
        j = _num(seg[0], "J")
        tau = _num(seg[1], "tau")
        if j < 0.0 or j > jmax:
            raise ValueError("J must lie in [0, J_max]")
        if tau < 0.0:
            raise ValueError("tau must be nonnegative")
        parsed.append((j, tau))
    qc = QuantumCircuit(1, name="st_piecewise")
    # eq_2: segments are applied in time order, so later segments multiply on the left
    for j, tau in parsed:
        omega = math.hypot(j, h)
        theta = omega * tau
        beta = math.atan2(h, j)  # Ry(beta) maps z axis to (h,0,J)/omega
        # exp(-i H tau) = Ry(beta) Rz(theta) Ry(-beta); H is traceless so no global phase
        qc.ry(-beta, 0)
        qc.rz(theta, 0)
        qc.ry(beta, 0)
    return qc
