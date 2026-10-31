"""Grover-type search iteration with systematic phase-inversion errors.

Implements eq_2 of the specification:
    I_t^{phi} = I - (1 - e^{i phi}) |t><t|      (marked-state inversion, phi = pi + delta1)
    I_s^{psi} = I - (1 - e^{i psi}) |s><s|      (mean-state inversion,   psi = pi + delta2)
    G_{phi,psi} = - I_s^{psi} I_t^{phi}          (one erroneous iteration)
The circuit applies G_{phi,psi}^k on n data qubits (N = 2^n items). The input
state |s> (eq_1) is prepared by the runner; no measurement is included (eq_3 is
evaluated by the runner).

Qubit layout: data qubits 0..n-1, qubit i holds bit i of the item index
(Qiskit little-endian: qubit 0 is the least significant bit).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _as_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _parse_instance(instance):
    """Validate the instance dictionary and return (n, marked, k, delta1, delta2)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    n = _as_int(instance.get("n_qubits"), "n_qubits")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError(f"n_qubits must be between 1 and {MAX_QUBITS}")
    marked = _as_int(instance.get("marked"), "marked")
    if marked < 0 or marked >= (1 << n):
        raise ValueError("marked must satisfy 0 <= marked < 2**n_qubits")
    k = _as_int(instance.get("iterations"), "iterations")
    if k < 0:
        raise ValueError("iterations must be non-negative")
    if "delta1" in instance or "delta2" in instance:
        if "delta1" not in instance or "delta2" not in instance:
            raise ValueError("provide both delta1 and delta2, or a single matched delta")
        delta1 = _as_real(instance.get("delta1"), "delta1")
        delta2 = _as_real(instance.get("delta2"), "delta2")
    elif "delta" in instance:
        delta1 = _as_real(instance.get("delta"), "delta")
        delta2 = delta1
    else:
        raise ValueError("instance must contain delta1 and delta2 (or matched delta)")
    return n, marked, k, delta1, delta2


def _phase_on_all_ones(qc, qubits, angle):
    """Multiply the basis state |1...1> of `qubits` by exp(i*angle)."""
    if len(qubits) == 1:
        qc.p(angle, qubits[0])
    else:
        qc.mcp(angle, qubits[:-1], qubits[-1])


def _marked_inversion(qc, qubits, marked, phi):
    """eq_2: I_t^{phi} = I - (1 - e^{i phi}) |t><t|, i.e. phase e^{i phi} on |t>."""
    flipped = [q for i, q in enumerate(qubits) if ((marked >> i) & 1) == 0]
    for q in flipped:
        qc.x(q)
    _phase_on_all_ones(qc, qubits, phi)
    for q in flipped:
        qc.x(q)


def _mean_inversion(qc, qubits, psi):
    """eq_2: I_s^{psi} = I - (1 - e^{i psi}) |s><s| = H^n (I - (1-e^{i psi})|0><0|) H^n."""
    for q in qubits:
        qc.h(q)
    for q in qubits:
        qc.x(q)
    _phase_on_all_ones(qc, qubits, psi)
    for q in qubits:
        qc.x(q)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Return the operation G_{phi,psi}^k (eq_2) on an n-qubit data register.

    instance keys:
        n_qubits   : int, number of data qubits (N = 2**n_qubits), 1..12
        marked     : int, marked item index t in [0, N)
        iterations : int, number k of erroneous iterations (>= 0)
        delta1     : real, phase error of the marked-state inversion (phi = pi + delta1)
        delta2     : real, phase error of the mean-state inversion (psi = pi + delta2)
        (alternatively a single key 'delta' for matched errors delta1 = delta2)
    """
    n, marked, k, delta1, delta2 = _parse_instance(instance)
    phi = math.pi + delta1
    psi = math.pi + delta2
    data = QuantumRegister(n, "data")
    qc = QuantumCircuit(data, name="G_phi_psi^k")
    qubits = list(range(n))
    for _ in range(k):
        # eq_2: one erroneous iteration G_{phi,psi} = - I_s^{psi} I_t^{phi}
        _marked_inversion(qc, qubits, marked, phi)
        _mean_inversion(qc, qubits, psi)
        qc.global_phase += math.pi  # overall sign -1 of G_{phi,psi}
    return qc
