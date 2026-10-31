"""Continuous-time quantum-walk spatial search operator (Trotterized).

Implements the (possibly multi-stage) unitary
    U = prod_k exp(-i H(gamma_k) t_k),   H(gamma) = -gamma * A - |w><w|
for graphs on N = 2**n vertices whose adjacency term is exactly compilable:
  * 'complete' : K_N with A = J - I, J = N |s><s|, |s> = H^{(x)n}|0...0>
  * 'hypercube': Q_n with A = sum_k X_k
The vertex index is stored in binary on the vertex register, qubit 0 = LSB.
The circuit does NOT prepare the uniform superposition nor measure.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

_ALLOWED_GRAPHS = ("complete", "hypercube")
_MAX_QUBITS = 12


def _check_real(value, name, strictly_positive):
    """Return value as a finite float, raising ValueError on bad input."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("%s must be a real number" % name)
    val = float(value)
    if not math.isfinite(val):
        raise ValueError("%s must be finite" % name)
    if strictly_positive and val <= 0.0:
        raise ValueError("%s must be > 0" % name)
    if (not strictly_positive) and val < 0.0:
        raise ValueError("%s must be >= 0" % name)
    return val


def _check_int(value, name, minimum, maximum):
    """Return value as an int within [minimum, maximum] or raise ValueError."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("%s must be an integer" % name)
    if value < minimum or value > maximum:
        raise ValueError("%s must lie in [%d, %d]" % (name, minimum, maximum))
    return int(value)


def _validate(instance):
    """Validate the instance dictionary and return normalized parameters."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    graph = instance.get("graph")
    if graph not in _ALLOWED_GRAPHS:
        raise ValueError("graph must be one of %s" % (_ALLOWED_GRAPHS,))
    n = _check_int(instance.get("num_qubits"), "num_qubits", 1, _MAX_QUBITS)
    num_vertices = 2 ** n
    marked = _check_int(instance.get("marked_vertex"), "marked_vertex", 0, num_vertices - 1)
    steps = _check_int(instance.get("trotter_steps"), "trotter_steps", 1, 100000)
    stages_raw = instance.get("stages")
    if not isinstance(stages_raw, list) or len(stages_raw) < 1:
        raise ValueError("stages must be a non-empty list of {gamma, time} dicts")
    stages = []
    for idx, st in enumerate(stages_raw):
        if not isinstance(st, dict):
            raise ValueError("stage %d must be a dict" % idx)
        gamma = _check_real(st.get("gamma"), "stages[%d].gamma" % idx, True)
        time = _check_real(st.get("time"), "stages[%d].time" % idx, False)
        stages.append((gamma, time))
    return graph, n, marked, steps, stages


def _apply_projector_phase(qc, qubits, basis_index, angle):
    """Apply exp(+i * angle * |b><b|) for computational basis state b.

    Implemented as X on the zero bits of b, a multi-controlled phase on
    |1...1>, then undoing the X gates.
    """
    n = len(qubits)
    flips = [qubits[k] for k in range(n) if not ((basis_index >> k) & 1)]
    for q in flips:
        qc.x(q)
    if n == 1:
        qc.p(angle, qubits[0])
    else:
        qc.mcp(angle, qubits[:-1], qubits[-1])
    for q in flips:
        qc.x(q)


def _apply_oracle_term(qc, qubits, marked, dt):
    """eq_2 oracle part: exp(-i * (-|w><w|) * dt) = exp(+i dt |w><w|)."""
    _apply_projector_phase(qc, qubits, marked, dt)


def _apply_graph_term(qc, qubits, graph, gamma, dt):
    """eq_2 graph part: exp(-i * (-gamma A) * dt) = exp(+i gamma dt A)."""
    n = len(qubits)
    if graph == "hypercube":
        # A = sum_k X_k ; exp(i gamma dt X) = RX(-2 gamma dt)
        for q in qubits:
            qc.rx(-2.0 * gamma * dt, q)
    else:
        # complete graph: A = J - I, J = N |s><s|, |s> = H^{(x)n}|0..0>
        # exp(i gamma dt J) = H^{(x)n} exp(i gamma dt N |0><0|) H^{(x)n}
        # exp(-i gamma dt I) contributes a global phase of -gamma dt.
        num_vertices = 2 ** n
        for q in qubits:
            qc.h(q)
        _apply_projector_phase(qc, qubits, 0, gamma * dt * num_vertices)
        for q in qubits:
            qc.h(q)
        qc.global_phase = qc.global_phase - gamma * dt


def _apply_stage(qc, qubits, graph, marked, gamma, time, steps):
    """eq_1: exp(-i H(gamma) time) via second-order (Strang) product formula.

    Each step applies exp(i dt/2 |w><w|) exp(i gamma dt A) exp(i dt/2 |w><w|)
    with dt = time / steps; the error is O(time * dt^2).
    """
    if time == 0.0:
        return
    dt = time / steps
    for _ in range(steps):
        _apply_oracle_term(qc, qubits, marked, 0.5 * dt)
        _apply_graph_term(qc, qubits, graph, gamma, dt)
        _apply_oracle_term(qc, qubits, marked, 0.5 * dt)


def build_circuit(instance):
    """Build the multi-stage quantum-walk search unitary (eq_5).

    instance keys:
      graph         : 'complete' or 'hypercube'
      num_qubits    : n, vertices N = 2**n (1 <= n <= 12)
      marked_vertex : integer w in [0, N)
      stages        : list of {'gamma': float > 0, 'time': float >= 0}
                      (one entry = single-stage walk, two = two-stage template)
      trotter_steps : positive integer, Strang steps per stage
    """
    graph, n, marked, steps, stages = _validate(instance)
    vertex = QuantumRegister(n, "vertex")
    qc = QuantumCircuit(vertex, name="ctqw_search")
    qubits = [vertex[k] for k in range(n)]
    # eq_5: consecutive piecewise-constant stages with rates gamma_k, times t_k
    for gamma, time in stages:
        _apply_stage(qc, qubits, graph, marked, gamma, time, steps)
    return qc
