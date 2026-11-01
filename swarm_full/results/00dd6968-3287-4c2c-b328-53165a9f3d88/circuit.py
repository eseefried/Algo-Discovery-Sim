from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Bell-like basis generator: H on m control qubits, then a controlled-X layer onto m targets.

    instance: {"m": int in 1..6, "variant": "copy" | "cascade"}
    Qubits 0..m-1 are controls, qubits m..2m-1 are targets.
    Label bits (i on controls, j on targets) are prepared by the runner.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    allowed = {"m", "variant"}
    for key in instance:
        if key not in allowed:
            raise ValueError("unknown instance key: " + str(key))
    if "m" not in instance:
        raise ValueError("m is required")
    m = instance["m"]
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError("m must be an integer")
    if m < 1 or 2 * m > 12:
        raise ValueError("m must satisfy 1 <= m <= 6")
    variant = instance.get("variant", "copy")
    if variant not in ("copy", "cascade"):
        raise ValueError("variant must be 'copy' or 'cascade'")
    ctrl = QuantumRegister(m, "c")
    targ = QuantumRegister(m, "t")
    qc = QuantumCircuit(ctrl, targ, name="bell_like_" + variant)
    # eq_1: uniform superposition over 2^m control strings, sign (-1)^(i.k) from the label bits
    for a in range(m):
        qc.h(ctrl[a])
    # eq_1: multi-qubit controlled-X layer, target register gets A k (invertible over GF(2))
    for a in range(m):
        if variant == "copy":
            qc.cx(ctrl[a], targ[a])
        else:
            for b in range(a, m):
                qc.cx(ctrl[a], targ[b])
    return qc
