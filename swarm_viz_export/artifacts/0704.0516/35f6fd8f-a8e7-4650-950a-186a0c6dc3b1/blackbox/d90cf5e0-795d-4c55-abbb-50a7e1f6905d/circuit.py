"""Shor order finding for N=15 with optionally imperfect inverse-QFT phase gates."""
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

_MODELS = ('ideal', 'systematic', 'random', 'combined')


def _num(instance, key, default_value):
    v = instance.get(key, default_value)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + ' must be finite')
    return v


def _int(instance, key, default_value):
    v = instance.get(key, default_value)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    return v


def _controlled_rotate_left(qc, ctrl, work, s):
    # eq_1: multiplication by 2^s mod 15 on y in 0..14 is a left cyclic rotation of 4 bits by s.
    # Controlled by ctrl via a chain of Fredkin gates; 15 (1111) is also fixed, so U is a permutation.
    for _ in range(s):
        for i in (2, 1, 0):
            qc.cswap(ctrl, work[i], work[i + 1])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance, 'N', 15)
    a = _int(instance, 'a', 2)
    t = _int(instance, 't', 4)
    seed = _int(instance, 'seed', 0)
    model = instance.get('error_model', 'ideal')
    if n != 15:
        raise ValueError('only N=15 is supported')
    if a not in (2, 4, 8):
        raise ValueError('a must be one of 2, 4, 8')
    if t < 1 or t > 8:
        raise ValueError('t must be in 1..8 (total qubits <= 12)')
    if not isinstance(model, str) or model not in _MODELS:
        raise ValueError('error_model must be ideal, systematic, random or combined')
    if seed < 0:
        raise ValueError('seed must be nonnegative')
    eps = _num(instance, 'epsilon', 0.0)
    dl = _num(instance, 'delta', 0.0)
    sg = _num(instance, 'sigma', 0.0)
    if sg < 0.0:
        raise ValueError('sigma must be >= 0')
    sys_on = model in ('systematic', 'combined')
    rnd_on = model in ('random', 'combined')
    e = eps if sys_on else 0.0
    d = dl if sys_on else 0.0
    w = sg * math.sqrt(3.0) if rnd_on else 0.0  # uniform on [-w,w] has variance sigma^2
    rng = np.random.default_rng(seed)

    count = list(range(t))
    work = list(range(t, t + 4))
    qc = QuantumCircuit(QuantumRegister(t, 'count'), QuantumRegister(4, 'work'))

    # Step 1: uniform superposition over counting register
    for q in count:
        qc.h(q)

    # Step 2 (eq_1): controlled U^(2^k), U^(2^k) = multiplication by a^(2^k) mod 15
    rot = {1: 0, 2: 1, 4: 2, 8: 3}
    for k in range(t):
        m = pow(a, 2 ** k, n)
        s = rot[m]
        if s:
            _controlled_rotate_left(qc, count[k], work, s)

    # Step 3 (eq_6, eq_3, eq_4): inverse QFT, swaps first then ascending H/CP ladder
    for i in range(t // 2):
        qc.swap(count[i], count[t - 1 - i])
    for j in range(t):
        for k in range(j):
            mag = math.pi / (2 ** (j - k))
            off = float(rng.uniform(-w, w)) if rnd_on else 0.0
            ang = -(mag * (1.0 + e) + d + off)
            qc.cp(ang, count[k], count[j])
        qc.h(count[j])
    return qc
