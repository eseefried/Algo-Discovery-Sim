from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate
import numpy as np
import math

MAX_TOTAL = 8


def _as_int(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)):
        raise ValueError(name + ' must be an integer')
    return int(x)


def _as_array(x, shape, name):
    try:
        a = np.array(x, dtype=float)
    except Exception:
        raise ValueError(name + ' is not numeric')
    if a.shape != shape:
        raise ValueError(name + ' must have shape ' + str(shape))
    if not np.all(np.isfinite(a)) or np.max(np.abs(a), initial=0.0) > 50.0:
        raise ValueError(name + ' must be finite with |entries| <= 50')
    return a


def _gibbs_probs(nv, nh, W, b, d):
    # eq_1 energy and eq_2 Gibbs distribution; basis index x: visible bit i = qubit i, hidden bit j = qubit nv+j
    n = nv + nh
    E = np.zeros(2 ** n)
    for x in range(2 ** n):
        v = np.array([(x >> i) & 1 for i in range(nv)], dtype=float)
        h = np.array([(x >> (nv + j)) & 1 for j in range(nh)], dtype=float)
        E[x] = -float(v @ b) - float(h @ d) - float(v @ W @ h)
    w = np.exp(-(E - E.min()))
    return w / w.sum()


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    nv = _as_int(instance.get('n_v'), 'n_v')
    nh = _as_int(instance.get('n_h'), 'n_h')
    if nv < 1 or nh < 1 or nv + nh > MAX_TOTAL:
        raise ValueError('need n_v>=1, n_h>=1, n_v+n_h<=' + str(MAX_TOTAL))
    W = _as_array(instance.get('W'), (nv, nh), 'W')
    b = _as_array(instance.get('b'), (nv,), 'b')
    d = _as_array(instance.get('d'), (nh,), 'd')
    n = nv + nh
    P = _gibbs_probs(nv, nh, W, b, d)
    vis = QuantumRegister(nv, 'v')
    hid = QuantumRegister(nh, 'h')
    qc = QuantumCircuit(vis, hid)
    # eq_5: amplitudes sqrt(P) via a tree of multiplexed Ry rotations, most significant qubit first
    for q in range(n - 1, -1, -1):
        m = P.reshape(2 ** (n - q - 1), 2, 2 ** q).sum(axis=2)
        for pre in range(2 ** (n - q - 1)):
            p0 = float(m[pre, 0])
            p1 = float(m[pre, 1])
            if p0 + p1 <= 1e-300:
                continue
            theta = 2.0 * math.atan2(math.sqrt(p1), math.sqrt(p0))
            if abs(theta) < 1e-14:
                continue
            ctrls = list(range(q + 1, n))
            if not ctrls:
                qc.ry(theta, q)
            else:
                g = RYGate(theta).control(len(ctrls), ctrl_state=pre)
                qc.append(g, ctrls + [q])
    return qc
