from qiskit import QuantumCircuit

_NQ = 3
_MAX_STEPS = 64


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    masks = instance.get('masks')
    if not isinstance(masks, (list, tuple)) or len(masks) < 1 or len(masks) > _MAX_STEPS:
        raise ValueError('masks must be a list of 1..64 edge masks')
    out = []
    for m in masks:
        if not isinstance(m, (list, tuple)) or len(m) != 4:
            raise ValueError('each mask needs exactly 4 entries')
        row = []
        for v in m:
            if isinstance(v, bool):
                row.append(int(v))
            elif isinstance(v, int) and v in (0, 1):
                row.append(v)
            else:
                raise ValueError('mask entries must be 0 or 1')
        out.append(row)
    prep = instance.get('prepare_initial_coin', False)
    if not isinstance(prep, bool):
        raise ValueError('prepare_initial_coin must be a bool')
    return out, prep


def _permutation(mask):
    # eq_1: basis index s = x + 4c, c=0 is L, c=1 is R. Returns pi with S|s> = |pi[s]>.
    pi = [0] * 8
    for x in range(4):
        if mask[x] == 1:
            pi[x + 4] = ((x + 1) % 4) + 4
        else:
            pi[x + 4] = x
        if mask[(x - 1) % 4] == 1:
            pi[x] = (x - 1) % 4
        else:
            pi[x] = x + 4
    if sorted(pi) != list(range(8)):
        raise ValueError('shift is not a bijection')
    return pi


def _transposition(qc, a, b):
    # Swap basis states a and b (little-endian indices on 3 qubits).
    diff = [k for k in range(_NQ) if ((a ^ b) >> k) & 1]
    t = diff[0]
    others = diff[1:]
    a2 = a
    for d in others:
        if (a >> t) & 1:
            a2 ^= (1 << d)
    for d in others:
        qc.cx(t, d)
    ctrls = [k for k in range(_NQ) if k != t]
    zeros = [k for k in ctrls if ((a2 >> k) & 1) == 0]
    for k in zeros:
        qc.x(k)
    qc.ccx(ctrls[0], ctrls[1], t)
    for k in zeros:
        qc.x(k)
    for d in reversed(others):
        qc.cx(t, d)


def _apply_permutation(qc, pi):
    # eq_2: forward map s -> pi[s]. Cycle (s0->s1->...->sk-1->s0) equals
    # transpositions (s0 s1),(s0 s2),...,(s0 s_{k-1}) applied in that order.
    seen = [False] * 8
    for s in range(8):
        if seen[s] or pi[s] == s:
            seen[s] = True
            continue
        cyc = []
        cur = s
        while not seen[cur]:
            seen[cur] = True
            cyc.append(cur)
            cur = pi[cur]
        for i in range(1, len(cyc)):
            _transposition(qc, cyc[0], cyc[i])


def build_circuit(instance):
    masks, prep = _parse(instance)
    qc = QuantumCircuit(_NQ, name='percolation_walk_trajectory')
    if prep:
        qc.h(2)  # eq_3 initial coin Hadamard: |x=0,c=0> -> |x=0,c=+>
    for mask in masks:
        qc.h(2)  # coin I_pos (x) H
        _apply_permutation(qc, _permutation(mask))  # shift S_omega
    return qc
