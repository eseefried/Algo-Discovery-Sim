import math
from qiskit import QuantumCircuit


def build_circuit(instance):
    """Return the 1-qubit circuit U(epsilon)^m with U = exp[-i pi(1+epsilon)/2 X].

    instance: {"epsilon": real with |epsilon| <= 1, "m": integer in [1, 1024]}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    eps = instance.get("epsilon")
    m = instance.get("m")
    if isinstance(eps, bool) or not isinstance(eps, (int, float)):
        raise ValueError("epsilon must be a real number")
    eps = float(eps)
    if not math.isfinite(eps) or abs(eps) > 1.0:
        raise ValueError("epsilon must be finite with |epsilon| <= 1")
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError("m must be an integer")
    if m < 1 or m > 1024:
        raise ValueError("m must be in [1, 1024]")
    # eq_1: RX(theta) = exp(-i theta X / 2) with theta = pi (1 + epsilon)
    theta = math.pi * (1.0 + eps)
    qc = QuantumCircuit(1, name="amp_err_pow_m")
    # eq_2: m repetitions of the identical coherent-error gate
    for _ in range(m):
        qc.rx(theta, 0)
    return qc
