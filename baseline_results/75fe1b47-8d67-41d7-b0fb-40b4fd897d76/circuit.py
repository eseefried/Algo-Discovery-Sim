"""Continuous-time quantum-walk search evolution on the complete graph K_N (N = 2**n).

Implements the OPERATION exp(-i H t) with (eq_1, eq_5)
    H = -gamma * A - |w><w|,      A = J - I  (complete graph adjacency matrix).
Using J = N |s><s| (|s> the uniform superposition) one has A = N|s><s| - I, hence
    exp(-i H t) = exp(-i gamma t) * exp( i t ( gamma*N |s><s| + |w><w| ) ).
The walk term (unperturbed H^(0)) and the oracle term (perturbation V) of the
perturbative split (eq_3) do not commute; their joint exponential is approximated by a
symmetric second-order Trotter product.  Each factor is an exact rank-one projector
phase: exp(i a |b><b|) is a multi-controlled phase on basis state |b>, and
exp(i a |s><s|) = H^{x n} exp(i a |0><0|) H^{x n}.

Qubit layout: qubit i of the register 'vertex' holds bit i of the vertex index v
(Qiskit little-endian; v = sum_i 2**i * v_i).  No input preparation, no measurement.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_TROTTER_STEPS = 4096
ALLOWED_KEYS = ("graph", "num_qubits", "marked_vertex", "gamma", "time", "trotter_steps")


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    return value


def _check_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    v = float(value)
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return v


def _parse_instance(instance):
    """Validate the instance dictionary and return (n, w, gamma, t, steps)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in instance:
        if key not in ALLOWED_KEYS:
            raise ValueError(f"unknown instance key {key!r}; allowed keys: {ALLOWED_KEYS}")
    graph = instance.get("graph", "complete")
    if graph != "complete":
        raise ValueError("only the complete graph ('complete') is supported")
    if "num_qubits" not in instance:
        raise ValueError("instance must contain 'num_qubits'")
    n = _check_int(instance["num_qubits"], "num_qubits")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError(f"num_qubits must be between 1 and {MAX_QUBITS}, got {n}")
    num_vertices = 2 ** n
    if "marked_vertex" not in instance:
        raise ValueError("instance must contain 'marked_vertex'")
    w = _check_int(instance["marked_vertex"], "marked_vertex")
    if w < 0 or w >= num_vertices:
        raise ValueError(f"marked_vertex must be in [0, {num_vertices - 1}], got {w}")
    # eq_5 defaults: critical jumping rate gamma_c = 1/N and runtime t_* = pi*sqrt(N)/2.
    if "gamma" in instance:
        gamma = _check_real(instance["gamma"], "gamma")
    else:
        gamma = 1.0 / num_vertices
    if gamma <= 0.0:
        raise ValueError(f"gamma must be positive, got {gamma}")
    if "time" in instance:
        t = _check_real(instance["time"], "time")
    else:
        t = math.pi * math.sqrt(num_vertices) / 2.0
    if t < 0.0:
        raise ValueError(f"time must be non-negative, got {t}")
    if "trotter_steps" in instance:
        steps = _check_int(instance["trotter_steps"], "trotter_steps")
    else:
        steps = 16
    if steps < 1 or steps > MAX_TROTTER_STEPS:
        raise ValueError(f"trotter_steps must be between 1 and {MAX_TROTTER_STEPS}, got {steps}")
    return n, w, gamma, t, steps


def _projector_phase(qc, qubits, basis_index, angle):
    """Apply exp(i * angle * |b><b|) for computational basis state b = basis_index.

    Realised as X-conjugation of the zero bits followed by a multi-controlled phase
    (a single phase gate when there is one qubit).  Exact, no approximation.
    """
    n = len(qubits)
    flips = [qubits[i] for i in range(n) if not (basis_index >> i) & 1]
    for q in flips:
        qc.x(q)
    if n == 1:
        qc.p(angle, qubits[0])
    else:
        qc.mcp(angle, qubits[:-1], qubits[-1])
    for q in flips:
        qc.x(q)


def _uniform_projector_phase(qc, qubits, angle):
    """Apply exp(i * angle * |s><s|), |s> the uniform superposition (eq_2 state).

    Since |s> = H^{x n}|0...0>, this is H^{x n} exp(i*angle*|0><0|) H^{x n}.
    """
    for q in qubits:
        qc.h(q)
    _projector_phase(qc, qubits, 0, angle)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Return the Trotterised search evolution exp(-i H t) on the complete graph K_{2**n}.

    H = -gamma*A - |w><w| with A = J - I  (eq_1 / eq_5).  Decomposition (eq_3):
        exp(-iHt) = e^{-i gamma t} [ e^{i (gamma N d/2)|s><s|} e^{i d |w><w|} e^{i (gamma N d/2)|s><s|} ]^r
    with d = t / r  (second-order Trotter, error O(t^3/r^2)).
    """
    n, w, gamma, t, steps = _parse_instance(instance)
    num_vertices = 2 ** n
    reg = QuantumRegister(n, "vertex")
    qc = QuantumCircuit(reg, name=f"ctqw_search_K{num_vertices}_w{w}")
    qubits = list(range(n))
    delta = t / steps
    half_walk_angle = gamma * num_vertices * delta / 2.0  # exp(+i gamma N d/2 |s><s|)
    oracle_angle = delta                                   # exp(+i d |w><w|)
    for _ in range(steps):
        _uniform_projector_phase(qc, qubits, half_walk_angle)
        _projector_phase(qc, qubits, w, oracle_angle)
        _uniform_projector_phase(qc, qubits, half_walk_angle)
    # Constant shift +gamma*I in H = -gamma*N|s><s| + gamma*I - |w><w| gives e^{-i gamma t}.
    qc.global_phase = (-gamma * t) % (2.0 * math.pi)
    return qc
