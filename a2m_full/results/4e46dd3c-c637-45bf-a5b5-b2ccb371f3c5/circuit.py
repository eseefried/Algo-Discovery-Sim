import math
from qiskit import QuantumCircuit, QuantumRegister


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _oracle(qc, data, idx, index_map, n, m):
    # U_j: |x>|y> -> |x>|y xor j(x)>  (self-inverse, eq_2)
    for x, j in enumerate(index_map):
        if j == 0:
            continue
        zeros = [data[i] for i in range(n) if not (x >> i) & 1]
        for q in zeros:
            qc.x(q)
        for b in range(m):
            if (j >> b) & 1:
                qc.mcx(list(data), idx[b])
        for q in zeros:
            qc.x(q)


def _walsh(f, m):
    # f(j) = sum_s c_s (-1)^{s.j}  (eq_3)
    size = 1 << m
    coeffs = []
    for s in range(size):
        tot = 0.0
        for j in range(size):
            sign = -1.0 if (bin(s & j).count('1') & 1) else 1.0
            tot += sign * f[j]
        coeffs.append(tot / size)
    return coeffs


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not _is_int(n) or n < 1 or n > 10:
        raise ValueError('n must be an integer in 1..10')
    phases = instance.get('phases')
    if not isinstance(phases, (list, tuple)) or len(phases) < 1 or len(phases) > (1 << n):
        raise ValueError('phases must be a list of 1..2^n reals')
    ph = []
    for p in phases:
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p):
            raise ValueError('phases must be finite reals')
        ph.append(float(p))
    k = len(ph)
    index_map = instance.get('index_map')
    if not isinstance(index_map, (list, tuple)) or len(index_map) != (1 << n):
        raise ValueError('index_map must have length 2^n')
    for j in index_map:
        if not _is_int(j) or j < 0 or j >= k:
            raise ValueError('index_map entries must be integers in 0..k-1')
    index_map = [int(j) for j in index_map]
    m = max(1, (k - 1).bit_length())
    if n + m > 12:
        raise ValueError('total qubits exceed 12')

    data_reg = QuantumRegister(n, 'data')
    idx_reg = QuantumRegister(m, 'index')
    qc = QuantumCircuit(data_reg, idx_reg)
    data = list(data_reg)
    idx = list(idx_reg)

    f = ph + [0.0] * ((1 << m) - k)  # unused index values get phase 0
    coeffs = _walsh(f, m)
    qc.global_phase = coeffs[0]  # gamma

    # compute index
    _oracle(qc, data, idx, index_map, n, m)

    # Delta via parity rotations: alpha_s = -2 c_s
    for s in range(1, 1 << m):
        alpha = -2.0 * coeffs[s]
        if abs(alpha) < 1e-15:
            continue
        bits = [b for b in range(m) if (s >> b) & 1]
        target = bits[0]
        for b in bits[1:]:
            qc.cx(idx[b], idx[target])
        qc.rz(alpha, idx[target])
        for b in reversed(bits[1:]):
            qc.cx(idx[b], idx[target])

    # uncompute index
    _oracle(qc, data, idx, index_map, n, m)
    return qc
