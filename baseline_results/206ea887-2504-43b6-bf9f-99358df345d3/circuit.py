'''Grover threshold-search iterate for one (min,+) matrix entry (trivial quantum APSP baseline).

build_circuit(instance) -> QuantumCircuit

instance keys:
  matrix     : n x n list of nonnegative numbers; null or 'inf' denotes INF (non-edge)
  i, j       : fixed entry whose minimum over k of matrix[i][k] + matrix[k][j] is searched
  threshold  : number or null (= +infinity); index k is marked iff matrix[i][k] + matrix[k][j] < threshold
  iterations : number r >= 0 of Grover iterates G_t = Diffusion * Oracle to apply

Registers (Qiskit little-endian):
  idx[q], q = 0..m-1 with m = ceil(log2 n): bit q of the search index k (qubit 0 = least significant bit)
  flag (qubit m): oracle output qubit; runner should prepare |-> for phase-kickback Grover search.
The runner is expected to prepare idx in the uniform superposition and flag in |->.
The circuit itself contains no state preparation or measurement.
'''
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _parse_entry(x):
    if x is None:
        return math.inf
    if isinstance(x, str):
        if x.strip().lower() in ('inf', '+inf', 'infinity'):
            return math.inf
        raise ValueError('matrix entries must be numbers, null, or "inf"')
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError('matrix entries must be numbers, null, or "inf"')
    v = float(x)
    if math.isnan(v) or v < 0.0:
        raise ValueError('matrix entries must be nonnegative (no negative weights)')
    return v


def _parse_matrix(mat):
    if not isinstance(mat, list) or len(mat) < 2:
        raise ValueError('matrix must be a list of at least 2 rows')
    n = len(mat)
    parsed = []
    for row in mat:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError('matrix must be square')
        parsed.append([_parse_entry(x) for x in row])
    return parsed


def _parse_index(value, n, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    if value < 0 or value >= n:
        raise ValueError(name + ' out of range')
    return value


def _parse_threshold(t):
    if t is None:
        return math.inf
    if isinstance(t, str):
        if t.strip().lower() in ('inf', '+inf', 'infinity'):
            return math.inf
        raise ValueError('threshold must be a number, null, or "inf"')
    if isinstance(t, bool) or not isinstance(t, (int, float)):
        raise ValueError('threshold must be a number, null, or "inf"')
    v = float(t)
    if math.isnan(v):
        raise ValueError('threshold must not be NaN')
    return v


def _marked_indices(matrix, i, j, t):
    # eq_3: f_t(k) = 1 iff D_ik + D_kj < t (INF + x = INF, never marked).
    # The (min,+) candidate values D_ik + D_kj of eq_2 are evaluated classically here.
    n = len(matrix)
    marked = []
    for k in range(n):
        s = matrix[i][k] + matrix[k][j]
        if s < t:
            marked.append(k)
    return marked


def _apply_oracle(qc, idx, flag, marked, m):
    # eq_3: O_t |k>|b> = |k>|b xor f_t(k)>, one multi-controlled X per marked k.
    # Padding indices k >= n are never marked.
    for k in marked:
        zero_bits = [idx[q] for q in range(m) if not ((k >> q) & 1)]
        for q in zero_bits:
            qc.x(q)
        if m == 1:
            qc.cx(idx[0], flag)
        else:
            qc.mcx(list(idx), flag)
        for q in zero_bits:
            qc.x(q)


def _apply_diffusion(qc, idx, m):
    # eq_4: 2|psi><psi| - I on the index register (implemented up to a global phase of -1),
    # psi = uniform superposition over all 2^m basis states of idx.
    for q in idx:
        qc.h(q)
    for q in idx:
        qc.x(q)
    if m == 1:
        qc.z(idx[0])
    else:
        qc.h(idx[m - 1])
        qc.mcx(list(idx[: m - 1]), idx[m - 1])
        qc.h(idx[m - 1])
    for q in idx:
        qc.x(q)
    for q in idx:
        qc.h(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('matrix', 'i', 'j', 'threshold', 'iterations'):
        if key not in instance:
            raise ValueError('missing instance key: ' + key)
    matrix = _parse_matrix(instance['matrix'])
    n = len(matrix)
    i = _parse_index(instance['i'], n, 'i')
    j = _parse_index(instance['j'], n, 'j')
    t = _parse_threshold(instance['threshold'])
    r = instance['iterations']
    if isinstance(r, bool) or not isinstance(r, int) or r < 0:
        raise ValueError('iterations must be a nonnegative integer')
    m = int(math.ceil(math.log2(n)))
    if (1 << m) < n:
        m += 1
    if m < 1:
        m = 1
    if m + 1 > MAX_QUBITS:
        raise ValueError('instance requires more than %d qubits' % MAX_QUBITS)
    marked = _marked_indices(matrix, i, j, t)
    idx = QuantumRegister(m, 'idx')
    flag_reg = QuantumRegister(1, 'flag')
    qc = QuantumCircuit(idx, flag_reg, name='grover_threshold_minplus')
    flag = flag_reg[0]
    # eq_4: G_t = (2|psi><psi| - I) O_t applied r times.
    for _ in range(r):
        _apply_oracle(qc, idx, flag, marked, m)
        _apply_diffusion(qc, idx, m)
    return qc
