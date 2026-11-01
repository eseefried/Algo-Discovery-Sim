from qiskit import QuantumCircuit, QuantumRegister

_ONE = ("h", "s", "sdg", "t", "tdg", "x", "z")


def _int(v, lo, hi, name):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " invalid")
    return v


def _swap(qc, q, p, occ, loc):
    # eq_4: SWAP = CX_ab CX_ba CX_ab on adjacent physical qubits p, p+1; tracks permutation
    a = q[p]
    b = q[p + 1]
    qc.cx(a, b)
    qc.cx(b, a)
    qc.cx(a, b)
    la = occ[p]
    lb = occ[p + 1]
    occ[p] = lb
    occ[p + 1] = la
    loc[la] = p + 1
    loc[lb] = p


def _single(qc, name, qubit):
    if name == "h":
        qc.h(qubit)
    elif name == "s":
        qc.s(qubit)
    elif name == "sdg":
        qc.sdg(qubit)
    elif name == "t":
        qc.t(qubit)
    elif name == "tdg":
        qc.tdg(qubit)
    elif name == "x":
        qc.x(qubit)
    elif name == "z":
        qc.z(qubit)
    else:
        raise ValueError("unknown gate")


def build_circuit(instance):
    """Route a logical Clifford+T gate list onto a line of n physical qubits.

    instance: {"n": int 2..12,
               "gates": [["h", l], ["t", l], ["cx", control, target], ...] (logical indices),
               "placement": optional permutation, logical i starts at physical placement[i],
               "restore_permutation": optional bool, undo routing permutation at the end}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be an object")
    n = _int(instance.get("n"), 2, 12, "n")
    gates = instance.get("gates")
    if not isinstance(gates, list) or len(gates) > 500:
        raise ValueError("gates invalid")
    placement = instance.get("placement", list(range(n)))
    if not isinstance(placement, list) or len(placement) != n:
        raise ValueError("placement invalid")
    for p in placement:
        _int(p, 0, n - 1, "placement entry")
    if sorted(placement) != list(range(n)):
        raise ValueError("placement must be a permutation")
    restore = instance.get("restore_permutation", False)
    if not isinstance(restore, bool):
        raise ValueError("restore_permutation must be bool")
    parsed = []
    for g in gates:
        if not isinstance(g, (list, tuple)) or len(g) < 2 or not isinstance(g[0], str):
            raise ValueError("bad gate")
        name = g[0]
        if name in _ONE:
            if len(g) != 2:
                raise ValueError("bad gate arity")
            parsed.append((name, _int(g[1], 0, n - 1, "qubit"), -1))
        elif name == "cx":
            if len(g) != 3:
                raise ValueError("bad gate arity")
            c = _int(g[1], 0, n - 1, "control")
            t = _int(g[2], 0, n - 1, "target")
            if c == t:
                raise ValueError("cx needs distinct qubits")
            parsed.append((name, c, t))
        else:
            raise ValueError("unsupported gate")
    q = QuantumRegister(n, "q")
    qc = QuantumCircuit(q)
    loc = list(placement)
    occ = [0] * n
    for l, p in enumerate(placement):
        occ[p] = l
    for name, a, b in parsed:
        if name != "cx":
            _single(qc, name, q[loc[a]])
            continue
        # eq_4 routing: move control toward target until physically adjacent
        while abs(loc[a] - loc[b]) > 1:
            step = 1 if loc[b] > loc[a] else -1
            lo = loc[a] if step == 1 else loc[a] - 1
            _swap(qc, q, lo, occ, loc)
        qc.cx(q[loc[a]], q[loc[b]])
    if restore:
        # bubble sort by home position using adjacent SWAPs
        for i in range(n):
            for p in range(n - 1 - i):
                if placement[occ[p]] > placement[occ[p + 1]]:
                    _swap(qc, q, p, occ, loc)
    return qc
