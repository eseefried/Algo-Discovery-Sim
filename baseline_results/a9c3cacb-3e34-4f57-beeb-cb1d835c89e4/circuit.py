"""Baseline quantum Viterbi stage (Durr-Hoyer threshold oracle + Grover iterate)
for ML decoding of the rate-1/2, memory-1 convolutional code with generators
(1, 1+D) over a hard-decision BSC.

Registers (qubit 0 = least significant):
  path   : N qubits, path[i] holds information bit x_{i+1} (x_0 = 0 fixed).
  metric : m = ceil(log2(2N+1)) qubits, little-endian unsigned Hamming metric d(x).
The metric register is uncomputed inside every oracle call and returns to |0...0>.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("N", None)
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("N must be a positive integer")
    received = instance.get("received", None)
    if not isinstance(received, list) or len(received) != n:
        raise ValueError("received must be a list of N frames")
    frames = []
    for fr in received:
        if not isinstance(fr, list) or len(fr) != 2:
            raise ValueError("each received frame must be a pair of bits")
        for b in fr:
            if not isinstance(b, int) or isinstance(b, bool) or b not in (0, 1):
                raise ValueError("received bits must be 0 or 1")
        frames.append((int(fr[0]), int(fr[1])))
    threshold = instance.get("threshold", None)
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise ValueError("threshold must be an integer")
    if threshold < 0 or threshold > 2 * n + 1:
        raise ValueError("threshold must lie in 0..2N+1")
    iterations = instance.get("iterations", None)
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 0:
        raise ValueError("iterations must be a non-negative integer")
    prepare = instance.get("prepare_superposition", True)
    if not isinstance(prepare, bool):
        raise ValueError("prepare_superposition must be a bool")
    m = max(1, math.ceil(math.log2(2 * n + 1)))
    if n + m > MAX_QUBITS:
        raise ValueError("instance needs %d qubits, cap is %d" % (n + m, MAX_QUBITS))
    return n, m, frames, threshold, iterations, prepare


def _controlled_increment(qc, control, metric):
    """metric <- metric + 1 (mod 2^m) when `control` is |1>; little-endian."""
    m = len(metric)
    for j in range(m - 1, -1, -1):
        controls = [control] + [metric[k] for k in range(j)]
        qc.mcx(controls, metric[j])


def _add_code_bit(qc, code_qubit, metric, y_bit):
    """Add wt(code_bit XOR y_bit) to the metric register (eq_3 summand)."""
    if y_bit == 1:
        qc.x(code_qubit)
    _controlled_increment(qc, code_qubit, metric)
    if y_bit == 1:
        qc.x(code_qubit)


def _metric_circuit(n, m, frames):
    """U_d |x>|0> = |x>|d(x)>  (eq_4 second form) using the encoder eq_2 and
    the Hamming metric eq_3 for generators (1, 1+D)."""
    path = QuantumRegister(n, "path")
    metric = QuantumRegister(m, "metric")
    qc = QuantumCircuit(path, metric)
    met = [metric[k] for k in range(m)]
    for i in range(n):
        y1, y2 = frames[i]
        # eq_2: c^(1)_t = x_t
        _add_code_bit(qc, path[i], met, y1)
        # eq_2: c^(2)_t = x_t XOR x_{t-1}, with x_0 = 0
        if i == 0:
            _add_code_bit(qc, path[i], met, y2)
        else:
            qc.cx(path[i - 1], path[i])
            _add_code_bit(qc, path[i], met, y2)
            qc.cx(path[i - 1], path[i])
    return qc


def _threshold_phase(qc, metric, threshold):
    """C_{<T}: multiply |d> by -1 for every d < T (eq_5 comparator phase)."""
    m = len(metric)
    for v in range(min(threshold, 2 ** m)):
        zeros = [metric[k] for k in range(m) if ((v >> k) & 1) == 0]
        for q in zeros:
            qc.x(q)
        if m == 1:
            qc.z(metric[0])
        else:
            qc.mcp(math.pi, [metric[k] for k in range(m - 1)], metric[m - 1])
        for q in zeros:
            qc.x(q)


def _diffusion(qc, path):
    """Reflection 2|psi_0><psi_0| - I about the uniform superposition (eq_6)."""
    n = len(path)
    for q in path:
        qc.h(q)
    for q in path:
        qc.x(q)
    if n == 1:
        qc.z(path[0])
    else:
        qc.mcp(math.pi, [path[k] for k in range(n - 1)], path[n - 1])
    for q in path:
        qc.x(q)
    for q in path:
        qc.h(q)


def build_circuit(instance):
    """Build H^{N} (optional, eq_1) followed by `iterations` Grover iterates
    G_T = (2|psi_0><psi_0| - I) U_d^dag C_{<T} U_d (eq_5, eq_6)."""
    n, m, frames, threshold, iterations, prepare = _validate(instance)
    path = QuantumRegister(n, "path")
    metric = QuantumRegister(m, "metric")
    qc = QuantumCircuit(path, metric)
    path_list = [path[k] for k in range(n)]
    metric_list = [metric[k] for k in range(m)]
    if prepare:
        # eq_1: tensor-product superposition over all legal paths
        for q in path_list:
            qc.h(q)
    u_d = _metric_circuit(n, m, frames)
    u_d_inv = u_d.inverse()
    all_qubits = path_list + metric_list
    for _ in range(iterations):
        # eq_5: O_T = U_d^dag (I x C_{<T}) U_d
        qc.compose(u_d, qubits=all_qubits, inplace=True)
        _threshold_phase(qc, metric_list, threshold)
        qc.compose(u_d_inv, qubits=all_qubits, inplace=True)
        # eq_6: Grover iterate completed by the diffusion reflection
        _diffusion(qc, path_list)
    return qc
