from qiskit import QuantumCircuit, QuantumRegister


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def build_circuit(instance):
    """Simon operation H^n . U_f . H^n on input register (qubits 0..n-1),
    with output register on qubits n..2n-1. Instance: {'n': int, 's': int}.
    s is the hidden period as an integer; bit i of s corresponds to qubit i."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _check_int(instance.get('n'), 'n')
    s = _check_int(instance.get('s'), 's')
    if n < 1 or n > 6:
        raise ValueError('n must be in 1..6 (at most 12 qubits)')
    if s < 0 or s >= 2 ** n:
        raise ValueError('s must satisfy 0 <= s < 2^n')
    xr = QuantumRegister(n, 'x')
    fr = QuantumRegister(n, 'f')
    qc = QuantumCircuit(xr, fr)
    # Hadamard layer on input register
    for i in range(n):
        qc.h(xr[i])
    # Oracle U_f: f(x) = x XOR (x_p * s), p = highest set bit of s (eq_1)
    for i in range(n):
        qc.cx(xr[i], fr[i])
    if s != 0:
        p = s.bit_length() - 1
        for i in range(n):
            if (s >> i) & 1:
                qc.cx(xr[p], fr[i])
    # Final Hadamard layer on input register; outputs y satisfy y.s=0 mod 2 (eq_2)
    for i in range(n):
        qc.h(xr[i])
    return qc
