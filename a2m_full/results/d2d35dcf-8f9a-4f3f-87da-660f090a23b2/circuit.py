import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + " must be a finite real number")
    return float(x)


def _pair(v, name):
    if not isinstance(v, (list, tuple)) or len(v) != 2:
        raise ValueError(name + " must have exactly two entries")
    return (_num(v[0], name), _num(v[1], name))


def build_circuit(instance):
    """Slice-product unitary of eq_3 on 2 qubits (q0 = electron 1, q1 = electron 2).

    instance = {"J_dt": J*dt, "slices": [{"zeeman": [phi1, phi2],
                "drive": [[theta1, phase1], [theta2, phase2]]}, ...]}
    Slice 1 is applied first. Within a slice the order is Zeeman, exchange, drive.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    j_dt = _num(instance.get("J_dt"), "J_dt")
    slices = instance.get("slices")
    if not isinstance(slices, (list, tuple)) or len(slices) < 1 or len(slices) > 100:
        raise ValueError("slices must be a list of 1..100 entries")
    parsed = []
    for s in slices:
        if not isinstance(s, dict):
            raise ValueError("each slice must be a dict")
        z1, z2 = _pair(s.get("zeeman"), "zeeman")
        d = s.get("drive")
        if not isinstance(d, (list, tuple)) or len(d) != 2:
            raise ValueError("drive must hold two (theta, phase) pairs")
        t1, p1 = _pair(d[0], "drive[0]")
        t2, p2 = _pair(d[1], "drive[1]")
        parsed.append((z1, z2, t1, p1, t2, p2))
    qr = QuantumRegister(2, "q")
    qc = QuantumCircuit(qr)
    for z1, z2, t1, p1, t2, p2 in parsed:
        # Zeeman: exp(-i phi Z/2) = Rz(phi), phi_j = g_j mu_B B_k dt
        qc.rz(z1, 0)
        qc.rz(z2, 1)
        # Exchange: exp(-i J dt/4 (XX+YY+ZZ)); the three terms commute, so this is exact
        qc.rxx(j_dt / 2.0, 0, 1)
        qc.ryy(j_dt / 2.0, 0, 1)
        qc.rzz(j_dt / 2.0, 0, 1)
        # Drive: exp(-i theta/2 (cos(phase) X + sin(phase) Y)) on each spin
        qc.r(t1, p1, 0)
        qc.r(t2, p2, 1)
    return qc
