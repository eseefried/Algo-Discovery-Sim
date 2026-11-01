from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    '''Depth-2 balanced NAND-tree coined quantum walk, U^T with x compiled in.
    Qubits 0-2: pos (vertex heap index, little-endian). Qubits 3-4: coin (direction 0=parent, 1=left child, 2=right child, 3=unused).
    '''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    x = instance.get('x')
    if not isinstance(x, (list, tuple)) or len(x) != 4:
        raise ValueError('x must be a list of 4 bits')
    bits = []
    for v in x:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError('x entries must be 0 or 1')
        bits.append(v)
    steps = instance.get('steps', 2)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 32:
        raise ValueError('steps must be an integer in 1..32')
    pos = QuantumRegister(3, 'pos')
    coin = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(pos, coin)
    n = 5
    # Edge list (u, v, dir_at_u, dir_at_v). Tail-root and internal edges always present.
    edges = [(0, 1, 1, 0), (1, 2, 1, 0), (1, 3, 2, 0)]
    # Leaf edge present iff x_i = 1 (O_x compiled from x).
    for leaf in range(4):
        if bits[leaf] == 1:
            edges.append((2 + leaf // 2, 4 + leaf, 1 + leaf % 2, 0))

    def swap_states(s, t):
        # Exact transposition of computational basis states s and t.
        diff = [i for i in range(n) if ((s >> i) & 1) != ((t >> i) & 1)]
        k = diff[0]
        others = diff[1:]
        for j in others:
            qc.cx(k, j)
        ctrl = []
        vals = []
        for i in range(n):
            if i == k:
                continue
            val = (s >> i) & 1
            if i in others:
                val ^= (s >> k) & 1
            ctrl.append(i)
            vals.append(val)
        for i, val in zip(ctrl, vals):
            if val == 0:
                qc.x(i)
        qc.mcx(ctrl, k)
        for i, val in zip(ctrl, vals):
            if val == 0:
                qc.x(i)
        for j in reversed(others):
            qc.cx(k, j)

    for _ in range(steps):
        # O_x: flip-flop shift over edges present for this x
        for (u, v, du, dv) in edges:
            swap_states(u | (du << 3), v | (dv << 3))
        # R_graph: Grover diffusion (I - 2|s><s|) on the coin register
        qc.h(3)
        qc.h(4)
        qc.x(3)
        qc.x(4)
        qc.cz(3, 4)
        qc.x(3)
        qc.x(4)
        qc.h(3)
        qc.h(4)
    return qc
