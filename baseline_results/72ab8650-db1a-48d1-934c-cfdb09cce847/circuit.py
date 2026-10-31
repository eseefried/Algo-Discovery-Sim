"""Generalized Kitaev phase estimation: product-state probe with N phase gates
distributed arbitrarily over M qubits (eq_1), followed by the local
measurement-basis rotation P(theta_j) then H (eq_2).

The returned circuit is the unitary operation only: no state preparation
(unless the optional flag 'prepare_plus' is set), no measurements.
The runner is expected to feed |+>^{\\otimes M} and measure in the
computational basis to sample the outcome string x of eq_2.

Qubit layout: spec qubit j (1-indexed) -> Qiskit qubit index j-1.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_TOTAL_GATES = 4096


def _as_int(value, name):
    """Validate a JSON integer (bool is rejected)."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    return value


def _as_real(value, name):
    """Validate a finite real number (bool is rejected)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    v = float(value)
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return v


def _parse_instance(instance):
    """Extract and validate (phi, n_list, theta_list, prepare_plus)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    if "phi" not in instance:
        raise ValueError("instance must contain 'phi'")
    if "n" not in instance:
        raise ValueError("instance must contain 'n' (list of per-qubit gate counts)")
    phi = _as_real(instance["phi"], "phi")

    n_raw = instance["n"]
    if not isinstance(n_raw, list) or len(n_raw) == 0:
        raise ValueError("'n' must be a non-empty list of non-negative integers")
    m = len(n_raw)
    if m > MAX_QUBITS:
        raise ValueError(f"M={m} qubits exceeds the cap of {MAX_QUBITS}")
    n_list = []
    for j, nj in enumerate(n_raw):
        nj = _as_int(nj, f"n[{j}]")
        if nj < 0:
            raise ValueError(f"n[{j}] must be non-negative, got {nj}")
        n_list.append(nj)
    total = sum(n_list)
    if total <= 0:
        raise ValueError("total number of phase gates N = sum(n) must be positive")
    if total > MAX_TOTAL_GATES:
        raise ValueError(f"N={total} exceeds the cap of {MAX_TOTAL_GATES} phase gates")
    if "N" in instance:
        n_total = _as_int(instance["N"], "N")
        if n_total != total:
            raise ValueError(f"N={n_total} inconsistent with sum(n)={total} (eq_1 constraint)")

    if "theta" in instance:
        th_raw = instance["theta"]
        if not isinstance(th_raw, list) or len(th_raw) != m:
            raise ValueError("'theta' must be a list with the same length as 'n'")
        theta_list = [_as_real(t, f"theta[{j}]") for j, t in enumerate(th_raw)]
    else:
        theta_list = [0.0] * m

    prepare_plus = False
    if "prepare_plus" in instance:
        flag = instance["prepare_plus"]
        if not isinstance(flag, bool):
            raise ValueError("'prepare_plus' must be a boolean")
        prepare_plus = flag

    return phi, n_list, theta_list, prepare_plus


def build_circuit(instance):
    """Build the generalized Kitaev probe-and-rotate operation.

    instance keys:
      phi   : float, the unknown phase of U_phi = diag(1, e^{i phi})
      n     : list[int], n_j >= 0, number of U_phi applications on qubit j
      theta : list[float] (optional, default zeros), local measurement phase
      N     : int (optional), must equal sum(n)
      prepare_plus : bool (optional, default False); if True, Hadamards are
                     prepended to turn |0>^M into |+>^M (eq_1 initial state).
    """
    phi, n_list, theta_list, prepare_plus = _parse_instance(instance)
    m = len(n_list)

    q = QuantumRegister(m, "q")
    qc = QuantumCircuit(q, name="gen_kitaev_probe")

    if prepare_plus:
        # eq_1 initial product state |+>^{\otimes M} (optional; runner normally prepares it)
        for j in range(m):
            qc.h(q[j])

    # eq_1: qubit j accumulates phase n_j*phi via n_j explicit applications of U_phi.
    # Each qc.p(phi) call is one use of the resource (sum over j equals N).
    for j in range(m):
        for _ in range(n_list[j]):
            qc.p(phi, q[j])

    # eq_2: local measurement basis rotation diag(1, e^{i theta_j}) followed by H,
    # so that a computational-basis measurement yields
    # p(x_j|phi) = [1 + (-1)^{x_j} cos(n_j phi + theta_j)]/2.
    for j in range(m):
        if theta_list[j] != 0.0:
            qc.p(theta_list[j], q[j])
        qc.h(q[j])

    return qc
