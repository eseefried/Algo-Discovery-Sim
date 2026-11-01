'''Fixed-point amplitude amplification (Yoder-Low-Chuang phases), 1-qubit A.'''
import math
from qiskit import QuantumCircuit


def _phases(d, eps):
    # eq_3: alpha_j = 2 arccot(tan(2 pi j / L) sqrt(1 - gamma^2)), gamma = 1/T_{1/L}(1/delta)
    L = 2 * d + 1
    delta = math.sqrt(eps)
    inv_gamma = math.cosh(math.acosh(1.0 / delta) / L)
    gamma = 1.0 / inv_gamma
    root = math.sqrt(max(0.0, 1.0 - gamma * gamma))
    alphas = []
    for j in range(1, d + 1):
        x = math.tan(2.0 * math.pi * j / L) * root
        alphas.append(2.0 * math.atan2(1.0, x))
    # beta_j = -alpha_{d-j+1}
    betas = [-alphas[d - j] for j in range(1, d + 1)]
    return alphas, betas


def _start_reflection(qc, theta, alpha):
    # eq_1: S_s(alpha) = A S_0(alpha) A^dagger, S_0(alpha) = diag(e^{i alpha}, 1) = X P(alpha) X
    qc.ry(-2.0 * theta, 0)
    qc.x(0)
    qc.p(alpha, 0)
    qc.x(0)
    qc.ry(2.0 * theta, 0)


def build_circuit(instance):
    try:
        lam = float(instance['lambda'])
        eps = float(instance['epsilon'])
        d_raw = float(instance['d'])
    except (KeyError, TypeError, ValueError):
        raise ValueError('instance needs numeric lambda, epsilon, d')
    if not (math.isfinite(lam) and math.isfinite(eps) and math.isfinite(d_raw)):
        raise ValueError('parameters must be finite')
    if not (0.0 < lam <= 1.0):
        raise ValueError('lambda must be in (0,1]')
    if not (1e-12 <= eps < 1.0):
        raise ValueError('epsilon must be in [1e-12,1)')
    if d_raw != int(d_raw) or d_raw < 1 or d_raw > 500:
        raise ValueError('d must be an integer in [1,500]')
    d = int(d_raw)
    theta = math.asin(math.sqrt(lam))
    alphas, betas = _phases(d, eps)
    qc = QuantumCircuit(1)
    # A|0> = sqrt(1-lambda)|0> + sqrt(lambda)|1>
    qc.ry(2.0 * theta, 0)
    for j in range(d):
        # eq_1/eq_2: target reflection S_t(beta_j) = diag(1, e^{i beta_j}), one oracle query
        qc.p(betas[j], 0)
        # eq_1/eq_2: start reflection S_s(alpha_j)
        _start_reflection(qc, theta, alphas[j])
    return qc
