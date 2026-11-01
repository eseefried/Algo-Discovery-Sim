from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Noiseless single-query parity Fourier sampling circuit.

    instance: {"n": int in [1, 11], "s": list of n bits or a bit string where s[i] is s_i}.
    Data qubit i is qubit i (s_i); label qubit is qubit n.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n + 1 > 12:
        raise ValueError("n must satisfy 1 <= n <= 11")
    s = instance.get("s")
    if isinstance(s, str):
        bits = []
        for ch in s:
            if ch not in ("0", "1"):
                raise ValueError("s string must contain only 0/1")
            bits.append(int(ch))
    elif isinstance(s, (list, tuple)):
        bits = []
        for b in s:
            if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
                raise ValueError("s entries must be 0 or 1")
            bits.append(int(b))
    else:
        raise ValueError("s must be a list or string of bits")
    if len(bits) != n:
        raise ValueError("s must have length n")

    data = QuantumRegister(n, "data")
    label = QuantumRegister(1, "label")
    qc = QuantumCircuit(data, label)
    lab = n

    # eq_1: coherent example oracle on |0^n>|0>: 2^{-n/2} sum_x |x>|s.x mod 2>
    for i in range(n):
        qc.h(i)
    for i in range(n):
        if bits[i] == 1:
            qc.cx(i, lab)

    # eq_2: Fourier sampling; H on label gives |-> by phase kickback, H^n maps data to |s>
    qc.h(lab)
    for i in range(n):
        qc.h(i)
    return qc
