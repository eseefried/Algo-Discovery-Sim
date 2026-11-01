import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

_EPS = 1e-12


def _bloch_vectors(povm, offset):
    '''Bloch vectors n_k and weight w with E_k = w|psi_k><psi_k| (eq_2 trine, eq_3 SIC).'''
    if povm == 'trine':
        vecs = [(math.cos(2.0 * math.pi * k / 3.0 + offset), math.sin(2.0 * math.pi * k / 3.0 + offset), 0.0) for k in range(3)]
        return vecs, 2.0 / 3.0
    s2 = math.sqrt(2.0)
    s23 = math.sqrt(2.0 / 3.0)
    base = [(0.0, 0.0, 1.0), (2.0 * s2 / 3.0, 0.0, -1.0 / 3.0), (-s2 / 3.0, s23, -1.0 / 3.0), (-s2 / 3.0, -s23, -1.0 / 3.0)]
    c = math.cos(offset)
    s = math.sin(offset)
    vecs = [(c * x - s * y, s * x + c * y, z) for (x, y, z) in base]
    return vecs, 0.5


def _isometry(povm, offset):
    '''4x2 isometry V with V[k,j] = sqrt(w) <psi_k|j>, so V^dag V = sum_k E_k = I (eq_1).'''
    vecs, w = _bloch_vectors(povm, offset)
    m = np.zeros((4, 2), dtype=complex)
    for k, (x, y, z) in enumerate(vecs):
        th = math.acos(max(-1.0, min(1.0, z)))
        ph = math.atan2(y, x)
        psi = np.array([math.cos(th / 2.0), np.exp(1j * ph) * math.sin(th / 2.0)])
        m[k, :] = math.sqrt(w) * np.conj(psi)
    return m


def _givens(m, col, a, b, keep):
    '''Two-level unitary that zeroes the non-kept entry of column col; applied to m in place.'''
    xa = m[a, col]
    xb = m[b, col]
    elim = xb if keep == a else xa
    if abs(elim) < _EPS:
        return None
    r = math.sqrt(abs(xa) ** 2 + abs(xb) ** 2)
    if keep == a:
        g = np.array([[np.conj(xa), np.conj(xb)], [-xb, xa]]) / r
    else:
        g = np.array([[xb, -xa], [np.conj(xa), np.conj(xb)]]) / r
    m[[a, b], :] = g @ m[[a, b], :]
    return g


def _cu_params(g):
    c = abs(g[0, 0])
    s = abs(g[1, 0])
    theta = 2.0 * math.atan2(s, c)
    if c > _EPS:
        gam = float(np.angle(g[0, 0]))
        if s > _EPS:
            phi = float(np.angle(g[1, 0])) - gam
            lam = float(np.angle(-g[0, 1])) - gam
        else:
            phi = 0.0
            lam = float(np.angle(g[1, 1])) - gam
    else:
        gam = 0.0
        phi = float(np.angle(g[1, 0]))
        lam = float(np.angle(-g[0, 1]))
    return theta, phi, lam, gam


def _two_level(qc, a, b, g):
    '''Apply 2x2 unitary g on basis states a<b (index = q0 + 2*q1) differing in one bit.'''
    diff = a ^ b
    if diff == 1:
        tgt, ctl, val = 0, 1, (a >> 1) & 1
    elif diff == 2:
        tgt, ctl, val = 1, 0, a & 1
    else:
        raise ValueError('unsupported two-level pair')
    th, ph, la, ga = _cu_params(g)
    if val == 0:
        qc.x(ctl)
    qc.cu(th, ph, la, ga, ctl, tgt)
    if val == 0:
        qc.x(ctl)


def build_circuit(instance):
    '''Naimark-dilation unitary for the trine or SIC POVM. Outcome k = q0 + 2*q1.'''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key not in ('povm', 'azimuth_offset'):
            raise ValueError('unknown instance key')
    povm = instance.get('povm')
    if povm not in ('trine', 'sic'):
        raise ValueError('povm must be trine or sic')
    offset = instance.get('azimuth_offset', 0.0)
    if isinstance(offset, bool) or not isinstance(offset, (int, float)):
        raise ValueError('azimuth_offset must be a real number')
    offset = float(offset)
    if not math.isfinite(offset):
        raise ValueError('azimuth_offset must be finite')
    m = _isometry(povm, offset)
    gates = []
    plan = [(0, 2, 3, 2), (0, 0, 2, 0), (0, 0, 1, 0), (1, 2, 3, 3), (1, 1, 3, 1)]
    for (col, a, b, keep) in plan:
        g = _givens(m, col, a, b, keep)
        if g is not None:
            gates.append((a, b, g))
    if abs(abs(m[0, 0]) - 1.0) > 1e-8 or abs(abs(m[1, 1]) - 1.0) > 1e-8:
        raise ValueError('internal elimination failed')
    alpha = float(np.angle(m[0, 0]))
    beta = float(np.angle(m[1, 1]))
    qc = QuantumCircuit(QuantumRegister(1, 'sys'), QuantumRegister(1, 'anc'))
    # D^dagger: phase e^{i alpha} on index 0 and e^{i beta} on index 1 (both have q1=0)
    qc.x(1)
    qc.p(alpha, 1)
    qc.cp(beta - alpha, 1, 0)
    qc.x(1)
    # U = G_1^dag ... G_m^dag D^dag : apply G_m^dag first
    for (a, b, g) in reversed(gates):
        _two_level(qc, a, b, np.conj(g.T))
    return qc
