from math import gcd
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def _cycles(m, N, size):
    # permutation f(x) = m*x mod N for x < N, identity otherwise
    seen = [False] * size
    out = []
    for s in range(N):
        if seen[s]:
            continue
        cyc = [s]
        seen[s] = True
        x = (m * s) % N
        while x != s:
            seen[x] = True
            cyc.append(x)
            x = (m * x) % N
        if len(cyc) > 1:
            out.append(cyc)
    return out


def _controlled_transposition(qc, ctrl, tq, n, u, v):
    # swap basis states |u> and |v> of the target register when ctrl is 1
    d = u ^ v
    p = (d & -d).bit_length() - 1
    others = [j for j in range(n) if ((d >> j) & 1) and j != p]
    for j in others:
        qc.cx(tq[p], tq[j])
    u2 = u
    if (u >> p) & 1:
        for j in others:
            u2 ^= 1 << j
    ctl_bits = [j for j in range(n) if j != p]
    zeros = [j for j in ctl_bits if not ((u2 >> j) & 1)]
    for j in zeros:
        qc.x(tq[j])
    qc.mcx([ctrl] + [tq[j] for j in ctl_bits], tq[p])
    for j in zeros:
        qc.x(tq[j])
    for j in reversed(others):
        qc.cx(tq[p], tq[j])


def _controlled_modmul(qc, ctrl, tq, n, N, m):
    # |x> -> |m*x mod N> for x < N, controlled on ctrl
    for cyc in _cycles(m, N, 1 << n):
        k = len(cyc)
        for j in range(k - 2, -1, -1):
            _controlled_transposition(qc, ctrl, tq, n, cyc[j], cyc[j + 1])


def build_circuit(instance):
    """instance: {'N': int>=3, 'a': int with 1<a<N and gcd(a,N)=1, optional 't': control qubits}.
    Qubits 0..t-1: control (little-endian, qubit k controls a^(2^k)); t..t+n-1: target, n=ceil(log2 N)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    N = _as_int(instance.get('N'), 'N')
    a = _as_int(instance.get('a'), 'a')
    if N < 3:
        raise ValueError('N must be at least 3')
    if N > 2047:
        raise ValueError('N too large for qubit cap')
    if not (1 < a < N) or gcd(a, N) != 1:
        raise ValueError('a must satisfy 1<a<N and gcd(a,N)=1')
    n = (N - 1).bit_length()
    if 't' in instance:
        t = _as_int(instance['t'], 't')
    else:
        t = min(2 * n, 12 - n)
    if t < 1:
        raise ValueError('t must be at least 1')
    if t + n > 12:
        raise ValueError('total qubits exceed 12')
    qc = QuantumCircuit(t + n)
    ctrl_q = list(range(t))
    tq = list(range(t, t + n))
    for q in ctrl_q:
        qc.h(q)
    for k in range(t):
        m = pow(a, 1 << k, N)
        if m != 1:
            _controlled_modmul(qc, ctrl_q[k], tq, n, N, m)
    qc.append(QFTGate(t).inverse(), ctrl_q)
    return qc
