"""Coherent unrolling of n weak-measurement steps for a qubit system coupled to
fresh qubit probes through the constant interaction Hamiltonian H = g Z_S (x) Y_P.

Each step k (eq_2, eq_3 of the specification) applies
    U = exp(-i * eps * Z_S (x) Y_Pk),   eps = g * dt,
to the system qubit and probe k, then (optionally) a Hadamard on probe k so that a
later computational-basis readout of probe k corresponds to the X-basis outcome
m_k in {+,-} of eq_3.  No measurement or reset is included: by deferred measurement
the n probes are distinct qubits (eq_4 product structure).  The classical stopping
rule (eq_5) is outside this operation.

Qubit layout (Qiskit index 0 = least significant bit):
    qubit 0        : system qubit S
    qubit k (1..n) : probe used in step k (prepared in |0> by the runner)
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    allowed = {"epsilon", "num_steps", "readout_hadamard"}
    for key in instance:
        if key not in allowed:
            raise ValueError("unknown instance key: %s" % str(key))
    if "epsilon" not in instance or "num_steps" not in instance:
        raise ValueError("instance requires 'epsilon' and 'num_steps'")
    eps = instance["epsilon"]
    if isinstance(eps, bool) or not isinstance(eps, (int, float)):
        raise ValueError("epsilon must be a real number")
    eps = float(eps)
    if not math.isfinite(eps) or not (0.0 < eps < math.pi / 4.0):
        raise ValueError("epsilon must satisfy 0 < epsilon < pi/4 (weak coupling)")
    n = instance["num_steps"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("num_steps must be an integer")
    if n < 1:
        raise ValueError("num_steps must be >= 1")
    if 1 + n > MAX_QUBITS:
        raise ValueError("1 system qubit + num_steps probes exceeds the %d-qubit cap" % MAX_QUBITS)
    readout = True
    if "readout_hadamard" in instance:
        readout = instance["readout_hadamard"]
        if not isinstance(readout, bool):
            raise ValueError("readout_hadamard must be a boolean")
    return eps, n, readout


def _weak_interaction(qc, s, p, eps):
    """eq_2 / eq_3: U = exp(-i eps Z_S (x) Y_P).

    Decomposition: Y = S X S^dag and X = H Z H on the probe, hence
        U = (I (x) S H) * exp(-i eps Z (x) Z) * (I (x) H S^dag),
    and exp(-i eps Z (x) Z) = RZZ(2 eps) in Qiskit's convention RZZ(t) = exp(-i t/2 Z Z).
    Acting on probe |0>, U gives cos(eps) I(x)|0> + sin(eps) Z(x)|1> as in eq_3.
    """
    qc.sdg(p)
    qc.h(p)
    qc.rzz(2.0 * eps, s, p)
    qc.h(p)
    qc.s(p)


def build_circuit(instance):
    """Return the unitary for num_steps weak-measurement iterations (eq_2-eq_4)."""
    eps, n, readout = _validate(instance)
    sys_reg = QuantumRegister(1, "s")
    probe_reg = QuantumRegister(n, "p")
    qc = QuantumCircuit(sys_reg, probe_reg, name="weak_meas_steps")
    s = sys_reg[0]
    # eq_4: sequential product K_{m_n} ... K_{m_1} realised coherently with one
    # fresh probe per step (deferred measurement); step k uses probe k.
    for k in range(n):
        p = probe_reg[k]
        _weak_interaction(qc, s, p, eps)
        if readout:
            # eq_3: X-basis readout |+-> -> |0/1>, so a later Z readout of the
            # probe gives outcome m_k ('+' <-> 0, '-' <-> 1).
            qc.h(p)
    return qc
