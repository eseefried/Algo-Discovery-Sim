import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RXXGate, RYYGate


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, np.integer)):
        raise ValueError(name + ' must be an integer')
    return int(v)


def _as_real(v, name):
    if isinstance(v, bool):
        raise ValueError(name + ' must be real')
    try:
        x = float(v)
    except (TypeError, ValueError):
        raise ValueError(name + ' must be real')
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    return x


def _controlled_trotter_step(qc, ctrl, sys_idx, eps_eff, G, h):
    # Diagonal part exp(-i h eps'_j n_j), n_j=|1><1|: controlled phase (eq_2, eq_3).
    n = len(sys_idx)
    for j in range(n):
        qc.cp(-h * eps_eff[j], ctrl, sys_idx[j])
    # Hopping part exp(+i (G h/2)(XX+YY)) = RXX(-G h) RYY(-G h) (XX and YY commute).
    theta = -G * h
    for j in range(n):
        for k in range(j + 1, n):
            qc.append(RXXGate(theta).control(1), [ctrl, sys_idx[j], sys_idx[k]])
            qc.append(RYYGate(theta).control(1), [ctrl, sys_idx[j], sys_idx[k]])


def build_circuit(instance):
    """QPE operation: controlled-U^(2^k) on ancilla k, then inverse QFT on ancillas.
    Layout: qubits 0..N-1 = system levels, qubits N..N+t-1 = ancillas (ancilla k at N+k)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('N', 't', 'eps', 'G', 'dt', 'r'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    N = _as_int(instance['N'], 'N')
    t = _as_int(instance['t'], 't')
    r = _as_int(instance['r'], 'r')
    if N < 2 or t < 1 or r < 1:
        raise ValueError('need N>=2, t>=1, r>=1')
    if N + t > 12:
        raise ValueError('total qubits exceed 12')
    if r * (2 ** t - 1) > 2000:
        raise ValueError('too many Trotter steps')
    eps = instance['eps']
    if not isinstance(eps, (list, tuple)) or len(eps) != N:
        raise ValueError('eps must be a list of length N')
    eps = [_as_real(e, 'eps') for e in eps]
    G = _as_real(instance['G'], 'G')
    dt = _as_real(instance['dt'], 'dt')
    if G < 0 or dt <= 0:
        raise ValueError('need G>=0 and dt>0')
    # j=k terms of -G sum P+_j P-_k give -G n_j: absorb into eps (eq_2).
    eps_eff = [e - G for e in eps]
    h = dt / r
    sysr = QuantumRegister(N, 'sys')
    anc = QuantumRegister(t, 'anc')
    qc = QuantumCircuit(sysr, anc)
    sys_idx = list(range(N))
    anc_idx = list(range(N, N + t))
    for k in range(t):
        for _ in range((2 ** k) * r):
            _controlled_trotter_step(qc, anc_idx[k], sys_idx, eps_eff, G, h)
    qc.append(QFTGate(t).inverse(), anc_idx)
    return qc
