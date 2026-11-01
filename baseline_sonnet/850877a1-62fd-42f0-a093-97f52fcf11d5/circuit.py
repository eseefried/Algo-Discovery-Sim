from math import gcd
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _swap_adjacent(qc, ctrl, work, m, s, t):
    # Swap basis states s,t (differing in exactly one bit) of the work register, controlled on ctrl.
    d = (s ^ t).bit_length() - 1
    others = [i for i in range(m) if i != d]
    zeros = [work[i] for i in others if not ((s >> i) & 1)]
    for q in zeros:
        qc.x(q)
    qc.mcx([ctrl] + [work[i] for i in others], work[d])
    for q in zeros:
        qc.x(q)


def _transposition(qc, ctrl, work, m, u, v):
    # Transposition (u v) as a Gray-type path of adjacent swaps: A, M, A^-1.
    diff = [i for i in range(m) if ((u ^ v) >> i) & 1]
    path = [u]
    for i in diff:
        path.append(path[-1] ^ (1 << i))
    k = len(diff)
    for i in range(k):
        _swap_adjacent(qc, ctrl, work, m, path[i], path[i + 1])
    for i in range(k - 2, -1, -1):
        _swap_adjacent(qc, ctrl, work, m, path[i], path[i + 1])


def _controlled_mult(qc, ctrl, work, m, N, c):
    # Controlled |y> -> |c*y mod N> for y<N, identity for y>=N (eq_4 modular exponentiation step).
    size = 1 << m
    f = [(c * y) % N if y < N else y for y in range(size)]
    seen = [False] * size
    for start in range(size):
        if seen[start]:
            continue
        cyc = [start]
        seen[start] = True
        y = f[start]
        while y != start:
            cyc.append(y)
            seen[y] = True
            y = f[y]
        # cycle c0->c1->...: time-ordered transpositions (c_{L-2},c_{L-1}), ..., (c_0,c_1)
        for j in range(len(cyc) - 2, -1, -1):
            _transposition(qc, ctrl, work, m, cyc[j], cyc[j + 1])


def build_circuit(instance):
    """Order-finding operation: controlled U_a^(2^k) on counting qubit k, then inverse QFT on counting register.
    instance: {"N": int>=3, "a": int with 1<a<N, gcd(a,N)=1, optional "n": counting qubits (default smallest with 2^n>=N^2)}.
    Layout: qubits 0..n-1 counting (little-endian x), qubits n..n+m-1 work (little-endian), m=ceil(log2 N)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    N = instance.get("N")
    a = instance.get("a")
    if not _is_int(N) or not _is_int(a) or N < 3 or N > 4096:
        raise ValueError("N and a must be integers with 3 <= N <= 4096")
    if not (1 < a < N) or gcd(a, N) != 1:
        raise ValueError("a must satisfy 1<a<N and gcd(a,N)=1")
    m = (N - 1).bit_length()
    n = instance.get("n")
    if n is None:
        n = max(1, (N * N - 1).bit_length())
    if not _is_int(n) or n < 1:
        raise ValueError("n must be a positive integer")
    if n + m > 12:
        raise ValueError("total qubits n + ceil(log2 N) must be <= 12")
    cnt = QuantumRegister(n, "count")
    wrk = QuantumRegister(m, "work")
    qc = QuantumCircuit(cnt, wrk)
    for k in range(n):
        c = pow(a, 2 ** k, N)
        if c != 1:
            _controlled_mult(qc, cnt[k], wrk, m, N, c)
    qc.append(QFTGate(n).inverse(), list(range(n)))
    return qc
