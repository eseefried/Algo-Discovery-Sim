from qiskit import QuantumCircuit, QuantumRegister
import math


def _theta(p):
    # eq_1: assumed linear map theta = pi * p / 8
    return math.pi * p / 8.0


def _mc(qc, controls, target):
    if len(controls) == 1:
        qc.cx(controls[0], target)
    else:
        qc.mcx(controls, target)


def _increment(qc, pos, ctrl):
    # |x> -> |x+1 mod 2^n> when ctrl=1; flip bit i if all lower bits are 1, high to low
    n = len(pos)
    for i in range(n - 1, -1, -1):
        _mc(qc, [ctrl] + pos[:i], pos[i])


def _decrement(qc, pos, ctrl):
    # inverse of increment: same gates in reverse (ascending) order
    n = len(pos)
    for i in range(n):
        _mc(qc, [ctrl] + pos[:i], pos[i])


def _coin_step(qc, coin, mem, theta):
    # eq_2: C(p) = SWAP_{c,m} CX_{m->c} (Ry(theta) on coin tensor I); rightmost factor acts first
    qc.ry(theta, coin)
    qc.cx(mem, coin)
    qc.swap(coin, mem)


def _shift(qc, pos, coin):
    # eq_3: S |x,c> = |x + (-1)^c mod N, c>
    qc.x(coin)
    _increment(qc, pos, coin)  # acts when original coin = 0
    qc.x(coin)
    _decrement(qc, pos, coin)  # acts when coin = 1


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('N', 'p', 'steps'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    N = instance['N']
    p = instance['p']
    steps = instance['steps']
    if isinstance(N, bool) or not isinstance(N, int):
        raise ValueError('N must be an integer')
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise ValueError('steps must be an integer')
    if isinstance(p, bool) or not isinstance(p, (int, float)):
        raise ValueError('p must be a real number')
    p = float(p)
    if not math.isfinite(p) or p < 0.0 or p > 8.0:
        raise ValueError('p must be in [0, 8]')
    if N < 4 or (N & (N - 1)) != 0:
        raise ValueError('N must be a power of two, N >= 4')
    n = N.bit_length() - 1
    if n + 2 > 12:
        raise ValueError('too many qubits (max 12)')
    if steps < 0 or steps > 512:
        raise ValueError('steps must be in [0, 512]')
    return n, p, steps


def build_circuit(instance):
    n, p, steps = _validate(instance)
    pos = QuantumRegister(n, 'pos')
    coin = QuantumRegister(1, 'coin')
    mem = QuantumRegister(1, 'mem')
    qc = QuantumCircuit(pos, coin, mem)
    posq = list(pos)
    theta = _theta(p)
    for _ in range(steps):
        _coin_step(qc, coin[0], mem[0], theta)
        _shift(qc, posq, coin[0])
    return qc
