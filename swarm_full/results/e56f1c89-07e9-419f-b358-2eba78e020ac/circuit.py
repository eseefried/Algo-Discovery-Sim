from __future__ import annotations
import math
from qiskit import QuantumCircuit, QuantumRegister


def _check_int(v, lo, hi, name):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return v


def _check_perm(perm, n, name):
    if not isinstance(perm, (list, tuple)) or len(perm) > 64:
        raise ValueError(name + " must be a list of at most 64 transpositions")
    out = []
    for pr in perm:
        if not isinstance(pr, (list, tuple)) or len(pr) != 2:
            raise ValueError(name + " entries must be pairs")
        a = _check_int(pr[0], 0, 2 ** n - 1, name + " state")
        b = _check_int(pr[1], 0, 2 ** n - 1, name + " state")
        if a == b:
            raise ValueError(name + " transposition needs distinct states")
        out.append((a, b))
    return out


def _swap_states(qc, qubits, n, a, b):
    # Swap basis states |a> and |b> (little-endian indices).
    d = a ^ b
    t = (d & -d).bit_length() - 1
    others = [j for j in range(n) if (d >> j) & 1 and j != t]
    mask = 0
    for j in others:
        mask |= 1 << j
    ap = a ^ mask if (a >> t) & 1 else a
    for j in others:
        qc.cx(qubits[t], qubits[j])
    ctrls = [j for j in range(n) if j != t]
    zeros = [j for j in ctrls if not (ap >> j) & 1]
    for j in zeros:
        qc.x(qubits[j])
    if ctrls:
        qc.mcx([qubits[j] for j in ctrls], qubits[t])
    else:
        qc.x(qubits[t])
    for j in zeros:
        qc.x(qubits[j])
    for j in reversed(others):
        qc.cx(qubits[t], qubits[j])


def _apply_perm(qc, qubits, n, pairs, transpose):
    seq = list(reversed(pairs)) if transpose else list(pairs)
    for a, b in seq:
        _swap_states(qc, qubits, n, a, b)


def _diagonal(qc, qubits, n, phases):
    # U'|k> = exp(i*phases[k])|k>
    for k, th in enumerate(phases):
        if abs(math.remainder(th, 2 * math.pi)) < 1e-12:
            continue
        zeros = [j for j in range(n) if not (k >> j) & 1]
        for j in zeros:
            qc.x(qubits[j])
        if n == 1:
            qc.p(th, qubits[0])
        else:
            qc.mcp(th, qubits[:-1], qubits[-1])
        for j in zeros:
            qc.x(qubits[j])


def build_circuit(instance):
    """Implements U = Q^T P^T U' P Q (eq_1) with P, Q products of basis-state
    transpositions and U' a diagonal unitary. Applied order: Q, P, U', P^T, Q^T."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _check_int(instance.get("n"), 1, 6, "n")
    p_pairs = _check_perm(instance.get("perm_P", []), n, "perm_P")
    q_pairs = _check_perm(instance.get("perm_Q", []), n, "perm_Q")
    ph = instance.get("phases")
    if not isinstance(ph, (list, tuple)) or len(ph) != 2 ** n:
        raise ValueError("phases must be a list of length 2**n")
    phases = []
    for v in ph:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError("phases must be finite real numbers")
        phases.append(float(v))
    reg = QuantumRegister(n, "q")
    qc = QuantumCircuit(reg)
    qubits = list(range(n))
    _apply_perm(qc, qubits, n, q_pairs, False)
    _apply_perm(qc, qubits, n, p_pairs, False)
    _diagonal(qc, qubits, n, phases)
    _apply_perm(qc, qubits, n, p_pairs, True)
    _apply_perm(qc, qubits, n, q_pairs, True)
    return qc
