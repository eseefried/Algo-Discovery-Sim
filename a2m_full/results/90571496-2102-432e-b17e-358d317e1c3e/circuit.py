from qiskit import QuantumCircuit, QuantumRegister


def _int(v, lo, hi, name):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " out of range or not an integer")
    return v


def _parse_gate(g, nq):
    if not isinstance(g, dict):
        raise ValueError("gate must be an object")
    ctrls = g.get("controls")
    if not isinstance(ctrls, list) or len(ctrls) > 2:
        raise ValueError("controls must be a list of at most 2 indices")
    cs = [_int(c, 0, nq - 1, "control") for c in ctrls]
    t = _int(g.get("target"), 0, nq - 1, "target")
    if t in cs or len(set(cs)) != len(cs):
        raise ValueError("gate qubits must be distinct")
    return (cs, t)


def _apply(qc, gate):
    cs, t = gate
    if len(cs) == 0:
        qc.x(t)
    elif len(cs) == 1:
        qc.cx(cs[0], t)
    else:
        qc.ccx(cs[0], cs[1], t)


def build_circuit(instance):
    """Palindromic NCT circuit h c h^-1 (eq_2, eq_3) on n data lines + optional ancilla (eq_5).
    instance: {"n":2..4, "ancilla":0|1, "half":[{"controls":[..],"target":t},..], "center":gate|null}
    Qubit indices: data 0..n-1 (little-endian), ancilla = n."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be an object")
    n = _int(instance.get("n"), 2, 4, "n")
    anc = _int(instance.get("ancilla", 0), 0, 1, "ancilla")
    nq = n + anc
    if nq > 12:
        raise ValueError("too many qubits")
    raw = instance.get("half", [])
    if not isinstance(raw, list) or len(raw) > 64:
        raise ValueError("half must be a list of at most 64 gates")
    half = [_parse_gate(g, nq) for g in raw]
    center_raw = instance.get("center")
    center = None
    if center_raw is not None:
        center = _parse_gate(center_raw, nq)
    if len(half) == 0 and center is None:
        raise ValueError("empty circuit")
    data = QuantumRegister(n, "data")
    if anc:
        qc = QuantumCircuit(data, QuantumRegister(1, "anc"))
    else:
        qc = QuantumCircuit(data)
    # g_1 ... g_k
    for g in half:
        _apply(qc, g)
    # optional central self-inverse gate c
    if center is not None:
        _apply(qc, center)
    # mirrored g_k ... g_1 (h^-1 for self-inverse gates)
    for g in reversed(half):
        _apply(qc, g)
    return qc
