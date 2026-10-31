from qiskit import QuantumCircuit, QuantumRegister


def _index(instance, key, n):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    if v < 0 or v >= n:
        raise ValueError(key + " out of range")
    return v


def build_circuit(instance):
    """Toffoli: |a,b,c> -> |a,b,c XOR ab> (eq_1) on selected qubits.

    instance keys: num_qubits (int, 3..12, optional, default 3),
    control_a, control_b, target (distinct qubit indices).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("num_qubits", 3)
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("num_qubits must be an integer")
    if n < 3 or n > 12:
        raise ValueError("num_qubits must be between 3 and 12")
    a = _index(instance, "control_a", n)
    b = _index(instance, "control_b", n)
    c = _index(instance, "target", n)
    if len({a, b, c}) != 3:
        raise ValueError("control_a, control_b and target must be distinct")
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    # eq_1: flip target c iff both controls a and b are 1
    qc.ccx(qr[a], qr[b], qr[c])
    return qc
