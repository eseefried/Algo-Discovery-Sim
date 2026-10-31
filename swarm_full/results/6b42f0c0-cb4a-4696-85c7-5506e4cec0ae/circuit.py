from qiskit import QuantumCircuit, QuantumRegister
import numpy as np
import math


def build_circuit(instance):
    """Diagonal unitary U on 2n qubits with phases phi_x, x = i*N + j, N = 2**n.
    Qubits 0..n-1 hold j (column index of A), qubits n..2n-1 hold i (row index of A),
    so A[i, j] = exp(i*phi[i*N + j]) is the row-major reshaping of the diagonal.
    Synthesis: phi(x) = sum_S w_S (-1)^(S.x), exp(i*phi(x)) is a product of parity phases."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 6:
        raise ValueError('n must be an integer in 1..6')
    m = 2 * n
    M = 1 << m
    ph = instance.get('phases')
    if ph is None:
        seed = instance.get('seed')
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError('provide phases or a non-negative integer seed')
        phi = np.random.default_rng(seed).uniform(0.0, 2.0 * math.pi, M)
    else:
        if not isinstance(ph, list) or len(ph) != M:
            raise ValueError('phases must be a list of length 4**n')
        try:
            phi = np.array([float(v) for v in ph], dtype=float)
        except (TypeError, ValueError):
            raise ValueError('phases must be real numbers')
        if not np.all(np.isfinite(phi)):
            raise ValueError('phases must be finite')
    w = phi.copy()
    h = 1
    while h < M:
        for s in range(0, M, 2 * h):
            a = w[s:s + h].copy()
            b = w[s + h:s + 2 * h].copy()
            w[s:s + h] = a + b
            w[s + h:s + 2 * h] = a - b
        h *= 2
    w = w / M
    reg = QuantumRegister(m, 'q')
    qc = QuantumCircuit(reg)
    qc.global_phase = float(phi[0])
    for S in range(1, M):
        theta = -2.0 * float(w[S])
        if abs(theta) < 1e-15:
            continue
        bits = [k for k in range(m) if (S >> k) & 1]
        t = bits[0]
        others = bits[1:]
        for c in others:
            qc.cx(c, t)
        qc.p(theta, t)
        for c in reversed(others):
            qc.cx(c, t)
    return qc
