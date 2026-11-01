from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import XGate


def build_circuit(instance):
    """Discrete query oracle O_x |i>|b> = |i>|b xor x_i>.

    instance: {"x": [0/1, ...]} with 1 <= N = len(x) <= 2048.
    Index register: ceil(log2 N) qubits (min 1), qubit 0 is least significant bit of i.
    Target: one qubit placed after the index register.
    Index values i >= N (if N is not a power of two) are left unchanged.
    """
    if not isinstance(instance, dict) or "x" not in instance:
        raise ValueError("instance must be a dict with key 'x'")
    x = instance["x"]
    if not isinstance(x, (list, tuple)):
        raise ValueError("x must be a list of bits")
    n_items = len(x)
    if n_items < 1:
        raise ValueError("x must be non-empty")
    bits = []
    for b in x:
        if isinstance(b, bool):
            b = int(b)
        if not isinstance(b, int) or b not in (0, 1):
            raise ValueError("entries of x must be 0 or 1")
        bits.append(b)
    n_idx = max(1, (n_items - 1).bit_length())
    if n_idx + 1 > 12:
        raise ValueError("too many qubits: N must be at most 2048")
    index = QuantumRegister(n_idx, "index")
    target = QuantumRegister(1, "target")
    qc = QuantumCircuit(index, target)
    # eq_5: for each i with x_i = 1 flip target when index register equals i
    for i, b in enumerate(bits):
        if b == 1:
            gate = XGate().control(n_idx, ctrl_state=i)
            qc.append(gate, list(range(n_idx)) + [n_idx])
    return qc
