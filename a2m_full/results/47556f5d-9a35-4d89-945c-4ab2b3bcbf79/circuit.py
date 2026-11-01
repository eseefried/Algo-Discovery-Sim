from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + " must be a finite real number")
    return float(x)


def _int(x, name):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError(name + " must be an integer")
    return x


def build_circuit(instance):
    """p=1 QAOA operation for Max E3LIN2 (no |+> preparation, no measurement).

    instance: {"n": int 3..12, "equations": [[a,b,c,rhs],...], "gamma": float,
               "beta": float, optional "D": int occurrence bound}
    Qubit i = boolean variable i.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int(instance.get("n"), "n")
    if n < 3 or n > 12:
        raise ValueError("n must be between 3 and 12")
    eqs = instance.get("equations")
    if not isinstance(eqs, (list, tuple)) or len(eqs) == 0 or len(eqs) > 200:
        raise ValueError("equations must be a list of 1..200 entries")
    gamma = _num(instance.get("gamma"), "gamma")
    beta = _num(instance.get("beta"), "beta")
    parsed = []
    deg = [0] * n
    for e in eqs:
        if not isinstance(e, (list, tuple)) or len(e) != 4:
            raise ValueError("each equation must be [a,b,c,rhs]")
        a = _int(e[0], "a")
        b = _int(e[1], "b")
        c = _int(e[2], "c")
        r = _int(e[3], "rhs")
        if min(a, b, c) < 0 or max(a, b, c) >= n:
            raise ValueError("variable index out of range")
        if len({a, b, c}) != 3:
            raise ValueError("variables in an equation must be distinct")
        if r not in (0, 1):
            raise ValueError("rhs must be 0 or 1")
        deg[a] += 1
        deg[b] += 1
        deg[c] += 1
        parsed.append((a, b, c, r))
    D = instance.get("D")
    if D is not None:
        D = _int(D, "D")
        if D < 1 or max(deg) > D:
            raise ValueError("some variable occurs in more than D equations")
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    # eq_1/eq_3: exp(-i*gamma*C) = global phase * prod_k exp(+i*gamma*s_k*Z_a Z_b Z_c/2)
    for (a, b, c, r) in parsed:
        s = 1 - 2 * r
        qc.cx(a, c)
        qc.cx(b, c)
        qc.rz(-gamma * s, c)
        qc.cx(b, c)
        qc.cx(a, c)
    # eq_2: mixer exp(-i*beta*X) = RX(2*beta) on every qubit
    for i in range(n):
        qc.rx(2.0 * beta, i)
    return qc
