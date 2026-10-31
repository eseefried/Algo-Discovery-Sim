from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np

_MAX_QUBITS = 12
_MAX_STEPS = 2000
_MAX_CLAUSES = 30


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return v


def _num(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + " must be a finite number")
    return float(v)


def _step_terms(n, clauses, s, sig):
    # eq_1 + eq_2: Pauli terms of (1-s)H0 + s*HP + H_sig at schedule value s
    # H0 = -sum X_i ; HP = sum_clauses (b_i+b_j+b_k-1)^2 = const - (Zi+Zj+Zk)/2 + (ZiZj+ZiZk+ZjZk)/2
    # H_sig = sig * sum_i Z_i (assumed signal form)
    terms = []
    for i in range(n):
        terms.append(("x", (i,), -(1.0 - s)))
    for c in clauses:
        for i in c:
            terms.append(("z", (i,), -0.5 * s))
        terms.append(("zz", (c[0], c[1]), 0.5 * s))
        terms.append(("zz", (c[0], c[2]), 0.5 * s))
        terms.append(("zz", (c[1], c[2]), 0.5 * s))
    if sig != 0.0:
        for i in range(n):
            terms.append(("z", (i,), sig))
    return [t for t in terms if abs(t[2]) > 1e-15]


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n_qubits", "clauses", "total_time", "steps", "signal_mode", "signal_amplitude", "seed"):
        if key not in instance:
            raise ValueError("missing key: " + key)
    n = _int(instance["n_qubits"], "n_qubits", 3, _MAX_QUBITS)
    steps = _int(instance["steps"], "steps", 1, _MAX_STEPS)
    seed = _int(instance["seed"], "seed", 0, 2 ** 32 - 1)
    T = _num(instance["total_time"], "total_time")
    if T <= 0.0:
        raise ValueError("total_time must be positive")
    amp = _num(instance["signal_amplitude"], "signal_amplitude")
    if amp < 0.0:
        raise ValueError("signal_amplitude must be nonnegative")
    mode = instance["signal_mode"]
    if mode not in ("none", "regular", "random"):
        raise ValueError("signal_mode must be none, regular or random")
    raw = instance["clauses"]
    if not isinstance(raw, (list, tuple)) or len(raw) < 1 or len(raw) > _MAX_CLAUSES:
        raise ValueError("clauses must be a list of 1..30 triples")
    clauses = []
    for c in raw:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            raise ValueError("each clause must have 3 bit indices")
        t = tuple(_int(v, "clause index", 0, n - 1) for v in c)
        if len(set(t)) != 3:
            raise ValueError("clause indices must be distinct")
        clauses.append(t)
    rng = np.random.default_rng(seed)
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    for j in range(steps):
        s = (j + 0.5) / steps
        if mode == "regular":
            sg = 1.0 if j % 2 == 0 else -1.0
        elif mode == "random":
            sg = 1.0 if int(rng.integers(0, 2)) == 1 else -1.0
        else:
            sg = 0.0
        terms = _step_terms(n, clauses, s, amp * sg)
        lam = sum(abs(t[2]) for t in terms)
        if lam <= 0.0:
            continue
        probs = np.array([abs(t[2]) / lam for t in terms])
        probs = probs / probs.sum()
        k = int(rng.choice(len(terms), p=probs))
        kind, qs, c = terms[k]
        # eq_3 (qDRIFT-style): exp(-i * sign(c) * lam * T/N * P)
        ang = 2.0 * (1.0 if c > 0 else -1.0) * lam * T / steps
        if kind == "x":
            qc.rx(ang, qs[0])
        elif kind == "z":
            qc.rz(ang, qs[0])
        else:
            qc.rzz(ang, qs[0], qs[1])
    return qc
