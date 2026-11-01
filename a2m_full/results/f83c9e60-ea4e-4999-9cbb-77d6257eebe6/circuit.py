'''Shor order finding for N=15 with optional controlled-phase angle noise in the inverse QFT.'''
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math
import numpy as np


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, np.integer)):
        raise ValueError(name + ' must be an integer')
    return int(v)


def _as_float(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float, np.integer, np.floating)):
        raise ValueError(name + ' must be a real number')
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    return x


def _cmult(qc, ctrl, work, b):
    # Controlled multiplication by b mod 15 on 4 work qubits (little-endian).
    # b = 2^s is a left bit rotation by s; b = 15 - 2^s is rotation followed by bitwise complement.
    table = {1: (0, False), 2: (1, False), 4: (2, False), 8: (3, False),
             14: (0, True), 13: (1, True), 11: (2, True), 7: (3, True)}
    if b not in table:
        raise ValueError('unsupported multiplier')
    s, comp = table[b]
    for _ in range(s):
        qc.cswap(ctrl, work[2], work[3])
        qc.cswap(ctrl, work[1], work[2])
        qc.cswap(ctrl, work[0], work[1])
    if comp:
        for q in work:
            qc.cx(ctrl, q)


def _noisy_iqft(qc, q, eps, sigma, rng):
    # Inverse of the Qiskit QFT circuit (H then CP per target, swaps last), with CP angles scaled by (1+delta).
    n = len(q)
    for i in range(n // 2):
        qc.swap(q[i], q[n - 1 - i])
    for j in range(n):
        for k in reversed(range(j)):
            theta = -math.pi * 2.0 ** (k - j)
            delta = eps
            if sigma > 0.0:
                delta += float(rng.normal(0.0, sigma))
            qc.cp(theta * (1.0 + delta), q[k], q[j])
        qc.h(q[j])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    allowed = {'N', 'a', 't', 'epsilon', 'sigma', 'seed', 'include_hadamards'}
    for key in instance:
        if key not in allowed:
            raise ValueError('unknown key ' + str(key))
    N = _as_int(instance.get('N', 15), 'N')
    if N != 15:
        raise ValueError('only N=15 is supported')
    a = _as_int(instance.get('a', 7), 'a')
    if a not in (2, 4, 7, 8, 11, 13, 14):
        raise ValueError('a must be coprime to 15 and in {2,4,7,8,11,13,14}')
    t = _as_int(instance.get('t', 8), 't')
    if t < 1 or t > 8:
        raise ValueError('t must be in 1..8 (total qubits t+4 <= 12)')
    eps = _as_float(instance.get('epsilon', 0.0), 'epsilon')
    sigma = _as_float(instance.get('sigma', 0.0), 'sigma')
    if sigma < 0.0:
        raise ValueError('sigma must be >= 0')
    seed = _as_int(instance.get('seed', 0), 'seed')
    if seed < 0:
        raise ValueError('seed must be >= 0')
    had = instance.get('include_hadamards', True)
    if not isinstance(had, bool):
        raise ValueError('include_hadamards must be a bool')

    count = QuantumRegister(t, 'count')
    work = QuantumRegister(4, 'work')
    qc = QuantumCircuit(count, work, name='shor_order_finding_N15')
    cq = [count[i] for i in range(t)]
    wq = [work[i] for i in range(4)]

    if had:
        for q in cq:
            qc.h(q)
    for k in range(t):
        b = pow(a, 2 ** k, 15)
        if b != 1:
            _cmult(qc, cq[k], wq, b)

    if eps == 0.0 and sigma == 0.0:
        qc.append(QFTGate(t).inverse(), list(range(t)))
    else:
        rng = np.random.default_rng(seed)
        _noisy_iqft(qc, cq, eps, sigma, rng)
    return qc
