"""Three-controlled-unitary decomposition of a two-qubit (d_A = d_B = 2) unitary.

Scoped reconstruction of the bipartite result 'N <= 2 d_A - 1 controlled unitaries
when d_A is a power of two' at its smallest case d_A = 2, instantiated on a single
qubit B (d_B = 2).  The construction follows the cosine-sine decomposition (CSD)

    U = C^A_P  *  C^B_theta  *  C^A_Q                                    (eq_5)

with
    C^A_Q     = sum_j |j><j|_A (x) Q_j            (A-controlled, target B)  (eq_1, eq_4)
    C^B_theta = sum_k Ry(2 theta_k) (x) |k><k|_B  (B-controlled, target A)  (eq_4)
    C^A_P     = sum_j |j><j|_A (x) P_j            (A-controlled, target B)  (eq_1, eq_4)

Operators act right-to-left, so the circuit applies C^A_Q first, then C^B_theta,
then C^A_P.

The classical CSD preprocessing (eq_3) is NOT performed here: the instance must
supply the CSD factors directly.  Each 2x2 target unitary W in {Q_0, Q_1, P_0, P_1}
is given as four real numbers [theta, phi, lam, gamma] meaning

    W = exp(i*gamma) * U(theta, phi, lam),
    U(theta, phi, lam) = [[cos(theta/2),            -exp(i*lam) sin(theta/2)],
                          [exp(i*phi) sin(theta/2),  exp(i*(phi+lam)) cos(theta/2)]],

which is exactly the target convention of Qiskit's CU gate.  The CSD angles are
given as 'theta': [theta_0, theta_1] with Ry(2 theta_k) = [[cos t, -sin t],[sin t, cos t]].

Qubit layout (Qiskit little-endian): qubit 0 = B (least significant), qubit 1 = A
(most significant), so the composite basis vector |j>_A |k>_B has integer index
j*d_B + k = 2 j + k, as in the specification.

Instance format:
    {
      "d_A": 2, "d_B": 2,
      "Q": [[theta, phi, lam, gamma], [theta, phi, lam, gamma]],   # Q_0, Q_1
      "theta": [theta_0, theta_1],                                  # CSD angles
      "P": [[theta, phi, lam, gamma], [theta, phi, lam, gamma]]    # P_0, P_1
    }
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_real(value, name):
    """Validate that value is a finite real number and return it as float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return out


def _as_u2_params(entry, name):
    """Validate a 4-tuple [theta, phi, lam, gamma] describing exp(i gamma) U(theta, phi, lam)."""
    if not isinstance(entry, (list, tuple)) or len(entry) != 4:
        raise ValueError(f"{name} must be a list of four reals [theta, phi, lam, gamma]")
    return tuple(_as_real(entry[i], f"{name}[{i}]") for i in range(4))


def _as_u2_pair(entry, name):
    """Validate a pair [W_0, W_1] of 2x2 unitary parameterisations."""
    if not isinstance(entry, (list, tuple)) or len(entry) != 2:
        raise ValueError(f"{name} must be a list of two entries (one per A basis state)")
    return (_as_u2_params(entry[0], f"{name}[0]"), _as_u2_params(entry[1], f"{name}[1]"))


def _a_controlled(qc, a, b, targets):
    """eq_1 / eq_4: append sum_j |j><j|_A (x) W_j with W_j = exp(i gamma_j) U(theta_j, phi_j, lam_j).

    Control value j = 1 is a plain CU gate; control value j = 0 is obtained by
    conjugating the CU gate with X on the control qubit A.
    """
    for j in (0, 1):
        theta, phi, lam, gamma = targets[j]
        if j == 0:
            qc.x(a)
        qc.cu(theta, phi, lam, gamma, a, b)
        if j == 0:
            qc.x(a)


def _b_controlled_ry(qc, a, b, angles):
    """eq_4: append sum_k Ry(2 theta_k) (x) |k><k|_B (control B, target A).

    Qiskit ry(2t) = [[cos t, -sin t], [sin t, cos t]] reproduces the CSD middle
    block [[C, -S], [S, C]] restricted to the pair |0>_A|k>_B, |1>_A|k>_B.
    """
    for k in (0, 1):
        if k == 0:
            qc.x(b)
        qc.cry(2.0 * angles[k], b, a)
        if k == 0:
            qc.x(b)


def build_circuit(instance):
    """Build U = C^A_P * C^B_theta * C^A_Q (eq_5) as a measurement-free two-qubit circuit."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    for key in ("d_A", "d_B", "Q", "theta", "P"):
        if key not in instance:
            raise ValueError(f"instance is missing required key {key!r}")

    d_a = instance["d_A"]
    d_b = instance["d_B"]
    if isinstance(d_a, bool) or isinstance(d_b, bool) or not isinstance(d_a, int) or not isinstance(d_b, int):
        raise ValueError("d_A and d_B must be integers")
    if d_a != 2 or d_b != 2:
        raise ValueError("this scoped construction supports only d_A = 2 and d_B = 2 (one qubit each)")

    n_a = 1  # qubits for A (d_A = 2)
    n_b = 1  # qubits for B (d_B = 2)
    if n_a + n_b > MAX_QUBITS:
        raise ValueError("too many qubits requested")

    q_params = _as_u2_pair(instance["Q"], "Q")
    p_params = _as_u2_pair(instance["P"], "P")
    theta_raw = instance["theta"]
    if not isinstance(theta_raw, (list, tuple)) or len(theta_raw) != d_b:
        raise ValueError("theta must be a list of d_B = 2 CSD angles")
    csd_angles = tuple(_as_real(theta_raw[k], f"theta[{k}]") for k in range(d_b))

    # qubit 0 = B (least significant), qubit 1 = A (most significant): index j*d_B + k
    reg_b = QuantumRegister(n_b, "b")
    reg_a = QuantumRegister(n_a, "a")
    qc = QuantumCircuit(reg_b, reg_a, name="three_controlled_unitaries")
    a = reg_a[0]
    b = reg_b[0]

    # eq_5, factor applied first (rightmost): C^A_Q = sum_j |j><j|_A (x) Q_j
    _a_controlled(qc, a, b, q_params)
    # eq_5, middle factor: C^B_theta = sum_k Ry(2 theta_k) (x) |k><k|_B
    _b_controlled_ry(qc, a, b, csd_angles)
    # eq_5, factor applied last (leftmost): C^A_P = sum_j |j><j|_A (x) P_j
    _a_controlled(qc, a, b, p_params)

    # Total: N = 3 = 2 d_A - 1 controlled unitaries (eq_2 bound at d_A = 2).
    return qc
