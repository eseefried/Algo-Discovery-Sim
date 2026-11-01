import math
from qiskit import QuantumCircuit


def _num(x, name):
    try:
        v = float(x)
    except (TypeError, ValueError):
        raise ValueError(name + " must be a real number")
    if not math.isfinite(v):
        raise ValueError(name + " must be finite")
    return v


def build_circuit(instance):
    """Piecewise-constant singlet-triplet-style qubit sequence (eq_1).

    U = prod_{k=N..1} exp[-i tau_k ( J_k (1+eps) Z/2 + (h0+delta_h) X/2 )]
    Segment k=1 is applied first. Each segment is an exact rotation about the
    axis (h, 0, J) by angle tau*sqrt(h^2+J^2), realised as Ry(phi) Rz(theta) Ry(-phi)
    with phi = atan2(h, J).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    h0 = _num(instance.get("h0"), "h0")
    dh = _num(instance.get("delta_h", 0.0), "delta_h")
    eps = _num(instance.get("epsilon", 0.0), "epsilon")
    js = instance.get("J")
    taus = instance.get("tau")
    if not isinstance(js, (list, tuple)) or not isinstance(taus, (list, tuple)):
        raise ValueError("J and tau must be lists")
    n = len(js)
    if n < 1 or n > 256 or len(taus) != n:
        raise ValueError("J and tau must have equal length between 1 and 256")
    jmax = instance.get("J_max")
    if jmax is not None:
        jmax = _num(jmax, "J_max")
        if jmax < 0:
            raise ValueError("J_max must be nonnegative")
    tmin = _num(instance.get("tau_min", 0.0), "tau_min")
    if tmin < 0:
        raise ValueError("tau_min must be nonnegative")
    jv = []
    tv = []
    for k in range(n):
        j = _num(js[k], "J[k]")
        t = _num(taus[k], "tau[k]")
        if t < tmin or t < 0:
            raise ValueError("tau[k] below minimum or negative")
        if jmax is not None and abs(j) > jmax:
            raise ValueError("|J[k]| exceeds J_max")
        jv.append(j)
        tv.append(t)
    qc = QuantumCircuit(1, name="dc_gate")
    h = h0 + dh
    for k in range(n):
        j = jv[k] * (1.0 + eps)
        w = math.hypot(j, h)
        if w == 0.0 or tv[k] == 0.0:
            continue
        theta = tv[k] * w
        phi = math.atan2(h, j)
        qc.ry(-phi, 0)
        qc.rz(theta, 0)
        qc.ry(phi, 0)
    return qc
