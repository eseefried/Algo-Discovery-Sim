from qiskit import QuantumCircuit, QuantumRegister


def _spec():
    # kind -> (quantum cost, arity); eq_2 cost values
    return {"not": (1, 1), "cnot": (1, 2), "toffoli": (5, 3), "peres": (4, 3), "fredkin": (7, 3)}


def _step(x, kind, q):
    # classical action of one gate on basis integer x (qubit 0 = LSB)
    if kind == "not":
        return x ^ (1 << q[0])
    if kind == "cnot":
        return x ^ (1 << q[1]) if (x >> q[0]) & 1 else x
    if kind == "toffoli":
        return x ^ (1 << q[2]) if ((x >> q[0]) & 1) and ((x >> q[1]) & 1) else x
    if kind == "peres":
        y = _step(x, "toffoli", q)
        return _step(y, "cnot", q[:2])
    if (x >> q[0]) & 1:
        a = (x >> q[1]) & 1
        b = (x >> q[2]) & 1
        if a != b:
            x ^= (1 << q[1]) | (1 << q[2])
    return x


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def build_circuit(instance):
    """Build the cascade pi = g_m o ... o g_1 (g_1 applied first) on 4 wires.

    instance: {"gates": [{"type": str, "qubits": [int,...]}, ...],
               "max_cost": optional int, "target": optional list of 16 ints}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("num_wires", 4)
    if not _is_int(n) or n != 4:
        raise ValueError("num_wires must be 4")
    gates = instance.get("gates")
    if not isinstance(gates, list) or len(gates) > 64:
        raise ValueError("gates must be a list of at most 64 gates")
    spec = _spec()
    parsed = []
    total = 0
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError("each gate must be a dict")
        kind = g.get("type")
        q = g.get("qubits")
        if kind not in spec:
            raise ValueError("unknown gate type")
        cost, arity = spec[kind]
        if not isinstance(q, list) or len(q) != arity:
            raise ValueError("wrong number of qubits for gate")
        for v in q:
            if not _is_int(v) or v < 0 or v >= n:
                raise ValueError("qubit index out of range")
        if len(set(q)) != len(q):
            raise ValueError("qubits of a gate must be distinct")
        parsed.append((kind, list(q)))
        total += cost
    max_cost = instance.get("max_cost")
    if max_cost is not None:
        if not _is_int(max_cost) or max_cost < 0:
            raise ValueError("max_cost must be a nonnegative int")
        if total > max_cost:
            raise ValueError("network quantum cost exceeds max_cost")
    target = instance.get("target")
    if target is not None:
        if not isinstance(target, list) or len(target) != 16:
            raise ValueError("target must be a list of 16 ints")
        if not all(_is_int(t) for t in target) or sorted(target) != list(range(16)):
            raise ValueError("target must be a permutation of 0..15")
        for x in range(16):
            y = x
            for kind, q in parsed:
                y = _step(y, kind, q)
            if y != target[x]:
                raise ValueError("network does not realize target permutation")
    reg = QuantumRegister(n, "q")
    qc = QuantumCircuit(reg)
    for kind, q in parsed:
        if kind == "not":
            qc.x(q[0])
        elif kind == "cnot":
            qc.cx(q[0], q[1])
        elif kind == "toffoli":
            qc.ccx(q[0], q[1], q[2])
        elif kind == "peres":
            qc.ccx(q[0], q[1], q[2])
            qc.cx(q[0], q[1])
        else:
            qc.cswap(q[0], q[1], q[2])
    return qc
