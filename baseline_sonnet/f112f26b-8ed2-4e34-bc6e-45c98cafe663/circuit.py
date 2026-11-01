from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Piecewise-constant single-qubit propagator for H=1/2[ux X + (uz+beta) Z] (eq_1).

    instance: {"controls": [[ux, uz, dt], ...], "beta": float (optional, quasi-static offset)}
    Segments are applied in list order (first entry acts first).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    segs = instance.get('controls')
    if not isinstance(segs, list) or len(segs) < 1 or len(segs) > 200:
        raise ValueError('controls must be a list with 1..200 segments')
    beta = instance.get('beta', 0.0)
    if isinstance(beta, bool) or not isinstance(beta, (int, float)) or not math.isfinite(beta):
        raise ValueError('beta must be a finite number')
    parsed = []
    for s in segs:
        if not isinstance(s, (list, tuple)) or len(s) != 3:
            raise ValueError('each segment must be [ux, uz, dt]')
        for v in s:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError('segment entries must be finite numbers')
        if s[2] < 0:
            raise ValueError('duration must be nonnegative')
        parsed.append((float(s[0]), float(s[1]), float(s[2])))
    q = QuantumRegister(1, 'q')
    qc = QuantumCircuit(q)
    for ux, uz, dt in parsed:
        hz = uz + float(beta)
        omega = math.sqrt(ux * ux + hz * hz)
        angle = dt * omega
        if omega == 0.0 or angle == 0.0:
            continue
        phi = math.atan2(ux, hz)
        # exp(-i angle/2 n.sigma) with n=(sin phi,0,cos phi) = Ry(phi) Rz(angle) Ry(-phi)
        qc.ry(-phi, q[0])
        qc.rz(angle, q[0])
        qc.ry(phi, q[0])
    return qc
