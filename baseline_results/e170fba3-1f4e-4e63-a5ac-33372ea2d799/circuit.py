"""Fixed-point amplitude amplification (Chebyshev phase schedule) as a Qiskit operation.

Operation built by build_circuit(instance) on n system qubits:

    U = S_L * A,     A = H^{(x) n}            (state preparation, eq_1 / eq_6)
    S_L = G(alpha_l, beta_l) ... G(alpha_1, beta_1),  L = 2 l + 1 oracle queries
    G(alpha, beta) = S_s(alpha) S_t(beta)     (global sign of eq_2 dropped)
    S_t(beta)  = I - (1 - e^{+i beta}) |t><t|   (phase e^{+i beta} on every target state)
    S_s(alpha) = A S_0(alpha) A^dag,  S_0(alpha) = I - (1 - e^{-i alpha}) |0..0><0..0|

Phase schedule (eq_3):
    1/gamma  = T_{1/L}(1/delta) = cosh( acosh(1/delta) / L )
    alpha_j  = -beta_{l-j+1} = 2 acot( tan(2 pi j / L) * sqrt(1 - gamma^2) ),  j = 1..l

NOTE on conventions: the specification's eq_2 wrote S_t(beta) with e^{-i beta}. Combined
with alpha_j = -beta_{l-j+1} that does NOT give the fixed-point response (hand check,
L=3, lambda=1/4: P ~ 0.24 instead of ~ 0.91). The published convention carries e^{+i beta}
in S_t, which is what is implemented here; equivalently the oracle applies e^{-i alpha_{l-j+1}}.

Qubit k of the register 'sys' is bit k (little-endian) of the integer basis-state label.
The circuit contains no measurements, resets, or input-state initialisation other than A.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    return value


def _fixed_point_phases(num_queries, delta):
    """eq_3: Chebyshev fixed-point phase schedule for L = num_queries (odd) and failure bound delta.

    Returns (alphas, betas) with alphas[j-1] = alpha_j, betas[j-1] = beta_j = -alpha_{l-j+1}.
    """
    l = (num_queries - 1) // 2
    inv_gamma = math.cosh(math.acosh(1.0 / delta) / num_queries)  # 1/gamma = T_{1/L}(1/delta)
    gamma_sq = 1.0 / (inv_gamma * inv_gamma)
    root = math.sqrt(max(0.0, 1.0 - gamma_sq))  # sqrt(1 - gamma^2) = sqrt(w)
    alphas = []
    for j in range(1, l + 1):
        x = math.tan(2.0 * math.pi * j / num_queries) * root
        # acot(x) taken on the branch (0, pi): acot(x) = atan2(1, x); 2*acot is defined mod 2 pi
        alphas.append(2.0 * math.atan2(1.0, x))
    betas = [-alphas[l - j] for j in range(1, l + 1)]  # beta_j = -alpha_{l-j+1}
    return alphas, betas


def _parse_targets(raw, n):
    """Target states given as integers in [0, 2^n) or as n-character bitstrings (leftmost = qubit n-1)."""
    if not isinstance(raw, (list, tuple)) or len(raw) == 0:
        raise ValueError("targets must be a non-empty list")
    dim = 1 << n
    out = []
    for item in raw:
        if isinstance(item, str):
            if len(item) != n or any(ch not in "01" for ch in item):
                raise ValueError(f"target bitstring {item!r} must have length {n} over {{0,1}}")
            value = int(item, 2)
        else:
            value = _as_int(item, "target")
        if value < 0 or value >= dim:
            raise ValueError(f"target {value} outside [0, {dim})")
        out.append(value)
    if len(set(out)) != len(out):
        raise ValueError("targets must be distinct")
    return out


def _apply_basis_state_phase(qc, n, basis_state, angle):
    """Multiply the amplitude of |basis_state> by exp(i*angle), identity on all other basis states."""
    flipped = [k for k in range(n) if ((basis_state >> k) & 1) == 0]
    for k in flipped:
        qc.x(k)
    if n == 1:
        qc.p(angle, 0)
    else:
        qc.mcp(angle, list(range(n - 1)), n - 1)
    for k in flipped:
        qc.x(k)


def _target_phase_oracle(qc, n, targets, beta):
    """eq_2: S_t(beta) = I - (1 - e^{+i beta}) |t><t|, one oracle query (phase e^{i beta} on each target)."""
    for t in targets:
        _apply_basis_state_phase(qc, n, t, beta)


def _reflection_about_s(qc, n, alpha):
    """eq_2: S_s(alpha) = A S_0(alpha) A^dag with A = H^{(x) n}; S_0 puts e^{-i alpha} on |0..0>."""
    qc.h(list(range(n)))  # A^dag = A for Hadamards
    _apply_basis_state_phase(qc, n, 0, -alpha)
    qc.h(list(range(n)))  # A


def build_circuit(instance):
    """Build the fixed-point amplitude-amplification unitary S_L * A for the given instance.

    instance keys:
      n        : number of system qubits (1..12)
      targets  : list of marked basis states (ints or bitstrings)
      L        : odd number of oracle queries, L = 2 l + 1 >= 1
      delta    : failure-probability bound parameter, 0 < delta < 1 (failure <= delta^2 for lambda >= 1-gamma^2)
      apply_state_preparation (optional bool, default True): prepend A = H^{(x) n} to |0..0>
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n", "targets", "L", "delta"):
        if key not in instance:
            raise ValueError(f"missing instance key {key!r}")
    n = _as_int(instance["n"], "n")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError(f"n must be in [1, {MAX_QUBITS}], got {n}")
    num_queries = _as_int(instance["L"], "L")
    if num_queries < 1 or num_queries % 2 == 0:
        raise ValueError(f"L must be an odd positive integer, got {num_queries}")
    delta = instance["delta"]
    if isinstance(delta, bool) or not isinstance(delta, (int, float)) or not (0.0 < float(delta) < 1.0):
        raise ValueError(f"delta must be a real number in (0, 1), got {delta!r}")
    delta = float(delta)
    prep = instance.get("apply_state_preparation", True)
    if not isinstance(prep, bool):
        raise ValueError("apply_state_preparation must be a bool")
    targets = _parse_targets(instance["targets"], n)

    alphas, betas = _fixed_point_phases(num_queries, delta)  # eq_3 / eq_6

    sys = QuantumRegister(n, "sys")
    qc = QuantumCircuit(sys, name=f"fixed_point_AA_L{num_queries}")

    if prep:
        # eq_1: |s> = A|0..0> with A = H^{(x) n}, lambda = |targets| / 2^n
        qc.h(list(range(n)))

    # eq_3: S_L = G(alpha_l, beta_l) ... G(alpha_1, beta_1); G(alpha, beta) = S_s(alpha) S_t(beta)
    for j in range(len(alphas)):
        _target_phase_oracle(qc, n, targets, betas[j])
        _reflection_about_s(qc, n, alphas[j])

    return qc
