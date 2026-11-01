"""Split-step Strang Trotter circuit for the 1D quantum harmonic oscillator on a 2^n grid."""
import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _diag(qc, n, theta):
    # Applies exp(-i*theta*s^2) up to global phase, where s=(j-N/2) and
    # s = -(1/2 + sum_i 2^(i-1) z_i), so s^2 = const + sum a_i z_i + 2 sum_{i<k} a_i a_k z_i z_k.
    for i in range(n):
        qc.rz(2.0 * theta * 2.0 ** (i - 1), i)
    for i in range(n):
        for k in range(i + 1, n):
            qc.rzz(4.0 * theta * 2.0 ** (i - 1) * 2.0 ** (k - 1), i, k)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    t = instance.get("t")
    r = instance.get("r")
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 12:
        raise ValueError("n must be an integer in [2, 12]")
    if isinstance(r, bool) or not isinstance(r, int) or r < 1 or r > 1000:
        raise ValueError("r must be an integer in [1, 1000]")
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t):
        raise ValueError("t must be a finite real number")
    t = float(t)
    N = 2 ** n
    dt = t / r
    c = 2.0 * math.pi / N  # dx^2
    qr = QuantumRegister(n, "pos")
    qc = QuantumCircuit(qr)
    idx = list(range(n))
    # first potential half step exp(-i V dt/2), V=x^2/2 -> theta = dt*dx^2/4
    _diag(qc, n, dt * c / 4.0)
    for s in range(r):
        # kinetic step: centered DFT = Z0 . QFT . Z0; the inner Z0 factors commute with the diagonal and cancel
        qc.z(0)
        qc.append(QFTGate(n), idx)
        _diag(qc, n, dt * c / 2.0)  # exp(-i p^2 dt/2), p_k=(k-N/2)dx
        qc.append(QFTGate(n).inverse(), idx)
        qc.z(0)
        # potential: full step merged between repetitions, half step at the end
        _diag(qc, n, dt * c / 4.0 if s == r - 1 else dt * c / 2.0)
    return qc
