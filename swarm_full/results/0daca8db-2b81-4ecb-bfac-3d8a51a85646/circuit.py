from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Unrolled qubit-probe weak-measurement loop with fixed system pulses.

    instance: {"n_steps": int 1..11, "phi": float (= g*dt),
               "pulses": optional list of n_steps [theta, phi, lam] U-gate angles}
    Qubit 0 = system S; qubit k (1..n) = probe of iteration k (runner prepares |0>).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n_steps")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 11:
        raise ValueError("n_steps must be an integer in 1..11")
    phi = instance.get("phi")
    if isinstance(phi, bool) or not isinstance(phi, (int, float)) or not math.isfinite(phi):
        raise ValueError("phi must be a finite real number")
    pulses = instance.get("pulses")
    if pulses is None:
        pulses = [[0.0, 0.0, 0.0] for _ in range(n)]
    if not isinstance(pulses, list) or len(pulses) != n:
        raise ValueError("pulses must be a list of length n_steps")
    clean = []
    for p in pulses:
        if not isinstance(p, (list, tuple)) or len(p) != 3:
            raise ValueError("each pulse needs three angles")
        row = []
        for a in p:
            if isinstance(a, bool) or not isinstance(a, (int, float)) or not math.isfinite(a):
                raise ValueError("pulse angles must be finite reals")
            row.append(float(a))
        clean.append(row)

    sys_reg = QuantumRegister(1, "S")
    probes = QuantumRegister(n, "P")
    qc = QuantumCircuit(sys_reg, probes)
    for k in range(n):
        # eq_2: exp(-i*phi*|0><0|_S (x) Y_P) = controlled-on-|0> RY(2*phi)
        qc.x(0)
        qc.cry(2.0 * float(phi), 0, 1 + k)
        qc.x(0)
        # fixed system pulse (replaces outcome-dependent feedback)
        qc.u(clean[k][0], clean[k][1], clean[k][2], 0)
    return qc
