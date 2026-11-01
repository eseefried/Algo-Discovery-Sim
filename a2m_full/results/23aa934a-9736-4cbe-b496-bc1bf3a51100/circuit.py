from qiskit import QuantumCircuit, QuantumRegister
import math


def _int_param(instance, key):
    value = instance.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(key + ' must be an integer')
    return value


def _closed_edge_swaps(qc, pos, coin, edges, m, sites):
    # Z: for each edge e, if closed (ancilla=0) swap |e,c=0> with |e+1,c=1>.
    # Implemented as CX-conjugated multi-controlled X on the coin qubit (eq_2).
    for e in range(sites - 1):
        anc = edges[e]
        diff = [i for i in range(m) if ((e >> i) & 1) != (((e + 1) >> i) & 1)]
        for d in diff:
            qc.cx(coin, pos[d])
        zeros = [pos[i] for i in range(m) if not ((e >> i) & 1)]
        for q in zeros:
            qc.x(q)
        qc.x(anc)
        qc.mcx(list(pos) + [anc], coin)
        qc.x(anc)
        for q in zeros:
            qc.x(q)
        for d in diff:
            qc.cx(coin, pos[d])


def _cycle_shift(qc, pos, coin, m):
    # T: cyclic permutation (0,0)->(1,0)->...->(L-1,0)->(L-1,1)->...->(0,1)->(0,0) (eq_2).
    # Encode k = x for c=0 and k = 2L-1-x for c=1 (CX from coin onto position),
    # increment k mod 2L with the coin as most significant bit, then undo the encoding.
    for q in pos:
        qc.cx(coin, q)
    qs = list(pos) + [coin]
    for i in range(m, -1, -1):
        ctrls = qs[:i]
        if len(ctrls) == 0:
            qc.x(qs[i])
        elif len(ctrls) == 1:
            qc.cx(ctrls[0], qs[i])
        else:
            qc.mcx(ctrls, qs[i])
    for q in pos:
        qc.cx(coin, q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    m = _int_param(instance, 'num_position_qubits')
    steps = _int_param(instance, 'steps')
    p = instance.get('p')
    if isinstance(p, bool) or not isinstance(p, (int, float)):
        raise ValueError('p must be a number')
    p = float(p)
    if not (p == p) or p < 0.0 or p > 1.0:
        raise ValueError('p must be in [0,1]')
    if m < 1 or m > 3:
        raise ValueError('num_position_qubits must be in 1..3')
    if steps < 1:
        raise ValueError('steps must be >= 1')
    sites = 2 ** m
    n_edges = sites - 1
    total = m + 1 + n_edges * steps
    if total > 12:
        raise ValueError('total qubits would exceed 12')
    pos_reg = QuantumRegister(m, 'pos')
    coin_reg = QuantumRegister(1, 'coin')
    edge_regs = [QuantumRegister(n_edges, 'edge' + str(s)) for s in range(steps)]
    qc = QuantumCircuit(pos_reg, coin_reg, *edge_regs)
    pos = list(pos_reg)
    coin = coin_reg[0]
    theta = 2.0 * math.asin(math.sqrt(p))
    for s in range(steps):
        edges = list(edge_regs[s])
        # eq_3: fresh edge ancillas, open with probability p
        for a in edges:
            qc.ry(theta, a)
        # eq_2: U_omega = S_omega (I x H)
        qc.h(coin)
        _closed_edge_swaps(qc, pos, coin, edges, m, sites)
        _cycle_shift(qc, pos, coin, m)
    return qc
