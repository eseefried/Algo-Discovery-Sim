"""Repeat-Until-Success (RUS) two-qubit unitary W for an exact Z-rotation primitive.

Implements eq_W_construction of the specification:
    W   = |0><0|_t (x) M_0 + |1><1|_t (x) M_1,
    M_1 = 2^{-L/2} [[z, -y], [y, z*]],   M_0 = conj(M_1),
with z in Z[omega] (omega = exp(i pi/4)), y in Z[sqrt2] and |z|^2 + y^2 = 2^L
(eq_norm_equation).  Then the ancilla-0 block is A = diag(z*, z)/2^{L/2}
(success: target gets R_z(2 arg z)) and the ancilla-1 block is C = y I / 2^{L/2}
(failure: identity on the target), as required by eq_rus_structure.

Exact gate factorization used here.  Write z = |z| e^{i phi},
cos(th) = |z|/sqrt(2^L), sin(th) = y/sqrt(2^L).  Then
    M_1 = Rz(-phi) Ry(2 th) Rz(-phi),   M_0 = Rz(+phi) Ry(2 th) Rz(+phi),
where Rz(alpha) = diag(e^{-i alpha/2}, e^{+i alpha/2}).  The target-conditioned
pair of Z-rotations on the ancilla is exactly exp(-i phi/2 Z_a Z_t) = RZZ(phi), so
    W = RZZ(phi) . RY(2 th)_ancilla . RZZ(phi).

Qubit layout (Qiskit little-endian): ancilla a = qubit `ancilla_index` (default 1,
the most significant qubit so that the joint basis index is 2a + t as in the
specification), target t = the other qubit.  The ancilla is expected in |0>; it
is not prepared or measured here.

Instance format:
    {"z": [a, b, c, d],       # z = a + b omega + c omega^2 + d omega^3, integers
     "y": [e, f],             # y = e + f sqrt(2), integers
     "L": L,                  # nonnegative integer, 2^L = |z|^2 + y^2
     "ancilla_index": 1}      # optional, 0 or 1
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

SQRT2 = math.sqrt(2.0)
MAX_L = 60
NUM_QUBITS = 2
MAX_QUBITS = 12


def _int_list(value, length, name):
    """Validate that `value` is a list/tuple of `length` Python integers."""
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError(name + ' must be a list of ' + str(length) + ' integers')
    out = []
    for v in value:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError(name + ' entries must be integers')
        out.append(int(v))
    return out


def _parse_instance(instance):
    """Extract and validate (z, y, L, ancilla_index) from the instance dict."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key not in ('z', 'y', 'L', 'ancilla_index'):
            raise ValueError('unknown instance key: ' + str(key))
    for key in ('z', 'y', 'L'):
        if key not in instance:
            raise ValueError('instance requires key ' + key)
    z = _int_list(instance['z'], 4, 'z')
    y = _int_list(instance['y'], 2, 'y')
    big_l = instance['L']
    if isinstance(big_l, bool) or not isinstance(big_l, int):
        raise ValueError('L must be an integer')
    if big_l < 0 or big_l > MAX_L:
        raise ValueError('L must satisfy 0 <= L <= ' + str(MAX_L))
    anc = instance.get('ancilla_index', 1)
    if isinstance(anc, bool) or not isinstance(anc, int) or anc not in (0, 1):
        raise ValueError('ancilla_index must be 0 or 1')
    return z, y, int(big_l), int(anc)


def _check_norm_equation(z, y, big_l):
    """eq_norm_equation: exact check of |z|^2 + y^2 = 2^L in Z[sqrt2].

    For z = a + b w + c w^2 + d w^3 (w = exp(i pi/4)):
        |z|^2 = (a^2+b^2+c^2+d^2) + sqrt2 (ab - ad + bc + cd),
    and for y = e + f sqrt2:
        y^2 = (e^2 + 2 f^2) + sqrt2 (2 e f).
    Both the rational and the sqrt2 coefficient must match 2^L + 0 sqrt2.
    """
    a, b, c, d = z
    e, f = y
    if a == 0 and b == 0 and c == 0 and d == 0:
        raise ValueError('z must be nonzero (success branch undefined for z = 0)')
    rational = a * a + b * b + c * c + d * d + e * e + 2 * f * f
    irrational = a * b - a * d + b * c + c * d + 2 * e * f
    if irrational != 0:
        raise ValueError('norm equation violated: sqrt2 coefficient of |z|^2 + y^2 is nonzero')
    if rational != 2 ** big_l:
        raise ValueError('norm equation violated: |z|^2 + y^2 != 2^L')


def _angles(z, y):
    """Rotation angles for the exact factorization of M_0 and M_1.

    Returns (phi, 2*th) with phi = arg z and
    cos(th) = |z|/sqrt(2^L), sin(th) = y/sqrt(2^L)  (sqrt(2^L) = hypot(|z|, y)).
    """
    a, b, c, d = z
    e, f = y
    re_z = a + (b - d) / SQRT2
    im_z = c + (b + d) / SQRT2
    phi = math.atan2(im_z, re_z)
    y_val = e + f * SQRT2
    mod_z = math.hypot(re_z, im_z)
    th = math.atan2(y_val, mod_z)
    return phi, 2.0 * th


def build_circuit(instance):
    """Return the 2-qubit RUS unitary W (eq_W_construction) as a QuantumCircuit.

    The circuit is unitary and measurement-free.  The runner is expected to
    prepare the ancilla (qubit `ancilla_index`) in |0> and, after W, measure it:
    outcome 0 -> target received R_z(2 arg z); outcome 1 -> target unchanged
    (eq_rus_structure); repetition/reset is outside this operation.
    """
    z, y, big_l, anc = _parse_instance(instance)
    _check_norm_equation(z, y, big_l)  # eq_norm_equation (exact integer check)
    if NUM_QUBITS > MAX_QUBITS:
        raise ValueError('qubit cap exceeded')
    phi, ry_angle = _angles(z, y)
    tgt = 1 - anc

    q = QuantumRegister(NUM_QUBITS, 'q')
    qc = QuantumCircuit(q, name='rus_W')

    # eq_W_construction / eq_rus_structure:
    # W = |0><0|_t (x) M_0 + |1><1|_t (x) M_1
    #   = RZZ(phi)_{a,t} . RY(2 th)_a . RZZ(phi)_{a,t}
    # RZZ(phi) = exp(-i phi/2 Z_a Z_t) applies Rz(+phi) to the ancilla when t=0
    # and Rz(-phi) when t=1, which is exactly the target-controlled choice between
    # M_0 = Rz(phi) Ry(2th) Rz(phi) and M_1 = Rz(-phi) Ry(2th) Rz(-phi).
    qc.rzz(phi, q[anc], q[tgt])
    qc.ry(ry_angle, q[anc])
    qc.rzz(phi, q[anc], q[tgt])
    return qc
