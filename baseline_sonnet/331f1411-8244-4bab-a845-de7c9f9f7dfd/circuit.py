from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_GATES = 500


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    return v


def build_circuit(instance):
    """Build the Toffoli-type cascade f = G_n o ... o G_1 (eq_1).

    instance: {"n_qubits": int (1..12, 4 for the 4-bit setting),
               "gates": [{"controls": [0-2 distinct ints], "target": int}, ...]}
    Gates are applied in list order (gates[0] = G_1 first).
    Qubit i carries bit x_i; qubit 0 is the least significant bit.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _as_int(instance.get("n_qubits", 4), "n_qubits")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError("n_qubits must be in 1..12")
    gates = instance.get("gates")
    if not isinstance(gates, list) or len(gates) > MAX_GATES:
        raise ValueError("gates must be a list of at most 500 gates")
    parsed = []
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError("each gate must be a dict")
        controls = g.get("controls", [])
        if not isinstance(controls, list) or len(controls) > 2:
            raise ValueError("controls must be a list of at most 2 qubits")
        cs = [_as_int(c, "control") for c in controls]
        t = _as_int(g.get("target"), "target")
        allq = cs + [t]
        if len(set(allq)) != len(allq):
            raise ValueError("gate qubits must be distinct")
        for q in allq:
            if q < 0 or q >= n:
                raise ValueError("qubit index out of range")
        parsed.append((cs, t))
    qr = QuantumRegister(n, "x")
    qc = QuantumCircuit(qr)
    for cs, t in parsed:
        if len(cs) == 0:
            qc.x(qr[t])
        elif len(cs) == 1:
            qc.cx(qr[cs[0]], qr[t])
        else:
            qc.ccx(qr[cs[0]], qr[cs[1]], qr[t])
    return qc
