'''Column-by-column isometry synthesis (Givens rotations as multi-controlled SU(2) gates).'''
import math
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, RZGate, PhaseGate


def _angles(p, q):
    '''ZYZ angles with Rz(phi) Ry(theta) Rz(lam) = [[p, q], [-conj(q), conj(p)]] (SU(2)).'''
    theta = 2.0 * float(np.arctan2(abs(q), abs(p)))
    ap = float(np.angle(p))
    aq = float(np.angle(q))
    return theta, -ap - aq - math.pi, -ap + aq + math.pi


def _ctrl(qc, gate, ctrls, t, cs):
    if ctrls:
        qc.append(gate.control(len(ctrls), ctrl_state=cs), list(ctrls) + [t])
    else:
        qc.append(gate, [t])


def _givens(qc, W, n, c, i):
    '''Zero W[i, c] into W[c, c] by a two-level rotation on span{|c>, |i>} (eq_3).'''
    if abs(W[i, c]) < 1e-12:
        return
    x = c ^ i
    t = (x & -x).bit_length() - 1
    if (c >> t) & 1:
        a, b = i, c
    else:
        a, b = c, i
    alpha = W[a, c]
    beta = W[b, c]
    r = math.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    if i == b:
        p = np.conj(alpha) / r
        q = np.conj(beta) / r
    else:
        p = beta / r
        q = -alpha / r
    um = np.array([[p, q], [-np.conj(q), np.conj(p)]], dtype=complex)
    W[[a, b], :] = um @ W[[a, b], :]
    theta, phi, lam = _angles(p, q)
    others = [j for j in range(n) if j != t]
    cs = 0
    for pos, j in enumerate(others):
        cs |= ((a >> j) & 1) << pos
    flips = [d for d in range(n) if d != t and (x >> d) & 1]
    for d in flips:
        qc.cx(t, d)
    if abs(lam) > 1e-12:
        _ctrl(qc, RZGate(lam), others, t, cs)
    if abs(theta) > 1e-12:
        _ctrl(qc, RYGate(theta), others, t, cs)
    if abs(phi) > 1e-12:
        _ctrl(qc, RZGate(phi), others, t, cs)
    for d in reversed(flips):
        qc.cx(t, d)


def _phase_fix(qc, W, n, c):
    '''Multiply basis state |c> by exp(-i arg W[c,c]) leaving all other basis states fixed.'''
    ph = float(np.angle(W[c, c]))
    if abs(ph) < 1e-12:
        return
    W[c, :] = W[c, :] * np.exp(-1j * ph)
    if (c & 1) == 0:
        qc.x(0)
    if n == 1:
        qc.p(-ph, 0)
    else:
        qc.append(PhaseGate(-ph).control(n - 1, ctrl_state=c >> 1), list(range(1, n)) + [0])
    if (c & 1) == 0:
        qc.x(0)


def build_circuit(instance):
    '''instance: {n, m, matrix_real, matrix_imag (optional)}; matrix has shape (2^n, 2^m).'''
    try:
        n = int(instance['n'])
        m = int(instance['m'])
        if n < 1 or n > 12 or m < 0 or m > n:
            raise ValueError('require 1 <= n <= 12 and 0 <= m <= n')
        re = np.array(instance['matrix_real'], dtype=float)
        if 'matrix_imag' in instance:
            im = np.array(instance['matrix_imag'], dtype=float)
        else:
            im = np.zeros_like(re)
    except (KeyError, TypeError, ValueError, AttributeError):
        raise ValueError('invalid instance: need integer n, m and numeric matrix_real[, matrix_imag]')
    if re.shape != (2 ** n, 2 ** m) or im.shape != re.shape:
        raise ValueError('matrix must have shape (2^n, 2^m)')
    V = re + 1j * im
    if not np.all(np.isfinite(V)):
        raise ValueError('matrix must be finite')
    if not np.allclose(V.conj().T @ V, np.eye(2 ** m), atol=1e-8):
        raise ValueError('matrix is not an isometry')
    W = V.astype(complex).copy()
    red = QuantumCircuit(n, name='isometry_reduction')
    for c in range(2 ** m):
        for i in range(2 ** n - 1, c, -1):
            _givens(red, W, n, c, i)
        _phase_fix(red, W, n, c)
    out = red.inverse()
    out.name = 'isometry'
    return out
