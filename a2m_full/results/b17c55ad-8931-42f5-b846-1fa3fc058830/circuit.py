from qiskit import QuantumCircuit
import math


def _int_param(instance, key, default, lo, hi):
    v = instance.get(key, default)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(key + " must be an integer in [" + str(lo) + "," + str(hi) + "]")
    return v


def build_circuit(instance):
    """Coin-shift quantum particle walk U^T on a 2^n ring.
    Qubits 0..n-1: position (little-endian); qubit n: coin.
    U = S (Ry(2 theta) on coin); S = |0><0| x (+1 mod 2^n) + |1><1| x (-1 mod 2^n).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int_param(instance, "n", 5, 2, 11)
    steps = _int_param(instance, "steps", 1, 1, 64)
    theta = instance.get("theta", None)
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError("theta must be a finite real number")
    theta = float(theta)
    coin = n
    qc = QuantumCircuit(n + 1)
    for _ in range(steps):
        # coin rotation C(theta) = Ry(2 theta)
        qc.ry(2.0 * theta, coin)
        # coin = 0: increment j -> j+1 (mod 2^n); high bit first, then flip bit 0
        for k in range(n - 1, 0, -1):
            ctrls = [coin] + list(range(k))
            state = ((1 << k) - 1) << 1  # coin bit (LSB) = 0, lower position bits = 1
            qc.mcx(ctrls, k, ctrl_state=state)
        qc.cx(coin, 0, ctrl_state=0)
        # coin = 1: decrement j -> j-1 (mod 2^n), inverse sequence
        qc.cx(coin, 0, ctrl_state=1)
        for k in range(1, n):
            ctrls = [coin] + list(range(k))
            state = (((1 << k) - 1) << 1) | 1  # coin bit = 1, lower position bits = 1
            qc.mcx(ctrls, k, ctrl_state=state)
    return qc
