"""Shor order finding for N = 15 with an imperfect inverse QFT.

build_circuit(instance) -> QuantumCircuit

instance keys:
  N        : must be 15 (fixed by scope)
  a        : base in {2, 4, 7, 8, 11, 13, 14}
  t        : number of control qubits, 1 <= t <= 8
  epsilon  : systematic fractional over-rotation of every QFT phase gate (eq_3)
  sigma    : std. dev. of Gaussian random phase error per gate (eq_4)
  seed     : non-negative integer seed for the random-error realization
  prepare_work_one (optional, default False): if True, apply X to the work LSB
             so that an all-zero input yields work register |1>.

Qubit layout: control qubits are indices 0..t-1 (index 0 = LSB of x),
work qubits are indices t..t+3 (index t = LSB of the work value).
The runner must supply control |0...0> and work |0001> (= integer 1),
unless prepare_work_one is set.
"""
from __future__ import annotations

import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

_N_FIXED = 15
_WORK_QUBITS = 4
_MAX_QUBITS = 12
# m -> (cyclic bit shift s, complement flag): m = (+/-) 2^s mod 15
_MULT_TABLE = {1: (0, False), 2: (1, False), 4: (2, False), 8: (3, False),
               14: (0, True), 13: (1, True), 11: (2, True), 7: (3, True)}


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _is_real(x):
    return (isinstance(x, (int, float)) and not isinstance(x, bool)
            and math.isfinite(float(x)))


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    N = instance.get("N")
    if not _is_int(N) or N != _N_FIXED:
        raise ValueError("scope supports only N = 15")
    a = instance.get("a")
    if not _is_int(a) or a not in _MULT_TABLE or a == 1:
        raise ValueError("a must be in {2, 4, 7, 8, 11, 13, 14}")
    t = instance.get("t")
    if not _is_int(t) or t < 1:
        raise ValueError("t must be a positive integer")
    if t + _WORK_QUBITS > _MAX_QUBITS:
        raise ValueError("t + 4 must not exceed 12 qubits")
    epsilon = instance.get("epsilon")
    if not _is_real(epsilon):
        raise ValueError("epsilon must be a finite real number")
    sigma = instance.get("sigma")
    if not _is_real(sigma) or float(sigma) < 0.0:
        raise ValueError("sigma must be a finite non-negative real number")
    seed = instance.get("seed")
    if not _is_int(seed) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    prep = instance.get("prepare_work_one", False)
    if not isinstance(prep, bool):
        raise ValueError("prepare_work_one must be a bool")
    return a, t, float(epsilon), float(sigma), seed, prep


def _controlled_mult_mod15(qc, ctrl, w, m):
    """Controlled |y> -> |m*y mod 15> on the 4 work qubits w (w[0] = LSB).

    Multiplication by 2 mod 15 is a cyclic bit rotation (bit i -> i+1);
    multiplication by -1 mod 15 is bitwise complement. (eq_1 network)
    """
    s, negate = _MULT_TABLE[m]
    for _ in range(s):
        # bit i -> bit i+1 (mod 4)
        qc.cswap(ctrl, w[2], w[3])
        qc.cswap(ctrl, w[1], w[2])
        qc.cswap(ctrl, w[0], w[1])
    if negate:
        for q in w:
            qc.cx(ctrl, q)


def _imperfect_inverse_qft(qc, c, epsilon, sigma, rng):
    """Inverse QFT on qubits c (c[0] = LSB), eq_2, with perturbed R_k gates.

    Ideal angle of each controlled phase: theta = -pi / 2^(j-k).
    Applied angle: (1 + epsilon) * theta + delta, delta ~ N(0, sigma^2)  (eq_3, eq_4).
    Hadamards are ideal.
    """
    t = len(c)
    for i in range(t // 2):
        qc.swap(c[i], c[t - 1 - i])
    for j in range(t):
        for k in range(j):
            theta = -math.pi / float(2 ** (j - k))
            delta = float(rng.normal(0.0, sigma)) if sigma > 0.0 else 0.0
            qc.cp((1.0 + epsilon) * theta + delta, c[k], c[j])
        qc.h(c[j])


def build_circuit(instance):
    a, t, epsilon, sigma, seed, prep = _validate(instance)
    ctrl = QuantumRegister(t, "c")
    work = QuantumRegister(_WORK_QUBITS, "w")
    qc = QuantumCircuit(ctrl, work)
    c = [ctrl[i] for i in range(t)]
    w = [work[i] for i in range(_WORK_QUBITS)]
    if prep:
        qc.x(w[0])
    # eq_1: Hadamards on control, then controlled U^(2^j), U|y> = |a y mod 15>
    for j in range(t):
        qc.h(c[j])
    for j in range(t):
        m = pow(a, 2 ** j, _N_FIXED)
        if m != 1:
            _controlled_mult_mod15(qc, c[j], w, m)
    # eq_2 with eq_3 / eq_4 perturbations
    rng = np.random.default_rng(seed)
    _imperfect_inverse_qft(qc, c, epsilon, sigma, rng)
    return qc
