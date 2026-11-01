from qiskit import QuantumCircuit, QuantumRegister
import math


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + " must be a finite real number")
    return float(v)


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return v


def build_circuit(instance):
    """First-order Trotter circuit for H = A + B, A = J sum Z_i Z_{i+1}, B = h sum X_i.

    Instance keys: num_qubits (2..12), n (1..500), t (>0), J, h, periodic (bool, optional).
    Qubit i is spin site i. Operation is (exp(-iAt/n) exp(-iBt/n))^n with ideal gates.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for k in ("num_qubits", "n", "t", "J", "h"):
        if k not in instance:
            raise ValueError("missing key " + k)
    num = _int(instance["num_qubits"], "num_qubits", 2, 12)
    n = _int(instance["n"], "n", 1, 500)
    t = _real(instance["t"], "t")
    if t <= 0:
        raise ValueError("t must be positive")
    jc = _real(instance["J"], "J")
    hc = _real(instance["h"], "h")
    periodic = instance.get("periodic", False)
    if not isinstance(periodic, bool):
        raise ValueError("periodic must be a bool")
    if periodic and num < 3:
        raise ValueError("periodic requires num_qubits >= 3")
    bonds = [(i, i + 1) for i in range(num - 1)]
    if periodic:
        bonds.append((num - 1, 0))
    dt = t / n
    reg = QuantumRegister(num, "sys")
    qc = QuantumCircuit(reg)
    for _ in range(n):
        # exp(-i A dt): RZZ(theta) = exp(-i theta/2 ZZ), theta = 2 J dt
        for a, b in bonds:
            qc.rzz(2.0 * jc * dt, a, b)
        # exp(-i B dt): RX(theta) = exp(-i theta/2 X), theta = 2 h dt
        for q in range(num):
            qc.rx(2.0 * hc * dt, q)
    return qc
