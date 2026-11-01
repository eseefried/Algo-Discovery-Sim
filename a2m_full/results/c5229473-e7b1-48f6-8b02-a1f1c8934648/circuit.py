import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + " must be a real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def _angles(t, key):
    v = t.get(key)
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        raise ValueError(key + " must be a list of 3 angles")
    return [_num(a, key) for a in v]


def build_circuit(instance):
    """Stinespring unitary U_k (eq_2) for the selected mixture term k (eq_3).

    Qubit 0 = system, qubit 1 = ancilla (expected to start in |0>).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    d = instance.get("d", 2)
    if isinstance(d, bool) or d != 2:
        raise ValueError("only d=2 is supported")
    terms = instance.get("terms")
    if not isinstance(terms, list) or len(terms) < 1 or len(terms) > d * d:
        raise ValueError("terms must be a list of 1..d^2 term dicts")
    probs = instance.get("probabilities")
    if not isinstance(probs, list) or len(probs) != len(terms):
        raise ValueError("probabilities must match terms in length")
    ps = [_num(p, "probability") for p in probs]
    if any(p < 0.0 for p in ps) or abs(sum(ps) - 1.0) > 1e-9:
        raise ValueError("probabilities must be nonnegative and sum to 1")
    k = instance.get("k")
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k >= len(terms):
        raise ValueError("k must be a valid term index")
    t = terms[k]
    if not isinstance(t, dict):
        raise ValueError("term must be a dict")
    pre = _angles(t, "pre")
    ctrl = _angles(t, "ctrl")
    post = _angles(t, "post")
    anc_post = _angles(t, "anc_post")
    theta = _num(t.get("theta"), "theta")

    sys_r = QuantumRegister(1, "sys")
    anc_r = QuantumRegister(1, "anc")
    qc = QuantumCircuit(sys_r, anc_r)
    # system pre-rotation
    qc.u(pre[0], pre[1], pre[2], 0)
    # ancilla (environment) state-preparation-like rotation, unitary
    qc.ry(theta, 1)
    # ancilla-controlled system unitary: couples system and environment
    qc.cu(ctrl[0], ctrl[1], ctrl[2], 0.0, 1, 0)
    # system post-rotation and ancilla basis choice (selects Kraus unraveling)
    qc.u(post[0], post[1], post[2], 0)
    qc.u(anc_post[0], anc_post[1], anc_post[2], 1)
    return qc
