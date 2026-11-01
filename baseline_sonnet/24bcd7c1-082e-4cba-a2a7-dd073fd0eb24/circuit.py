from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _get_int(instance, key, lo, hi):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' out of range')
    return v


def _get_prob(instance, key):
    v = instance.get(key, 0.0)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a number')
    v = float(v)
    if not math.isfinite(v) or v < 0.0 or v > 1.0:
        raise ValueError(key + ' must be in [0, 1]')
    return v


def _shift(qc, spin, pos, n):
    # eq_1: S = |up><up| (x) T_+ + |down><down| (x) T_-, up = |0>, cyclic lattice.
    # Shift by +-1 is diagonal in the Fourier basis: phase exp(+-2 pi i k / N).
    qc.append(QFTGate(n), pos)
    for j in range(n):
        theta = 2.0 * math.pi * (2 ** j) / (2 ** n)
        qc.p(theta, pos[j])
        qc.cp(-2.0 * theta, spin, pos[j])
    qc.append(QFTGate(n).inverse(), pos)


def build_circuit(instance):
    """instance: {n_position_qubits, steps, p_spin, q_space}. Returns unitary dilation of the decohered walk."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _get_int(instance, 'n_position_qubits', 1, 10)
    steps = _get_int(instance, 'steps', 1, 10)
    p = _get_prob(instance, 'p_spin')
    q = _get_prob(instance, 'q_space')
    n_es = steps if p > 0.0 else 0
    n_ep = steps if q > 0.0 else 0
    if 1 + n + n_es + n_ep > 12:
        raise ValueError('total qubits exceed 12')
    spin_r = QuantumRegister(1, 'spin')
    pos_r = QuantumRegister(n, 'pos')
    regs = [spin_r, pos_r]
    es_r = None
    ep_r = None
    if n_es:
        es_r = QuantumRegister(n_es, 'env_spin')
        regs.append(es_r)
    if n_ep:
        ep_r = QuantumRegister(n_ep, 'env_pos')
        regs.append(ep_r)
    qc = QuantumCircuit(*regs)
    spin = spin_r[0]
    pos = list(pos_r)
    th_s = 2.0 * math.asin(math.sqrt(p))
    th_q = 2.0 * math.asin(math.sqrt(q))
    for t in range(steps):
        # eq_1: U = S (C (x) 1), Hadamard coin then shift
        qc.h(spin)
        _shift(qc, spin, pos, n)
        # eq_2: spin phase-flip channel with prob p (environment qubit dilation)
        if n_es:
            e = es_r[t]
            qc.ry(th_s, e)
            qc.cz(e, spin)
        # eq_3: Z_x = (-1)^x = Z on position bit 0, applied with prob q
        if n_ep:
            e = ep_r[t]
            qc.ry(th_q, e)
            qc.cz(e, pos[0])
    return qc
