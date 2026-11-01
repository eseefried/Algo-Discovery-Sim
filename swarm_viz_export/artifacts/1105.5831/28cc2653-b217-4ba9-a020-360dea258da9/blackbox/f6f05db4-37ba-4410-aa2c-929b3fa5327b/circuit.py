from qiskit import QuantumCircuit, QuantumRegister


def _gate_cost(num_controls):
    # eq_3: standard quantum cost qc(g): NOT=1, CNOT=1, TOF3=5, TOF4=13
    if num_controls == 0 or num_controls == 1:
        return 1
    if num_controls == 2:
        return 5
    if num_controls == 3:
        return 13
    raise ValueError("unsupported gate size")


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def build_circuit(instance):
    """Compile a Toffoli network to a unitary circuit.

    instance: {"num_qubits": int in 1..12,
               "gates": [{"controls": [ints, at most 3], "target": int}, ...],
               optional "max_qc": int}
    gates[0] is applied first (G_1).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("num_qubits")
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError("num_qubits must be an integer in 1..12")
    gates = instance.get("gates")
    if not isinstance(gates, list) or len(gates) > 500:
        raise ValueError("gates must be a list of at most 500 gates")
    parsed = []
    total_cost = 0
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError("each gate must be a dict")
        ctrls = g.get("controls")
        tgt = g.get("target")
        if not isinstance(ctrls, list) or len(ctrls) > 3:
            raise ValueError("controls must be a list of at most 3 indices")
        if not _is_int(tgt):
            raise ValueError("target must be an integer")
        idx = list(ctrls) + [tgt]
        for q in idx:
            if not _is_int(q) or q < 0 or q >= n:
                raise ValueError("qubit index out of range")
        if len(set(idx)) != len(idx):
            raise ValueError("gate qubits must be distinct")
        if len(ctrls) == 3 and n < 4:
            raise ValueError("too few qubits")
        total_cost += _gate_cost(len(ctrls))
        parsed.append((list(ctrls), tgt))
    max_qc = instance.get("max_qc")
    if max_qc is not None:
        if not _is_int(max_qc) or max_qc < 0:
            raise ValueError("max_qc must be a non-negative integer")
        if total_cost > max_qc:
            raise ValueError("network quantum cost exceeds max_qc")
    # eq_1 / eq_2: qubit q_i holds bit i (little-endian); U = G_k ... G_1
    qc = QuantumCircuit(QuantumRegister(n, "q"))
    for ctrls, tgt in parsed:
        k = len(ctrls)
        if k == 0:
            qc.x(tgt)
        elif k == 1:
            qc.cx(ctrls[0], tgt)
        elif k == 2:
            qc.ccx(ctrls[0], ctrls[1], tgt)
        else:
            qc.mcx(ctrls, tgt)
    return qc
