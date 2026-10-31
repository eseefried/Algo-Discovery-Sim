"""Amplitude-estimation mean estimator for a black-box F on N = 2^n points.

Registers (Qiskit little-endian, qubit 0 = least significant):
  idx[0..n-1]  : index register, idx[k] has weight 2^k in x
  anc          : value ancilla, marked subspace is anc = |1>
  prec[0..m-1] : phase-estimation register, prec[k] controls Q^(2^k)

build_circuit(instance) returns the unitary (no measurement):
  A on (idx,anc); H on prec; controlled-Q^(2^k) from prec[k]; inverse QFT on prec.
Classical post-processing (not part of the circuit): read y = sum_k y_k 2^k from
prec and output mu_tilde = sin^2(pi * y / 2^m)   (eq_5).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate, ZGate

MAX_QUBITS = 12


def _validate(instance):
    """Validate the instance and return (n, m, list_of_F_values)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    n = instance.get("n")
    m = instance.get("m")
    values = instance.get("values")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer (number of index qubits)")
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError("m must be a positive integer (number of precision qubits)")
    if n + 1 + m > MAX_QUBITS:
        raise ValueError("total qubits n + 1 + m exceeds the cap of 12")
    if not isinstance(values, (list, tuple)) or len(values) != 2 ** n:
        raise ValueError("values must be a list of exactly 2**n numbers")
    vals = []
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError("each F value must be a real number")
        f = float(v)
        if not math.isfinite(f) or f < 0.0 or f > 1.0:
            raise ValueError("each F value must lie in [0, 1]  (eq_1 normalisation)")
        vals.append(f)
    return n, m, vals


def _oracle(n, vals):
    """eq_2: U_F |x>|0> = |x>(sqrt(1-F(x))|0> + sqrt(F(x))|1>) via controlled RY."""
    qc = QuantumCircuit(n + 1, name="U_F")
    idx = list(range(n))
    anc = n
    for x, f in enumerate(vals):
        angle = 2.0 * math.asin(math.sqrt(f))
        if angle == 0.0:
            continue
        # control state x in little-endian over idx[0..n-1]; RY(angle)|0> has amplitude sqrt(F(x)) on |1>
        qc.append(RYGate(angle).control(num_ctrl_qubits=n, ctrl_state=x), idx + [anc])
    return qc


def _prep_a(n, vals):
    """eq_3: A = U_F (H^{(x)n} (x) I); ancilla-1 probability equals the mean mu."""
    qc = QuantumCircuit(n + 1, name="A")
    for q in range(n):
        qc.h(q)
    qc.compose(_oracle(n, vals), inplace=True)
    return qc


def _grover_q_prime(n, vals):
    """eq_4: Q' = A S_0 A^dag S_chi, so that Q = -Q'.

    S_chi = Z on the ancilla (sign flip of ancilla-1 states),
    S_0 = I - 2|0...0><0...0| = X^{(x)(n+1)} (multi-controlled Z) X^{(x)(n+1)}.
    The overall minus sign of Q is applied in build_circuit as a Z on the control
    qubit of the odd power (controlled -I == Z on control).
    """
    a = _prep_a(n, vals)
    qc = QuantumCircuit(n + 1, name="Qp")
    qc.z(n)                                   # S_chi
    qc.compose(a.inverse(), inplace=True)     # A^dag
    for q in range(n + 1):                    # S_0
        qc.x(q)
    qc.append(ZGate().control(num_ctrl_qubits=n), list(range(n + 1)))
    for q in range(n + 1):
        qc.x(q)
    qc.compose(a, inplace=True)               # A
    return qc


def build_circuit(instance):
    """Amplitude estimation of the mean of F (eq_3-eq_5), measurement-free."""
    n, m, vals = _validate(instance)
    idx = QuantumRegister(n, "idx")
    anc = QuantumRegister(1, "anc")
    prec = QuantumRegister(m, "prec")
    qc = QuantumCircuit(idx, anc, prec)
    sys_q = list(idx) + list(anc)

    # state preparation A |0^n>|0>  (eq_3)
    qc.compose(_prep_a(n, vals), qubits=sys_q, inplace=True)

    # phase estimation of Q (eq_4 -> eq_5)
    for k in range(m):
        qc.h(prec[k])
    cqp = _grover_q_prime(n, vals).to_gate().control(1)
    for k in range(m):
        if k == 0:
            # Q^(2^0) = -Q': controlled (-1) factor == Z on the control qubit
            qc.z(prec[0])
        for rep in range(2 ** k):
            qc.append(cqp, [prec[k]] + sys_q)

    # inverse QFT on the precision register; prec[0] is the least significant bit of y
    qc.append(QFTGate(m).inverse(), list(prec))
    return qc
