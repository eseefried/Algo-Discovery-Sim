"""Exact derivative-based Bernstein-Vazirani step over F_2 for learning a
multilinear polynomial (one set S, one level of the recursion).

Register layout (n variable qubits + 1 target qubit, n <= 11):
  qubit i-1 (0 <= i-1 <= n-1) : variable x_i, i = 1..n (1-indexed in the instance)
  qubit n                     : target qubit of the additive oracle O_p

Instance keys:
  n                : number of variables (int, 1..11)
  S                : list of distinct variable indices in 1..n, |S| <= n-1 (eq_3)
  monomials        : list of monomials M (lists of distinct indices) with c_M = 1 (eq_1)
  known_monomials  : (optional) subset of 'monomials' of degree > |S|+1 whose coefficients
                     are already learned; their contribution is removed by a phase
                     correction so the effective polynomial has degree <= |S|+1.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _index_list(lst, n, name):
    """Validate a list of distinct variable indices in 1..n; return it sorted."""
    if not isinstance(lst, list):
        raise ValueError(f"{name} must be a list")
    out = []
    for i in lst:
        _check_int(i, f"entry of {name}")
        if i < 1 or i > n:
            raise ValueError(f"index {i} in {name} out of range 1..{n}")
        out.append(i)
    if len(set(out)) != len(out):
        raise ValueError(f"{name} contains repeated indices")
    return sorted(out)


def _apply_oracle(qc, monomials, var_qubits, target):
    """Additive oracle O_p |x>|b> = |x>|b + p(x) mod 2>  (eq_1, eq_2).

    Each monomial prod_{i in M} x_i with c_M = 1 is a multi-controlled X from the
    qubits of M onto the target; the constant monomial is a plain X.
    """
    for mono in monomials:
        if len(mono) == 0:
            qc.x(target)
        else:
            qc.mcx([var_qubits[i - 1] for i in mono], target)


def _apply_known_phase(qc, known, var_qubits):
    """Phase correction omega^{-p_{>k}(x)} = (-1)^{p_known(x)} for q = 2 (eq_6 assumption,
    step 1 of the specification): the already-learned higher-degree part is removed in
    superposition by multi-controlled phase gates, costing no oracle query."""
    for mono in known:
        qs = [var_qubits[i - 1] for i in mono]
        if len(qs) == 0:
            continue  # constant term would only be a global phase
        if len(qs) == 1:
            qc.p(math.pi, qs[0])
        else:
            qc.mcp(math.pi, qs[:-1], qs[-1])


def build_circuit(instance):
    """Build the derivative-step circuit D_S followed by the exact BV read-out."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _check_int(instance.get("n"), "n")
    if n < 1 or n + 1 > MAX_QUBITS:
        raise ValueError(f"n must satisfy 1 <= n <= {MAX_QUBITS - 1}")
    s_set = _index_list(instance.get("S"), n, "S")
    if len(s_set) > n - 1:
        raise ValueError("S must leave at least one free variable (|S| <= n-1)")
    level_degree = len(s_set) + 1  # k = |S| + 1 : degree being learned (eq_3)

    raw_monos = instance.get("monomials")
    if not isinstance(raw_monos, list):
        raise ValueError("monomials must be a list of index lists")
    monomials = [_index_list(m, n, "monomial") for m in raw_monos]
    if len(set(tuple(m) for m in monomials)) != len(monomials):
        raise ValueError("monomials must be distinct (coefficients live in F_2)")

    raw_known = instance.get("known_monomials", [])
    if not isinstance(raw_known, list):
        raise ValueError("known_monomials must be a list of index lists")
    known = [_index_list(m, n, "known monomial") for m in raw_known]
    known_keys = set(tuple(m) for m in known)
    if len(known_keys) != len(known):
        raise ValueError("known_monomials must be distinct")
    mono_keys = set(tuple(m) for m in monomials)
    for m in known:
        if len(m) <= level_degree:
            raise ValueError("known_monomials must have degree > |S|+1")
        if tuple(m) not in mono_keys:
            raise ValueError("known_monomials must be monomials of p with coefficient 1")
    for m in monomials:
        if len(m) > level_degree and tuple(m) not in known_keys:
            raise ValueError(
                "every monomial of degree > |S|+1 must be listed in known_monomials "
                "so that the effective polynomial has degree <= |S|+1 (eq_3)"
            )

    var = QuantumRegister(n, "x")
    tgt = QuantumRegister(1, "t")
    qc = QuantumCircuit(var, tgt, name="derivative_BV_step")
    var_qubits = [var[i] for i in range(n)]
    target = tgt[0]
    s_qubits = [var_qubits[i - 1] for i in s_set]
    free_qubits = [var_qubits[i - 1] for i in range(1, n + 1) if i not in s_set]

    # Prepare target in |psi_1> = |-> for phase kickback (eq_2) and the uniform
    # superposition over y on the free qubits, F_2 = H (eq_4); S qubits stay |0>.
    qc.x(target)
    qc.h(target)
    for qb in free_qubits:
        qc.h(qb)

    # Finite difference D_S p(y) = sum_{A subset S} p(1_A + y)  (eq_3; signs are + in F_2):
    # 2^{|S|} oracle calls, one per subset A, each sandwiched by the shift 1_A.
    num_s = len(s_qubits)
    for mask in range(2 ** num_s):
        shift = [s_qubits[j] for j in range(num_s) if (mask >> j) & 1]
        for qb in shift:
            qc.x(qb)
        _apply_oracle(qc, monomials, var_qubits, target)  # phase (-1)^{p(1_A + y)}
        _apply_known_phase(qc, known, var_qubits)  # remove known higher-degree part
        for qb in shift:
            qc.x(qb)

    # Exact Bernstein-Vazirani read-out: F_2^{-1} = H on the free qubits maps
    # (-1)^{c_S + a.y} superposition to |a>, a_i = c_{S u {i}}  (eq_4).
    for qb in free_qubits:
        qc.h(qb)
    # Return the target to |0> (uncompute the |-> preparation).
    qc.h(target)
    qc.x(target)
    return qc
