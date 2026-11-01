from qiskit import QuantumCircuit, QuantumRegister


def _parse_steps(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key != 'steps':
            raise ValueError('unknown instance key: ' + str(key))
    if 'steps' not in instance:
        raise ValueError('steps is required')
    t = instance['steps']
    if isinstance(t, bool) or not isinstance(t, int):
        raise ValueError('steps must be an integer')
    if t < 0 or t > 64:
        raise ValueError('steps must be in 0..64')
    return t


def _coin(qc, pos, coin):
    # eq_2: C = sum_v |v><v| (x) (G_2 + I_2 on padding); G_2 = X on coin LSB when coin MSB = 0
    qc.x(coin[1])
    qc.cx(coin[1], coin[0])
    qc.x(coin[1])


def _shift(qc, pos, coin):
    # eq_3: flip-flop shift, |v,0> -> |v+1,1>, |v,1> -> |v-1,0>, identity for c=2,3
    p0, p1 = pos[0], pos[1]
    c0, c1 = coin[0], coin[1]
    # increment v (mod 4) when c=0: q1 ^= q0 ; q0 ^= 1, controlled on c1=0,c0=0
    qc.x(c1)
    qc.x(c0)
    qc.mcx([c1, c0, p0], p1)
    qc.mcx([c1, c0], p0)
    qc.x(c0)
    qc.x(c1)
    # decrement v (mod 4) when c=1: q0 ^= 1 ; q1 ^= q0, controlled on c1=0,c0=1
    qc.x(c1)
    qc.mcx([c1, c0], p0)
    qc.mcx([c1, c0, p0], p1)
    qc.x(c1)
    # flip arc label (reverse arc) on used subspace c in {0,1}
    qc.x(c1)
    qc.cx(c1, c0)
    qc.x(c1)


def build_circuit(instance):
    t = _parse_steps(instance)
    pos = QuantumRegister(2, 'pos')
    coin = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(pos, coin, name='C4_grover_flipflop_walk')
    for _ in range(t):
        # eq_4: U = S C, repeated t times
        _coin(qc, pos, coin)
        _shift(qc, pos, coin)
    return qc
