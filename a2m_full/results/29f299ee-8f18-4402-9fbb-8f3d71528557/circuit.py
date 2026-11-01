from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
import math


def _num(instance, key):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(key + ' must be a finite real number')
    return float(v)


def _int(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(key + ' must be an integer in [' + str(lo) + ',' + str(hi) + ']')
    return v


def _build_ut(m, theta, alpha, beta):
    # eq_2: U_T|i>|0>|psi> = sum_j |i>|j> (x) B_ij|psi>, B_{i,i+1}=cos(theta)Ry(alpha), B_{i,i-1}=sin(theta)Rz(beta)
    # eq_1: cos^2 + sin^2 = 1 with unitary Ry, Rz => sum_j B^dagger B = I
    node = list(range(m))
    tgt = list(range(m, 2 * m))
    s = 2 * m
    qc = QuantumCircuit(2 * m + 1)
    # target holds 0 (direction +) or 2^m-2 (direction -), amplitudes cos/sin
    qc.ry(2.0 * theta, tgt[1])
    for q in tgt[2:]:
        qc.cx(tgt[1], q)
    # direction-controlled internal operation (control = tgt[1])
    qc.cry(alpha, tgt[1], s, ctrl_state=0)
    qc.crz(beta, tgt[1], s, ctrl_state=1)
    # Draper adder: target += node + 1 (mod 2^m); value becomes i+1 or i-1
    qc.append(QFTGate(m), tgt)
    for q in range(m):
        qc.p(2.0 * math.pi * (2 ** q) / (2 ** m), tgt[q])
    for k in range(m):
        for q in range(m):
            if k + q < m:
                qc.cp(2.0 * math.pi * (2 ** (k + q)) / (2 ** m), node[k], tgt[q])
    qc.append(QFTGate(m).inverse(), tgt)
    return qc


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    m = _int(instance, 'node_qubits', 2, 5)
    steps = _int(instance, 'steps', 0, 64)
    theta = _num(instance, 'theta')
    alpha = _num(instance, 'alpha')
    beta = _num(instance, 'beta')
    n = 2 * m + 1
    if n > 12:
        raise ValueError('too many qubits')
    node = list(range(m))
    tgt = list(range(m, 2 * m))
    ut = _build_ut(m, theta, alpha, beta)
    utd = ut.inverse()
    qc = QuantumCircuit(n)
    for _ in range(steps):
        # eq_3: R = U_T (2|0><0|_tgt - I) U_T^dagger = 2 Pi - I
        qc.compose(ut, qubits=list(range(n)), inplace=True)
        for q in tgt:
            qc.x(q)
        qc.h(tgt[-1])
        qc.mcx(tgt[:-1], tgt[-1])
        qc.h(tgt[-1])
        for q in tgt:
            qc.x(q)
        qc.compose(utd, qubits=list(range(n)), inplace=True)
        qc.global_phase = qc.global_phase + math.pi
        # eq_3: S = SWAP(node, target)
        for a, b in zip(node, tgt):
            qc.swap(a, b)
    return qc
