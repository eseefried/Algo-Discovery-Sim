"""Second-order Trotter-Suzuki simulation of the discretized 1D quantum harmonic oscillator.

Operation implemented (eq_3 of the specification):
    exp(-i H_N t) ~= ( exp(-i X^2 d/4) F_c^dag exp(-i X^2 d/2) F_c exp(-i X^2 d/4) )^r,  d = t / r,
with H_N = (X^2 + P^2)/2, P = F_c^dag X F_c (eq_2), on an n-qubit register holding a
wavefunction on the symmetric Fourier grid x_j = (j - N/2) * sqrt(2 pi / N), N = 2^n.

Qubit layout: a single register ``pos`` of n qubits; qubit a (Qiskit index a, 0 = least
significant) holds the bit of weight 2^a of the grid label j in 0..N-1.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12
MAX_TROTTER_STEPS = 4096


def _validate_instance(instance):
    """Validate and unpack the instance dictionary. Returns (n, t, r, include_frft_phase)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "n" not in instance or "t" not in instance or "r" not in instance:
        raise ValueError("instance must contain keys 'n', 't' and 'r'")
    n = instance["n"]
    t = instance["t"]
    r = instance["r"]
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > MAX_QUBITS:
        raise ValueError("n must satisfy 1 <= n <= %d" % MAX_QUBITS)
    if isinstance(r, bool) or not isinstance(r, int):
        raise ValueError("r must be an integer")
    if r < 1 or r > MAX_TROTTER_STEPS:
        raise ValueError("r must satisfy 1 <= r <= %d" % MAX_TROTTER_STEPS)
    if isinstance(t, bool) or not isinstance(t, (int, float)):
        raise ValueError("t must be a real number")
    t = float(t)
    if not math.isfinite(t):
        raise ValueError("t must be finite")
    include_frft_phase = instance.get("include_frft_phase", False)
    if not isinstance(include_frft_phase, bool):
        raise ValueError("include_frft_phase must be a boolean")
    return n, t, r, include_frft_phase


def _apply_quadratic_phase(qc, qubits, theta, n):
    """Apply exp(-i theta X^2) = sum_j exp(-i theta dx^2 (j - N/2)^2) |j><j|  (eq_4, eq_2).

    Expanding (j - N/2)^2 = sum_a j_a (4^a - N 2^a) + sum_{a<b} j_a j_b 2^(a+b+1) + N^2/4
    (using j_a^2 = j_a) gives single-qubit phases, pairwise controlled phases and a
    global phase. The grid spacing is dx^2 = 2 pi / N.
    """
    big_n = 2 ** n
    dx2 = 2.0 * math.pi / big_n
    c = -theta * dx2
    for a in range(n):
        qc.p(c * (4 ** a - big_n * 2 ** a), qubits[a])
    for a in range(n):
        for b in range(a + 1, n):
            qc.cp(c * 2 ** (a + b + 1), qubits[a], qubits[b])
    qc.global_phase += c * (big_n * big_n / 4.0)


def _apply_centered_qft(qc, qubits, n, inverse):
    """Apply the centered DFT F_c (or its inverse) of eq_2.

    (F_c)_{kj} = N^(-1/2) exp(2 pi i (j - N/2)(k - N/2)/N)
               = exp(i pi N/2) (-1)^k (QFT)_{kj} (-1)^j,
    and (-1)^j = (-1)^{j_0} is a Z gate on the least significant qubit. Hence
    F_c = exp(i pi N/2) Z_0 QFT Z_0 and F_c^dag = exp(-i pi N/2) Z_0 QFT^dag Z_0.
    """
    big_n = 2 ** n
    gate = QFTGate(n)
    if inverse:
        gate = gate.inverse()
    qc.z(qubits[0])
    qc.append(gate, qubits)
    qc.z(qubits[0])
    if inverse:
        qc.global_phase += -math.pi * big_n / 2.0
    else:
        qc.global_phase += math.pi * big_n / 2.0


def build_circuit(instance):
    """Build the r-step second-order Trotter-Suzuki circuit for exp(-i H_N t) (eq_3).

    instance keys:
        n (int): number of qubits, 1 <= n <= 12 (N = 2^n grid points)
        t (float): total evolution time
        r (int): number of Trotter steps
        include_frft_phase (bool, optional): if True, add the global phase exp(i t/2) so the
            circuit approximates the fractional Fourier transform of angle alpha = t (eq_6).
    """
    n, t, r, include_frft_phase = _validate_instance(instance)
    pos = QuantumRegister(n, "pos")
    qc = QuantumCircuit(pos, name="qho_trotter2")
    qubits = list(range(n))
    delta = t / r
    for _ in range(r):
        # eq_3: symmetric Strang step  e^{-iX^2 d/4} e^{-iP^2 d/2} e^{-iX^2 d/4}
        _apply_quadratic_phase(qc, qubits, delta / 4.0, n)
        _apply_centered_qft(qc, qubits, n, False)          # F_c
        _apply_quadratic_phase(qc, qubits, delta / 2.0, n)  # e^{-iX^2 d/2} in momentum basis
        _apply_centered_qft(qc, qubits, n, True)           # F_c^dag  -> e^{-iP^2 d/2}
        _apply_quadratic_phase(qc, qubits, delta / 4.0, n)
    if include_frft_phase:
        # eq_6: F_alpha = exp(i alpha/2) exp(-i alpha H), alpha = t
        qc.global_phase += t / 2.0
    return qc
