from qiskit import QuantumCircuit, QuantumRegister
import math


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(name + ' out of range [' + str(lo) + ', ' + str(hi) + ']')
    return v


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(name + ' must be a real number')
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    return x


def _phase_all_ones(qc, angle, n):
    # diag(1,...,1,exp(i*angle)) on the all-ones basis state of qubits 0..n-1
    if n == 2:
        qc.cp(angle, 0, 1)
    else:
        qc.mcp(angle, list(range(n - 1)), n - 1)


def build_circuit(instance):
    """k iterations of Q = D O with O = I-(1-e^{ia})|w><w| (eq_1), D = I-(1-e^{ib})|s><s| (eq_1), Q^k (eq_2)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance.get('n'), 'n', 2, 6)
    marked = _int(instance.get('marked'), 'marked', 0, 2 ** n - 1)
    k = _int(instance.get('iterations'), 'iterations', 0, 200)
    d1 = _real(instance.get('delta1', 0.0), 'delta1')
    d2 = _real(instance.get('delta2', 0.0), 'delta2')
    a = math.pi + d1
    b = math.pi + d2
    q = QuantumRegister(n, 'data')
    qc = QuantumCircuit(q)
    zeros = [i for i in range(n) if not (marked >> i) & 1]
    for _ in range(k):
        # oracle O: phase e^{ia} on |marked>
        for i in zeros:
            qc.x(i)
        _phase_all_ones(qc, a, n)
        for i in zeros:
            qc.x(i)
        # diffusion D = H^n (I-(1-e^{ib})|0><0|) H^n
        for i in range(n):
            qc.h(i)
        for i in range(n):
            qc.x(i)
        _phase_all_ones(qc, b, n)
        for i in range(n):
            qc.x(i)
        for i in range(n):
            qc.h(i)
    return qc
