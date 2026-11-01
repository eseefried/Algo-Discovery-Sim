from qiskit import QuantumCircuit, QuantumRegister


def _perm(mask):
    perm = [0] * 8
    for x in range(4):
        for c in (0, 1):
            s = x + 4 * c
            if c == 1:
                t = (x + 1) % 4 + 4 if mask[x] else x
            else:
                t = (x - 1) % 4 if mask[(x - 1) % 4] else x + 4
            perm[s] = t
    return perm


def _swap_states(qc, a, b):
    diff = a ^ b
    t = (diff & -diff).bit_length() - 1
    others = [d for d in range(3) if d != t and (diff >> d) & 1]
    ap = a
    for d in others:
        if (a >> t) & 1:
            ap ^= (1 << d)
    controls = [q for q in range(3) if q != t]
    zeros = [q for q in controls if not (ap >> q) & 1]
    for d in others:
        qc.cx(t, d)
    for q in zeros:
        qc.x(q)
    qc.mcx(controls, t)
    for q in zeros:
        qc.x(q)
    for d in reversed(others):
        qc.cx(t, d)


def _parse_masks(instance):
    if not isinstance(instance, dict) or 'masks' not in instance:
        raise ValueError('instance must be a dict with key masks')
    masks = instance['masks']
    if not isinstance(masks, (list, tuple)) or len(masks) < 1 or len(masks) > 32:
        raise ValueError('masks must be a list of 1..32 masks')
    parsed = []
    for m in masks:
        if not isinstance(m, (list, tuple)) or len(m) != 4:
            raise ValueError('each mask must have 4 entries')
        row = []
        for v in m:
            if isinstance(v, bool):
                row.append(int(v))
            elif isinstance(v, int) and v in (0, 1):
                row.append(v)
            else:
                raise ValueError('mask entries must be 0 or 1')
        parsed.append(row)
    return parsed


def build_circuit(instance):
    """Qubits: pos0,pos1 (x=x0+2*x1) then coin (0=L,1=R). Per step: H on coin, then shift S_w."""
    parsed = _parse_masks(instance)
    pos = QuantumRegister(2, 'pos')
    coin = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pos, coin)
    for mask in parsed:
        qc.h(2)
        perm = _perm(mask)
        seen = [False] * 8
        for s in range(8):
            if seen[s]:
                continue
            cyc = [s]
            seen[s] = True
            n = perm[s]
            while n != s:
                cyc.append(n)
                seen[n] = True
                n = perm[n]
            for j in range(1, len(cyc)):
                _swap_states(qc, cyc[0], cyc[j])
    return qc
