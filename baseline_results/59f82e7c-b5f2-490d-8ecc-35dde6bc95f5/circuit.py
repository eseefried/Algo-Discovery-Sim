"""Cyclic mutually-unbiased-basis (MUB) generator powers for MUB tomography.

build_circuit(instance) -> QuantumCircuit

The returned circuit is the unitary (U^dagger)^k (default) or U^k acting on an
n-qubit data register, where U is a cyclic MUB generator (eq_2).  Applying
(U^dagger)^k before a computational-basis measurement realises a measurement in
the k-th basis B_k = {U^k |j>} (eq_5).

Generators:
  * n = 1 (default): U_1 = S H, i.e. Hadamard first, then the phase gate S
    (eq_4).  U_1^3 = exp(i*pi/4) * identity, so k in {0, 1, 2} cycles through
    the Z, Y and X eigenbases, the complete set of three single-qubit MUBs.
  * template (n >= 1): U = H^{(x)n} D with D = prod CZ_{ab} prod S_c over a
    user-supplied edge set 'cz_edges' and vertex set 's_qubits' (eq_3).  The
    diagonal network D acts first, then the Hadamard layer.  Whether a given
    pattern is cyclic of order d+1 and produces MUBs is NOT verified here.

Instance keys:
  n         : int, number of data qubits, 1 <= n <= 12
  k         : int, basis index / power, 0 <= k <= 2**n
  inverse   : bool (optional, default True). True -> (U^dagger)^k, False -> U^k
  cz_edges  : list of [a, b] qubit pairs (required for n > 1, optional for n = 1)
  s_qubits  : list of qubit indices receiving S (required with cz_edges)

Qubit 0 of the register is the least significant bit of the basis label j.
"""
from __future__ import annotations

import math
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"'{name}' must be an integer, got {value!r}")
    return value


def _as_bool(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"'{name}' must be a boolean, got {value!r}")
    return value


def _validate_pattern(n, cz_edges, s_qubits):
    """Validate the eq_3 diagonal network description."""
    if not isinstance(cz_edges, (list, tuple)):
        raise ValueError("'cz_edges' must be a list of [a, b] pairs")
    if not isinstance(s_qubits, (list, tuple)):
        raise ValueError("'s_qubits' must be a list of qubit indices")
    edges = []
    for pair in cz_edges:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError(f"edge {pair!r} must be a pair [a, b]")
        a = _as_int(pair[0], "cz_edges entry")
        b = _as_int(pair[1], "cz_edges entry")
        if a < 0 or b < 0 or a >= n or b >= n:
            raise ValueError(f"edge {pair!r} refers to a qubit outside 0..{n - 1}")
        if a == b:
            raise ValueError(f"edge {pair!r} must connect two distinct qubits")
        edges.append((a, b))
    verts = []
    for c in s_qubits:
        c_int = _as_int(c, "s_qubits entry")
        if c_int < 0 or c_int >= n:
            raise ValueError(f"s_qubits entry {c!r} outside 0..{n - 1}")
        verts.append(c_int)
    return edges, verts


def _generator_eq4(n):
    """eq_4: U_1 = S H on a single qubit (H applied first, then S)."""
    if n != 1:
        raise ValueError("the built-in generator of eq_4 is defined only for n = 1")
    gen = QuantumCircuit(1, name="U_SH")
    gen.h(0)
    gen.s(0)
    return gen


def _generator_eq3(n, edges, verts):
    """eq_3 template: U = H^{(x)n} D, D = prod CZ_ab prod S_c (D acts first)."""
    gen = QuantumCircuit(n, name="U_HD")
    # diagonal network D (all factors commute, so ordering is immaterial)
    for c in verts:
        gen.s(c)
    for (a, b) in edges:
        gen.cz(a, b)
    # Hadamard layer
    for q in range(n):
        gen.h(q)
    return gen


def build_circuit(instance):
    """Return the unitary (U^dagger)^k (or U^k) of the cyclic MUB generator.

    eq_2: B_k = {U^k |j>}; the circuit is k repetitions of U (or U^dagger).
    eq_5: measuring in B_k == applying (U^dagger)^k then a Z-basis measurement.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "k" not in instance:
        raise ValueError("instance must contain 'n' and 'k'")
    n = _as_int(instance["n"], "n")
    k = _as_int(instance["k"], "k")
    inverse = True
    if "inverse" in instance:
        inverse = _as_bool(instance["inverse"], "inverse")

    if n < 1 or n > MAX_QUBITS:
        raise ValueError(f"'n' must satisfy 1 <= n <= {MAX_QUBITS}, got {n}")
    d = 2 ** n
    if k < 0 or k > d:
        raise ValueError(f"'k' must satisfy 0 <= k <= d = {d}, got {k}")

    has_pattern = ("cz_edges" in instance) or ("s_qubits" in instance)
    if has_pattern:
        if "cz_edges" not in instance or "s_qubits" not in instance:
            raise ValueError("'cz_edges' and 's_qubits' must be supplied together")
        edges, verts = _validate_pattern(n, instance["cz_edges"], instance["s_qubits"])
        gen = _generator_eq3(n, edges, verts)
    else:
        if n != 1:
            raise ValueError(
                "for n > 1 the generator pattern ('cz_edges', 's_qubits') must be "
                "supplied; the explicit multi-qubit generator is not fixed by the "
                "specification"
            )
        gen = _generator_eq4(n)

    if inverse:
        gen = gen.inverse()

    data = QuantumRegister(n, "data")
    qc = QuantumCircuit(data, name=f"MUB_power_k{k}")
    # eq_2 / eq_5: k-fold repetition of the (inverse) generator
    for _ in range(k):
        qc.compose(gen, qubits=list(range(n)), inplace=True)
    return qc
