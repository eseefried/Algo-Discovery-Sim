"""Exact decomposition of a diagonal Hermitian quantum gate into multiple-controlled Z gates.

The gate D = diag(d_0, ..., d_{2^n - 1}) with every d_j in {+1, -1} is written as
D = (-1)^{a_empty} * prod_{S nonempty, a_S = 1} C^S Z, where a_S are the GF(2)
algebraic-normal-form coefficients of the Boolean sign function f (d_j = (-1)^{f(j)}).

Index convention (Qiskit little-endian): bit k of the diagonal index j is the value of
Qiskit qubit k (qubit 0 = least significant bit). The specification's qubit i (1-indexed,
most significant) therefore corresponds to Qiskit qubit n - i.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate

MAX_QUBITS = 12
TOL = 1e-9


def _sign_to_bit(value):
    """eq_1: d_x = (-1)^{f(x)}. Return f(x) in {0, 1} from a diagonal entry +1 / -1."""
    if isinstance(value, bool):
        raise ValueError("diagonal entries must be numeric +1 or -1, not booleans")
    if isinstance(value, complex):
        if abs(value.imag) > TOL:
            raise ValueError("diagonal entries of a Hermitian gate must be real")
        value = value.real
    try:
        real_value = float(value)
    except (TypeError, ValueError):
        raise ValueError("diagonal entries must be numeric +1 or -1")
    if abs(real_value - 1.0) <= TOL:
        return 0
    if abs(real_value + 1.0) <= TOL:
        return 1
    raise ValueError("diagonal Hermitian gate entries must be exactly +1 or -1")


def _anf_coefficients(truth_table, n):
    """eq_4 / eq_5: GF(2) Mobius inversion a_S = XOR_{T subset S} f(1_T).

    truth_table is the binary representation b(D) (eq_2) as a list of 0/1 of length 2^n.
    The returned list a has a[idx] = a_S where S = {k : bit k of idx is 1}; this is the
    unique expansion of f in the monomial basis {m_S} (eq_4).
    """
    size = 1 << n
    a = list(truth_table)
    for k in range(n):
        mask = 1 << k
        for idx in range(size):
            if idx & mask:
                a[idx] ^= a[idx ^ mask]
    return a


def _append_multi_controlled_z(qc, qubits):
    """eq_3: append C^S Z on the given Qiskit qubit indices (set S).

    The gate is symmetric in its qubits, so the last qubit is used as the target.
    """
    size = len(qubits)
    if size == 1:
        qc.z(qubits[0])
    elif size == 2:
        qc.cz(qubits[0], qubits[1])
    else:
        qc.append(ZGate().control(size - 1), qubits)


def build_circuit(instance):
    """Build the multiple-controlled-Z decomposition of a diagonal Hermitian gate.

    instance: dict with keys
        "n": int, number of qubits (1 <= n <= 12)
        "diagonal": list of 2^n entries, each +1 or -1; entry j is d_j with the
                    little-endian index convention (bit k of j <-> Qiskit qubit k).
    Returns a measurement-free unitary QuantumCircuit equal to diag(diagonal), including
    the global sign (-1)^{a_empty} as the circuit global phase.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "diagonal" not in instance:
        raise ValueError("instance must contain 'n' and 'diagonal'")
    n = instance["n"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError("n must satisfy 1 <= n <= %d" % MAX_QUBITS)
    diagonal = instance["diagonal"]
    if not isinstance(diagonal, (list, tuple)):
        raise ValueError("diagonal must be a list")
    size = 1 << n
    if len(diagonal) != size:
        raise ValueError("diagonal must have exactly 2^n entries")

    # eq_1 / eq_2: binary representation b(D) = truth table of f.
    truth_table = [_sign_to_bit(v) for v in diagonal]

    # eq_4 / eq_5: coordinates of b(D) in the monomial (multiple-controlled Z) basis.
    coeffs = _anf_coefficients(truth_table, n)

    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr, name="diag_hermitian_mcz")

    # eq_6: D = (-1)^{a_empty} prod_{S nonempty, a_S = 1} C^S Z.
    if coeffs[0] == 1:
        qc.global_phase = math.pi
    for idx in range(1, size):
        if coeffs[idx] == 1:
            qubits = [k for k in range(n) if (idx >> k) & 1]
            _append_multi_controlled_z(qc, qubits)
    return qc
