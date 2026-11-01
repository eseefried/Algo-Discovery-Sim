import math
from qiskit import QuantumCircuit, QuantumRegister


def _nonneg(instance, key):
    if key not in instance:
        raise ValueError('missing key: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    f = float(v)
    if not math.isfinite(f) or f < 0.0:
        raise ValueError(key + ' must be finite and >= 0')
    return f


def build_circuit(instance):
    """System qubit 0; slice k uses ancillas 1+2k (damping) and 2+2k (dephasing).

    Generator (eq_1): L = gamma*(s- rho s+ - 1/2{s+ s-, rho}) + kappa*(Z rho Z - rho).
    Gates implement T_t = (e^{(t/r)L_a} e^{(t/r)L_d})^r (eq_4), each factor a dilation (eq_5).
    Ancillas are fresh per slice (no reset), so the circuit is unitary.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    gamma = _nonneg(instance, 'gamma')
    kappa = _nonneg(instance, 'kappa')
    t = _nonneg(instance, 't')
    r = instance.get('r')
    if isinstance(r, bool) or not isinstance(r, int) or r < 1:
        raise ValueError('r must be a positive integer')
    if 1 + 2 * r > 12:
        raise ValueError('total qubits 1+2r must be <= 12')
    s = t / r
    # amplitude damping: excited population decays by exp(-gamma*s)
    q_a = min(1.0, max(0.0, 1.0 - math.exp(-gamma * s)))
    theta_a = 2.0 * math.asin(math.sqrt(q_a))
    # dephasing: rho -> (1-p) rho + p Z rho Z, p=(1-exp(-2 kappa s))/2
    p = min(0.5, max(0.0, 0.5 * (1.0 - math.exp(-2.0 * kappa * s))))
    theta_p = 2.0 * math.asin(math.sqrt(p))
    qs = QuantumRegister(1, 'S')
    qa = QuantumRegister(2 * r, 'A')
    qc = QuantumCircuit(qs, qa)
    for k in range(r):
        anc_d = 1 + 2 * k
        anc_p = 2 + 2 * k
        # amplitude damping dilation: K0=|0><0|+cos|1><1|, K1=sin|0><1|
        qc.cry(theta_a, 0, anc_d)
        qc.cx(anc_d, 0)
        # dephasing dilation: K0=sqrt(1-p) I, K1=sqrt(p) Z
        qc.ry(theta_p, anc_p)
        qc.cz(anc_p, 0)
    return qc
