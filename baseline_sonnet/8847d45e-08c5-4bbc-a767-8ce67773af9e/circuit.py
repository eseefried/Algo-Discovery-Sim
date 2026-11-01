from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Noiseless quantum parity-learning round.

    instance: {"n": int in [1, 11], "s": bitstring of length n}.
    s is written most-significant-bit first: s[n-1-i] is s_i, which acts on x qubit i.
    Layout: qubits 0..n-1 = X (x_i on qubit i), qubit n = label qubit B.
    Gate sequence: H on X; CX(x_i -> B) for each s_i = 1; H on all n+1 qubits.
    On |0>^n|0> this yields H^{n+1}|psi_s>.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    s = instance.get("s")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > 11:
        raise ValueError("n must be in [1, 11] so that n+1 <= 12 qubits")
    if not isinstance(s, str) or len(s) != n:
        raise ValueError("s must be a bitstring of length n")
    for ch in s:
        if ch not in ("0", "1"):
            raise ValueError("s must contain only 0 and 1")
    x = QuantumRegister(n, "x")
    b = QuantumRegister(1, "b")
    qc = QuantumCircuit(x, b)
    # eq_2: uniform superposition over x (sets up |psi_s> from |0>)
    for i in range(n):
        qc.h(x[i])
    # eq_1 / eq_2: oracle |x>|c> -> |x>|c XOR s.x>
    for i in range(n):
        if s[n - 1 - i] == "1":
            qc.cx(x[i], b[0])
    # eq_3: Fourier sampling Hadamards on X and B
    for i in range(n):
        qc.h(x[i])
    qc.h(b[0])
    return qc
