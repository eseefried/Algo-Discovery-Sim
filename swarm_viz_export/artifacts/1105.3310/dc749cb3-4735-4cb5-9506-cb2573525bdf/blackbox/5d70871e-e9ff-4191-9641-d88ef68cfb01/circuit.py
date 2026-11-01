import math
from qiskit import QuantumCircuit, QuantumRegister


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    d = instance.get('d')
    mons = instance.get('monomials')
    a = instance.get('direction')
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError('n must be an integer in [1,12]')
    if not _is_int(d) or d < 1 or d > n:
        raise ValueError('d must be an integer in [1,n]')
    if not isinstance(mons, list):
        raise ValueError('monomials must be a list of index lists')
    if not _is_int(a) or a < 0 or a >= 2 ** n:
        raise ValueError('direction must be an integer mask in [0,2^n)')
    parity = {}
    for m in mons:
        if not isinstance(m, list):
            raise ValueError('each monomial must be a list of variable indices')
        for idx in m:
            if not _is_int(idx) or idx < 0 or idx >= n:
                raise ValueError('variable index out of range')
        if len(set(m)) != len(m):
            raise ValueError('multilinear monomials cannot repeat a variable')
        if len(m) > d:
            raise ValueError('monomial degree exceeds d')
        key = tuple(sorted(m))
        parity[key] = parity.get(key, 0) ^ 1
    active = [k for k in parity if parity[k] == 1]
    active.sort(key=lambda k: (len(k), k))
    return n, a, active


def _apply_phase_oracle(qc, active):
    # eq_1 / eq_2: O_f|x> = (-1)^f(x)|x>; each monomial with c_S=1 gives a Z-type phase on the qubits in S
    for S in active:
        if len(S) == 0:
            qc.global_phase = qc.global_phase + math.pi
        elif len(S) == 1:
            qc.z(S[0])
        elif len(S) == 2:
            qc.cz(S[0], S[1])
        else:
            qc.mcp(math.pi, list(S[:-1]), S[-1])


def build_circuit(instance):
    n, a, active = _parse(instance)
    qc = QuantumCircuit(QuantumRegister(n, 'x'))
    # eq_3: first Hadamard layer
    qc.h(range(n))
    # eq_2: phase oracle O_f
    _apply_phase_oracle(qc, active)
    if a:
        # eq_5: O_{D_a f} = O_f (X^a O_f X^a)
        bits = [i for i in range(n) if (a >> i) & 1]
        for i in bits:
            qc.x(i)
        _apply_phase_oracle(qc, active)
        for i in bits:
            qc.x(i)
    # eq_3: final Hadamard layer
    qc.h(range(n))
    return qc
