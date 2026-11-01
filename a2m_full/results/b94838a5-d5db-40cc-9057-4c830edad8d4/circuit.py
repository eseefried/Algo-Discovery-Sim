from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np


def _get_phases(instance, n):
    """Return N*N phases indexed as phases[j*N+k] (eq_1 reshape A_{jk})."""
    size = (1 << n) * (1 << n)
    if "phases" in instance:
        ph = instance["phases"]
        if not isinstance(ph, (list, tuple)) or len(ph) != size:
            raise ValueError("phases must be a list of length N^2")
        out = []
        for v in ph:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError("phases must be finite real numbers")
            out.append(float(v))
        return out
    seed = instance.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("provide 'phases' or a non-negative integer 'seed'")
    rng = np.random.default_rng(seed)
    return [float(v) for v in rng.uniform(0.0, 2.0 * math.pi, size)]


def build_circuit(instance):
    """Diagonal gate U of eq_1 on registers A (low n qubits, index j) and B (high n qubits, index k)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 6:
        raise ValueError("n must be an integer in 1..6 (2n <= 12 qubits)")
    N = 1 << n
    ph = _get_phases(instance, n)
    A = QuantumRegister(n, "A")
    B = QuantumRegister(n, "B")
    qc = QuantumCircuit(A, B)
    m = 2 * n
    size = 1 << m
    # phase table by computational basis index x = k*N + j (A is least significant)
    a = [0.0] * size
    for j in range(N):
        for k in range(N):
            a[k * N + j] = ph[j * N + k]
    # Moebius transform: phi(x) = sum_{S subset of x} a_S
    for i in range(m):
        bit = 1 << i
        for x in range(size):
            if x & bit:
                a[x] -= a[x ^ bit]
    qc.global_phase = a[0]
    for s in range(1, size):
        ang = math.remainder(a[s], 2.0 * math.pi)
        if abs(ang) < 1e-12:
            continue
        qs = [i for i in range(m) if (s >> i) & 1]
        if len(qs) == 1:
            qc.p(ang, qs[0])
        else:
            qc.mcp(ang, qs[:-1], qs[-1])
    return qc
