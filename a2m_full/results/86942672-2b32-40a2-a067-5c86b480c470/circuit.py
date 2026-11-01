from qiskit import QuantumCircuit
import math


def _increment(qc, n):
    # x -> x+1 mod 2^n (little-endian): flip bit i if all lower bits are 1, top bit first
    for i in range(n - 1, -1, -1):
        if i == 0:
            qc.x(0)
        else:
            qc.mcx(list(range(i)), i)


def _decrement(qc, n):
    # inverse of _increment: x -> x-1 mod 2^n
    for i in range(n):
        if i == 0:
            qc.x(0)
        else:
            qc.mcx(list(range(i)), i)


def _reflect_pairs(qc, theta):
    # U0 = I (x) (2|a><a| - I), |a> = cos(theta)|0> + sin(theta)|1> on qubit 0
    # 2|a><a| - I = RY(2 theta) Z  (Z applied first)
    qc.z(0)
    qc.ry(2.0 * theta, 0)


def build_circuit(instance):
    """Coinless 1D staggered walk, t steps of U = U1 U0 on a cycle of 2^n sites.
    instance: {"n": int 2..12, "steps": int 0..1000, optional "theta": float}
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    steps = instance.get('steps')
    theta = instance.get('theta', math.pi / 4)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 12:
        raise ValueError('n must be an integer in [2, 12]')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0 or steps > 1000:
        raise ValueError('steps must be an integer in [0, 1000]')
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError('theta must be a finite number')
    theta = float(theta)
    qc = QuantumCircuit(n, name='coinless_walk')
    for _ in range(steps):
        # U0: reflection on pairs (2k, 2k+1)
        _reflect_pairs(qc, theta)
        # U1 = S U0 S^dagger: reflection on pairs (2k+1, 2k+2)
        _decrement(qc, n)
        _reflect_pairs(qc, theta)
        _increment(qc, n)
    return qc
