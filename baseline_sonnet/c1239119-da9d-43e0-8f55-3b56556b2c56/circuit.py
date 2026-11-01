from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np


def _walsh(values):
    a = np.array(values, dtype=float)
    h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h)
        a = np.stack([a[:, 0, :] + a[:, 1, :], a[:, 0, :] - a[:, 1, :]], axis=1)
        a = a.reshape(-1)
        h *= 2
    return a / len(a)


def _truth_table(instance, n):
    tt = instance.get('truth_table')
    fn = instance.get('function')
    if tt is not None and fn is not None:
        raise ValueError('give either truth_table or function, not both')
    if tt is not None:
        if not isinstance(tt, (list, tuple)) or len(tt) != 2 ** n:
            raise ValueError('truth_table must have length 2**n')
        out = []
        for v in tt:
            if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
                raise ValueError('truth_table entries must be 0 or 1')
            out.append(v)
        return out
    if fn == 'or':
        # eq_5: OR(x) = 1 xor prod(1 xor x_i); x = 0 is the only zero
        return [0] + [1] * (2 ** n - 1)
    raise ValueError('unknown or missing function; use truth_table or function="or"')


def build_circuit(instance):
    """Oracle on x (qubits 0..n-1, bit i of index x = qubit i) and target y (qubit n)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n + 1 > 12:
        raise ValueError('n must be an integer with 1 <= n <= 11')
    tt = _truth_table(instance, n)
    # eq_3: Walsh coefficients of g = (-1)^f
    g = [1 - 2 * v for v in tt]
    coef = _walsh(g)
    xr = QuantumRegister(n, 'x')
    yr = QuantumRegister(1, 'y')
    qc = QuantumCircuit(xr, yr)
    y = n
    # eq_2 (corrected): H on target conjugating controlled-Z^{f(x)}
    qc.h(y)
    # f(x) = f(0) + sum_{S != empty} ghat(S) x_S, so phase exp(i pi y f(x))
    if tt[0] == 1:
        qc.z(y)
    for mask in range(1, 2 ** n):
        c = float(coef[mask])
        if abs(c) < 1e-12:
            continue
        bits = [i for i in range(n) if (mask >> i) & 1]
        t = bits[0]
        others = bits[1:]
        for o in others:
            qc.cx(o, t)
        qc.cp(math.pi * c, t, y)
        for o in reversed(others):
            qc.cx(o, t)
    qc.h(y)
    return qc
