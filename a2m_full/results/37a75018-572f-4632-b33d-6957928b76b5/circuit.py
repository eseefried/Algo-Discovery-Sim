from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Two-qubit Simon operation H(x) U_f H(x) on x=q0,q1 and f=q2,q3.

    instance: {"s": "s1s0"} with s a 2-character bit string (q0 is bit 0).
    Oracle: |x>|y> -> |x>|y xor f(x)>, f(x) = x xor (x_j * s), j = highest set bit of s.
    """
    try:
        s = instance.get("s", None)
    except AttributeError:
        raise ValueError("instance must be a JSON object")
    if s not in ("00", "01", "10", "11"):
        raise ValueError("s must be one of '00','01','10','11'")
    xr = QuantumRegister(2, "x")
    fr = QuantumRegister(2, "f")
    qc = QuantumCircuit(xr, fr)
    bits = s[::-1]  # bits[i] is s_i
    # eq_1: uniform superposition on x
    qc.h(0)
    qc.h(1)
    # eq_1: oracle query, copy x into f register
    for i in range(2):
        qc.cx(i, 2 + i)
    # fold by s: f(x) = f(x xor s)
    if s != "00":
        j = 1 if bits[1] == "1" else 0
        for k in range(2):
            if bits[k] == "1":
                qc.cx(j, 2 + k)
    # eq_3: Hadamard readout basis on x
    qc.h(0)
    qc.h(1)
    return qc
