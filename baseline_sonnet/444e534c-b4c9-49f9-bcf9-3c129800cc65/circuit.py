from qiskit import QuantumCircuit, QuantumRegister
import numpy as np


def _wht(v):
    """Unnormalized fast Walsh-Hadamard transform of a length-2^m vector."""
    v = np.array(v, dtype=float)
    h = 1
    while h < v.shape[0]:
        w = v.reshape(-1, 2, h)
        a = w[:, 0, :]
        b = w[:, 1, :]
        v = np.stack([a + b, a - b], axis=1).reshape(-1)
        h *= 2
    return v


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    if 'N' not in instance or 'phases' not in instance:
        raise ValueError('instance needs N and phases')
    N = instance['N']
    if isinstance(N, bool) or not isinstance(N, int):
        raise ValueError('N must be an integer')
    if N < 2 or (N & (N - 1)) != 0:
        raise ValueError('N must be a power of two >= 2')
    n = N.bit_length() - 1
    if 2 * n > 12:
        raise ValueError('at most 12 qubits allowed (N <= 64)')
    try:
        ph = np.asarray(instance['phases'], dtype=float)
    except (TypeError, ValueError):
        raise ValueError('phases must be real numbers')
    if ph.shape == (N, N):
        ph = ph.reshape(-1)
    elif ph.shape != (N * N,):
        raise ValueError('phases must have shape (N,N) or (N*N,)')
    if not np.all(np.isfinite(ph)):
        raise ValueError('phases must be finite')
    return n, ph


def build_circuit(instance):
    """Diagonal gate U = sum_{jk} exp(i phi_jk)|j><j| x |k><k|.

    Diagonal index x = j*N + k (row-major, eq_1): qubits 0..n-1 hold k (register B),
    qubits n..2n-1 hold j (register A).
    phi(x) = sum_S a_S (-1)^{x.S}, a_S = WHT(phi)[S]/N^2; exp(i a_S Z_S) is a parity RZ.
    """
    n, ph = _parse(instance)
    M = ph.shape[0]
    coeffs = _wht(ph) / M
    kreg = QuantumRegister(n, 'B_k')
    jreg = QuantumRegister(n, 'A_j')
    qc = QuantumCircuit(kreg, jreg)
    nq = 2 * n
    qc.global_phase = float(coeffs[0])
    for S in range(1, M):
        a = float(coeffs[S])
        if abs(a) < 1e-13:
            continue
        qs = [i for i in range(nq) if (S >> i) & 1]
        t = qs[-1]
        for q in qs[:-1]:
            qc.cx(q, t)
        qc.rz(-2.0 * a, t)
        for q in reversed(qs[:-1]):
            qc.cx(q, t)
    return qc
