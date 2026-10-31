"""Nearest-neighbour CNOT fanout on a 2D grid (non-adaptive model).

Implements eq_5 of the specification: control at grid site (0, 0), row-0
broadcast followed by parallel column broadcast.  Grid site (r, c) is mapped to
Qiskit qubit index r * cols + c; qubit 0 is the control.  All two-qubit gates
act on L1-adjacent sites (eq_2).  On clean targets |0> the circuit realises the
fanout F_n of eq_1.  Depth = (cols - 1) + (rows - 1), size = rows * cols - 1.
"""
from __future__ import annotations

import math
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _read_positive_int(instance, key):
    """Fetch a strictly positive integer field from the instance dict."""
    if key not in instance:
        raise ValueError("instance is missing required key '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("'%s' must be an integer, got %r" % (key, value))
    if value < 1:
        raise ValueError("'%s' must be >= 1, got %d" % (key, value))
    return value


def _parse_instance(instance):
    """Validate the instance and return (rows, cols)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict with keys 'rows' and 'cols'")
    rows = _read_positive_int(instance, "rows")
    cols = _read_positive_int(instance, "cols")
    n = rows * cols
    if n < 2:
        raise ValueError("grid must contain at least 2 qubits (1 control + 1 target)")
    if n > MAX_QUBITS:
        raise ValueError(
            "grid has %d qubits, exceeding the cap of %d" % (n, MAX_QUBITS)
        )
    return rows, cols


def _site_index(r, c, cols):
    """Linear qubit index of grid site (r, c): i = r * cols + c (eq_2 layout)."""
    return r * cols + c


def _nn_cx(qc, qr, src, dst, cols):
    """Apply CNOT from grid site src to grid site dst, enforcing eq_2 adjacency."""
    dist = abs(src[0] - dst[0]) + abs(src[1] - dst[1])
    if dist != 1:
        # eq_2: only L1-adjacent grid sites may interact
        raise ValueError("non-nearest-neighbour CNOT requested: %r -> %r" % (src, dst))
    qc.cx(qr[_site_index(src[0], src[1], cols)], qr[_site_index(dst[0], dst[1], cols)])


def build_circuit(instance):
    """Build the row-then-column nearest-neighbour fanout circuit (eq_5).

    instance: {"rows": int, "cols": int} with 2 <= rows * cols <= 12.
    Returns a measurement-free unitary QuantumCircuit on rows * cols qubits.
    Qubit 0 = control at site (0, 0); qubit r * cols + c = site (r, c).
    On input |x>|0...0> the output is |x>^{(rows*cols)} (eq_1 with clean targets).
    """
    rows, cols = _parse_instance(instance)
    n = rows * cols
    qr = QuantumRegister(n, "grid")
    qc = QuantumCircuit(qr, name="nn_fanout_%dx%d" % (rows, cols))

    # eq_5, first factor (applied first): sequential broadcast along row 0.
    # CNOT_{(0,t-1) -> (0,t)} for t = 1..cols-1; depth cols - 1.
    for t in range(1, cols):
        _nn_cx(qc, qr, (0, t - 1), (0, t), cols)

    # eq_5, second factor: parallel broadcast down every column.
    # Layer t applies CNOT_{(t-1,c) -> (t,c)} for all c simultaneously; depth rows - 1.
    for t in range(1, rows):
        for c in range(cols):
            _nn_cx(qc, qr, (t - 1, c), (t, c), cols)

    # Sanity: size = n - 1 CNOTs, as stated in eq_5.
    if qc.size() != n - 1:
        raise ValueError("internal error: unexpected gate count")
    return qc
