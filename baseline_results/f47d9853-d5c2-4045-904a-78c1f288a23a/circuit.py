"""First-order Trotter step for a Jordan-Wigner Pauli-string Hamiltonian.

build_circuit(instance) returns the unitary
    U_T(dt)^num_steps,  U_T(dt) = prod_{j=1}^{L} exp(-i c_j P_j dt)
(eq_2, product applied in the listed term order j = 1..L), where
H = sum_j c_j P_j (eq_1, after Jordan-Wigner) is given by the instance.

Pauli labels use the Qiskit convention: the rightmost character acts on
qubit 0 (least significant, occupation of spin orbital 0).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

_MAX_QUBITS = 12
_MAX_STEPS = 64
_PAULI_CHARS = "IXYZ"


def _check_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    val = float(value)
    if not math.isfinite(val):
        raise ValueError(f"{name} must be finite")
    return val


def _check_int(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < lo or value > hi:
        raise ValueError(f"{name} must satisfy {lo} <= {name} <= {hi}")
    return value


def _parse_terms(instance, n):
    """eq_1: parse H = sum_j c_j P_j (ordered list of Pauli strings)."""
    terms = instance.get("terms")
    if not isinstance(terms, list) or len(terms) == 0:
        raise ValueError("terms must be a non-empty list")
    parsed = []
    for k, term in enumerate(terms):
        if not isinstance(term, dict):
            raise ValueError(f"terms[{k}] must be an object")
        label = term.get("pauli")
        if not isinstance(label, str) or len(label) != n:
            raise ValueError(f"terms[{k}].pauli must be a string of length {n}")
        for ch in label:
            if ch not in _PAULI_CHARS:
                raise ValueError(f"terms[{k}].pauli contains invalid character {ch!r}")
        coeff = _check_real(term.get("coeff"), f"terms[{k}].coeff")
        parsed.append((label, coeff))
    return parsed


def _append_pauli_rotation(qc, label, theta, n):
    """Append exp(-i * theta * P) for Pauli string P (Qiskit label order)."""
    support = []
    for q in range(n):
        ch = label[n - 1 - q]
        if ch != "I":
            support.append((q, ch))
    if len(support) == 0:
        # exp(-i theta I) is a global phase
        qc.global_phase -= theta
        return
    # basis change to Z eigenbasis
    for q, ch in support:
        if ch == "X":
            qc.h(q)
        elif ch == "Y":
            qc.sdg(q)
            qc.h(q)
    # parity ladder onto the last support qubit
    qubits = [q for q, _ in support]
    for i in range(len(qubits) - 1):
        qc.cx(qubits[i], qubits[i + 1])
    # Rz(2 theta) = exp(-i theta Z)
    qc.rz(2.0 * theta, qubits[-1])
    for i in range(len(qubits) - 2, -1, -1):
        qc.cx(qubits[i], qubits[i + 1])
    for q, ch in support:
        if ch == "X":
            qc.h(q)
        elif ch == "Y":
            qc.h(q)
            qc.s(q)


def build_circuit(instance):
    """Return U_T(dt)^num_steps as a measurement-free QuantumCircuit (eq_2)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object")
    n = _check_int(instance.get("num_qubits"), "num_qubits", 1, _MAX_QUBITS)
    dt = _check_real(instance.get("dt"), "dt")
    if dt <= 0.0:
        raise ValueError("dt must be positive")
    num_steps = instance.get("num_steps")
    if num_steps is None:
        num_steps = 1
    num_steps = _check_int(num_steps, "num_steps", 1, _MAX_STEPS)
    terms = _parse_terms(instance, n)

    sys_reg = QuantumRegister(n, "sys")
    qc = QuantumCircuit(sys_reg, name="trotter_step")
    # eq_2: U_T(dt) = prod_j exp(-i H_j dt), H_j = c_j P_j, fixed order j = 1..L
    for _ in range(num_steps):
        for label, coeff in terms:
            _append_pauli_rotation(qc, label, coeff * dt, n)
    return qc
