from qiskit import QuantumCircuit


def build_circuit(instance):
    """Scoped CNOT(A->B) for dA=dB=2.

    instance: {"dA": 2, "dB": 2, "mode": "direct" | "teleport"}
    direct: qubits [A=0, B=1].
    teleport: qubits [A=0, B=1, e0=2 (Alice side), e1=3 (Bob side)];
    ancillas e0, e1 are assumed |0> on input and are returned to |0>.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    dA = instance.get("dA", 2)
    dB = instance.get("dB", 2)
    mode = instance.get("mode", "teleport")
    for d in (dA, dB):
        if isinstance(d, bool) or not isinstance(d, int):
            raise ValueError("dA and dB must be integers")
    if dA != 2 or dB != 2:
        raise ValueError("only dA=dB=2 is implemented")
    if not isinstance(mode, str) or mode not in ("direct", "teleport"):
        raise ValueError("mode must be 'direct' or 'teleport'")
    if mode == "direct":
        qc = QuantumCircuit(2, name="cnot_direct")
        # eq_4: |0><0| (x) I + |1><1| (x) X
        qc.cx(0, 1)
        return qc
    qc = QuantumCircuit(4, name="cnot_teleport_coherent")
    a, b, e0, e1 = 0, 1, 2, 3
    # Bell pair across the cut: e0 (Alice side), e1 (Bob side)
    qc.h(e0)
    qc.cx(e0, e1)
    # Alice: entangle data with her half
    qc.cx(a, e0)
    # coherent version of 'measure e0, Bob applies X^m on e1': e1 -> a, e0 -> |+>
    qc.cx(e0, e1)
    # Bob: local CNOT from the copy of a onto B
    qc.cx(e1, b)
    # coherent version of 'X-basis measure e1, Alice applies Z^k on A'
    qc.h(e1)
    qc.cz(a, e1)
    qc.h(e1)
    # e1 is back to |0>; e0 is |+>, return it to |0>
    qc.h(e0)
    return qc
