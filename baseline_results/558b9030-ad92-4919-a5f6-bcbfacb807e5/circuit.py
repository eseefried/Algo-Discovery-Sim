"""Programmable-query Grover search over a small quantum phone book.

Registers (Qiskit qubit 0 = least significant bit):
  I  index register, n qubits, qubit j of I holds bit j of index i (LSB first)
  A  name field work register, m qubits (bit b of name_i on A[b])
  B  number field work register, m qubits (bit b of num_i on B[b])
  S  selector qubit s (0 = search by name, 1 = search by number)
  V  query value register, m qubits (bit b of q on V[b])
The circuit is an operation: it does not prepare |s,q> on S,V (runner does) and
has no measurements. If apply_hadamard_layer is true, H^{x n} is applied to I
as the first step of Grover's algorithm (eq_3 definition of |psi_0>).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _validate_instance(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _as_int(instance.get("n_index_qubits"), "n_index_qubits")
    m = _as_int(instance.get("field_bits"), "field_bits")
    k = _as_int(instance.get("iterations"), "iterations")
    hlayer = instance.get("apply_hadamard_layer", True)
    if not isinstance(hlayer, bool):
        raise ValueError("apply_hadamard_layer must be a bool")
    if n < 1:
        raise ValueError("n_index_qubits must be >= 1")
    if m < 1:
        raise ValueError("field_bits must be >= 1")
    if k < 0:
        raise ValueError("iterations must be >= 0")
    total = n + 3 * m + 1
    if total > MAX_QUBITS:
        raise ValueError(f"total qubits {total} exceeds cap {MAX_QUBITS}")
    size = 2 ** n
    names = instance.get("names")
    numbers = instance.get("numbers")
    if not isinstance(names, list) or not isinstance(numbers, list):
        raise ValueError("names and numbers must be lists")
    if len(names) != size or len(numbers) != size:
        raise ValueError(f"names and numbers must each have 2**n = {size} entries")
    limit = 2 ** m
    names = [_as_int(v, "names entry") for v in names]
    numbers = [_as_int(v, "numbers entry") for v in numbers]
    for v in names + numbers:
        if v < 0 or v >= limit:
            raise ValueError(f"field values must lie in [0, {limit})")
    return n, m, names, numbers, k, hlayer


def _mcx_on_value(qc, controls, target, value):
    """X on target iff the control register (LSB first) encodes integer value."""
    flips = [controls[j] for j in range(len(controls)) if not (value >> j) & 1]
    for qb in flips:
        qc.x(qb)
    qc.mcx(list(controls), target)
    for qb in flips:
        qc.x(qb)


def _mcz(qc, qubits):
    """Multi-controlled Z: phase -1 iff all listed qubits are |1>."""
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        qc.mcp(math.pi, list(qubits[:-1]), qubits[-1])


def _apply_database(qc, idx, name_reg, num_reg, names, numbers, m):
    """eq_1: U_DB |i>|0>|0> = |i>|name_i>|num_i> via a table of multi-controlled NOTs.
    Self-inverse, so it also serves as U_DB^dagger."""
    for i in range(len(names)):
        for b in range(m):
            if (names[i] >> b) & 1:
                _mcx_on_value(qc, idx, name_reg[b], i)
            if (numbers[i] >> b) & 1:
                _mcx_on_value(qc, idx, num_reg[b], i)


def _apply_field_compare(qc, field, qval, sel, sel_value):
    """eq_2 (P_{s,q} part): phase -1 iff selector == sel_value and field == q."""
    m = len(field)
    for b in range(m):
        qc.cx(qval[b], field[b])
    for b in range(m):
        qc.x(field[b])
    if sel_value == 0:
        qc.x(sel)
    _mcz(qc, [sel] + [field[b] for b in range(m)])
    if sel_value == 0:
        qc.x(sel)
    for b in range(m):
        qc.x(field[b])
    for b in range(m):
        qc.cx(qval[b], field[b])


def _apply_programmable_oracle(qc, idx, name_reg, num_reg, sel, qval, names, numbers, m):
    """eq_2: O_{s,q} = U_DB^dagger P_{s,q} U_DB, acting as (-1)^{f_{s,q}(i)} on |i>."""
    _apply_database(qc, idx, name_reg, num_reg, names, numbers, m)
    _apply_field_compare(qc, name_reg, qval, sel, 0)
    _apply_field_compare(qc, num_reg, qval, sel, 1)
    _apply_database(qc, idx, name_reg, num_reg, names, numbers, m)


def _apply_diffusion(qc, idx):
    """eq_3: inversion about |psi_0>, 2|psi_0><psi_0| - I on the index register.
    H X MCZ X H equals -(2|psi_0><psi_0| - I); the global phase pi is restored."""
    n = len(idx)
    for j in range(n):
        qc.h(idx[j])
    for j in range(n):
        qc.x(idx[j])
    _mcz(qc, [idx[j] for j in range(n)])
    for j in range(n):
        qc.x(idx[j])
    for j in range(n):
        qc.h(idx[j])
    qc.global_phase = qc.global_phase + math.pi


def build_circuit(instance):
    """Build the programmable-query Grover phone-book search circuit.

    instance keys:
      n_index_qubits (int >= 1): n, database size N = 2**n
      field_bits (int >= 1): m, bit width of name and number fields
      names (list[int]): name_i for i = 0..N-1, each in [0, 2**m)
      numbers (list[int]): num_i for i = 0..N-1, each in [0, 2**m)
      iterations (int >= 0): number of Grover iterates k
      apply_hadamard_layer (bool, optional): apply H on I first (default True)
    """
    n, m, names, numbers, k, hlayer = _validate_instance(instance)
    idx = QuantumRegister(n, "idx")
    name_reg = QuantumRegister(m, "name")
    num_reg = QuantumRegister(m, "num")
    sel_reg = QuantumRegister(1, "sel")
    qval = QuantumRegister(m, "qry")
    qc = QuantumCircuit(idx, name_reg, num_reg, sel_reg, qval, name="phonebook_grover")
    sel = sel_reg[0]
    if hlayer:
        # eq_3: |psi_0> = H^{x n}|0>
        for j in range(n):
            qc.h(idx[j])
    for _ in range(k):
        # eq_3: G_{s,q} = (2|psi_0><psi_0| - I) O_{s,q}
        _apply_programmable_oracle(qc, idx, name_reg, num_reg, sel, qval, names, numbers, m)
        _apply_diffusion(qc, idx)
    return qc
