"""Trotterized time evolution under the truncated (compressed) transverse-field Ising
patch Hamiltonian H_S(x) used by the trusted small simulator (eq_2 / unitary part of eq_3).

H_S(x) = sum_{i=1}^{n-1} J_i Z_i Z_{i+1} + sum_{i=1}^{n} h_i X_i   (open chain, n patch qubits)

Site i of the patch (site 1 = measured edge site) is mapped to Qiskit qubit index i-1.
The circuit returned is the unitary U = exp(-i H_S(x) t), approximated by a product formula
with `trotter_steps` repetitions of order 1 or 2.  No state preparation or measurement.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MIN_QUBITS = 2


def _as_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _as_positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a positive integer")
    if value < 1:
        raise ValueError(f"{name} must be >= 1")
    return int(value)


def _as_real_list(value, length, name):
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be a list of real numbers")
    if len(value) != length:
        raise ValueError(f"{name} must have length {length}")
    return [_as_real(v, f"{name}[{k}]") for k, v in enumerate(value)]


def _parse_instance(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    if "n" not in instance or "J" not in instance or "h" not in instance or "t" not in instance:
        raise ValueError("instance requires keys 'n', 'J', 'h', 't'")
    n = _as_positive_int(instance["n"], "n")
    if n < MIN_QUBITS or n > MAX_QUBITS:
        raise ValueError(f"n must satisfy {MIN_QUBITS} <= n <= {MAX_QUBITS}")
    couplings = _as_real_list(instance["J"], n - 1, "J")
    fields = _as_real_list(instance["h"], n, "h")
    t = _as_real(instance["t"], "t")
    steps = _as_positive_int(instance["trotter_steps"], "trotter_steps") if "trotter_steps" in instance else 1
    order = _as_positive_int(instance["order"], "order") if "order" in instance else 2
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    return n, couplings, fields, t, steps, order


def _append_zz_layer(qc, couplings, dt):
    # exp(-i J_i Z_i Z_{i+1} dt) == RZZ(2 J_i dt) on (i-1, i)  [eq_2 coupling terms]
    for i, coupling in enumerate(couplings):
        qc.rzz(2.0 * coupling * dt, i, i + 1)


def _append_x_layer(qc, fields, dt):
    # exp(-i h_i X_i dt) == RX(2 h_i dt) on qubit i-1  [eq_2 transverse-field terms]
    for i, field in enumerate(fields):
        qc.rx(2.0 * field * dt, i)


def build_circuit(instance):
    """Return the Trotterized unitary exp(-i H_S(x) t) on an n-qubit 'sim' register.

    instance keys:
      n             : patch size (2..12)
      J             : list of n-1 real ZZ couplings J_1..J_{n-1}
      h             : list of n real transverse fields h_1..h_n
      t             : real evolution time
      trotter_steps : positive integer number of product-formula repetitions (optional, default 1)
      order         : 1 (Lie-Trotter) or 2 (symmetric Strang) (optional, default 2)
    """
    n, couplings, fields, t, steps, order = _parse_instance(instance)
    sim = QuantumRegister(n, "sim")
    qc = QuantumCircuit(sim, name="exp(-i H_S t)")
    dt = t / steps
    # eq_3 (unitary part): U = exp(-i H_S(x) t) approximated by a product formula.
    for _ in range(steps):
        if order == 1:
            _append_zz_layer(qc, couplings, dt)
            _append_x_layer(qc, fields, dt)
        else:
            _append_x_layer(qc, fields, 0.5 * dt)
            _append_zz_layer(qc, couplings, dt)
            _append_x_layer(qc, fields, 0.5 * dt)
    return qc
