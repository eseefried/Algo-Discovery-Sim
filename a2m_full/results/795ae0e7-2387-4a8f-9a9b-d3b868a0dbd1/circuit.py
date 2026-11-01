from qiskit import QuantumCircuit
import math


def _get_int(instance, key, lo, hi, default):
    """Read an integer parameter in [lo, hi]; default None means required."""
    if key not in instance:
        if default is None:
            raise ValueError("missing required parameter: " + key)
        return default
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    if v < lo or v > hi:
        raise ValueError(key + " out of range")
    return v


def _mcz(qc, n):
    """Z on the all-ones state of n qubits: H(target), mcx, H(target)."""
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)


def _oracle(qc, n, w):
    """eq_1: O_w = I - 2|w><w| (qubit i is bit i of w)."""
    zeros = [i for i in range(n) if not (w >> i) & 1]
    for i in zeros:
        qc.x(i)
    _mcz(qc, n)
    for i in zeros:
        qc.x(i)


def _diffusion(qc, n):
    """eq_1: D = 2|s><s| - I = -(H^n X^n MCZ X^n H^n)."""
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.x(i)
    _mcz(qc, n)
    for i in range(n):
        qc.x(i)
    for i in range(n):
        qc.h(i)
    qc.global_phase = qc.global_phase + math.pi


def build_circuit(instance):
    """Grover operation (D O_w)^k on n qubits. Parameters: n (2..12, default 4), w (required, 0..2^n-1), iterations (0..100, default floor(pi/4*sqrt(2^n))), include_uniform_layer (bool, default False; prepends H^n)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _get_int(instance, "n", 2, 12, 4)
    w = _get_int(instance, "w", 0, 2 ** n - 1, None)
    k_star = int(math.floor(math.pi / 4.0 * math.sqrt(2 ** n)))  # eq_2
    k = _get_int(instance, "iterations", 0, 100, k_star)
    flag = instance.get("include_uniform_layer", False)
    if not isinstance(flag, bool):
        raise ValueError("include_uniform_layer must be a bool")
    qc = QuantumCircuit(n, name="grover")
    if flag:
        for i in range(n):
            qc.h(i)
    for _ in range(k):  # eq_3
        _oracle(qc, n, w)
        _diffusion(qc, n)
    return qc
