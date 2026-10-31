import math
from qiskit import QuantumCircuit


def _get_int(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + " must be an integer")
    if value < lo or value > hi:
        raise ValueError(name + " must be in [" + str(lo) + ", " + str(hi) + "]")
    return value


def _apply_coin(qc, coin, theta):
    # C acts on coin qubit 0 (part of eq_1)
    if coin == "hadamard":
        qc.h(0)
    elif coin == "grover":
        # Grover coin for degree 2: 2|s><s| - I = X
        qc.x(0)
    else:
        qc.ry(theta, 0)


def _apply_shift(qc, n):
    # S (part of eq_1): coin 0 -> node+1 mod 2^n, coin 1 -> node-1 mod 2^n
    # node bit k is qubit 1+k
    qc.x(0)
    for k in reversed(range(n)):
        lower = [1 + j for j in range(k)]
        qc.mcx([0] + lower, 1 + k)
    qc.x(0)
    for k in reversed(range(n)):
        lower = [1 + j for j in range(k)]
        for q in lower:
            qc.x(q)
        qc.mcx([0] + lower, 1 + k)
        for q in lower:
            qc.x(q)


def build_circuit(instance):
    """Return t steps of the coined walk U = S (I (x) C) on the cycle C_{2^n}."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _get_int(instance.get("node_qubits"), "node_qubits", 2, 11)
    steps = _get_int(instance.get("steps"), "steps", 0, 256)
    coin = instance.get("coin", "hadamard")
    if coin not in ("hadamard", "grover", "rotation"):
        raise ValueError("coin must be hadamard, grover or rotation")
    theta = instance.get("theta", 0.0)
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError("theta must be a finite number")
    if n + 1 > 12:
        raise ValueError("too many qubits")
    qc = QuantumCircuit(n + 1, name="dtqw_cycle")
    for _ in range(steps):
        _apply_coin(qc, coin, float(theta))
        _apply_shift(qc, n)
    return qc
