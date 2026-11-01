import math
from qiskit import QuantumCircuit, QuantumRegister


def _get_int(instance, name, lo, hi):
    v = instance.get(name)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' must be an integer in [' + str(lo) + ', ' + str(hi) + ']')
    return v


def _mc(qc, controls, target):
    if len(controls) == 1:
        qc.cx(controls[0], target)
    else:
        qc.mcx(controls, target)


def _oracle(qc, vq, m):
    # eq_1: O = I - 2|m><m| on vertex register, identity on coin (one query)
    n = len(vq)
    for i in range(n):
        if not (m >> i) & 1:
            qc.x(vq[i])
    if n == 1:
        qc.z(vq[0])
    else:
        qc.mcp(math.pi, vq[:-1], vq[-1])
    for i in range(n):
        if not (m >> i) & 1:
            qc.x(vq[i])


def _shift(qc, vq, cq):
    # S|v,c> = |v+1,c> for c=1 and |v-1,c> for c=0 (mod 2^n)
    n = len(vq)
    for i in reversed(range(n)):
        _mc(qc, [cq] + vq[:i], vq[i])
    qc.x(cq)
    for i in range(n):
        _mc(qc, [cq] + vq[:i], vq[i])
    qc.x(cq)


def _walk_step(qc, vq, cq, coin):
    # eq_2: coin step then shift
    if coin == 'grover':
        qc.x(cq)  # 2|s><s|-I = X for a 1-qubit coin
    else:
        qc.h(cq)
    _shift(qc, vq, cq)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _get_int(instance, 'n', 1, 11)
    m = _get_int(instance, 'marked', 0, 2 ** n - 1)
    k = _get_int(instance, 'k', 1, 200)
    T = _get_int(instance, 'T', 1, 200)
    if k * T > 2000:
        raise ValueError('k*T too large')
    coin = instance.get('coin', 'grover')
    if coin not in ('grover', 'hadamard'):
        raise ValueError('coin must be grover or hadamard')
    vertex = QuantumRegister(n, 'vertex')
    cr = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(vertex, cr)
    vq = list(vertex)
    cq = cr[0]
    # eq_3: (W^k O)^T
    for _ in range(T):
        _oracle(qc, vq, m)
        for _ in range(k):
            _walk_step(qc, vq, cq, coin)
    return qc
