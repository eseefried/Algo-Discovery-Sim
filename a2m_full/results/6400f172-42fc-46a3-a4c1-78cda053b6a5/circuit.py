from qiskit import QuantumCircuit, QuantumRegister
import math


def _int(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' out of range')
    return v


def _real(d, key):
    v = d.get(key, 0.0)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(key + ' must be a finite real number')
    return float(v)


def _shift(qc, pos, coin):
    # eq_1: S = |0><0| (x) T+ + |1><1| (x) T-  (little-endian position register)
    n = len(pos)
    # coin=0 -> increment x -> x+1 mod 2^n (flip high bits first)
    qc.x(coin)
    for i in range(n - 1, -1, -1):
        qc.mcx([coin] + pos[:i], pos[i])
    qc.x(coin)
    # coin=1 -> decrement: reversed gate order of the increment
    for i in range(n):
        qc.mcx([coin] + pos[:i], pos[i])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance, 'n', 1, 11)
    t = _int(instance, 't', 0, 1000)
    coin_name = instance.get('coin')
    if coin_name not in ('I', 'X', 'H', 'RY'):
        raise ValueError('coin must be one of I, X, H, RY')
    theta = _real(instance, 'theta')
    corr = instance.get('correction')
    if corr is not None:
        if not isinstance(corr, dict):
            raise ValueError('correction must be an object or null')
        ct = _real(corr, 'theta')
        cp = _real(corr, 'phi')
        cl = _real(corr, 'lam')
    pr = QuantumRegister(n, 'pos')
    cr = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pr, cr)
    pos = list(pr)
    coin = cr[0]
    # eq_2: U = S (C (x) I); repeat t times
    for _ in range(t):
        if coin_name == 'X':
            qc.x(coin)
        elif coin_name == 'H':
            qc.h(coin)
        elif coin_name == 'RY':
            qc.ry(theta, coin)
        _shift(qc, pos, coin)
    # eq_2: final state-independent correction D on the coin only
    if corr is not None:
        qc.u(ct, cp, cl, coin)
    return qc
