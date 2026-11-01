import math
from qiskit import QuantumCircuit, QuantumRegister


def _get_int(instance, key, lo, hi):
    if not isinstance(instance, dict) or key not in instance:
        raise ValueError('missing parameter ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError('invalid parameter ' + key)
    return v


def _dft_coin(qc, c0, c1):
    # eq_3: 3x3 DFT on logical levels k=0,1,2 with physical codes (c1 c0) = 00, 01, 11; code 10 is untouched.
    # DFT = W V with V = -S*H on span{1,2} and W = R12(pi/4) R01(beta), cos(beta)=1/sqrt(3).
    beta = math.acos(math.sqrt(1.0 / 3.0))
    gamma = math.pi / 4.0
    qc.ch(c0, c1)
    qc.cp(math.pi / 2.0, c0, c1)
    qc.z(c0)
    qc.cry(2.0 * beta, c1, c0, ctrl_state=0)
    qc.cry(2.0 * gamma, c0, c1)


def _shift(qc, pos, c0, c1):
    # eq_2: S|x,c> = |x+c,c> mod 2^n. Coin 11 = right (+1), coin 00 = left (-1), coin 01 = stay.
    n = len(pos)
    for i in reversed(range(n)):
        qc.mcx([c0, c1] + pos[:i], pos[i])
    qc.x(c0)
    qc.x(c1)
    for i in range(n):
        qc.mcx([c0, c1] + pos[:i], pos[i])
    qc.x(c0)
    qc.x(c1)


def build_circuit(instance):
    t = _get_int(instance, 'steps', 0, 64)
    n = _get_int(instance, 'position_qubits', 2, 10)
    if n + 2 > 12:
        raise ValueError('too many qubits')
    pos_reg = QuantumRegister(n, 'pos')
    coin_reg = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(pos_reg, coin_reg)
    pos = list(pos_reg)
    c0, c1 = coin_reg[0], coin_reg[1]
    for _ in range(t):
        _dft_coin(qc, c0, c1)
        _shift(qc, pos, c0, c1)
    return qc
