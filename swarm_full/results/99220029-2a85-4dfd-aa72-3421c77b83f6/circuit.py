import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + " must be a finite real number")
    return float(x)


def _int(x, name, lo, hi):
    if isinstance(x, bool) or not isinstance(x, int) or x < lo or x > hi:
        raise ValueError(name + " must be an integer in [%d, %d]" % (lo, hi))
    return x


def _local(qc, eps_eff, dt):
    # exp(-i dt e (1-Z)/2) = exp(-i dt e/2) * RZ(-e dt)
    for j, e in enumerate(eps_eff):
        qc.rz(-e * dt, j)
        qc.global_phase += -e * dt / 2.0


def _pairs(qc, pairs, G, dt):
    # exp(-i dt * (-G/2)(XX+YY)) = RXX(-G dt) RYY(-G dt); XX and YY commute on a pair
    for (j, k) in pairs:
        qc.rxx(-G * dt, j, k)
        qc.ryy(-G * dt, j, k)


def build_circuit(instance):
    """Trotterized exp(-i H t), H = sum_j eps_j*2*n_j - G sum_{j,k} b_j^dag b_k, hard-core pairs b=sigma^-."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int(instance.get("n_levels"), "n_levels", 1, 12)
    eps = instance.get("epsilon")
    if not isinstance(eps, (list, tuple)) or len(eps) != n:
        raise ValueError("epsilon must be a list of length n_levels")
    eps = [_num(e, "epsilon") for e in eps]
    G = _num(instance.get("G"), "G")
    t = _num(instance.get("time"), "time")
    steps = _int(instance.get("steps"), "steps", 1, 200)
    order = _int(instance.get("order"), "order", 1, 2)
    # single-particle energy per pair-occupation: each pair has 2 fermions (2*eps_j), plus j=k term -G
    eps_eff = [2.0 * e - G for e in eps]
    pairs = [(j, k) for j in range(n) for k in range(j + 1, n)]
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    dt = t / steps
    for _ in range(steps):
        if order == 1:
            _local(qc, eps_eff, dt)
            _pairs(qc, pairs, G, dt)
        else:
            _local(qc, eps_eff, dt / 2.0)
            _pairs(qc, pairs, G, dt / 2.0)
            _pairs(qc, pairs[::-1], G, dt / 2.0)
            _local(qc, eps_eff, dt / 2.0)
    return qc
