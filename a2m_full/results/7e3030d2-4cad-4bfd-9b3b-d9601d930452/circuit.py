from qiskit import QuantumCircuit
import math


def _get(instance, key, lo_inclusive):
    if key not in instance:
        raise ValueError('missing parameter ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError('parameter ' + key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v) or v < 0.0 or (v == 0.0 and not lo_inclusive):
        raise ValueError('parameter ' + key + ' out of range')
    return v


def _dephase(qc, sys_q, anc, gamma, s):
    # eq_5 dephasing: rho01 -> exp(-gamma s) rho01 = Kraus {sqrt(1-q) I, sqrt(q) Z}, q=(1-e^{-gamma s})/2
    # eq_4: dilation with a fresh ancilla in |0>
    q = (1.0 - math.exp(-gamma * s)) / 2.0
    phi = 2.0 * math.asin(math.sqrt(min(1.0, max(0.0, q))))
    qc.ry(phi, anc)
    qc.cz(anc, sys_q)


def _damp(qc, sys_q, anc, rate, s):
    # eq_5 amplitude damping, p = 1 - exp(-Gamma s); eq_4 dilation:
    # controlled-RY(2 asin sqrt p) from system to ancilla, then CNOT ancilla -> system
    p = 1.0 - math.exp(-rate * s)
    phi = 2.0 * math.asin(math.sqrt(min(1.0, max(0.0, p))))
    qc.cry(phi, sys_q, anc)
    qc.cx(anc, sys_q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    t = _get(instance, 't', True)
    omega = _get(instance, 'omega', True)
    gamma = _get(instance, 'gamma', True)
    rate = _get(instance, 'Gamma', True)
    r = instance.get('r')
    if isinstance(r, bool) or not isinstance(r, int) or r < 1:
        raise ValueError('r must be a positive integer')
    if 1 + 2 * r > 12:
        raise ValueError('r too large: needs 1+2r <= 12 qubits')
    qc = QuantumCircuit(1 + 2 * r)
    s = t / r
    # eq_2: S2(s) = H(s/2) D(s/2) A(s) D(s/2) H(s/2); D and A commute so D(s/2)A(s)D(s/2)=D(s)A(s);
    # adjacent H(s/2) factors of neighbouring segments merge to H(s). H(s)=exp(-i omega s X/2)=rx(omega s)
    qc.rx(omega * s / 2.0, 0)
    for k in range(r):
        _dephase(qc, 0, 1 + 2 * k, gamma, s)
        _damp(qc, 0, 2 + 2 * k, rate, s)
        if k < r - 1:
            qc.rx(omega * s, 0)
    qc.rx(omega * s / 2.0, 0)
    return qc
