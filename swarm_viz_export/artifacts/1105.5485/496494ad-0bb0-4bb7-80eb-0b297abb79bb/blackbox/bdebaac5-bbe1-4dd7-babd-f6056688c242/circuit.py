import math
import numpy as np
from qiskit import QuantumCircuit


def _phase_level(qc, level, angle):
    # phase e^{i angle} on one level (0..2) of a qutrit held in qubits 0,1 of qc
    if level == 0:
        zeros = [0, 1]
    elif level == 1:
        zeros = [1]
    else:
        zeros = [0]
    for q in zeros:
        qc.x(q)
    qc.cp(float(angle), 0, 1)
    for q in zeros:
        qc.x(q)


def _ctrl_u(qc, M, ctrl, ctrl_state, tgt):
    # controlled arbitrary 2x2 unitary M = e^{i alpha} Rz(beta) Ry(gamma) Rz(delta)
    det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
    alpha = np.angle(det) / 2.0
    V = M * np.exp(-1j * alpha)
    gamma = 2.0 * math.atan2(abs(V[1, 0]), abs(V[0, 0]))
    s = -2.0 * np.angle(V[0, 0])
    d = 2.0 * np.angle(V[1, 0])
    beta = (s + d) / 2.0
    delta = (s - d) / 2.0
    if ctrl_state == 0:
        qc.x(ctrl)
    qc.p(float(alpha), ctrl)
    qc.crz(float(delta), ctrl, tgt)
    qc.cry(float(gamma), ctrl, tgt)
    qc.crz(float(beta), ctrl, tgt)
    if ctrl_state == 0:
        qc.x(ctrl)


def _two_level(qc, i, j, M):
    # apply 2x2 unitary M on levels (i,j) of a qutrit in qubits (0,1); other levels fixed
    if (i, j) == (0, 1):
        _ctrl_u(qc, M, 1, 0, 0)
    elif (i, j) == (1, 2):
        qc.cx(0, 1)
        M2 = np.array([[M[1, 1], M[1, 0]], [M[0, 1], M[0, 0]]])
        _ctrl_u(qc, M2, 1, 1, 0)
        qc.cx(0, 1)
    else:
        raise ValueError('unsupported level pair')


def _fourier_circuit():
    # eq_1: F|j> = 3^-1/2 sum_k w^{jk}|k> on levels 0..2, identity on level 3
    w = np.exp(2j * np.pi / 3.0)
    U = np.array([[w ** (j * k) for j in range(3)] for k in range(3)], dtype=complex) / math.sqrt(3.0)
    gates = []
    for c in range(2):
        for r in range(2, c, -1):
            a = U[r - 1, c]
            b = U[r, c]
            if abs(b) < 1e-12:
                continue
            n = math.hypot(abs(a), abs(b))
            G = np.array([[np.conj(a), np.conj(b)], [-b, a]]) / n
            rows = [r - 1, r]
            U[rows, :] = G @ U[rows, :]
            gates.append((r - 1, r, G))
    diag = np.diag(U)
    sub = QuantumCircuit(2)
    for k in range(3):
        _phase_level(sub, k, float(np.angle(diag[k])))
    for (i, j, G) in reversed(gates):
        _two_level(sub, i, j, np.conj(G.T))
    return sub


def _cz3(qc, sign):
    # eq_2: CZ3|a,b> = w^{ab}|a,b>; qutrit a on qubits 0,1; qutrit b on qubits 2,3
    zero_a = {1: 1, 2: 0}
    zero_b = {1: 3, 2: 2}
    for a in (1, 2):
        for b in (1, 2):
            angle = sign * 2.0 * math.pi / 3.0 * ((a * b) % 3)
            zs = [zero_a[a], zero_b[b]]
            for q in zs:
                qc.x(q)
            qc.mcp(float(angle), [0, 1, 2], 3)
            for q in zs:
                qc.x(q)


def _cx3(qc, target, inverse):
    # eq_3: CX3 = (I x F^dag) CZ3^(+-1) (I x F) on the target qutrit (CZ3 is symmetric)
    fc = _fourier_circuit()
    tq = [0, 1] if target == 0 else [2, 3]
    qc.compose(fc, qubits=tq, inplace=True)
    _cz3(qc, -1.0 if inverse else 1.0)
    qc.compose(fc.inverse(), qubits=tq, inplace=True)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    op = instance.get('operation')
    if op == 'cx3':
        allowed = {'operation', 'control', 'inverse'}
    elif op == 'swap3':
        allowed = {'operation'}
    else:
        raise ValueError('operation must be cx3 or swap3')
    if not set(instance.keys()) <= allowed:
        raise ValueError('unknown instance keys')
    qc = QuantumCircuit(4)
    if op == 'cx3':
        control = instance.get('control', 0)
        inverse = instance.get('inverse', False)
        if isinstance(control, bool) or control not in (0, 1):
            raise ValueError('control must be 0 or 1')
        if not isinstance(inverse, bool):
            raise ValueError('inverse must be bool')
        _cx3(qc, 1 - control, inverse)
    else:
        # eq_4: SWAP3 = (N x I) CX(a->b) CX(b->a)^-1 CX(a->b); N = F^2 = qubit SWAP on qutrit a
        _cx3(qc, 1, False)
        _cx3(qc, 0, True)
        _cx3(qc, 1, False)
        qc.swap(0, 1)
    return qc
