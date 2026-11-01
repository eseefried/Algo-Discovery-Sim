from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Return the unitary 2-qubit Clifford+T block W (eq_1).

    instance: {"gates": [[name, q...], ...]} with name in
    h,s,sdg,t,tdg,x,y,z (one qubit) or cx (control, target); qubits in {0,1}.
    Qubit 0 is the data qubit and qubit 1 is the ancilla (little-endian).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    gates = instance.get("gates")
    if not isinstance(gates, list) or len(gates) > 200:
        raise ValueError("gates must be a list of at most 200 entries")
    data = QuantumRegister(1, "data")
    anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(data, anc)
    singles = {
        "h": qc.h,
        "s": qc.s,
        "sdg": qc.sdg,
        "t": qc.t,
        "tdg": qc.tdg,
        "x": qc.x,
        "y": qc.y,
        "z": qc.z,
    }
    for g in gates:
        if not isinstance(g, (list, tuple)) or len(g) < 2:
            raise ValueError("each gate must be [name, qubit, ...]")
        name = g[0]
        qs = list(g[1:])
        for q in qs:
            if type(q) is not int or q < 0 or q > 1:
                raise ValueError("qubit index must be 0 or 1")
        if not isinstance(name, str):
            raise ValueError("gate name must be a string")
        if name in singles:
            if len(qs) != 1:
                raise ValueError("single-qubit gate takes one qubit")
            singles[name](qs[0])
        elif name == "cx":
            if len(qs) != 2 or qs[0] == qs[1]:
                raise ValueError("cx needs two distinct qubits")
            qc.cx(qs[0], qs[1])
        else:
            raise ValueError("unsupported gate")
    return qc
