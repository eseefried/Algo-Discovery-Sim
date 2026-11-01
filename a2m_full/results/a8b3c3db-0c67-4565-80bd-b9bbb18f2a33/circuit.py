from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _is_real(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    return math.isfinite(float(x))


def build_circuit(instance):
    """Phase encoding: n_k applications of P(phi) on probe qubit k (eq_1, eq_2),
    optional offset P(theta_k) and readout Hadamard giving P(b0|phi)=(1+cos(n_k phi+theta_k))/2 (eq_3).
    Instance keys: phi (real), n (list of positive ints), theta (optional list of reals),
    readout_hadamard (optional bool, default True)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not isinstance(n, (list, tuple)) or len(n) < 1:
        raise ValueError('n must be a non-empty list of positive integers')
    m = len(n)
    if m > 12:
        raise ValueError('at most 12 probe qubits are allowed')
    for nk in n:
        if not _is_int(nk) or nk < 1 or nk > 64:
            raise ValueError('each n_k must be an integer in [1, 64]')
    total = sum(n)
    if total > 128:
        raise ValueError('total number of gate applications N must be <= 128')
    phi = instance.get('phi')
    if not _is_real(phi):
        raise ValueError('phi must be a finite real number')
    phi = float(phi)
    theta = instance.get('theta')
    if theta is None:
        theta = [0.0] * m
    if not isinstance(theta, (list, tuple)) or len(theta) != m:
        raise ValueError('theta must be a list with one entry per probe qubit')
    for t in theta:
        if not _is_real(t):
            raise ValueError('theta entries must be finite reals')
    readout = instance.get('readout_hadamard', True)
    if not isinstance(readout, bool):
        raise ValueError('readout_hadamard must be a bool')
    qr = QuantumRegister(m, 'probe')
    qc = QuantumCircuit(qr)
    for k in range(m):
        for _ in range(n[k]):
            qc.p(phi, qr[k])
        if float(theta[k]) != 0.0:
            qc.p(float(theta[k]), qr[k])
        if readout:
            qc.h(qr[k])
    return qc
