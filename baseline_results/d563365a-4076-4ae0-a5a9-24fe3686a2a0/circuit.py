'''Unitary Permutation problem: query-model upper bound via a Karp permutation-supersequence word.

Operation implemented (eq_1, eq_2):
  W |sigma>_C |psi>_D |0>_A |0>_t = |sigma>_C (U_sigma |psi>)_D |g>_A |0>_t,
  U_sigma = U_{sigma(n)} ... U_{sigma(1)},  |g> = prod_i U_i^{m_i-1}|0>  (sigma independent, eq_6).

Register layout (Qiskit index 0 = least significant bit):
  C   : n*b qubits, b = ceil(log2 n), indices 0 .. n*b-1. Block k (k=0..n-1) occupies
        indices [k*b, (k+1)*b) and stores sigma(k+1)-1 in binary, index k*b being its LSB.
  D   : 1 data qubit, index n*b.
  A_i : 1 dummy qubit for each symbol i with multiplicity m_i >= 2 in w, in increasing i,
        indices n*b+1, n*b+2, ...
  t   : 1 activity ancilla, last index.
Black boxes U_i are single-qubit u(theta, phi, lam) gates given by the instance.
'''
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
# eq_3 / eq_7: default Karp words (all permutations of {1..n} occur as subsequences)
DEFAULT_WORDS = {2: [1, 2, 1], 3: [1, 2, 1, 3, 1, 2, 1]}


def _permutations(items):
    if len(items) <= 1:
        return [list(items)]
    out = []
    for idx in range(len(items)):
        rest = items[:idx] + items[idx + 1:]
        for tail in _permutations(rest):
            out.append([items[idx]] + tail)
    return out


def _greedy_embedding(word, perm):
    # eq_4: deterministic (leftmost) embedding p_sigma of sigma as a subsequence of w.
    # Positions are 0-based here (spec eq_3 uses 1-based positions).
    positions = []
    pos = 0
    for sym in perm:
        while pos < len(word) and word[pos] != sym:
            pos += 1
        if pos >= len(word):
            return None
        positions.append(pos)
        pos += 1
    return positions


def _parse_instance(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError('n must be an integer >= 2')
    gates = instance.get('gates')
    if not isinstance(gates, list) or len(gates) != n:
        raise ValueError('gates must be a list of n [theta, phi, lam] triples')
    parsed_gates = []
    for g in gates:
        if not isinstance(g, (list, tuple)) or len(g) != 3:
            raise ValueError('each gate must be a [theta, phi, lam] triple')
        angles = []
        for a in g:
            if isinstance(a, bool) or not isinstance(a, (int, float)) or not math.isfinite(float(a)):
                raise ValueError('gate angles must be finite real numbers')
            angles.append(float(a))
        parsed_gates.append(angles)
    word = instance.get('word')
    if word is None:
        if n not in DEFAULT_WORDS:
            raise ValueError('no default word for this n; supply word explicitly')
        word = list(DEFAULT_WORDS[n])
    if not isinstance(word, list) or len(word) == 0:
        raise ValueError('word must be a non-empty list of integers in 1..n')
    for s in word:
        if isinstance(s, bool) or not isinstance(s, int) or s < 1 or s > n:
            raise ValueError('word symbols must be integers in 1..n')
    return n, parsed_gates, list(word)


def _activity(qc, creg, tq, n, b, perms, flags):
    # eq_5: T_j computes a_j(sigma) into t as a sum of projector-controlled X gates:
    # for every sigma with a_j(sigma) = 1, flip t when C holds |sigma>.  Self-inverse.
    if all(flags):
        qc.x(tq)
        return
    for perm, flag in zip(perms, flags):
        if not flag:
            continue
        zero_qubits = []
        for k in range(n):
            val = perm[k] - 1
            for l in range(b):
                if not ((val >> l) & 1):
                    zero_qubits.append(creg[k * b + l])
        for q in zero_qubits:
            qc.x(q)
        qc.mcx(list(creg), tq)
        for q in zero_qubits:
            qc.x(q)


def _routed_call(qc, dq, aq, tq, angles):
    # eq_5: CSWAP^{(t=0)}_{D,A}  U_{w_j} on D  CSWAP^{(t=0)}_{D,A}  (exactly one black-box call)
    qc.x(tq)
    qc.cswap(tq, dq, aq)
    qc.x(tq)
    qc.u(angles[0], angles[1], angles[2], dq)
    qc.x(tq)
    qc.cswap(tq, dq, aq)
    qc.x(tq)


def build_circuit(instance):
    n, gates, word = _parse_instance(instance)
    perms = _permutations(list(range(1, n + 1)))
    # eq_3: verify that w contains every permutation as a subsequence; store embeddings (eq_4)
    embeddings = []
    for perm in perms:
        emb = _greedy_embedding(word, perm)
        if emb is None:
            raise ValueError('word does not contain every permutation as a subsequence')
        embeddings.append(emb)
    b = 1
    while (1 << b) < n:
        b += 1
    mult = [0] * (n + 1)
    for s in word:
        mult[s] += 1
    dummy_symbols = [i for i in range(1, n + 1) if mult[i] >= 2]
    total = n * b + 1 + len(dummy_symbols) + 1
    if total > MAX_QUBITS:
        raise ValueError('instance needs %d qubits, exceeding the cap of %d' % (total, MAX_QUBITS))
    creg = QuantumRegister(n * b, 'c')
    dreg = QuantumRegister(1, 'd')
    aregs = {}
    reg_list = [creg, dreg]
    for i in dummy_symbols:
        aregs[i] = QuantumRegister(1, 'a%d' % i)
        reg_list.append(aregs[i])
    treg = QuantumRegister(1, 't')
    reg_list.append(treg)
    qc = QuantumCircuit(*reg_list)
    dq = dreg[0]
    tq = treg[0]
    # eq_6: W = G_L ... G_1, one black-box call per letter of w
    for j in range(len(word)):
        sym = word[j]
        angles = gates[sym - 1]
        if mult[sym] == 1:
            # unique occurrence of sym: active for every sigma, no routing needed (eq_4 with a_j = 1)
            qc.u(angles[0], angles[1], angles[2], dq)
            continue
        flags = [j in emb for emb in embeddings]
        _activity(qc, creg, tq, n, b, perms, flags)      # T_j
        _routed_call(qc, dq, aregs[sym][0], tq, angles)  # G_j core, one call to U_{w_j}
        _activity(qc, creg, tq, n, b, perms, flags)      # T_j^dagger (self-inverse)
    return qc
