import math
from qiskit import QuantumCircuit


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + "," + str(hi) + "]")
    return v


def _mcphase(qc, angle, qs):
    # phase `angle` on the all-ones pattern of qubits qs
    if len(qs) == 1:
        qc.p(angle, qs[0])
    else:
        qc.mcp(angle, list(qs[:-1]), qs[-1])


def _flip_zeros(qc, qs, bits):
    for q, b in zip(qs, bits):
        if not b:
            qc.x(q)


def _prepare_A(n_steps, q_len, phases):
    # eq_1/eq_2: uniform superposition over f^N = 2^N paths (S_0 = 1), then eq_3 phase layer.
    a = QuantumCircuit(n_steps)
    a.h(range(n_steps))
    for t in range(1, n_steps + 1):
        m = min(t - 1, q_len - 1)
        qs = [t - 1 - j for j in range(m + 1)]
        row = phases[t - 1]
        for idx in range(2 ** (m + 1)):
            ang = row[idx]
            if ang == 0.0:
                continue
            bits = [(idx >> j) & 1 for j in range(m + 1)]
            _flip_zeros(a, qs, bits)
            _mcphase(a, ang, qs)
            _flip_zeros(a, qs, bits)
    return a


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n_steps = _int(instance.get("N"), "N", 1, 12)
    q_len = _int(instance.get("Q"), "Q", 1, 16)
    k = _int(instance.get("iterations", 1), "iterations", 0, 64)
    fan = instance.get("fanout", 2)
    if fan != 2 or isinstance(fan, bool):
        raise ValueError("only fanout 2 is supported")
    raw = instance.get("edge_phases")
    if not isinstance(raw, list) or len(raw) != n_steps:
        raise ValueError("edge_phases must be a list with N rows")
    phases = []
    for t in range(1, n_steps + 1):
        m = min(t - 1, q_len - 1)
        row = raw[t - 1]
        if not isinstance(row, list) or len(row) != 2 ** (m + 1):
            raise ValueError("edge_phases row has wrong length")
        out = []
        for v in row:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError("edge phase must be a finite number")
            out.append(float(v))
        phases.append(out)
    marked = instance.get("marked_path")
    if k > 0:
        if not isinstance(marked, list) or len(marked) != n_steps:
            raise ValueError("marked_path must be a list of N bits")
        for b in marked:
            if isinstance(b, bool) or b not in (0, 1):
                raise ValueError("marked_path entries must be 0 or 1")
    a = _prepare_A(n_steps, q_len, phases)
    a_inv = a.inverse()
    allq = list(range(n_steps))
    qc = QuantumCircuit(n_steps)
    qc.compose(a, inplace=True)
    for _ in range(k):
        # eq_4: oracle I-2|m><m|
        _flip_zeros(qc, allq, marked)
        _mcphase(qc, math.pi, allq)
        _flip_zeros(qc, allq, marked)
        # A (I-2|0><0|) A^dagger  (equals -U_psi)
        qc.compose(a_inv, inplace=True)
        qc.x(allq)
        _mcphase(qc, math.pi, allq)
        qc.x(allq)
        qc.compose(a, inplace=True)
    return qc
