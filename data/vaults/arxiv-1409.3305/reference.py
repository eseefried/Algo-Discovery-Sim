"""Reference: fixed-point search with optimal query complexity (Yoder, Low & Chuang,
arXiv:1409.3305, Eqs. 13-14).

A sequence of l generalized Grover iterates, S_L = prod_j G(alpha_j, beta_j) with L = 2l+1,
where G(alpha, beta) = -S_s(alpha) S_t(beta) uses *partial* reflections rather than the
inversions of ordinary Grover. The phases are not free parameters: they are

    alpha_j = -beta_{l-j+1} = 2 arccot( tan(2 pi j / L) sqrt(1 - gamma^2) ),
    1/gamma = T_{1/L}(1/delta),

which makes the sequence realise a Dolph-Chebyshev response and gives
P_L = 1 - delta^2 T_L(T_{1/L}(1/delta) sqrt(1-lambda))^2 >= 1 - delta^2 for every lambda above
1 - gamma^2. The palindromic phase matching alpha_j = -beta_{l-j+1} is what makes it work;
delta = 1 collapses the phases to +-pi and recovers ordinary Grover.
"""

import numpy as np
from qiskit import QuantumCircuit

from a2m_task import oracle


def _phases(big_l, delta):
    """The alpha_j of Eq. 14, and beta_k = -alpha_{l-k+1}."""
    l = (big_l - 1) // 2
    gamma = 1.0 / np.cosh(np.arccosh(1.0 / delta) / big_l)
    root = np.sqrt(1.0 - gamma * gamma)
    alpha = [2.0 * np.arctan2(1.0, np.tan(2 * np.pi * j / big_l) * root)
             for j in range(1, l + 1)]
    beta = [-alpha[l - 1 - k] for k in range(l)]
    return alpha, beta


def _reflect_about_s(qc, qubits, alpha):
    """S_s(alpha) = I - (1 - e^{-i alpha})|s><s|, conjugating a phase on |0...0> by H^n."""
    qc.h(qubits)
    qc.x(qubits)
    if len(qubits) == 1:
        qc.p(-alpha, qubits[0])
    else:
        qc.mcp(-alpha, qubits[:-1], qubits[-1])
    qc.x(qubits)
    qc.h(qubits)


def build_circuits(spec):
    n, big_l, delta = spec["n"], spec["L"], spec["delta"]
    alpha, beta = _phases(big_l, delta)
    qubits = list(range(n))

    qc = QuantumCircuit(n)
    qc.h(qubits)                                   # |s>: the uniform superposition
    for j in range(len(alpha)):
        qc.append(oracle(n, beta[j]), qubits)      # S_t(beta_j): partial phase on the targets
        _reflect_about_s(qc, qubits, alpha[j])     # S_s(alpha_j): partial reflection about |s>
    return [qc]
