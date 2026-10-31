"""Two-axis SU(2) control-sequence compiler (Qiskit).

Compiles an alternating sequence of rotations about two non-parallel Bloch-sphere
axes into a single-qubit circuit.

Conventions
-----------
* eq_1: R_n(theta) = exp(-i theta/2 n.sigma). Qiskit's rz(theta) is exactly
  exp(-i theta Z/2), so axis 1 = z is implemented by rz.
* Axis 1 is n_1 = z. Axis 2 is n_2 = (sin gamma, 0, cos gamma), i.e. at angle gamma
  from z in the xz-plane (azimuth fixed to 0 without loss of generality by the
  rotational symmetry about n_1). R_{n_2}(theta) = Ry(gamma) Rz(theta) Ry(-gamma),
  which in circuit (time) order is ry(-gamma), rz(theta), ry(gamma).
* eq_3: the first segment in the list is applied first (rightmost factor of the
  operator product). T = sum_k |theta_k| / omega_{i_k} is stored in qc.metadata.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
NUM_QUBITS = 1
TWO_PI = 2.0 * math.pi


def _as_float(value, name):
    """Convert a JSON number to a finite float or raise ValueError."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _axis_rotation(qc, qubit, axis_index, theta, gamma):
    """eq_1: append R_{n_axis}(theta) = exp(-i theta/2 n.sigma) to the circuit.

    axis_index 1 -> n_1 = z (single rz).
    axis_index 2 -> n_2 = (sin gamma, 0, cos gamma) via Ry(gamma) Rz(theta) Ry(-gamma).
    """
    if axis_index == 1:
        qc.rz(theta, qubit)
    else:
        qc.ry(-gamma, qubit)
        qc.rz(theta, qubit)
        qc.ry(gamma, qubit)


def build_circuit(instance):
    """Build the single-qubit circuit for a two-axis control sequence (eq_2, eq_3).

    instance keys
    -------------
    gamma : float in (0, pi) -- angle between the two control axes (eq_2).
    omega : [omega_1, omega_2] -- positive rotation speeds (eq_2).
    bidirectional : bool -- if True both senses allowed, theta in (-2pi, 2pi);
        if False only the positive sense, theta in [0, 2pi) (eq_2).
    segments : list of [axis_index, theta] with axis_index in {1, 2}; consecutive
        axes must differ and angles must be nonzero (eq_3).
    enforce_length_bound : bool -- if True and bidirectional, require N <= 5 (eq_5).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")

    if NUM_QUBITS > MAX_QUBITS:
        raise ValueError("qubit budget exceeded")

    # --- eq_2: control geometry and speeds -------------------------------------
    gamma = _as_float(instance.get("gamma", math.pi / 2.0), "gamma")
    if not (0.0 < gamma < math.pi):
        raise ValueError("gamma must lie strictly in (0, pi): axes must be non-parallel")

    omega = instance.get("omega", [1.0, 1.0])
    if not isinstance(omega, (list, tuple)) or len(omega) != 2:
        raise ValueError("omega must be a list [omega_1, omega_2]")
    omega_1 = _as_float(omega[0], "omega_1")
    omega_2 = _as_float(omega[1], "omega_2")
    if omega_1 <= 0.0 or omega_2 <= 0.0:
        raise ValueError("rotation speeds must be positive")
    speeds = (omega_1, omega_2)

    bidirectional = instance.get("bidirectional", True)
    if not isinstance(bidirectional, bool):
        raise ValueError("bidirectional must be a boolean")
    enforce_bound = instance.get("enforce_length_bound", False)
    if not isinstance(enforce_bound, bool):
        raise ValueError("enforce_length_bound must be a boolean")

    # --- eq_3: alternating segment sequence --------------------------------------
    segments = instance.get("segments", None)
    if not isinstance(segments, (list, tuple)):
        raise ValueError("segments must be a list of [axis_index, theta] pairs")
    parsed = []
    previous_axis = 0
    for k, seg in enumerate(segments):
        if not isinstance(seg, (list, tuple)) or len(seg) != 2:
            raise ValueError(f"segment {k} must be a pair [axis_index, theta]")
        axis_raw = seg[0]
        if isinstance(axis_raw, bool) or not isinstance(axis_raw, int) or axis_raw not in (1, 2):
            raise ValueError(f"segment {k}: axis_index must be 1 or 2")
        theta = _as_float(seg[1], f"segment {k} theta")
        if theta == 0.0:
            raise ValueError(f"segment {k}: zero-angle segments are not admissible")
        if bidirectional:
            if not (-TWO_PI < theta < TWO_PI):
                raise ValueError(f"segment {k}: theta must lie in (-2pi, 2pi)")
        else:
            if not (0.0 < theta < TWO_PI):
                raise ValueError(f"segment {k}: clockwise-only case requires theta in (0, 2pi)")
        if axis_raw == previous_axis:
            raise ValueError(f"segment {k}: consecutive segments must use different axes")
        previous_axis = axis_raw
        parsed.append((axis_raw, theta))

    n_segments = len(parsed)
    # --- eq_5: optional five-concatenation bound (bidirectional case) ----------
    if enforce_bound and bidirectional and n_segments > 5:
        raise ValueError("bidirectional time-optimal sequences have at most 5 segments (eq_5)")

    qr = QuantumRegister(NUM_QUBITS, "q")
    qc = QuantumCircuit(qr, name="two_axis_sequence")

    # eq_3: time-ordered application, first listed segment applied first.
    total_time = 0.0
    for axis_index, theta in parsed:
        _axis_rotation(qc, qr[0], axis_index, theta, gamma)
        total_time += abs(theta) / speeds[axis_index - 1]

    qc.metadata = {
        "total_time": total_time,
        "num_segments": n_segments,
        "gamma": gamma,
        "omega": [omega_1, omega_2],
        "bidirectional": bidirectional,
    }
    return qc
