from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key != 'phase_offset':
            raise ValueError('unknown instance key: %s' % key)
    off = instance.get('phase_offset', 0.0)
    if isinstance(off, bool) or not isinstance(off, (int, float)) or not math.isfinite(off):
        raise ValueError('phase_offset must be a finite real number')
    return float(off)


def _isometry_columns(off):
    # eq_2: Trine elements E_k = (2/3)|psi_k><psi_k|, Bloch vector (cos t_k, sin t_k, 0), t_k = off + 2 pi k/3.
    # Rotated frame: |psi_k> = Rx(-pi/2)|psi'_k>, psi' real with Bloch polar angle alpha_k = pi/2 - t_k.
    # Kraus row k of the isometry: sqrt(2/3) <psi'_k| (real). Returned as a 4x2 matrix (4th row zero).
    m = np.zeros((4, 2))
    for k in range(3):
        t = off + 2.0 * math.pi * k / 3.0
        alpha = math.pi / 2.0 - t
        m[k, 0] = math.sqrt(2.0 / 3.0) * math.cos(alpha / 2.0)
        m[k, 1] = math.sqrt(2.0 / 3.0) * math.sin(alpha / 2.0)
    return m


def _givens_sequence(m):
    # Givens rotations (only between basis states differing in one bit) with G m = [e0, e1].
    mm = m.copy()
    seq = []
    for (i, j, col) in [(1, 3, 0), (0, 2, 0), (0, 1, 0), (3, 2, 1), (1, 3, 1)]:
        th = math.atan2(mm[j, col], mm[i, col])
        c = math.cos(th)
        s = math.sin(th)
        ri = mm[i].copy()
        rj = mm[j].copy()
        mm[i] = c * ri + s * rj
        mm[j] = -s * ri + c * rj
        seq.append((i, j, th))
    return seq


def _inverse_givens_gate(qc, i, j, th):
    # Append G^T for G = [[c, s], [-s, c]] on (i, j); position bit b is qubit 1 + b.
    if abs(th) < 1e-13:
        return
    diff = i ^ j
    t = diff.bit_length() - 1
    o = 1 - t
    i_low = ((i >> t) & 1) == 0
    phi = -2.0 * th if i_low else 2.0 * th
    angle = -phi
    val = (i >> o) & 1
    ctrl = 1 + o
    tgt = 1 + t
    if val == 0:
        qc.x(ctrl)
    qc.cry(angle, ctrl, tgt)
    if val == 0:
        qc.x(ctrl)


def build_circuit(instance):
    """Trine-POVM dilation. Qubit 0 = polarisation (input), qubits 1,2 = position x = q1 + 2*q2 (input |00>).
    Output: pol |0>, position sum_k sqrt(2/3)<psi_k|phi> |k>, k in {0,1,2}."""
    off = _parse(instance)
    pol = QuantumRegister(1, 'pol')
    pos = QuantumRegister(2, 'pos')
    qc = QuantumCircuit(pol, pos)
    seq = _givens_sequence(_isometry_columns(off))
    # eq_3 (modified): V = sum_k sqrt(2/3)|0><psi_k| (x) |k>; frame change R^dagger = Rx(pi/2)
    qc.rx(math.pi / 2.0, 0)
    # move the input qubit into the position register (pol ends in |0>)
    qc.swap(0, 1)
    # real orthogonal Q on position qubits with Q e0 = u0, Q e1 = u1 (Q = G_1^T ... G_m^T)
    for (i, j, th) in reversed(seq):
        _inverse_givens_gate(qc, i, j, th)
    return qc
