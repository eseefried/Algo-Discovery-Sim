"""Trotterised continuous-time quantum walk search operator on a periodic honeycomb lattice.

build_circuit(instance) returns the unitary U ~ exp(-i H_w t) for
  H_w = H_0 + epsilon * sum_{j in N(w)} (|w><j| + |j><w|) + mu |w><w|       (eq_3)
  H_0 = -gamma * sum_{cells} sum_{delta} (|m1,m2,A><m1-d1,m2-d2,B| + h.c.)   (eq_1)
encoded on a binary site register idx(m1,m2,sigma) = 2(n m1 + m2) + sigma (eq_6).
No state preparation and no measurement are included (eq_4 / eq_5 measurement left to runner).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import PhaseGate, RXGate

MAX_QUBITS = 12
ALLOWED_KEYS = ("n", "gamma", "epsilon", "mu", "t", "marked_site", "trotter_steps", "trotter_order")


def _check_real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("parameter '%s' must be a real number" % name)
    val = float(value)
    if not math.isfinite(val):
        raise ValueError("parameter '%s' must be finite" % name)
    return val


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("parameter '%s' must be an integer" % name)
    return value


def _site_index(n, m1, m2, sigma):
    # eq_6: idx(m1, m2, sigma) = 2 (n m1 + m2) + sigma, cell coordinates taken mod n
    return 2 * (n * (m1 % n) + (m2 % n)) + sigma


def _bond_list(n, gamma, epsilon, w):
    # eq_1 (hopping -gamma on every A-B bond) + bond part of eq_3 (bonds touching w get -gamma + epsilon)
    bonds = []
    for m1 in range(n):
        for m2 in range(n):
            a = _site_index(n, m1, m2, 0)
            for d1, d2 in ((0, 0), (1, 0), (0, 1)):
                b = _site_index(n, m1 - d1, m2 - d2, 1)
                coeff = -gamma
                if a == w or b == w:
                    coeff += epsilon
                bonds.append((a, b, coeff))
    return bonds


def _apply_two_level_x(qc, qubits, k, l, angle):
    """Apply exp(-i (angle/2) (|k><l| + |l><k|)) exactly on basis states k != l (RX(angle) on the 2-level subspace)."""
    nq = len(qubits)
    diff = [p for p in range(nq) if ((k >> p) & 1) != ((l >> p) & 1)]
    p = diff[0]
    # CX chain maps k -> k', l -> l' with k', l' differing only at bit p (chain is an involution)
    for q in diff[1:]:
        qc.cx(qubits[p], qubits[q])
    kp = (k >> p) & 1
    controls = []
    flips = []
    for q in range(nq):
        if q == p:
            continue
        bit = (k >> q) & 1
        if q in diff:
            bit ^= kp
        controls.append(qubits[q])
        if bit == 0:
            flips.append(qubits[q])
    for f in flips:
        qc.x(f)
    qc.append(RXGate(angle).control(nq - 1), controls + [qubits[p]])
    for f in flips:
        qc.x(f)
    for q in reversed(diff[1:]):
        qc.cx(qubits[p], qubits[q])


def _apply_onsite_phase(qc, qubits, w, angle):
    """Apply exp(i angle |w><w|): a phase on the single computational basis state w (on-site term of eq_3)."""
    nq = len(qubits)
    flips = [qubits[q] for q in range(nq) if ((w >> q) & 1) == 0]
    for f in flips:
        qc.x(f)
    qc.append(PhaseGate(angle).control(nq - 1), [qubits[q] for q in range(nq)])
    for f in flips:
        qc.x(f)


def build_circuit(instance):
    """Return the Trotterised evolution U ~ exp(-i H_w t) (eq_5) on the binary site register."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in instance:
        if key not in ALLOWED_KEYS:
            raise ValueError("unknown parameter '%s'" % str(key))
    for key in ALLOWED_KEYS:
        if key not in instance:
            raise ValueError("missing parameter '%s'" % key)
    n = _check_int(instance["n"], "n")
    if n < 3 or n % 3 != 0:
        raise ValueError("n must be a positive multiple of 3 (Dirac points must be allowed momenta)")
    gamma = _check_real(instance["gamma"], "gamma")
    if gamma <= 0.0:
        raise ValueError("gamma must be positive")
    epsilon = _check_real(instance["epsilon"], "epsilon")
    mu = _check_real(instance["mu"], "mu")
    t = _check_real(instance["t"], "t")
    if t < 0.0:
        raise ValueError("t must be non-negative")
    num_sites = 2 * n * n
    w = _check_int(instance["marked_site"], "marked_site")
    if w < 0 or w >= num_sites:
        raise ValueError("marked_site must lie in [0, 2 n^2)")
    steps = _check_int(instance["trotter_steps"], "trotter_steps")
    if steps < 1:
        raise ValueError("trotter_steps must be >= 1")
    order = _check_int(instance["trotter_order"], "trotter_order")
    if order not in (1, 2):
        raise ValueError("trotter_order must be 1 or 2")
    nq = (num_sites - 1).bit_length()
    if nq > MAX_QUBITS:
        raise ValueError("instance needs %d qubits, exceeding the cap of %d" % (nq, MAX_QUBITS))

    reg = QuantumRegister(nq, "site")
    qc = QuantumCircuit(reg, name="graphene_ctqw_search")
    qubits = list(range(nq))
    bonds = _bond_list(n, gamma, epsilon, w)
    dt = t / steps
    # eq_5: exp(-i H_w t) ~ product of exponentials of the bond terms and the on-site term
    for _ in range(steps):
        if order == 1:
            for a, b, c in bonds:
                _apply_two_level_x(qc, qubits, a, b, 2.0 * c * dt)
            if mu != 0.0:
                _apply_onsite_phase(qc, qubits, w, -mu * dt)
        else:
            for a, b, c in bonds:
                _apply_two_level_x(qc, qubits, a, b, c * dt)
            if mu != 0.0:
                _apply_onsite_phase(qc, qubits, w, -mu * dt)
            for a, b, c in reversed(bonds):
                _apply_two_level_x(qc, qubits, a, b, c * dt)
    return qc
