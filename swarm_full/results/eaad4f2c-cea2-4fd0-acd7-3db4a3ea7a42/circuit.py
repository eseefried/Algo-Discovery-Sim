from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Fourier/phase-polynomial XOR oracle for f on n bits.

    Qubits: x_i -> index i (i<n), b -> index n, parity ancillas -> n+1...
    Ancillas must be supplied in |0> and are returned to |0>.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 8:
        raise ValueError('n must be an integer in 1..8')
    kind = instance.get('function', 'or')
    size = 1 << n
    if kind == 'or':
        table = [0] + [1] * (size - 1)
    elif kind == 'truth_table':
        tt = instance.get('truth_table')
        if not isinstance(tt, list) or len(tt) != size:
            raise ValueError('truth_table must be a list of length 2**n')
        table = []
        for v in tt:
            if isinstance(v, bool):
                v = int(v)
            if not isinstance(v, int) or v not in (0, 1):
                raise ValueError('truth_table entries must be 0 or 1')
            table.append(v)
    else:
        raise ValueError("function must be 'or' or 'truth_table'")

    # Fourier coefficients fhat(S) = 2^-n sum_x f(x) (-1)^{S.x}; f = sum_S fhat(S) Z_S
    coeffs = {}
    for s in range(size):
        tot = 0
        for x in range(size):
            if table[x]:
                tot += -1 if (bin(s & x).count('1') % 2) else 1
        c = tot / size
        if abs(c) > 1e-12:
            coeffs[s] = c
    subsets = [s for s in sorted(coeffs) if s != 0]
    total = n + 1 + len(subsets)
    if total > 12:
        raise ValueError('instance needs more than 12 qubits')

    xr = QuantumRegister(n, 'x')
    br = QuantumRegister(1, 'b')
    ar = QuantumRegister(len(subsets), 'anc')
    qc = QuantumCircuit(xr, br, ar)
    b = n

    # X^f = H Z^f H; Z^f = exp(i pi/2 f) exp(-i pi/2 f Z_b)
    qc.h(b)
    if 0 in coeffs:
        qc.rz(math.pi * coeffs[0], b)  # constant-term Z_b rotation
    for k, s in enumerate(subsets):
        a = n + 1 + k
        c = coeffs[s]
        bits = [i for i in range(n) if (s >> i) & 1]
        for i in bits:
            qc.cx(i, a)  # fan-out/parity of S into ancilla
        qc.rz(-math.pi * c, a)  # exp(i pi/2 c Z_S)
        qc.cx(b, a)
        qc.rz(math.pi * c, a)  # exp(-i pi/2 c Z_S Z_b)
        qc.cx(b, a)
        for i in reversed(bits):
            qc.cx(i, a)  # uncompute parity
    qc.h(b)
    return qc
