"""Alternating-operator (QAOA) MaxCut circuit builder.

Implements the unitary of eq_3 of the specification for an arbitrary simple
graph on n <= 12 vertices and p >= 1 layers with caller-supplied angles:

    U(gamma, beta) = prod_{l=1}^{p} exp(-i beta_l B) exp(-i gamma_l C)  [ H^{(x)n} ]

where C = sum_{(j,k) in E} (1 - Z_j Z_k)/2 (eq_1) and B = sum_j X_j (eq_2).
Qubit j <-> vertex j; qubit 0 is the least significant bit of |z>.
The runner supplies the input state (expected |0...0>); when
``prepare_plus`` is true the Hadamard layer of eq_3 that maps |0...0> to the
uniform superposition |+>^n is included as part of the algorithmic unitary.
No measurements are appended.
"""

import math
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _validate_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _validate_angles(values, name):
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{name} must be a list of real numbers")
    out = []
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"{name} entries must be real numbers")
        f = float(v)
        if not math.isfinite(f):
            raise ValueError(f"{name} entries must be finite")
        out.append(f)
    return out


def _validate_edges(edges, num_qubits):
    if not isinstance(edges, (list, tuple)) or len(edges) < 1:
        raise ValueError("edges must be a non-empty list of [j, k] pairs")
    seen = set()
    out = []
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError("each edge must be a pair [j, k]")
        j = _validate_int(e[0], "edge endpoint")
        k = _validate_int(e[1], "edge endpoint")
        if j < 0 or k < 0 or j >= num_qubits or k >= num_qubits:
            raise ValueError("edge endpoint out of range")
        if j == k:
            raise ValueError("self-loops are not allowed")
        key = (min(j, k), max(j, k))
        if key in seen:
            raise ValueError("duplicate edge in graph")
        seen.add(key)
        out.append(key)
    return out


def _apply_cost_unitary(qc, q, edges, gamma):
    """eq_1 / eq_3: exp(-i gamma C) = prod_{(j,k) in E} exp(-i gamma (1 - Z_j Z_k)/2).

    Each edge factor is diagonal: phase 1 when z_j == z_k and exp(-i gamma)
    when z_j != z_k.  CX(j,k); P(-gamma) on k; CX(j,k) realises exactly this
    (no global-phase discrepancy).  All edge factors commute, so edge order
    is irrelevant.
    """
    for (j, k) in edges:
        qc.cx(q[j], q[k])
        qc.p(-gamma, q[k])
        qc.cx(q[j], q[k])


def _apply_mixer_unitary(qc, q, num_qubits, beta):
    """eq_2 / eq_3: exp(-i beta B) = prod_j exp(-i beta X_j) = prod_j RX(2 beta)_j."""
    for j in range(num_qubits):
        qc.rx(2.0 * beta, q[j])


def build_circuit(instance):
    """Build the p-layer QAOA MaxCut unitary (eq_3) for the given instance.

    instance keys:
      num_qubits   : int, number of vertices n (1 <= n <= 12)
      edges        : list of [j, k] pairs (simple graph, at least one edge)
      gammas       : list of p cost angles gamma_l (layer 1 first)
      betas        : list of p mixer angles beta_l (layer 1 first)
      prepare_plus : bool, include the Hadamard layer mapping |0>^n -> |+>^n
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("num_qubits", "edges", "gammas", "betas", "prepare_plus"):
        if key not in instance:
            raise ValueError(f"missing instance key: {key}")
    num_qubits = _validate_int(instance["num_qubits"], "num_qubits")
    if num_qubits < 1 or num_qubits > MAX_QUBITS:
        raise ValueError(f"num_qubits must be in [1, {MAX_QUBITS}]")
    edges = _validate_edges(instance["edges"], num_qubits)
    gammas = _validate_angles(instance["gammas"], "gammas")
    betas = _validate_angles(instance["betas"], "betas")
    if len(gammas) < 1 or len(gammas) != len(betas):
        raise ValueError("gammas and betas must have equal length p >= 1")
    prepare_plus = instance["prepare_plus"]
    if not isinstance(prepare_plus, bool):
        raise ValueError("prepare_plus must be a bool")

    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q, name="qaoa_maxcut")

    # eq_3: |+>^n = H^{(x)n}|0>^n (algorithmic Hadamard layer, optional)
    if prepare_plus:
        for j in range(num_qubits):
            qc.h(q[j])

    # eq_3: layer l = 1 acts first; within a layer the cost unitary precedes the mixer
    for gamma, beta in zip(gammas, betas):
        _apply_cost_unitary(qc, q, edges, gamma)
        _apply_mixer_unitary(qc, q, num_qubits, beta)

    return qc
