from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(obj, key):
    if not isinstance(obj, dict) or key not in obj:
        raise ValueError('missing parameter: ' + key)
    v = obj[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError('parameter must be a real number: ' + key)
    v = float(v)
    if not math.isfinite(v):
        raise ValueError('parameter must be finite: ' + key)
    return v


def _unitary(instance, name):
    p = instance.get(name)
    if not isinstance(p, dict):
        raise ValueError('missing unitary spec: ' + name)
    th = _num(p, 'theta')
    ph = _num(p, 'phi')
    lam = _num(p, 'lam')
    gamma = _num(p, 'gamma') if 'gamma' in p else 0.0
    return th, ph, lam, gamma


def build_circuit(instance):
    """Dilation circuit: qubit 0 = system s, qubit 1 = probe p (starts in |0>).

    instance: {"a": float, "b": float, "V": {theta, phi, lam[, gamma]},
               "U0": {...}, "U1": {...}}
    Each unitary is exp(i*gamma) * U(theta, phi, lam) (Qiskit U gate).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    a = _num(instance, 'a')
    b = _num(instance, 'b')
    if not (0.0 <= a <= 1.0) or not (0.0 <= b <= 1.0):
        raise ValueError('a and b must lie in [0, 1]')
    v_par = _unitary(instance, 'V')
    u0_par = _unitary(instance, 'U0')
    u1_par = _unitary(instance, 'U1')

    # eq_2: cos(theta_z/2) = singular value, theta in [0, pi]
    theta0 = 2.0 * math.acos(a)
    theta1 = 2.0 * math.acos(b)

    s = QuantumRegister(1, 's')
    p = QuantumRegister(1, 'p')
    qc = QuantumCircuit(s, p)

    # eq_1 / eq_4: pre-rotation V on the system
    qc.u(v_par[0], v_par[1], v_par[2], s[0])
    qc.global_phase += v_par[3]

    # eq_4: C = sum_z |z><z| (x) RY(theta_z) on probe
    qc.x(s[0])
    qc.cry(theta0, s[0], p[0])
    qc.x(s[0])
    qc.cry(theta1, s[0], p[0])

    # eq_4: U_k on the system controlled on probe = k
    qc.x(p[0])
    qc.cu(u0_par[0], u0_par[1], u0_par[2], u0_par[3], p[0], s[0])
    qc.x(p[0])
    qc.cu(u1_par[0], u1_par[1], u1_par[2], u1_par[3], p[0], s[0])
    return qc
