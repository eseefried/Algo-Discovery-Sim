"""Bernstein-Vazirani circuit for an arbitrary Boolean function f.

Operation implemented (specification eq_1, eq_2, eq_6):
    (H^{(x)n} (x) I) . U_f . (H^{(x)n} (x) H)   acting on |0^n>_in |1>_anc

The runner prepares |0^n>_in |1>_anc.  After this circuit the input register
holds sum_y fhat(y) |y> with fhat(y) = 2^{-n} sum_x (-1)^{f(x) + x.y}, so
measuring input qubit (i-1) yields 1 with probability Inf_i(f) (eq_3/eq_4).

Qubit layout: input qubit index j-1 stores x_j and yields y_j (j = 1..n);
qubit index n is the oracle ancilla.  Truth tables are indexed by
k = sum_j x_j 2^{j-1}, i.e. x_1 is the least significant bit of k, which
matches Qiskit's little-endian convention (qubit 0 = least significant).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
KNOWN_FUNCTIONS = ("and", "or", "parity", "majority", "constant0", "constant1")


def _validate_n(instance: dict) -> int:
    if "n" not in instance:
        raise ValueError("instance must contain 'n' (number of input variables)")
    n = instance["n"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("'n' must be an integer")
    if n < 1:
        raise ValueError("'n' must be at least 1")
    if n + 1 > MAX_QUBITS:
        raise ValueError(
            "n + 1 ancilla exceeds the qubit cap of %d (n <= %d)" % (MAX_QUBITS, MAX_QUBITS - 1)
        )
    return n


def _named_truth_table(name: str, n: int) -> list:
    """Truth table of a named Boolean function; index k has x_j = (k >> (j-1)) & 1."""
    if name not in KNOWN_FUNCTIONS:
        raise ValueError("unknown function name %r; known: %s" % (name, list(KNOWN_FUNCTIONS)))
    table = []
    for k in range(2 ** n):
        weight = 0
        for j in range(n):
            weight += (k >> j) & 1
        if name == "and":
            value = 1 if weight == n else 0
        elif name == "or":
            value = 1 if weight > 0 else 0
        elif name == "parity":
            value = weight % 2
        elif name == "majority":
            value = 1 if 2 * weight > n else 0
        elif name == "constant0":
            value = 0
        else:
            value = 1
        table.append(value)
    return table


def _truth_table_from_instance(instance: dict, n: int) -> list:
    has_table = "truth_table" in instance
    has_name = "function" in instance
    if has_table == has_name:
        raise ValueError("instance must contain exactly one of 'truth_table' or 'function'")
    if has_name:
        name = instance["function"]
        if not isinstance(name, str):
            raise ValueError("'function' must be a string")
        return _named_truth_table(name.lower(), n)
    raw = instance["truth_table"]
    if not isinstance(raw, (list, tuple)):
        raise ValueError("'truth_table' must be a list of 0/1 entries")
    if len(raw) != 2 ** n:
        raise ValueError("'truth_table' must have length 2**n = %d, got %d" % (2 ** n, len(raw)))
    table = []
    for entry in raw:
        if isinstance(entry, bool):
            table.append(1 if entry else 0)
            continue
        if not isinstance(entry, int) or entry not in (0, 1):
            raise ValueError("'truth_table' entries must be 0 or 1")
        table.append(int(entry))
    return table


def _anf_monomials(table: list, n: int) -> list:
    """Mobius transform: returns the set of monomials (as bitmasks) in the
    algebraic normal form f(x) = XOR_{m in monomials} prod_{j in m} x_j."""
    coeffs = list(table)
    for j in range(n):
        bit = 1 << j
        for k in range(2 ** n):
            if k & bit:
                coeffs[k] ^= coeffs[k ^ bit]
    return [k for k in range(2 ** n) if coeffs[k] == 1]


def _append_oracle(qc: QuantumCircuit, inputs: QuantumRegister, anc, monomials: list, n: int) -> None:
    """eq_1: bit-flip oracle U_f |x>|b> = |x>|b xor f(x)>, realised as one
    multi-controlled X per ANF monomial (empty monomial -> plain X)."""
    for mask in monomials:
        controls = [inputs[j] for j in range(n) if (mask >> j) & 1]
        if len(controls) == 0:
            qc.x(anc)
        elif len(controls) == 1:
            qc.cx(controls[0], anc)
        else:
            qc.mcx(controls, anc)


def build_circuit(instance: dict) -> QuantumCircuit:
    """Bernstein-Vazirani operation for a general Boolean function (eq_2).

    instance keys:
        n            : int, number of input variables (1 <= n <= 11)
        truth_table  : list of 2**n bits, index k = sum_j x_j 2**(j-1)
        function     : alternatively a name in KNOWN_FUNCTIONS
    Returns a circuit on n+1 qubits: qubits 0..n-1 = input (x_j on qubit j-1),
    qubit n = ancilla (runner prepares it in |1>).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _validate_n(instance)
    table = _truth_table_from_instance(instance, n)
    monomials = _anf_monomials(table, n)

    inputs = QuantumRegister(n, "x")
    anc_reg = QuantumRegister(1, "anc")
    qc = QuantumCircuit(inputs, anc_reg, name="bernstein_vazirani_influence")
    anc = anc_reg[0]

    # eq_2 step 1: H on every qubit (input -> uniform superposition, |1>_anc -> |->)
    for j in range(n):
        qc.h(inputs[j])
    qc.h(anc)

    # eq_2 step 2 / eq_1: oracle query with phase kickback (-1)^{f(x)}
    _append_oracle(qc, inputs, anc, monomials, n)

    # eq_2 step 3: H on the input register -> sum_y fhat(y) |y> |->
    for j in range(n):
        qc.h(inputs[j])

    return qc
