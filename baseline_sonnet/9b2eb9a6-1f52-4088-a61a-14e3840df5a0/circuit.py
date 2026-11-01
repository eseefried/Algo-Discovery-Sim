import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

_ROT = {2: ((2, 3), (1, 2), (0, 1)), 4: ((0, 2), (1, 3)), 8: ((0, 1), (1, 2), (2, 3))}
_MULT = {1: (1, False), 2: (2, False), 4: (4, False), 8: (8, False), 14: (1, True), 13: (2, True), 11: (4, True), 7: (8, True)}


def _num(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError('numeric parameter required')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError('parameter must be finite')
    return v


def _cmult(qc, c, w, m):
    # controlled |y> -> |m y mod 15> on 4 work qubits (little endian); eq_2 modular exponentiation
    base, comp = _MULT[m]
    if base != 1:
        for i, j in _ROT[base]:
            qc.cswap(c, w[i], w[j])
    if comp:
        for q in w:
            qc.cx(c, q)


def _perturbed_qft(qc, q, eps, deltas):
    # eq_3: QFT (same convention as QFTGate) with angle 2*pi/2^k + eps + delta_g per controlled phase
    n = len(q)
    g = 0
    for j in range(n - 1, -1, -1):
        qc.h(q[j])
        for m in range(j - 1, -1, -1):
            qc.cp(2 * math.pi / 2 ** (j - m + 1) + eps + deltas[g], q[m], q[j])
            g += 1
    for i in range(n // 2):
        qc.swap(q[i], q[n - 1 - i])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    N = instance.get('N', 15)
    a = instance.get('a', 7)
    t = instance.get('t', 8)
    for v in (N, a, t):
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('N, a, t must be integers')
    if N != 15:
        raise ValueError('only N=15 is supported')
    if a not in (2, 4, 7, 8, 11, 13, 14) or math.gcd(a, N) != 1:
        raise ValueError('a must be coprime to 15 with 1<a<15')
    if t < 1 or t > 8:
        raise ValueError('t must be in 1..8 (total qubits <= 12)')
    eps = _num(instance.get('epsilon', 0.0))
    sigma = _num(instance.get('sigma', 0.0))
    if sigma < 0:
        raise ValueError('sigma must be >= 0')
    ng = t * (t - 1) // 2
    if 'deltas' in instance:
        d = instance['deltas']
        if not isinstance(d, list) or len(d) != ng:
            raise ValueError('deltas must be a list of length t(t-1)/2')
        deltas = [_num(x) for x in d]
    elif sigma > 0:
        seed = instance.get('seed', 0)
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError('seed must be a non-negative integer')
        deltas = [float(x) for x in np.random.default_rng(seed).normal(0.0, sigma, ng)]
    else:
        deltas = [0.0] * ng
    cnt = QuantumRegister(t, 'cnt')
    wrk = QuantumRegister(4, 'wrk')
    qc = QuantumCircuit(cnt, wrk)
    w = list(wrk)
    for k in range(t):
        m = pow(a, 2 ** k, 15)
        _cmult(qc, cnt[k], w, m)
    _perturbed_qft(qc, list(cnt), eps, deltas)
    return qc
