from qiskit import QuantumCircuit
import math


def _phase_on_basis(qc, n, value, phi):
    """Apply exp(-i*phi*|value><value|) on qubits 0..n-1."""
    for i in range(n):
        if not (value >> i) & 1:
            qc.x(i)
    if n == 1:
        qc.p(-phi, 0)
    else:
        qc.mcp(-phi, list(range(n - 1)), n - 1)
    for i in range(n):
        if not (value >> i) & 1:
            qc.x(i)


def build_circuit(instance):
    """Lie-Trotter approximation (eq_3) of exp(-i(|w><w|+|s><s|)t) with m steps.

    instance: {"n": int 1..12, "marked": int in [0,2^n), "t": real, "m": int>=1}
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('n', 'marked', 't', 'm'):
        if key not in instance:
            raise ValueError('missing key: ' + key)
    n = instance['n']
    w = instance['marked']
    t = instance['t']
    m = instance['m']
    for v in (n, w, m):
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('n, marked, m must be integers')
    if isinstance(t, bool) or not isinstance(t, (int, float)):
        raise ValueError('t must be real')
    t = float(t)
    if not math.isfinite(t):
        raise ValueError('t must be finite')
    if n < 1 or n > 12:
        raise ValueError('n must be in 1..12')
    if w < 0 or w >= 2 ** n:
        raise ValueError('marked out of range')
    if m < 1 or m > 100000:
        raise ValueError('m must be in 1..100000')
    phi = t / m
    qc = QuantumCircuit(n, name='grover_trotter')
    for _ in range(m):
        # rightmost factor of eq_3 acts first: exp(-i|s><s| t/m) = H^n exp(-i|0><0| t/m) H^n
        for i in range(n):
            qc.h(i)
        _phase_on_basis(qc, n, 0, phi)
        for i in range(n):
            qc.h(i)
        # then exp(-i|w><w| t/m)
        _phase_on_basis(qc, n, w, phi)
    return qc
