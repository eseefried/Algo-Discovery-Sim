from qiskit import QuantumCircuit, QuantumRegister
import math


def _real(instance, key, lo, hi, default):
    value = instance.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(key + ' must be a real number')
    value = float(value)
    if not math.isfinite(value) or value < lo or value > hi:
        raise ValueError(key + ' out of range')
    return value


def build_circuit(instance):
    """Noisy first-order Trotter circuit for H = Z0 Z1 + g (X0 + X1).

    Parameters: g (real), t (>0), n (positive int Trotter number), eps (real
    coherent over-rotation added to every elementary gate angle).
    Each step: RZZ(2t/n + eps) on (0,1), then RX(2gt/n + eps) on qubit 0 and 1.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    g = _real(instance, 'g', -100.0, 100.0, 1.0)
    t = _real(instance, 't', 0.0, 100.0, 1.0)
    if t <= 0.0:
        raise ValueError('t must be positive')
    eps = _real(instance, 'eps', -1.0, 1.0, 0.0)
    n = instance.get('n', 1)
    if isinstance(n, bool) or not isinstance(n, int):
        if isinstance(n, float) and n.is_integer():
            n = int(n)
        else:
            raise ValueError('n must be an integer')
    if n < 1 or n > 5000:
        raise ValueError('n must be in 1..5000')
    qr = QuantumRegister(2, 'sys')
    qc = QuantumCircuit(qr)
    theta_zz = 2.0 * t / n + eps  # eq_1: R_ZZ(2t/n) with over-rotation
    theta_x = 2.0 * g * t / n + eps  # eq_1: R_X(2gt/n) with over-rotation
    for _ in range(n):
        qc.rzz(theta_zz, qr[0], qr[1])
        qc.rx(theta_x, qr[0])
        qc.rx(theta_x, qr[1])
    return qc
