import math
from qiskit import QuantumCircuit


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    d = instance.get('d')
    i = instance.get('direction')
    monos = instance.get('monomials')
    for v in (n, d, i):
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('n, d, direction must be integers')
    if n < 1 or n > 12:
        raise ValueError('n must be in 1..12')
    if d < 1 or d > n:
        raise ValueError('d must be in 1..n')
    if i < 0 or i >= n:
        raise ValueError('direction out of range')
    if not isinstance(monos, list):
        raise ValueError('monomials must be a list')
    kept = set()
    for S in monos:
        if not isinstance(S, list):
            raise ValueError('monomial must be a list of variable indices')
        for v in S:
            if isinstance(v, bool) or not isinstance(v, int) or v < 0 or v >= n:
                raise ValueError('bad variable index')
        if len(set(S)) != len(S):
            raise ValueError('repeated variable: polynomial must be multilinear')
        if len(S) > d:
            raise ValueError('monomial degree exceeds d')
        key = tuple(sorted(S))
        # coefficients live in F_2: repeated monomials cancel in pairs
        if key in kept:
            kept.remove(key)
        else:
            kept.add(key)
    return n, i, sorted(kept, key=lambda s: (len(s), s))


def _phase_oracle(qc, monos):
    # eq_1 (q=2): U_f|x> = (-1)^{f(x)}|x>, f = sum_S c_S prod_{j in S} x_j
    for S in monos:
        if len(S) == 0:
            qc.global_phase += math.pi
        elif len(S) == 1:
            qc.z(S[0])
        else:
            qc.mcp(math.pi, list(S[:-1]), S[-1])


def build_circuit(instance):
    n, i, monos = _parse(instance)
    qc = QuantumCircuit(n, name='bv_derivative')
    for q in range(n):
        qc.h(q)
    # eq_3: derivative phase oracle (-1)^{f(x+e_i)+f(x)} = X_i U_f X_i . U_f
    _phase_oracle(qc, monos)
    qc.x(i)
    _phase_oracle(qc, monos)
    qc.x(i)
    # eq_2: closing Hadamards of Bernstein-Vazirani
    for q in range(n):
        qc.h(q)
    return qc
