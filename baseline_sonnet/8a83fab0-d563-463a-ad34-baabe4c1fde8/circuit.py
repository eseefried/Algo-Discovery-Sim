from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, XGate
import math


def _int_in_range(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, int) or value < lo or value > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return value


def build_circuit(instance):
    """Noisy hop (eq_2) along one hypercube edge of an n-qubit vertex register.

    Two-level unitary on vertices a=source and b=source^(1<<direction):
    M = X . RY(theta), theta = 2*asin(epsilon), so M = [[eps, s], [s, -eps]], s = sqrt(1-eps^2),
    in the basis (|a>, |b>). All other vertices are untouched.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int_in_range(instance.get("n_qubits"), "n_qubits", 1, 12)
    source = _int_in_range(instance.get("source"), "source", 0, 2 ** n - 1)
    d = _int_in_range(instance.get("direction"), "direction", 0, n - 1)
    eps = instance.get("epsilon")
    if isinstance(eps, bool) or not isinstance(eps, (int, float)):
        raise ValueError("epsilon must be a number in [0, 1]")
    eps = float(eps)
    if not math.isfinite(eps) or eps < 0.0 or eps > 1.0:
        raise ValueError("epsilon must be a number in [0, 1]")
    theta = 2.0 * math.asin(eps)

    qc = QuantumCircuit(n, name="noisy_hop")
    controls = [q for q in range(n) if q != d]
    flips = [q for q in controls if not (source >> q) & 1]
    # map the source vertex to the all-ones control pattern with target bit 0
    for q in flips:
        qc.x(q)
    if (source >> d) & 1:
        qc.x(d)
    # eq_2 core: M = X * RY(theta) on the target, controlled on the other bits
    if controls:
        k = len(controls)
        qc.append(RYGate(theta).control(k), controls + [d])
        qc.append(XGate().control(k), controls + [d])
    else:
        qc.ry(theta, d)
        qc.x(d)
    if (source >> d) & 1:
        qc.x(d)
    for q in flips:
        qc.x(q)
    return qc
