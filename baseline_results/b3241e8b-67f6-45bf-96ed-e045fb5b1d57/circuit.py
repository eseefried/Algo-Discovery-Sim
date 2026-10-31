"""Tulsi-like controlled-rotation coined-walk search: U_delta^tau on a 2D periodic grid.

Registers (Qiskit little-endian, qubit 0 least significant):
  pos[0..k-1]   : column coordinate x_2 (k = p/2 qubits)
  pos[k..p-1]   : row coordinate x_1, vertex x = x_1 * 2^k + x_2
  coin[0]       : direction sign bit (0 -> +1, 1 -> -1)
  coin[1]       : direction axis bit (0 -> column/x axis, 1 -> row/y axis)
  ctrl[0]       : Tulsi control qubit rotated by R_delta at the marked vertex
The circuit is the measurement-free unitary U_delta^tau (eq_2 repeated tau times),
i.e. the evolution between two control measurements in eq_3.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate, PhaseGate

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _parse_instance(instance):
    """Validate the instance dictionary and return (p, w, delta, tau)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    required = ("num_position_qubits", "marked_vertex", "delta", "tau")
    for key in instance:
        if key not in required:
            raise ValueError(f"unknown instance key: {key}")
    for key in required:
        if key not in instance:
            raise ValueError(f"missing instance key: {key}")
    p = _as_int(instance["num_position_qubits"], "num_position_qubits")
    if p < 2 or p % 2 != 0:
        raise ValueError("num_position_qubits must be an even integer >= 2 (square grid)")
    if p + 3 > MAX_QUBITS:
        raise ValueError(f"total qubits {p + 3} exceeds the cap of {MAX_QUBITS}")
    w = _as_int(instance["marked_vertex"], "marked_vertex")
    if w < 0 or w >= 2 ** p:
        raise ValueError("marked_vertex must satisfy 0 <= w < 2**num_position_qubits")
    delta = instance["delta"]
    if isinstance(delta, bool) or not isinstance(delta, (int, float)):
        raise ValueError("delta must be a real number")
    delta = float(delta)
    if not math.isfinite(delta):
        raise ValueError("delta must be finite")
    tau = _as_int(instance["tau"], "tau")
    if tau < 1:
        raise ValueError("tau must be a positive integer")
    return p, w, delta, tau


def _controlled_marked_rotation(qc, pos_qubits, ctrl_qubit, w, delta):
    """eq_2 (first factor): R_delta on the control conditioned on position == w.

    R_delta = [[cos d, -sin d], [sin d, cos d]] = RY(2*delta).
    """
    p = len(pos_qubits)
    zero_bits = [pos_qubits[i] for i in range(p) if ((w >> i) & 1) == 0]
    for q in zero_bits:
        qc.x(q)
    qc.append(RYGate(2.0 * delta).control(p), list(pos_qubits) + [ctrl_qubit])
    for q in zero_bits:
        qc.x(q)


def _grover_coin(qc, coin_qubits):
    """eq_2 (coin C): 4-dimensional Grover diffusion 2|c_u><c_u| - I on the coin register."""
    c0, c1 = coin_qubits[0], coin_qubits[1]
    qc.h(c0)
    qc.h(c1)
    qc.x(c0)
    qc.x(c1)
    qc.cz(c0, c1)
    qc.x(c0)
    qc.x(c1)
    qc.h(c0)
    qc.h(c1)
    # X X CZ X X conjugated by H gives -(2|c_u><c_u| - I); fix the sign exactly.
    qc.global_phase += math.pi


def _controlled_coordinate_shift(qc, coord_qubits, axis_qubit, sign_qubit, axis_value):
    """Add +1 (sign bit 0) or -1 (sign bit 1) modulo 2^k to one coordinate when axis bit == axis_value.

    Uses QFTGate; in the Fourier frame adding m is the diagonal phase exp(2*pi*i*m*2^l/2^k) on qubit l,
    which is independent of the internal bit-reversal convention of QFTGate.
    """
    k = len(coord_qubits)
    if axis_value == 0:
        qc.x(axis_qubit)
    qc.append(QFTGate(k), list(coord_qubits))
    for l in range(k):
        theta = 2.0 * math.pi * (2 ** l) / (2 ** k)
        # +theta when axis active; extra -2*theta when sign bit is 1 gives net -theta.
        qc.cp(theta, axis_qubit, coord_qubits[l])
        qc.append(PhaseGate(-2.0 * theta).control(2), [axis_qubit, sign_qubit, coord_qubits[l]])
    qc.append(QFTGate(k).inverse(), list(coord_qubits))
    if axis_value == 0:
        qc.x(axis_qubit)


def _flip_flop_shift(qc, pos_qubits, coin_qubits):
    """eq_2 (shift S): flip-flop shift |d, x> -> |-d, x + e_d> on the periodic grid."""
    p = len(pos_qubits)
    k = p // 2
    column = [pos_qubits[i] for i in range(k)]
    row = [pos_qubits[i] for i in range(k, p)]
    sign_qubit, axis_qubit = coin_qubits[0], coin_qubits[1]
    _controlled_coordinate_shift(qc, column, axis_qubit, sign_qubit, 0)
    _controlled_coordinate_shift(qc, row, axis_qubit, sign_qubit, 1)
    # flip-flop: reverse the direction for every coin state
    qc.x(sign_qubit)


def _tulsi_step(qc, pos_qubits, coin_qubits, ctrl_qubit, w, delta):
    """eq_2: U_delta = (I x S)(I x C x I)(R_delta x I x |w><w| + I x I x (I - |w><w|))."""
    _controlled_marked_rotation(qc, pos_qubits, ctrl_qubit, w, delta)
    _grover_coin(qc, coin_qubits)
    _flip_flop_shift(qc, pos_qubits, coin_qubits)


def build_circuit(instance):
    """Return the unitary U_delta^tau (eq_3 inter-measurement block) as a QuantumCircuit."""
    p, w, delta, tau = _parse_instance(instance)
    position = QuantumRegister(p, "pos")
    coin = QuantumRegister(2, "coin")
    control = QuantumRegister(1, "ctrl")
    qc = QuantumCircuit(position, coin, control, name="tulsi_walk_U_delta_pow_tau")
    pos_qubits = [position[i] for i in range(p)]
    coin_qubits = [coin[0], coin[1]]
    ctrl_qubit = control[0]
    # eq_3 (unitary part): tau applications of U_delta between control measurements
    for _ in range(tau):
        _tulsi_step(qc, pos_qubits, coin_qubits, ctrl_qubit, w, delta)
    return qc
