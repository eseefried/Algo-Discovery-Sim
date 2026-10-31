"""Trotterized pairing-Hamiltonian evolution in pseudospin (XY) form, optionally ancilla-controlled.

System qubit (m-1) encodes pair mode m (|1> = Cooper pair present).  The circuit implements
    U_Trotter(t) = [ prod_m RZ_m(eps_m*dt) * prod_m U_XY^{(m,m+1)}(V_{m,m+1}*dt) ]^{n_T},  dt = t/n_T,
which approximates exp(-i H_P t) with H_P from eq_2 (constant term dropped).
If instance["controlled"] is true, one extra ancilla qubit (highest index) controls every Trotter
factor, giving controlled-U_Trotter(t) as used in the spectrum-extraction scheme (eq_5).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_float_list(values, name):
    """Validate a list of finite real numbers and return it as floats."""
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"'{name}' must be a list of real numbers")
    out = []
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"'{name}' entries must be real numbers")
        f = float(v)
        if not math.isfinite(f):
            raise ValueError(f"'{name}' entries must be finite")
        out.append(f)
    return out


def _zz_core(qc, a, b, theta, anc):
    """exp(-i theta/2 Z_a Z_b) via CX - RZ - CX; controlled on anc if anc is not None."""
    qc.cx(a, b)
    if anc is None:
        qc.rz(theta, b)
    else:
        qc.crz(theta, anc, b)
    qc.cx(a, b)


def _xy_gate(qc, a, b, theta, anc):
    """eq_4: U_XY(theta) = exp(-i theta/2 (X_a X_b + Y_a Y_b)) = RXX(theta) RYY(theta).

    XX and YY commute, so the product is exact.  Each factor is a ZZ rotation conjugated by
    single-qubit basis changes; only the central RZ carries the angle, so controlling it on the
    ancilla yields the controlled XY gate (all other gates cancel when the RZ is the identity).
    """
    # XX part: X = H Z H
    qc.h(a)
    qc.h(b)
    _zz_core(qc, a, b, theta, anc)
    qc.h(a)
    qc.h(b)
    # YY part: Y = S H Z H S^dagger
    qc.sdg(a)
    qc.sdg(b)
    qc.h(a)
    qc.h(b)
    _zz_core(qc, a, b, theta, anc)
    qc.h(a)
    qc.h(b)
    qc.s(a)
    qc.s(b)


def build_circuit(instance):
    """Build the (optionally ancilla-controlled) Trotterized pairing evolution operator.

    instance keys:
      levels        : list of N real single-particle energies eps_m (N >= 2)
      couplings     : list of N-1 real nearest-neighbor pairing couplings V_{m,m+1}
      time          : simulated time t >= 0
      trotter_steps : positive integer n_T
      controlled    : bool; if true an ancilla qubit (index N) controls the evolution (eq_5)
    Qubit layout: system qubits 0..N-1 (qubit m-1 <-> pair mode m), ancilla at index N if used.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("levels", "couplings", "time", "trotter_steps", "controlled"):
        if key not in instance:
            raise ValueError(f"missing instance key '{key}'")

    levels = _as_float_list(instance["levels"], "levels")
    couplings = _as_float_list(instance["couplings"], "couplings")
    n_sys = len(levels)
    if n_sys < 2:
        raise ValueError("at least two levels (system qubits) are required")
    if len(couplings) != n_sys - 1:
        raise ValueError("'couplings' must have length len(levels)-1 (nearest-neighbor chain)")

    t = instance["time"]
    if isinstance(t, bool) or not isinstance(t, (int, float)):
        raise ValueError("'time' must be a real number")
    t = float(t)
    if not math.isfinite(t) or t < 0.0:
        raise ValueError("'time' must be finite and nonnegative")

    n_steps = instance["trotter_steps"]
    if isinstance(n_steps, bool) or not isinstance(n_steps, int) or n_steps < 1:
        raise ValueError("'trotter_steps' must be a positive integer")

    controlled = instance["controlled"]
    if not isinstance(controlled, bool):
        raise ValueError("'controlled' must be a boolean")

    n_total = n_sys + (1 if controlled else 0)
    if n_total > MAX_QUBITS:
        raise ValueError(f"total qubits {n_total} exceeds cap of {MAX_QUBITS}")

    sys_reg = QuantumRegister(n_sys, "sys")
    if controlled:
        anc_reg = QuantumRegister(1, "anc")
        qc = QuantumCircuit(sys_reg, anc_reg, name="pairing_trotter_ctrl")
        anc = n_sys
    else:
        qc = QuantumCircuit(sys_reg, name="pairing_trotter")
        anc = None

    dt = t / n_steps  # eq_3: Delta t = t / n_T

    for _ in range(n_steps):
        # eq_2/eq_3 single-qubit terms: exp(-i eps_m/2 sigma_z dt) = RZ(eps_m * dt)
        for m in range(n_sys):
            angle = levels[m] * dt
            if anc is None:
                qc.rz(angle, m)
            else:
                qc.crz(angle, anc, m)
        # eq_3/eq_4 two-qubit nearest-neighbor XY factors with theta = V_{m,m+1} dt
        for m in range(n_sys - 1):
            _xy_gate(qc, m, m + 1, couplings[m] * dt, anc)

    return qc
