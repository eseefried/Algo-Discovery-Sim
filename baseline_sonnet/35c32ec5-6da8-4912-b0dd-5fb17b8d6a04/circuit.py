from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Fanout: |x>|y_1..y_n> -> |x>|y_1^x,...,y_n^x>.

    Layout: qubit 0 = control x, qubits 1..n = targets y_1..y_n.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance:
        raise ValueError("missing n")
    n = instance["n"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n + 1 > 12:
        raise ValueError("n must satisfy 1 <= n <= 11")
    control = QuantumRegister(1, "control")
    targets = QuantumRegister(n, "targets")
    qc = QuantumCircuit(control, targets)
    # eq_4: one CNOT from the control onto each target
    for i in range(n):
        qc.cx(control[0], targets[i])
    return qc
