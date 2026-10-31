"""Toffoli-network (MCT) circuit builder for n-bit reversible functions.

Scoped construction from the specification: given an ordered list of
multiple-control Toffoli gates T(C;t) (eq_2) on n wires (paper: n = 4),
build the reversible circuit f = g_L o ... o g_1 (eq_3) and report the
additive quantum cost QC(G) (eq_4) and gate count GC(G) in the circuit
metadata.  Wire i (1 = top / most significant bit of the truth-table
label) is mapped to Qiskit qubit n - i, so that the integer label
x = sum_i x_i 2^(n-i) coincides with Qiskit's little-endian basis index.

Instance format:
  {"n": 4, "gates": [{"controls": [1, 2, 3], "target": 4}, ...]}
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("%s must be an integer" % name)
    return value


def _parse_instance(instance):
    """Validate the instance and return (n, [(controls_tuple, target), ...])."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "gates" not in instance:
        raise ValueError("instance needs keys 'n' and 'gates'")
    n = _check_int(instance["n"], "n")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError("n must satisfy 1 <= n <= %d" % MAX_QUBITS)
    gates_in = instance["gates"]
    if not isinstance(gates_in, list):
        raise ValueError("gates must be a list")
    gates = []
    for idx, g in enumerate(gates_in):
        if not isinstance(g, dict) or "controls" not in g or "target" not in g:
            raise ValueError("gate %d must be a dict with 'controls' and 'target'" % idx)
        controls_in = g["controls"]
        if not isinstance(controls_in, list):
            raise ValueError("gate %d: controls must be a list" % idx)
        target = _check_int(g["target"], "gate %d target" % idx)
        if target < 1 or target > n:
            raise ValueError("gate %d: target wire out of range 1..%d" % (idx, n))
        controls = []
        for c in controls_in:
            c = _check_int(c, "gate %d control" % idx)
            if c < 1 or c > n:
                raise ValueError("gate %d: control wire out of range 1..%d" % (idx, n))
            if c == target:
                raise ValueError("gate %d: target wire cannot also be a control" % idx)
            if c in controls:
                raise ValueError("gate %d: duplicate control wire" % idx)
            controls.append(c)
        gates.append((tuple(controls), target))
    return n, gates


def gate_quantum_cost(num_controls):
    """eq_4 per-gate cost table: NOT/CNOT = 1, Toffoli = 5, 3-control = 13.

    For k >= 1 controls the table is 2^(k+1) - 3 (a standard MCT cost
    formula consistent with the assumed table); k = 0 (NOT) costs 1.
    """
    if num_controls == 0:
        return 1
    return 2 ** (num_controls + 1) - 3


def quantum_cost(gates):
    """eq_4: QC(G) = sum_i qc(g_i), additive over the gate list."""
    total = 0
    for controls, _target in gates:
        total += gate_quantum_cost(len(controls))
    return total


def _wire_to_qubit(n, wire):
    """Wire 1 (top, MSB of the truth-table label) -> qubit n-1; wire n -> qubit 0."""
    return n - wire


def _apply_mct(qc, n, controls, target):
    """eq_2: T(C;t): x_t -> x_t XOR AND_{c in C} x_c, other wires unchanged."""
    tq = _wire_to_qubit(n, target)
    cqs = [_wire_to_qubit(n, c) for c in controls]
    k = len(cqs)
    if k == 0:
        qc.x(tq)
    elif k == 1:
        qc.cx(cqs[0], tq)
    elif k == 2:
        qc.ccx(cqs[0], cqs[1], tq)
    else:
        qc.mcx(cqs, tq)


def build_circuit(instance):
    """Build the Toffoli network f = g_L o ... o g_1 (eq_3) on n wires.

    Gates are appended in list order, so gates[0] = g_1 acts first.  The
    resulting circuit permutes computational basis states exactly as the
    composed MCT gates (eq_1/eq_3); GC(G) and QC(G) (eq_4) are stored in
    qc.metadata.  The example instance is f_0 = T({1,2,3};4) of eq_7.
    """
    n, gates = _parse_instance(instance)
    qr = QuantumRegister(n, "x")
    qc = QuantumCircuit(qr, name="mct_network")
    for controls, target in gates:
        _apply_mct(qc, n, controls, target)
    qc.metadata = {"gate_count": len(gates), "quantum_cost": quantum_cost(gates)}
    return qc
