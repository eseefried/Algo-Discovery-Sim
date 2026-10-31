"""Coinless (tessellation / staggered) discrete-time quantum walk on a cycle.

Sites x in Z_N with N = 2**n are encoded as the n-bit integer x on the site
register (Qiskit convention: qubit 0 is the least significant bit).  There is
no coin register (eq_1).  One walk step is U = U_1 U_0 (eq_3) where each U_j is
the reflection 2 P_j - I about the span of its two-site polygon states (eq_2).
build_circuit returns the operation U**t only (no state preparation, no
measurement).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12
MAX_STEPS = 1000


def _as_angle(instance, key):
    """Fetch a finite real angle from the instance dictionary."""
    if key not in instance:
        raise ValueError("instance is missing required key '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("'%s' must be a real number" % key)
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("'%s' must be finite" % key)
    return value


def _as_int(instance, key, lower, upper):
    """Fetch an integer in [lower, upper] from the instance dictionary."""
    if key not in instance:
        raise ValueError("instance is missing required key '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("'%s' must be an integer" % key)
    if value < lower or value > upper:
        raise ValueError("'%s' must lie in [%d, %d]" % (key, lower, upper))
    return value


def _polygon_reflection(qc, qubit, theta, phi):
    """Apply 2|alpha><alpha| - I on one qubit (eq_2, eq_3, eq_7).

    |alpha> = cos(theta/2)|0> + exp(i phi) sin(theta/2)|1> = U(theta,phi,0)|0>,
    hence 2|alpha><alpha| - I = R Z R^dagger with R = U(theta, phi, 0) and
    R^dagger = U(-theta, 0, -phi).  Because every tessellation-0 polygon
    {2k, 2k+1} differs only in the least significant bit, acting with this
    single-qubit reflection on qubit 0 implements U_0 = sum_k (2|alpha_k><alpha_k|)
    - I on all polygons simultaneously; in the relabelled picture of eq_7 this
    is exactly I_{N/2} (x) C_0 with the LSB playing the role of the coin.
    """
    qc.u(-theta, 0.0, -phi, qubit)  # R^dagger
    qc.z(qubit)                     # 2|0><0| - I
    qc.u(theta, phi, 0.0, qubit)    # R


def _cyclic_shift(qc, qubits, sign):
    """Apply S^sign, S|x> = |x + 1 mod N>, via QFT, phases, inverse QFT.

    QFTGate maps |x> -> N^{-1/2} sum_k exp(2 pi i x k / N)|k> with qubit 0 as
    the least significant bit of k, so the phase exp(2 pi i sign * k / N)
    factorises into p(sign * 2 pi 2^j / N) on qubit j.
    """
    n = len(qubits)
    big_n = 2 ** n
    qc.append(QFTGate(n), qubits)
    for j, q in enumerate(qubits):
        qc.p(sign * 2.0 * math.pi * (2 ** j) / big_n, q)
    qc.append(QFTGate(n).inverse(), qubits)


def _walk_step(qc, qubits, theta, phi, theta_p, phi_p):
    """One coinless step U = U_1 U_0 (eq_3).

    U_0 acts on polygons {2k, 2k+1}: single-qubit reflection on the LSB.
    U_1 acts on polygons {2k+1, 2k+2 mod N} = S{2k, 2k+1}; since
    S^dagger|beta_k> = cos(theta'/2)|2k> + exp(i phi') sin(theta'/2)|2k+1>,
    we have U_1 = S U_0(theta', phi') S^dagger.
    """
    lsb = qubits[0]
    # U_0
    _polygon_reflection(qc, lsb, theta, phi)
    # U_1 = S U_0' S^dagger  (apply S^dagger, then U_0', then S)
    _cyclic_shift(qc, qubits, -1.0)
    _polygon_reflection(qc, lsb, theta_p, phi_p)
    _cyclic_shift(qc, qubits, 1.0)


def build_circuit(instance):
    """Build the coinless walk operator U**t on a cycle of N = 2**num_qubits sites.

    instance keys:
      num_qubits  : int, 1..12, site register size (N = 2**num_qubits, eq_1)
      steps       : int, 0..1000, number of walk steps t (eq_4)
      theta, phi  : real, polygon-state parameters of tessellation 0 (eq_2)
      theta_prime, phi_prime : real, parameters of tessellation 1 (eq_2)
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dictionary")
    n = _as_int(instance, "num_qubits", 1, MAX_QUBITS)
    steps = _as_int(instance, "steps", 0, MAX_STEPS)
    theta = _as_angle(instance, "theta")
    phi = _as_angle(instance, "phi")
    theta_p = _as_angle(instance, "theta_prime")
    phi_p = _as_angle(instance, "phi_prime")

    # eq_1: the whole Hilbert space is the site register, no coin factor.
    site = QuantumRegister(n, "site")
    qc = QuantumCircuit(site, name="coinless_walk")
    qubits = list(range(n))

    # eq_4: |psi(t)> = U**t |psi(0)>  (the operator part only)
    for _ in range(steps):
        _walk_step(qc, qubits, theta, phi, theta_p, phi_p)
    return qc
