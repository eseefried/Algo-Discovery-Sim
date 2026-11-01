from qiskit import QuantumCircuit, QuantumRegister


def _int_param(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' must be in [%d, %d]' % (lo, hi))
    return v


def _incrementer(qc, pos, ctrl, decrement):
    # Ripple incrementer mod 2^n controlled on ctrl: bit k flips if ctrl and all lower bits are 1,
    # applied from the highest bit to the lowest. The decrement is the inverse, i.e. the reversed gate order.
    n = len(pos)
    order = list(range(n - 1, -1, -1))
    if decrement:
        order = order[::-1]
    for k in order:
        controls = [ctrl] + list(pos[:k])
        if len(controls) == 1:
            qc.cx(controls[0], pos[k])
        else:
            qc.mcx(controls, pos[k])


def _shift(qc, pos, coin):
    # eq_1: coin=0 -> x+1 mod N, coin=1 -> x-1 mod N
    qc.x(coin)
    _incrementer(qc, pos, coin, False)
    qc.x(coin)
    _incrementer(qc, pos, coin, True)


def _coin_op(qc, coin, name):
    # eq_2 coin factor C on the coin qubit
    if name == 'hadamard':
        qc.h(coin)
    elif name == 'grover':
        qc.x(coin)  # 2/d |s><s| - I with d=2 equals X
    elif name == 'dft':
        qc.h(coin)  # 2-point DFT equals H
    else:
        raise ValueError('coin must be hadamard, grover or dft')


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int_param(instance, 'n_pos', 2, 11)
    steps = _int_param(instance, 'steps', 1, 64)
    coin_name = instance.get('coin', 'hadamard')
    if not isinstance(coin_name, str):
        raise ValueError('coin must be a string')
    if coin_name not in ('hadamard', 'grover', 'dft'):
        raise ValueError('coin must be hadamard, grover or dft')
    pos = QuantumRegister(n, 'pos')
    coin = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pos, coin)
    p = [pos[i] for i in range(n)]
    c = coin[0]
    for _ in range(steps):
        _coin_op(qc, c, coin_name)
        _shift(qc, p, c)
    return qc
