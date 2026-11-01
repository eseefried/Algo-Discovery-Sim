from qiskit import QuantumCircuit, QuantumRegister


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    d = instance.get('d')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 3:
        raise ValueError('n must be an integer in 1..3')
    if isinstance(d, bool) or not isinstance(d, int) or d < 1 or d > 2:
        raise ValueError('d must be 1 or 2')
    coeffs = instance.get('coefficients')
    if not isinstance(coeffs, dict):
        raise ValueError('coefficients must be a dict')
    mons = {}
    for key, val in coeffs.items():
        if not isinstance(key, str) or key == '':
            raise ValueError('bad coefficient key')
        if isinstance(val, bool):
            val = int(val)
        if val not in (0, 1) or not isinstance(val, int):
            raise ValueError('coefficients must be 0 or 1')
        if key == '0':
            S = ()
        else:
            if not key.isdigit():
                raise ValueError('bad coefficient key')
            S = tuple(int(ch) for ch in key)
            if len(S) > d:
                if val:
                    raise ValueError('monomial degree exceeds d')
            for a, b in zip(S, S[1:]):
                if a >= b:
                    raise ValueError('monomial indices must be strictly increasing')
            if any(j < 1 or j > n for j in S):
                raise ValueError('variable index out of range')
        if S in mons:
            raise ValueError('duplicate key')
        mons[S] = val
    return n, d, mons


def _phase(qc, qs):
    # multi-controlled Z on the listed qubits (phase -1 iff all are 1)
    k = len(qs)
    if k == 1:
        qc.z(qs[0])
    elif k == 2:
        qc.cz(qs[0], qs[1])
    elif k == 3:
        qc.ccz(qs[0], qs[1], qs[2])
    else:
        raise ValueError('unsupported monomial size')


def _restricted_oracle(qc, ctrl, qmap, mons, i, val):
    # eq_2: controlled phase oracle C-O_f with x_i fixed to val (val in {0,1});
    # each monomial prod_{j in S} x_j becomes a (multi-)controlled Z.
    for S, c in mons.items():
        if not c:
            continue
        if i in S:
            if val == 0:
                continue
            rest = [j for j in S if j != i]
        else:
            rest = list(S)
        _phase(qc, [ctrl] + [qmap[j] for j in rest])


def build_circuit(instance):
    """Derivative-BV identification of a multilinear F_2 polynomial (n<=3, d<=2).

    Layout: block i (1..n) occupies qubits (i-1)*n .. i*n-1: first the ancilla a_i,
    then the variables j != i ascending. Final qubit n*n is a0.
    """
    n, d, mons = _parse(instance)
    nq = n * n + 1
    if nq > 12:
        raise ValueError('too many qubits')
    qr = QuantumRegister(nq, 'q')
    qc = QuantumCircuit(qr)
    a0 = n * n
    blocks = []
    for i in range(1, n + 1):
        base = (i - 1) * n
        others = [j for j in range(1, n + 1) if j != i]
        qmap = {j: base + 1 + others.index(j) for j in others}
        blocks.append((i, base, qmap))
    # input layer: H on ancillas and x registers
    for i, base, qmap in blocks:
        qc.h(base)
        for q in qmap.values():
            qc.h(q)
    qc.h(a0)
    # eq_3/eq_4: derivative phase (-1)^{b D_i f(x)} = C-O_f(x_i=1) * C-O_f(x_i=0)
    for i, base, qmap in blocks:
        _restricted_oracle(qc, base, qmap, mons, i, 1)
        _restricted_oracle(qc, base, qmap, mons, i, 0)
    # eq_5: C-O_f on fixed |0..0> gives phase (-1)^{b c_0} on the control only
    if mons.get((), 0):
        qc.z(a0)
    # output layer
    for i, base, qmap in blocks:
        qc.h(base)
        for q in qmap.values():
            qc.h(q)
    qc.h(a0)
    return qc
