"""Singlet-triplet (S-T_0) piecewise-constant control propagator as a Qiskit circuit.

Implements eq_1 (segment Hamiltonian H_k = (J_k+dJ_k)/2 sigma_z + (h+dh)/2 sigma_x, with
quasi-static error terms dJ_k = epsilon_J * J_k and dh = delta_h) and eq_2 (ordered
product of segment unitaries exp[-i tau_k H_k], segment 1 acting first).

Each segment is an SU(2) rotation about the axis n_k = (h+dh, 0, J_k+dJ_k)/Omega_k by
angle Omega_k * tau_k, with Omega_k = sqrt((J_k+dJ_k)^2 + (h+dh)^2).  Writing
n_k = (sin a_k, 0, cos a_k) with a_k = atan2(h+dh, J_k+dJ_k), the exact identity
    exp(-i theta/2 n_k.sigma) = R_y(a_k) R_z(theta) R_y(-a_k)
is used, which in circuit (time) order is ry(-a_k), rz(theta), ry(a_k).

The module compiles a given sequence; it does not search for one (eq_4/eq_5 are classical
post-processing outside this operation).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
NUM_QUBITS = 1


def _as_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _as_real_list(values, name):
    if not isinstance(values, (list, tuple)) or len(values) == 0:
        raise ValueError(f"{name} must be a non-empty list of real numbers")
    return [_as_real(v, f"{name}[{i}]") for i, v in enumerate(values)]


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    allowed = {"h", "J", "tau", "delta_h", "epsilon_J", "J_min", "J_max"}
    unknown = set(instance.keys()) - allowed
    if unknown:
        raise ValueError(f"unknown instance keys: {sorted(unknown)}")
    for key in ("h", "J", "tau"):
        if key not in instance:
            raise ValueError(f"instance is missing required key '{key}'")
    h = _as_real(instance["h"], "h")
    j_list = _as_real_list(instance["J"], "J")
    tau_list = _as_real_list(instance["tau"], "tau")
    if len(j_list) != len(tau_list):
        raise ValueError("J and tau must have the same number of segments N")
    for i, t in enumerate(tau_list):
        if t <= 0.0:
            raise ValueError(f"tau[{i}] must be strictly positive")
    delta_h = _as_real(instance.get("delta_h", 0.0), "delta_h")
    epsilon_j = _as_real(instance.get("epsilon_J", 0.0), "epsilon_J")
    j_min = _as_real(instance.get("J_min", 0.0), "J_min")
    j_max = instance.get("J_max", None)
    if j_max is not None:
        j_max = _as_real(j_max, "J_max")
        if j_max < j_min:
            raise ValueError("J_max must be >= J_min")
    for i, jk in enumerate(j_list):
        if jk < j_min:
            raise ValueError(f"J[{i}] violates the lower control bound J_min={j_min}")
        if j_max is not None and jk > j_max:
            raise ValueError(f"J[{i}] violates the upper control bound J_max={j_max}")
    if NUM_QUBITS > MAX_QUBITS:
        raise ValueError("qubit budget exceeded")
    return h, j_list, tau_list, delta_h, epsilon_j


def _append_segment(qc, qubit, jz, hx, tau):
    """eq_2 segment: exp[-i tau/2 (jz sigma_z + hx sigma_x)] via ry(-a) rz(theta) ry(a)."""
    omega = math.hypot(jz, hx)
    if omega == 0.0:
        return
    theta = omega * tau
    a = math.atan2(hx, jz)
    qc.ry(-a, qubit)
    qc.rz(theta, qubit)
    qc.ry(a, qubit)


def build_circuit(instance):
    """Return the (ideal or fixed-noise-realization) S-T_0 propagator U(T) as a circuit.

    instance keys:
      h        : Overhauser gradient (sigma_x coefficient, fixed during the gate)
      J        : list of N exchange values J_k (sigma_z coefficients)
      tau      : list of N segment durations tau_k > 0
      delta_h  : optional quasi-static nuclear-bath shift of h (default 0)
      epsilon_J: optional relative voltage-noise amplitude, dJ_k = epsilon_J*J_k (default 0)
      J_min    : optional lower control bound (default 0, exchange non-negative)
      J_max    : optional upper control bound (default: unbounded)
    """
    h, j_list, tau_list, delta_h, epsilon_j = _validate(instance)
    qreg = QuantumRegister(NUM_QUBITS, "q")
    qc = QuantumCircuit(qreg, name="st0_dcg_sequence")
    # eq_1: effective per-segment coefficients including the quasi-static error terms.
    hx = h + delta_h
    for jk, tk in zip(j_list, tau_list):
        jz = jk * (1.0 + epsilon_j)
        # eq_2: ordered product, segment k=1 applied first (rightmost factor).
        _append_segment(qc, qreg[0], jz, hx, tk)
    return qc
