from qiskit import QuantumCircuit, QuantumRegister


def _swap_states(qc, m, s, t):
    """Transposition of computational basis states s and t on qubits 0..m-1."""
    diff = [b for b in range(m) if ((s ^ t) >> b) & 1]
    d0 = diff[0]
    others = diff[1:]
    for b in others:
        qc.cx(d0, b)
    sp = s
    for b in others:
        if (sp >> d0) & 1:
            sp ^= (1 << b)
    ctrls = [b for b in range(m) if b != d0]
    cs = 0
    for i, b in enumerate(ctrls):
        if (sp >> b) & 1:
            cs |= (1 << i)
    qc.mcx(ctrls, d0, ctrl_state=cs)
    for b in reversed(others):
        qc.cx(d0, b)


def _increment(qc, m):
    """y -> y+1 mod 2^m on qubits 0..m-1 (qubit 0 least significant)."""
    for b in range(m - 1, 0, -1):
        qc.mcx(list(range(b)), b)
    qc.x(0)


def build_circuit(instance):
    """Percolated coined walk on an open chain, U_w = S_w (I (x) H) per step.
    instance: {'n_pos': int in [1,11], 'edge_configs': list of steps; each step is a
    list of N-1 values in {0,1} (1 = edge (x,x+1) present), N = 2**n_pos}.
    Qubits 0..n_pos-1: position (LSB first); qubit n_pos: coin.
    Coin 0 moves right, coin 1 moves left, blocked edge/boundary -> stay and flip coin.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_pos')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n + 1 > 12:
        raise ValueError('n_pos must be an integer in [1, 11]')
    cfgs = instance.get('edge_configs')
    if not isinstance(cfgs, (list, tuple)) or len(cfgs) < 1 or len(cfgs) > 64:
        raise ValueError('edge_configs must be a list of 1..64 configurations')
    N = 2 ** n
    for cfg in cfgs:
        if not isinstance(cfg, (list, tuple)) or len(cfg) != N - 1:
            raise ValueError('each configuration needs N-1 entries')
        for v in cfg:
            if not (isinstance(v, (bool, int)) and v in (0, 1)):
                raise ValueError('edge entries must be 0 or 1')
    m = n + 1
    pos = QuantumRegister(n, 'pos')
    coin = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pos, coin)
    for cfg in cfgs:
        # coin operator I (x) H
        qc.h(n)
        # unfold: ring index y = (coin, x if coin==0 else ~x); qubit order matches basis index
        for b in range(n):
            qc.cx(n, b)
        # all-edges-present shift is y -> y+1 mod 2N
        _increment(qc, m)
        # absent edge x: swap images y=x+1 and y=2N-1-x (reflection)
        for x in range(N - 1):
            if not cfg[x]:
                _swap_states(qc, m, x + 1, 2 * N - 1 - x)
        # refold
        for b in range(n):
            qc.cx(n, b)
    return qc
