from qiskit import QuantumCircuit, QuantumRegister


def _gate_library():
    # eq_1 (Toffoli maps as permutations) and eq_3 (costs 1/1/5/13)
    lib = []
    for t in range(4):
        others = [i for i in range(4) if i != t]
        for m in range(8):
            ctrl = tuple(others[j] for j in range(3) if (m >> j) & 1)
            cost = {0: 1, 1: 1, 2: 5, 3: 13}[len(ctrl)]
            perm = tuple((x ^ (1 << t)) if all((x >> c) & 1 for c in ctrl) else x for x in range(16))
            lib.append((ctrl, t, cost, perm))
    return lib


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    pi = instance.get('pi')
    if not isinstance(pi, (list, tuple)) or len(pi) != 16:
        raise ValueError('pi must be a list of 16 integers')
    for v in pi:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('pi entries must be integers')
    if sorted(pi) != list(range(16)):
        raise ValueError('pi must be a permutation of 0..15')
    mc = instance.get('max_cost', 13)
    if isinstance(mc, bool) or not isinstance(mc, int) or mc < 0 or mc > 16:
        raise ValueError('max_cost must be an integer in 0..16')
    return tuple(pi), mc


def _search(target, max_cost):
    # eq_4: Dijkstra from identity with integer edge weights (bucket queue), pruned at max_cost
    lib = _gate_library()
    ident = tuple(range(16))
    dist = {ident: 0}
    pred = {}
    buckets = {0: [ident]}
    settled = set()
    found = False
    for c in range(max_cost + 1):
        for s in buckets.get(c, []):
            if s in settled or dist[s] != c:
                continue
            settled.add(s)
            if s == target:
                found = True
                break
            for gi in range(len(lib)):
                gp = lib[gi][3]
                nc = c + lib[gi][2]
                if nc > max_cost:
                    continue
                ns = tuple(gp[v] for v in s)  # g o sigma
                if ns not in dist or nc < dist[ns]:
                    dist[ns] = nc
                    pred[ns] = (s, gi)
                    buckets.setdefault(nc, []).append(ns)
        if found:
            break
    if not found:
        raise ValueError('no network with cost <= max_cost realizes pi')
    seq = []
    cur = target
    while cur != ident:
        prev, gi = pred[cur]
        seq.append(lib[gi])
        cur = prev
    seq.reverse()  # G_1 first
    return seq


def build_circuit(instance):
    """Build U_pi = G_k...G_1 (eq_2) from a QC-minimal network found by classical search."""
    pi, max_cost = _parse(instance)
    seq = _search(pi, max_cost)
    q = QuantumRegister(4, 'q')
    qc = QuantumCircuit(q)
    for ctrl, t, cost, perm in seq:
        if len(ctrl) == 0:
            qc.x(q[t])
        elif len(ctrl) == 1:
            qc.cx(q[ctrl[0]], q[t])
        elif len(ctrl) == 2:
            qc.ccx(q[ctrl[0]], q[ctrl[1]], q[t])
        else:
            qc.mcx([q[c] for c in ctrl], q[t])
    return qc
