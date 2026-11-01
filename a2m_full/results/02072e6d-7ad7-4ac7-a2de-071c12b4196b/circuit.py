import math
from qiskit import QuantumCircuit, QuantumRegister


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + "," + str(hi) + "]")
    return v


def _cond(qc, coin, c):
    # X on coin qubits whose bit in c is 0, so an all-ones control means coin == c
    for i in range(2):
        if not (c >> i) & 1:
            qc.x(coin[i])


def _inc(qc, reg, ctrls):
    # controlled +1 mod 2^len(reg), cascade of MCX from the top bit down
    for j in range(len(reg) - 1, -1, -1):
        qc.mcx(list(ctrls) + list(reg[:j]), reg[j])


def _dec(qc, reg, ctrls):
    # controlled -1 mod 2^len(reg), the inverse cascade
    for j in range(len(reg)):
        qc.mcx(list(ctrls) + list(reg[:j]), reg[j])


def _shift(qc, coin, x, y, s):
    # eq_3: flip-flop twisted shift. Directions: 0:+x, 1:-x, 2:+y, 3:-y
    xs = list(x)
    cx = list(coin) + xs
    cl = list(coin)
    _cond(qc, coin, 0)
    for _ in range(s):
        _inc(qc, y, cx)  # wrap detect: x all ones, before x is incremented
    _inc(qc, x, cl)
    _cond(qc, coin, 0)
    _cond(qc, coin, 1)
    qc.x(xs)
    for _ in range(s):
        _dec(qc, y, cx)  # wrap detect: x == 0, before x is decremented
    qc.x(xs)
    _dec(qc, x, cl)
    _cond(qc, coin, 1)
    _cond(qc, coin, 2)
    _inc(qc, y, cl)
    _cond(qc, coin, 2)
    _cond(qc, coin, 3)
    _dec(qc, y, cl)
    _cond(qc, coin, 3)
    qc.x(coin[0])  # coin reversal c -> c XOR 1


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    m = _int(instance.get("m"), "m", 1, 4)
    n = 1 << (2 * m)
    w = _int(instance.get("marked"), "marked", 0, n - 1)
    T = _int(instance.get("iterations"), "iterations", 0, 1000)
    s = _int(instance.get("twist", 1), "twist", 0, (1 << m) - 1)
    coin = QuantumRegister(2, "coin")
    x = QuantumRegister(m, "x")
    y = QuantumRegister(m, "y")
    qc = QuantumCircuit(coin, x, y)
    pos = list(x) + list(y)
    zeros = [pos[i] for i in range(2 * m) if not (w >> i) & 1]
    for _ in range(T):
        # O: phase flip on marked position for all coin values (eq_2)
        if zeros:
            qc.x(zeros)
        qc.mcp(math.pi, pos[:-1], pos[-1])
        if zeros:
            qc.x(zeros)
        # C: Grover coin 2|s><s| - I = -(H H)(I - 2|00><00|)(H H) (eq_2)
        qc.h(list(coin))
        qc.x(list(coin))
        qc.cz(coin[0], coin[1])
        qc.x(list(coin))
        qc.h(list(coin))
        qc.global_phase = qc.global_phase + math.pi
        # S: twisted flip-flop shift (eq_3)
        _shift(qc, coin, x, y, s)
    return qc
