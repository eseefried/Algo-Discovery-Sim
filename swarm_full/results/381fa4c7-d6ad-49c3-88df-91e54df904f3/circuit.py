from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate
import math
import numpy as np


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _energy(k, n, m, W, b, d):
    # eq_1: E(v,h) = -sum_i b_i v_i - sum_j d_j h_j - sum_ij W_ij v_i h_j
    v = [(k >> i) & 1 for i in range(n)]
    h = [(k >> (n + j)) & 1 for j in range(m)]
    e = 0.0
    for i in range(n):
        e -= float(b[i]) * v[i]
    for j in range(m):
        e -= float(d[j]) * h[j]
    for i in range(n):
        for j in range(m):
            e -= float(W[i][j]) * v[i] * h[j]
    return e


def build_circuit(instance):
    """Qubits: vis 0..n-1, hid n..n+m-1, ancilla n+m."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_visible')
    m = instance.get('n_hidden')
    if not _is_int(n) or not _is_int(m) or n < 1 or m < 1:
        raise ValueError('n_visible and n_hidden must be positive integers')
    if n + m > 8 or n + m + 1 > 12:
        raise ValueError('n_visible + n_hidden must be at most 8')
    try:
        W = np.array(instance.get('W'), dtype=float)
        b = np.array(instance.get('b'), dtype=float)
        d = np.array(instance.get('d'), dtype=float)
    except Exception:
        raise ValueError('W, b, d must be numeric arrays')
    if W.shape != (n, m) or b.shape != (n,) or d.shape != (m,):
        raise ValueError('shape mismatch: W is n x m, b length n, d length m')
    if not (np.all(np.isfinite(W)) and np.all(np.isfinite(b)) and np.all(np.isfinite(d))):
        raise ValueError('parameters must be finite')
    N = 2 ** (n + m)
    energies = [_energy(k, n, m, W, b, d) for k in range(N)]
    emin = min(energies)
    vis = QuantumRegister(n, 'vis')
    hid = QuantumRegister(m, 'hid')
    anc = QuantumRegister(1, 'anc')
    qc = QuantumCircuit(vis, hid, anc)
    data = list(vis) + list(hid)
    for q in data:
        qc.h(q)
    for k in range(N):
        # eq_2: ancilla-|1> amplitude exp(-(E-Emin)/2) -> probability prop. to exp(-E)
        a = math.exp(-(energies[k] - emin) / 2.0)
        a = min(1.0, a)
        theta = 2.0 * math.asin(a)
        if theta == 0.0:
            continue
        gate = RYGate(theta).control(n + m, ctrl_state=k)
        qc.append(gate, data + [anc[0]])
    return qc
