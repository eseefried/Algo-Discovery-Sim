from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """One-query Bernstein-Vazirani operation H^n . O_f . H^n with phase oracle O_f|x> = (-1)^{a.x}|x>.

    instance: {"n": int in [1, 12], "a": list of n bits; a[i] is the coefficient of qubit i}.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n must be an integer in [1, 12]")
    a = instance.get("a")
    if not isinstance(a, (list, tuple)) or len(a) != n:
        raise ValueError("a must be a list of length n")
    bits = []
    for v in a:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError("a entries must be 0 or 1")
        bits.append(v)
    qr = QuantumRegister(n, "x")
    qc = QuantumCircuit(qr)
    # eq_3: first Hadamard layer
    qc.h(qr)
    # eq_1: phase oracle for f(x) = a.x mod 2, i.e. (-1)^{a.x} = product of Z_i^{a_i}
    for i, bit in enumerate(bits):
        if bit == 1:
            qc.z(qr[i])
    # eq_3: final Hadamard layer, mapping the phase pattern to |a>
    qc.h(qr)
    return qc
