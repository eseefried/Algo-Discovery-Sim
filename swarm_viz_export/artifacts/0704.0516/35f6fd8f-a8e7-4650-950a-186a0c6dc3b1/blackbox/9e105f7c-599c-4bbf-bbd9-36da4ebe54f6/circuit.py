import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _num(d, key, default):
    v = d.get(key, default)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(key + " must be a finite number")
    return float(v)


def _int(d, key, default):
    v = d.get(key, default)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    return v


def build_circuit(instance):
    """Shor order-finding unitary for N=15 with optional QFT phase-gate errors."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int(instance, "N", 15)
    a = _int(instance, "a", 2)
    t = _int(instance, "t", 4)
    if n != 15 or a not in (2, 4, 8):
        raise ValueError("only N=15 with a in {2,4,8} is supported")
    if t < 1 or t + 4 > 12:
        raise ValueError("t must satisfy 1 <= t <= 8")
    model = instance.get("error_model", "none")
    if model not in ("none", "systematic", "random", "combined"):
        raise ValueError("unknown error_model")
    eps = _num(instance, "epsilon", 0.0)
    dl = _num(instance, "delta", 0.0)
    sg = _num(instance, "sigma", 0.0)
    seed = _int(instance, "seed", 0)
    if sg < 0 or seed < 0:
        raise ValueError("sigma and seed must be non-negative")
    init = instance.get("include_work_init", False)
    if not isinstance(init, bool):
        raise ValueError("include_work_init must be bool")
    ng = t * (t - 1) // 2
    eps_u = eps if model in ("systematic", "combined") else 0.0
    dl_u = dl if model in ("systematic", "combined") else 0.0
    offs = [0.0] * ng
    if model in ("random", "combined"):
        given = instance.get("random_offsets")
        if given is not None:
            if not isinstance(given, list) or len(given) != ng:
                raise ValueError("random_offsets must be a list of length t(t-1)/2")
            offs = []
            for v in given:
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                    raise ValueError("random_offsets entries must be finite numbers")
                offs.append(float(v))
        elif sg > 0:
            offs = [float(v) for v in np.random.default_rng(seed).normal(0.0, sg, ng)]
    ideal = eps_u == 0.0 and dl_u == 0.0 and all(o == 0.0 for o in offs)

    count = QuantumRegister(t, "count")
    work = QuantumRegister(4, "work")
    qc = QuantumCircuit(count, work, name="shor_order_finding")

    # eq_1: optional preparation of y=1 (off by default; runner prepares inputs)
    if init:
        qc.x(work[0])
    # eq_2: uniform superposition over x
    for k in range(t):
        qc.h(count[k])
    # eq_1: controlled U^(2^k), U = multiply by a mod 15 = left bit rotation by log2(a)
    for k in range(t):
        p = pow(a, 2 ** k, n)
        s = p.bit_length() - 1
        for _ in range(s):
            qc.cswap(count[k], work[2], work[3])
            qc.cswap(count[k], work[1], work[2])
            qc.cswap(count[k], work[0], work[1])
    # eq_6 / eq_3 / eq_4: inverse QFT on counting register
    if ideal:
        qc.append(QFTGate(t).inverse(), list(range(t)))
    else:
        for i in range(t // 2):
            qc.swap(count[i], count[t - 1 - i])
        g = 0
        for j in range(t):
            for k in range(j):
                m = j - k
                mag = (math.pi / 2 ** m) * (1.0 + eps_u) + dl_u + offs[g]
                g += 1
                qc.cp(-mag, count[k], count[j])
            qc.h(count[j])
    return qc
