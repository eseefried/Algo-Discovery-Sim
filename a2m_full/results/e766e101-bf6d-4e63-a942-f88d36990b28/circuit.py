from qiskit import QuantumCircuit, QuantumRegister
import math


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    tt = instance.get('truth_table')
    if not isinstance(tt, (list, tuple)) or len(tt) < 2:
        raise ValueError('truth_table must be a list of length 2**n, n>=1')
    size = len(tt)
    n = size.bit_length() - 1
    if (1 << n) != size or n > 6:
        raise ValueError('truth_table length must be 2**n with 1<=n<=6')
    if 'n' in instance and instance['n'] != n:
        raise ValueError('n inconsistent with truth_table length')
    vals = []
    for v in tt:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError('truth_table entries must be 0 or 1')
        vals.append(v)
    return n, vals


def _coeffs(n, vals):
    # eq_4 / eq_5: F(s) = 2^-n sum_x (-1)^(f(x)+s.x); c_s = F(s) for s != 0, c_0 = f(0)
    size = 1 << n
    out = {}
    for s in range(1, size):
        tot = 0
        for x in range(size):
            tot += -1 if (vals[x] + bin(s & x).count('1')) % 2 else 1
        c = tot / size
        if abs(c) > 1e-12:
            out[s] = c
    return out


def build_circuit(instance):
    """Qubits: x_0..x_{n-1} = 0..n-1, y = n, parity ancillas after y."""
    n, vals = _parse(instance)
    coeffs = _coeffs(n, vals)
    anc_masks = [s for s in sorted(coeffs) if s & (s - 1)]
    total = n + 1 + len(anc_masks)
    if total > 12:
        raise ValueError('circuit would need more than 12 qubits')
    regs = [QuantumRegister(n, 'x'), QuantumRegister(1, 'y')]
    if anc_masks:
        regs.append(QuantumRegister(len(anc_masks), 'a'))
    qc = QuantumCircuit(*regs)
    y = n
    # eq_2: Hadamards on target
    qc.h(y)
    # parity computation (fan-in of x bits onto ancillas)
    anc_index = {}
    for k, s in enumerate(anc_masks):
        a = n + 1 + k
        anc_index[s] = a
        for i in range(n):
            if (s >> i) & 1:
                qc.cx(i, a)
    # eq_3 / eq_6: y-controlled phase pi*c_s on each parity; total phase pi*f(x)*y
    if vals[0] == 1:
        qc.p(math.pi, y)  # constant term c_0 = f(0)
    for s in sorted(coeffs):
        theta = math.pi * coeffs[s]
        if s in anc_index:
            qc.cp(theta, y, anc_index[s])
        else:
            qc.cp(theta, y, s.bit_length() - 1)
    # uncompute parities
    for s in reversed(anc_masks):
        a = anc_index[s]
        for i in reversed(range(n)):
            if (s >> i) & 1:
                qc.cx(i, a)
    qc.h(y)
    return qc
