"""Quantum Particle Automaton (QPA) evolution U(theta)^T for density classification.

Implements eq_3 (one-step unitary U(theta) = S (I x C(theta))) and eq_4 (T repeated steps)
of the specification as a measurement-free unitary circuit on a periodic n-site ring.

Register layout (Qiskit little-endian):
  qubits 0..m-1 : position register, m = ceil(log2 n); site j <-> computational basis |j>
                  (qubit 0 is the least significant bit of j); basis states j >= n are
                  unused ancilla-like states that are permuted among themselves only.
  qubit  m      : coin (internal/velocity) qubit c.

Instance keys: n_sites (int >= 2), theta (real), steps (int >= 1).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    return value


def _as_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _controlled_shift_plus(m, n):
    """Circuit on m+1 qubits (0..m-1 position, m control) implementing, when the control
    is |1>, the cyclic shift |j> -> |j+1 mod n> on the n used sites (the shift S for
    coin branch |0> in eq_3). Unused states j >= n are permuted among themselves."""
    qc = QuantumCircuit(m + 1, name="cshift+1")
    pos = list(range(m))
    ctrl = m
    # Controlled increment modulo 2^m: flip bit k iff control=1 and all lower bits are 1.
    for k in range(m - 1, -1, -1):
        controls = [ctrl] + pos[:k]
        qc.mcx(controls, pos[k])
    # If n < 2^m, redirect the wrap: site n-1 was mapped to |n>; swap |n> <-> |0>
    # (controlled on ctrl) so that n-1 -> 0, giving an exact mod-n cycle on 0..n-1.
    if n < (1 << m):
        ones = [i for i in range(m) if (n >> i) & 1]
        h = ones[-1]
        others = [i for i in ones if i != h]
        # Gray-code conjugation: map |n> -> |2^h>, keep |0> fixed.
        for i in others:
            qc.cx(pos[h], pos[i])
        zero_controls = [pos[i] for i in range(m) if i != h]
        for q in zero_controls:
            qc.x(q)
        qc.mcx([ctrl] + zero_controls, pos[h])
        for q in zero_controls:
            qc.x(q)
        for i in reversed(others):
            qc.cx(pos[h], pos[i])
    return qc


def _qpa_step(qc, pos, coin, theta, shift_plus, shift_minus):
    """One application of U(theta) = S (I_n x C(theta)) (eq_3).
    C(theta) = [[cos t, i sin t],[i sin t, cos t]] = Rx(-2 t)."""
    qc.rx(-2.0 * theta, coin)
    # Coin |0> -> shift +1 (conditioned via X conjugation), coin |1> -> shift -1.
    qubits = list(pos) + [coin]
    qc.x(coin)
    qc.compose(shift_plus, qubits=qubits, inplace=True)
    qc.x(coin)
    qc.compose(shift_minus, qubits=qubits, inplace=True)


def build_circuit(instance):
    """Return the unitary U(theta)^T (eq_4) on the position+coin registers."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n_sites", "theta", "steps"):
        if key not in instance:
            raise ValueError(f"missing instance key {key!r}")
    n = _as_int(instance["n_sites"], "n_sites")
    theta = _as_real(instance["theta"], "theta")
    steps = _as_int(instance["steps"], "steps")
    if n < 2:
        raise ValueError("n_sites must be >= 2")
    if steps < 1:
        raise ValueError("steps must be >= 1")
    m = max(1, math.ceil(math.log2(n)))
    while (1 << m) < n:
        m += 1
    total = m + 1
    if total > MAX_QUBITS:
        raise ValueError(f"instance needs {total} qubits, exceeding the cap of {MAX_QUBITS}")
    position = QuantumRegister(m, "pos")
    coin_reg = QuantumRegister(1, "coin")
    qc = QuantumCircuit(position, coin_reg, name=f"QPA_U^{steps}")
    pos = [position[i] for i in range(m)]
    coin = coin_reg[0]
    shift_plus = _controlled_shift_plus(m, n)
    shift_minus = shift_plus.inverse()
    # eq_4: |psi_T> = U(theta)^T |psi_0>
    for _ in range(steps):
        _qpa_step(qc, pos, coin, theta, shift_plus, shift_minus)
    return qc
