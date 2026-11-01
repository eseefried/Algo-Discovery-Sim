from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be a finite real number')
    return float(x)


def build_circuit(instance):
    """Level-one QAOA layer for E3LIN2. Equation k = [a, b, c, s] means x_a+x_b+x_c = s mod 2.
    Phase layer: exp(-i*gamma*sum_k (1+(-1)^s Z_a Z_b Z_c)/2) up to global phase.
    Mixer layer: exp(-i*beta*sum_j X_j). Input |+>^n is prepared by the runner."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    if not _is_int(n) or n < 3 or n > 12:
        raise ValueError('n must be an integer in [3, 12]')
    eqs = instance.get('equations')
    if not isinstance(eqs, (list, tuple)) or len(eqs) == 0 or len(eqs) > 200:
        raise ValueError('equations must be a list with 1..200 entries')
    counts = [0] * n
    parsed = []
    for e in eqs:
        if not isinstance(e, (list, tuple)) or len(e) != 4:
            raise ValueError('each equation must be [a, b, c, s]')
        a, b, c, s = e
        if not (_is_int(a) and _is_int(b) and _is_int(c) and _is_int(s)):
            raise ValueError('equation entries must be integers')
        for v in (a, b, c):
            if v < 0 or v >= n:
                raise ValueError('variable index out of range')
        if len(set((a, b, c))) != 3:
            raise ValueError('equation variables must be distinct')
        if s not in (0, 1):
            raise ValueError('right-hand side must be 0 or 1')
        counts[a] += 1
        counts[b] += 1
        counts[c] += 1
        parsed.append((a, b, c, s))
    D = instance.get('D')
    if D is not None:
        if not _is_int(D) or D < 1:
            raise ValueError('D must be a positive integer')
        if max(counts) > D:
            raise ValueError('a variable occurs in more than D equations')
    gamma = _num(instance.get('gamma'), 'gamma')
    beta = _num(instance.get('beta'), 'beta')
    qr = QuantumRegister(n, 'z')
    qc = QuantumCircuit(qr)
    for a, b, c, s in parsed:
        theta = gamma if s == 0 else -gamma
        qc.cx(a, c)
        qc.cx(b, c)
        qc.rz(theta, c)
        qc.cx(b, c)
        qc.cx(a, c)
    for q in range(n):
        qc.rx(2.0 * beta, q)
    return qc
