"""Discretised Hamiltonian-evolution operator for Grover search.

Implements U(delta, m) = [ exp(-i*delta*|s><s|) * exp(-i*delta*|t><t|) ]^m
on an n-qubit search register (qubit 0 = least significant bit of x).

- step_mode 'trotter'    : delta = T/m with T = pi*sqrt(N)/2  (eq_2, eq_3)
- step_mode 'reflection' : delta = pi, each factor is an exact reflection
                           (eq_4); m steps = m Grover iterations up to a
                           global phase (-1)^m  (eq_5 for n=2, t=3, m=1).

The runner prepares the input state (|s> = H^{(x)n}|0>) and measures.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    for key in ("n", "marked", "steps", "step_mode"):
        if key not in instance:
            raise ValueError("instance is missing key '%s'" % key)
    n = instance["n"]
    marked = instance["marked"]
    steps = instance["steps"]
    mode = instance["step_mode"]
    if not _is_int(n) or n < 1 or n > MAX_QUBITS:
        raise ValueError("n must be an integer in [1, %d]" % MAX_QUBITS)
    if not _is_int(marked) or marked < 0 or marked >= (1 << n):
        raise ValueError("marked must be an integer in [0, 2^n)")
    if not _is_int(steps) or steps < 1:
        raise ValueError("steps must be a positive integer")
    if mode not in ("trotter", "reflection"):
        raise ValueError("step_mode must be 'trotter' or 'reflection'")
    return n, marked, steps, mode


def _projector_phase(qc, qubits, marked, delta):
    """Append exp(-i*delta*|marked><marked|) on the given qubits (eq_3 factor).

    exp(-i*delta*|t><t|) = 1 + (e^{-i delta} - 1)|t><t| is a phase e^{-i delta}
    on the single basis state |t>, realised as X-conjugation (to map |t> to
    |1...1>) around a multi-controlled phase gate with angle -delta.
    For delta = pi this is exactly the reflection 1 - 2|t><t| (eq_4).
    """
    n = len(qubits)
    flip = [qubits[q] for q in range(n) if ((marked >> q) & 1) == 0]
    for q in flip:
        qc.x(q)
    if n == 1:
        qc.p(-delta, qubits[0])
    else:
        qc.mcp(-delta, qubits[:-1], qubits[-1])
    for q in flip:
        qc.x(q)


def _uniform_projector_phase(qc, qubits, delta):
    """Append exp(-i*delta*|s><s|) = H^{(x)n} exp(-i*delta*|0><0|) H^{(x)n} (eq_3).

    For delta = pi this is exactly 1 - 2|s><s| = -(2|s><s| - 1), i.e. the
    Grover diffusion reflection up to a global sign (eq_4, eq_5).
    """
    for q in qubits:
        qc.h(q)
    _projector_phase(qc, qubits, 0, delta)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Return the discretised evolution operator U(delta, m) as a QuantumCircuit.

    instance keys:
      n         : number of search qubits (N = 2^n), 1 <= n <= 12
      marked    : marked item t in [0, 2^n), little-endian encoding
      steps     : number m of product-formula steps (m >= 1)
      step_mode : 'trotter' (delta = T/m, T = pi*sqrt(N)/2) or
                  'reflection' (delta = pi, exact reflections / Grover steps)
    """
    n, marked, steps, mode = _validate(instance)
    big_n = 1 << n
    if mode == "trotter":
        # eq_2: exact evolution time T = pi*sqrt(N)/2 ; eq_3: delta = T/m
        total_time = math.pi * math.sqrt(big_n) / 2.0
        delta = total_time / steps
    else:
        # eq_4: maximal step delta = pi turns each exponential into a reflection
        delta = math.pi
    reg = QuantumRegister(n, "search")
    qc = QuantumCircuit(reg, name="search_evolution_%s" % mode)
    qubits = list(range(n))
    for _ in range(steps):
        # one product-formula step: oracle factor first, then uniform factor
        # (eq_3 split of H = |s><s| + |t><t|; Grover ordering of eq_4/eq_5)
        _projector_phase(qc, qubits, marked, delta)
        _uniform_projector_phase(qc, qubits, delta)
    return qc
