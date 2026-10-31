"""Ancilla-indicator decomposition of a diagonal operator with k distinct phases.

Construction (specification eq_1-eq_3):
  D = sum_j e^{i theta_j} Pi_j = prod_j exp(i theta_j Pi_j)
Each factor exp(i theta_j Pi_j) is realised as
  O_j^dagger (I (x) P(theta_j)) O_j,
where O_j XORs the Boolean indicator f_j(x) of the phase class S_j into a clean
ancilla.  Restricted to ancilla |0> the product equals D (x) I exactly.

Qubit layout: data qubits 0..n-1 (qubit 0 = least significant bit of the basis
label x), ancilla at index n.

The single-qubit phase gate is applied exactly (qc.p); the Clifford+T
approximation of eq_4 is NOT performed here (see specification_changes).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

_TWO_PI = 2.0 * math.pi
_MAX_QUBITS = 12
_ROUND_DIGITS = 10


def _validate_instance(instance):
    """Validate the instance dictionary and return (n, phases, epsilon)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("num_qubits")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("num_qubits must be a positive integer")
    if n + 1 > _MAX_QUBITS:
        raise ValueError("num_qubits + 1 ancilla exceeds the qubit cap of 12")
    phases = instance.get("phases")
    if not isinstance(phases, (list, tuple)) or len(phases) != 2 ** n:
        raise ValueError("phases must be a list of length 2**num_qubits")
    clean = []
    for value in phases:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("phases must be real numbers")
        f = float(value)
        if not math.isfinite(f):
            raise ValueError("phases must be finite")
        clean.append(f)
    eps = instance.get("epsilon")
    if eps is not None:
        if isinstance(eps, bool) or not isinstance(eps, (int, float)):
            raise ValueError("epsilon must be a real number in (0, 1)")
        eps = float(eps)
        if not (0.0 < eps < 1.0):
            raise ValueError("epsilon must lie in the open interval (0, 1)")
    return n, clean, eps


def _group_phases(phases):
    """eq_1: regroup the diagonal by its k distinct phase values.

    Returns an ordered list of (theta_j, S_j) with S_j the list of basis labels
    x whose phase equals theta_j (mod 2 pi).  theta_j is reduced to [0, 2 pi).
    """
    classes = {}
    order = []
    for x, theta in enumerate(phases):
        reduced = math.fmod(theta, _TWO_PI)
        if reduced < 0.0:
            reduced += _TWO_PI
        key = round(reduced / _TWO_PI, _ROUND_DIGITS)
        if key >= 1.0:
            key = 0.0
        if key not in classes:
            classes[key] = []
            order.append(key)
        classes[key].append(x)
    return [(key * _TWO_PI, classes[key]) for key in order]


def _apply_indicator(qc, data, anc, n, members):
    """eq_3: reversible network O_j with O_j|x>|a> = |x>|a XOR f_j(x)>.

    f_j is the OR of the minterms of S_j; since minterms are pairwise disjoint
    the XOR of the minterm flips equals the OR.  Each minterm is an
    X-conjugated multi-controlled-X on all n data qubits.  O_j is self-inverse,
    so the same routine performs the uncomputation O_j^dagger.
    """
    if len(members) == 2 ** n:
        # Indicator is identically 1: a single X suffices (constant function).
        qc.x(anc)
        return
    controls = [data[i] for i in range(n)]
    for x in members:
        zero_bits = [i for i in range(n) if not ((x >> i) & 1)]
        for i in zero_bits:
            qc.x(data[i])
        if n == 1:
            qc.cx(controls[0], anc)
        elif n == 2:
            qc.ccx(controls[0], controls[1], anc)
        else:
            qc.mcx(controls, anc)
        for i in zero_bits:
            qc.x(data[i])


def build_circuit(instance):
    """Return the unitary circuit realising D (x) I on data (x) ancilla |0>.

    instance keys:
      num_qubits : n >= 1 with n + 1 <= 12
      phases     : list of 2**n real angles theta(x), x little-endian
      epsilon    : optional target precision in (0, 1); validated only, since
                   rotations are applied exactly in this module (eq_4/eq_5
                   budget epsilon/k is not consumed by any synthesis step).
    """
    n, phases, _eps = _validate_instance(instance)
    data = QuantumRegister(n, "data")
    anc_reg = QuantumRegister(1, "anc")
    qc = QuantumCircuit(data, anc_reg, name="diag_k_phases")
    anc = anc_reg[0]

    # eq_2: D = prod_j exp(i theta_j Pi_j); factors with theta_j = 0 are the
    # identity and are skipped, so at most k (and at least k-1) rotations occur.
    for theta_j, members in _group_phases(phases):
        if theta_j == 0.0:
            continue
        # eq_3: U_j = O_j^dagger (I (x) P(theta_j)) O_j
        _apply_indicator(qc, data, anc, n, members)   # O_j
        qc.p(theta_j, anc)                            # P(theta_j) = diag(1, e^{i theta_j})
        _apply_indicator(qc, data, anc, n, members)   # O_j^dagger (self-inverse)
    return qc
