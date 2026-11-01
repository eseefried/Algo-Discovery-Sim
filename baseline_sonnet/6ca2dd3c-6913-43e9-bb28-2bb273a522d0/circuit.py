from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np


def _num(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError('phase must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError('phase must be finite')
    return v


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    N = 1 << n
    has_theta = 'theta' in instance
    has_classes = 'classes' in instance
    if has_theta == has_classes:
        raise ValueError('provide exactly one of theta or classes')
    if has_theta:
        th = instance['theta']
        if not isinstance(th, list) or len(th) != N:
            raise ValueError('theta must be a list of length 2^n')
        arr = np.array([_num(v) for v in th], dtype=float)
    else:
        classes = instance['classes']
        if not isinstance(classes, list) or len(classes) == 0:
            raise ValueError('classes must be a nonempty list')
        arr = np.zeros(N, dtype=float)
        seen = [False] * N
        for c in classes:
            if not isinstance(c, dict):
                raise ValueError('class must be a dict')
            ph = _num(c.get('phase'))
            states = c.get('states')
            if not isinstance(states, list):
                raise ValueError('states must be a list')
            for s in states:
                if isinstance(s, bool) or not isinstance(s, int) or s < 0 or s >= N or seen[s]:
                    raise ValueError('invalid or repeated basis state')
                seen[s] = True
                arr[s] = ph
        if not all(seen):
            raise ValueError('classes must partition all basis states')
    return n, arr


def _fwht(a):
    a = np.array(a, dtype=float)
    N = a.size
    h = 1
    while h < N:
        b = a.reshape(-1, 2, h)
        x = b[:, 0, :] + b[:, 1, :]
        y = b[:, 0, :] - b[:, 1, :]
        a = np.stack([x, y], axis=1).reshape(-1)
        h *= 2
    return a


def build_circuit(instance):
    n, theta = _parse(instance)
    N = 1 << n
    w = _fwht(theta) / N
    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q)
    # theta(x) = theta(0) - 2 * sum_{s>0} w_s * parity(s.x)
    qc.global_phase = float(theta[0])
    for s in range(1, N):
        if abs(w[s]) < 1e-12:
            continue
        bits = [i for i in range(n) if (s >> i) & 1]
        tgt = bits[-1]
        others = bits[:-1]
        for b in others:
            qc.cx(q[b], q[tgt])
        qc.p(float(-2.0 * w[s]), q[tgt])
        for b in reversed(others):
            qc.cx(q[b], q[tgt])
    return qc
