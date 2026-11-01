from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate
import math
import numpy as np


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [%d, %d]" % (lo, hi))
    return v


def _effective_weights(instance, na, nb):
    rows = 2 ** na
    cols = 2 ** nb
    w = instance.get("weights")
    if not isinstance(w, list) or len(w) != rows:
        raise ValueError("weights must have 2**na rows")
    arr = np.zeros((rows, cols))
    for a in range(rows):
        if not isinstance(w[a], list) or len(w[a]) != cols:
            raise ValueError("weights must have 2**nb columns")
        for b in range(cols):
            v = w[a][b]
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValueError("weights must be numeric")
            v = float(v)
            if not math.isfinite(v) or v < 0.0:
                raise ValueError("weights must be finite and nonnegative")
            arr[a, b] = v
    idx = instance.get("input_index")
    if idx is not None:
        x = instance.get("x")
        if not isinstance(x, list) or len(x) == 0 or len(x) > 64:
            raise ValueError("x must be a nonempty bit list")
        for bit in x:
            if isinstance(bit, bool) or bit not in (0, 1):
                raise ValueError("x entries must be 0 or 1")
        if not isinstance(idx, list) or len(idx) != rows:
            raise ValueError("input_index must match weights shape")
        for a in range(rows):
            if not isinstance(idx[a], list) or len(idx[a]) != cols:
                raise ValueError("input_index must match weights shape")
            for b in range(cols):
                i = idx[a][b]
                if isinstance(i, bool) or not isinstance(i, int) or i < -1 or i >= len(x):
                    raise ValueError("bad input_index entry")
                if i >= 0 and x[i] == 0:
                    arr[a, b] = 0.0
    if np.any(arr.sum(axis=1) <= 0.0) or np.any(arr.sum(axis=0) <= 0.0):
        raise ValueError("every vertex needs a positive-weight edge")
    return arr


def _prep(probs, n):
    # Ry-tree loading nonnegative amplitudes sqrt(probs) from |0...0>.
    c = QuantumCircuit(n)
    for k in range(n):
        t = n - 1 - k
        for prefix in range(2 ** k):
            lo = prefix << (n - k)
            half = 1 << (n - k - 1)
            left = sum(probs[lo:lo + half])
            right = sum(probs[lo + half:lo + 2 * half])
            if left + right <= 1e-15:
                continue
            theta = 2.0 * math.atan2(math.sqrt(right), math.sqrt(left))
            if k == 0:
                c.ry(theta, t)
            else:
                g = RYGate(theta).control(k, ctrl_state=prefix)
                c.append(g, list(range(n - k, n)) + [t])
    return c


def _reflector(probs, n):
    # V (I - 2|0><0|) V^dagger = -(2|phi><phi| - I); the sign is a global -1 per reflection.
    v = _prep(probs, n)
    c = QuantumCircuit(n)
    c.compose(v.inverse(), inplace=True)
    for q in range(n):
        c.x(q)
    if n == 1:
        c.z(0)
    else:
        c.mcp(math.pi, list(range(n - 1)), n - 1)
    for q in range(n):
        c.x(q)
    c.compose(v, inplace=True)
    return c


def _walk(w, na, nb):
    # Edge-space walk U = R_B R_A (R_A applied first). Edge |a>|b>: a on qubits 0..na-1, b on na..na+nb-1.
    n = na + nb
    qc = QuantumCircuit(n)
    rows = 2 ** na
    cols = 2 ** nb
    for a in range(rows):
        p = w[a, :] / w[a, :].sum()
        g = _reflector([float(t) for t in p], nb).to_gate().control(na, ctrl_state=a)
        qc.append(g, list(range(na)) + list(range(na, n)))
    for b in range(cols):
        p = w[:, b] / w[:, b].sum()
        g = _reflector([float(t) for t in p], na).to_gate().control(nb, ctrl_state=b)
        qc.append(g, list(range(na, n)) + list(range(na)))
    return qc


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    na = _int(instance.get("na"), "na", 1, 3)
    nb = _int(instance.get("nb"), "nb", 1, 3)
    m = _int(instance.get("m"), "m", 1, 6)
    if na + nb + m > 12:
        raise ValueError("too many qubits")
    conv = instance.get("convention", "plain")
    if conv not in ("plain", "zero_eigenvalue"):
        raise ValueError("unknown convention")
    w = _effective_weights(instance, na, nb)
    n = na + nb
    u = _walk(w, na, nb)
    if conv == "zero_eigenvalue":
        wc = QuantumCircuit(n)
        wc.compose(u, inplace=True)
        wc.compose(u, inplace=True)
        cg = wc.to_gate().control(1)
    else:
        cg = u.to_gate().control(1)
    qc = QuantumCircuit(QuantumRegister(na, "left"), QuantumRegister(nb, "right"), QuantumRegister(m, "phase"))
    edge = list(range(n))
    phase = list(range(n, n + m))
    for q in phase:
        qc.h(q)
    for j in range(m):
        ctrl = phase[j]
        for _ in range(2 ** j):
            qc.append(cg, [ctrl] + edge)
            if conv == "zero_eigenvalue":
                qc.p(math.pi, ctrl)
    qc.append(QFTGate(m).inverse(), phase)
    return qc
