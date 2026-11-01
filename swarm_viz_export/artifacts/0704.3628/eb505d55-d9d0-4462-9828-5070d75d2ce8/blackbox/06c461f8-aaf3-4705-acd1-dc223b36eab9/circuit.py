import math
from qiskit import QuantumCircuit


def _phase_on(qc, qubits, value):
    """Apply a -1 phase to the basis state `value` of the listed qubits (little-endian)."""
    zeros = [q for i, q in enumerate(qubits) if not (value >> i) & 1]
    for q in zeros:
        qc.x(q)
    qc.mcp(math.pi, qubits[:-1], qubits[-1])
    for q in zeros:
        qc.x(q)


def _coin3_gate():
    """Coin I - 2|s><s| on slots {0,1,2}, s uniform; identity on slot 3 (eq_2 coin)."""
    theta = 2.0 * math.asin(math.sqrt(1.0 / 3.0))
    w = QuantumCircuit(2)
    w.ry(theta, 1)
    w.ch(1, 0, ctrl_state=0)
    sub = QuantumCircuit(2)
    sub.compose(w.inverse(), inplace=True)
    sub.x([0, 1])
    sub.cz(0, 1)
    sub.x([0, 1])
    sub.compose(w, inplace=True)
    return sub.to_gate(label="coin3")


def _swap_states(qc, a, b):
    """Transposition of 5-qubit basis states a and b (index = slot + 4*vertex)."""
    diff = [i for i in range(5) if ((a ^ b) >> i) & 1]
    k = diff[0]
    others = diff[1:]
    for j in others:
        qc.cx(k, j)
    ap = a
    if (a >> k) & 1:
        for j in others:
            ap ^= (1 << j)
    controls = [i for i in range(5) if i != k]
    cs = 0
    for idx, c in enumerate(controls):
        cs |= ((ap >> c) & 1) << idx
    qc.mcx(controls, k, ctrl_state=cs)
    for j in reversed(others):
        qc.cx(k, j)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "x" not in instance or "steps" not in instance:
        raise ValueError("instance needs keys x and steps")
    x = instance["x"]
    if not isinstance(x, (list, tuple)) or len(x) != 4:
        raise ValueError("x must be a list of 4 bits")
    bits = []
    for v in x:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError("x entries must be 0 or 1")
        bits.append(v)
    t = instance["steps"]
    if isinstance(t, bool) or not isinstance(t, int) or t < 1 or t > 64:
        raise ValueError("steps must be an integer in 1..64")
    return bits, t


def _step(qc, x, coin3):
    """One walk step U_x = S_x C_x (eq_2)."""
    # coin: degree-1 vertices (tail and present leaves) get -1 on slot 0
    _phase_on(qc, [0, 1, 2, 3, 4], 0)
    for i in range(4):
        if x[i] == 1:
            _phase_on(qc, [0, 1, 2, 3, 4], 4 * (4 + i))
    # degree-3 coins at root, a, b
    for v in (1, 2, 3):
        qc.append(coin3.control(3, ctrl_state=v), [2, 3, 4, 0, 1])
    # flip-flop shift: swap |u, slot toward v> <-> |v, slot toward u>
    edges = [((0, 0), (1, 0), None), ((1, 1), (2, 0), None), ((1, 2), (3, 0), None),
             ((2, 1), (4, 0), 0), ((2, 2), (5, 0), 1), ((3, 1), (6, 0), 2), ((3, 2), (7, 0), 3)]
    for (u, su), (v, sv), leaf in edges:
        if leaf is not None and x[leaf] == 0:
            continue  # absent edge: self-loop, state fixed
        _swap_states(qc, su + 4 * u, sv + 4 * v)


def build_circuit(instance):
    x, t = _parse(instance)
    qc = QuantumCircuit(5, name="nand_walk")
    coin3 = _coin3_gate()
    for _ in range(t):
        _step(qc, x, coin3)
    return qc
