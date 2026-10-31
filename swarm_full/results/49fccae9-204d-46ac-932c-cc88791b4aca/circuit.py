import math
from qiskit import QuantumCircuit, QuantumRegister


def _flt(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + " must be a finite number")
    return float(v)


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return v


def _mc(qc, controls, target):
    if len(controls) == 1:
        qc.cx(controls[0], target)
    else:
        qc.mcx(controls, target)


def build_circuit(instance):
    """Circuit for (I_x (x) C_f) U^t, U = S (I (x) C), on a 2^m-site cycle.
    Qubit 0 = coin; qubits 1..m = position (little-endian).
    Shift: coin 0 -> x+1, coin 1 -> x-1 (mod 2^m)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    m = _int(instance.get("position_qubits"), "position_qubits", 1, 11)
    t = _int(instance.get("steps"), "steps", 0, 256)
    name = instance.get("coin", "hadamard")
    if name not in ("identity", "flip", "hadamard", "biased"):
        raise ValueError("coin must be identity, flip, hadamard or biased")
    theta = _flt(instance.get("coin_theta", 0.0), "coin_theta")
    fc = instance.get("final_coin", [0, 0, 0])
    if not isinstance(fc, (list, tuple)) or len(fc) != 3:
        raise ValueError("final_coin must be [theta, phi, lam]")
    fa = [_flt(x, "final_coin entry") for x in fc]
    coin = QuantumRegister(1, "coin")
    pos = QuantumRegister(m, "pos")
    qc = QuantumCircuit(coin, pos)
    c = coin[0]
    p = list(pos)
    for _ in range(t):
        # coin operator C (eq_1)
        if name == "flip":
            qc.x(c)
        elif name == "hadamard":
            qc.h(c)
        elif name == "biased":
            # [[cos th, sin th],[sin th, -cos th]] = RY(2 th) Z
            qc.z(c)
            qc.ry(2.0 * theta, c)
        # conditional shift S (eq_1): increment if coin=0
        qc.x(c)
        for i in range(m - 1, -1, -1):
            _mc(qc, [c] + p[:i], p[i])
        qc.x(c)
        # decrement if coin=1 (inverse of the increment ladder)
        for i in range(m):
            _mc(qc, [c] + p[:i], p[i])
    # final state-independent coin C_f (eq_2 operator)
    qc.u(fa[0], fa[1], fa[2], c)
    return qc
