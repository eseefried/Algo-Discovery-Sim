from qiskit import QuantumCircuit, QuantumRegister

_ARITY = {"x": 1, "cx": 2, "ccx": 3}


def _normalize_gate(g, n):
    if not isinstance(g, (list, tuple)) or len(g) < 2:
        raise ValueError("each gate must be [name, qubit, ...]")
    name = g[0]
    if not isinstance(name, str) or name.lower() not in _ARITY:
        raise ValueError("unsupported gate name")
    name = name.lower()
    qs = list(g[1:])
    if len(qs) != _ARITY[name]:
        raise ValueError("wrong number of qubits for gate")
    for q in qs:
        if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
            raise ValueError("qubit index out of range")
    if len(set(qs)) != len(qs):
        raise ValueError("qubits must be distinct")
    if name == "ccx":
        # controls are symmetric; canonicalize so equality is of the actual gate
        qs = sorted(qs[:2]) + [qs[2]]
    return (name, tuple(qs))


def build_circuit(instance):
    """Palindromic circuit over self-inverse gates (eq_2). Qubit i = bit i of x (LSB = qubit 0)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n must be an integer in [1, 12]")
    gates = instance.get("gates")
    if not isinstance(gates, (list, tuple)) or len(gates) > 200:
        raise ValueError("gates must be a list of at most 200 gates")
    norm = [_normalize_gate(g, n) for g in gates]
    # eq_2: g_i = g_{k+1-i} for all i
    if norm != norm[::-1]:
        raise ValueError("gate sequence is not palindromic")
    qr = QuantumRegister(n, "x")
    qc = QuantumCircuit(qr)
    for name, qs in norm:
        if name == "x":
            qc.x(qr[qs[0]])
        elif name == "cx":
            qc.cx(qr[qs[0]], qr[qs[1]])
        else:
            qc.ccx(qr[qs[0]], qr[qs[1]], qr[qs[2]])
    return qc
