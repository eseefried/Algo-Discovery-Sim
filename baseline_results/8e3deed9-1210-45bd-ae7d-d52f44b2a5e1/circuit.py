"""Two-fermion continuous-time quantum walk on a graph (Trotterised adjacency Hamiltonian).

Implements the operation
    U^(2)(t) = exp(-i t (A (x) I + I (x) A)) = exp(-i t A) (x) exp(-i t A)        [eq_4]
on two vertex registers v1, v2 that encode the positions of the two particles in binary
(qubit 0 of each register = least significant bit).  Because both tensor factors are the
same unitary, the antisymmetric (fermionic) subspace spanned by |ij>_- (eq_3) is preserved
exactly, even after the product-formula approximation used below.

Each single-register factor exp(-i t A) with A = sum_{(i,j) in E} (|i><j| + |j><i|) is
approximated by a first- or second-order product formula over edge terms.  A single edge
term exp(-i theta (|i><j| + |j><i|)) is implemented exactly: CNOT/X gates map |i>, |j> to
|c,0>, |c,1> on a pivot qubit with all other qubits in state |1>, a multi-controlled
RX(2 theta) acts as exp(-i theta X) on that pair only, and the basis change is undone.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RXGate

MAX_TOTAL_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _validate_instance(instance):
    """Validate the instance dict and return (num_vertices, m, edges, time, steps, order)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    for key in ("num_vertices", "edges", "time", "trotter_steps", "trotter_order"):
        if key not in instance:
            raise ValueError(f"instance is missing required key '{key}'")
    num_vertices = _as_int(instance["num_vertices"], "num_vertices")
    if num_vertices < 2:
        raise ValueError("num_vertices must be at least 2")
    m = max(1, (num_vertices - 1).bit_length())
    if 2 * m > MAX_TOTAL_QUBITS:
        raise ValueError(
            f"two vertex registers of {m} qubits each exceed the cap of {MAX_TOTAL_QUBITS} qubits"
        )
    time = instance["time"]
    if isinstance(time, bool) or not isinstance(time, (int, float)) or not math.isfinite(time):
        raise ValueError("time must be a finite real number")
    steps = _as_int(instance["trotter_steps"], "trotter_steps")
    if steps < 1:
        raise ValueError("trotter_steps must be a positive integer")
    order = _as_int(instance["trotter_order"], "trotter_order")
    if order not in (1, 2):
        raise ValueError("trotter_order must be 1 or 2")
    raw_edges = instance["edges"]
    if not isinstance(raw_edges, (list, tuple)):
        raise ValueError("edges must be a list of [i, j] pairs")
    seen = set()
    edges = []
    degree = [0] * num_vertices
    for edge in raw_edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError("each edge must be a pair [i, j]")
        i = _as_int(edge[0], "edge endpoint")
        j = _as_int(edge[1], "edge endpoint")
        if i < 0 or j < 0 or i >= num_vertices or j >= num_vertices:
            raise ValueError("edge endpoints must lie in range(num_vertices)")
        if i == j:
            raise ValueError("self-loops are not allowed (simple graph required)")
        key = (min(i, j), max(i, j))
        if key in seen:
            raise ValueError(f"duplicate edge {key}")
        seen.add(key)
        edges.append(key)
        degree[i] += 1
        degree[j] += 1
    if not edges:
        raise ValueError("graph must contain at least one edge")
    if "degree" in instance:
        k = _as_int(instance["degree"], "degree")
        if any(d != k for d in degree):
            raise ValueError(f"graph is not {k}-regular as requested")
    return num_vertices, m, edges, float(time), steps, order


def _apply_edge_term(qc, qubits, i, j, theta):
    """Apply exp(-i theta (|i><j| + |j><i|)) exactly on the register `qubits` (qubit 0 = LSB).

    This is one hopping term of the adjacency Hamiltonian A (eq_4).  i != j is required.
    """
    m = len(qubits)
    d = i ^ j
    pivot = 0
    while not (d >> pivot) & 1:
        pivot += 1
    others = [q for q in range(m) if q != pivot]
    flip = [q for q in others if (d >> q) & 1]
    # Step 1: CNOTs from the pivot make |i> and |j> agree on every non-pivot bit.
    for q in flip:
        qc.cx(qubits[pivot], qubits[q])
    # Common bit pattern of the two states on the non-pivot qubits after step 1.
    zeros = []
    for q in others:
        bit = (i >> q) & 1
        if q in flip:
            bit ^= (i >> pivot) & 1
        if bit == 0:
            zeros.append(q)
    # Step 2: X gates so that the common pattern becomes all ones (controls active).
    for q in zeros:
        qc.x(qubits[q])
    # Step 3: exp(-i theta X) = RX(2 theta) on the pivot, controlled on all other qubits.
    gate = RXGate(2.0 * theta)
    if others:
        qc.append(gate.control(len(others)), [qubits[q] for q in others] + [qubits[pivot]])
    else:
        qc.append(gate, [qubits[pivot]])
    # Step 4: undo the basis change.
    for q in reversed(zeros):
        qc.x(qubits[q])
    for q in reversed(flip):
        qc.cx(qubits[pivot], qubits[q])


def _apply_single_particle_walk(qc, qubits, edges, time, steps, order):
    """Product-formula approximation of exp(-i time A) on one vertex register (eq_4)."""
    dt = time / steps
    for _ in range(steps):
        if order == 1:
            for (i, j) in edges:
                _apply_edge_term(qc, qubits, i, j, dt)
        else:
            for (i, j) in edges:
                _apply_edge_term(qc, qubits, i, j, 0.5 * dt)
            for (i, j) in reversed(edges):
                _apply_edge_term(qc, qubits, i, j, 0.5 * dt)


def build_circuit(instance):
    """Return the two-fermion walk unitary U^(2)(t) (eq_4) on registers v1, v2.

    instance keys:
      num_vertices  : int N (2 <= N <= 64), vertices labelled 0..N-1
      edges         : list of [i, j] pairs (simple undirected graph)
      time          : real walk time t
      trotter_steps : positive int r
      trotter_order : 1 (Lie-Trotter) or 2 (Strang)
      degree        : optional int k; if present the graph must be k-regular
    Register v1 (qubits 0..m-1) holds particle 1, v2 (qubits m..2m-1) holds particle 2,
    m = ceil(log2 N), least significant bit first.  The operator is U (x) U with the same
    U on both registers, so the antisymmetric subspace |ij>_- (eq_3) is preserved.
    """
    num_vertices, m, edges, time, steps, order = _validate_instance(instance)
    v1 = QuantumRegister(m, "v1")
    v2 = QuantumRegister(m, "v2")
    qc = QuantumCircuit(v1, v2, name=f"two_fermion_walk_N{num_vertices}")
    # eq_4: exp(-i t (A (x) I + I (x) A)) = exp(-i t A)_v1 * exp(-i t A)_v2 (commuting factors)
    _apply_single_particle_walk(qc, list(v1), edges, time, steps, order)
    _apply_single_particle_walk(qc, list(v2), edges, time, steps, order)
    return qc
