from qiskit import QuantumCircuit, QuantumRegister
import math


def _transpose(qc, a, b, nq):
    # Swap computational basis states |a> and |b> (a != b); identity elsewhere.
    diff = a ^ b
    bits = [i for i in range(nq) if (diff >> i) & 1]
    p = bits[0]
    others = bits[1:]
    pbit = (a >> p) & 1
    for q in others:
        qc.cx(p, q)
    controls = [q for q in range(nq) if q != p]
    zeros = []
    for q in controls:
        v = (a >> q) & 1
        if q in others:
            v ^= pbit
        if v == 0:
            zeros.append(q)
    for q in zeros:
        qc.x(q)
    qc.mcx(controls, p)
    for q in zeros:
        qc.x(q)
    for q in reversed(others):
        qc.cx(p, q)


def build_circuit(instance):
    # eq_1: each step applies one branch U_omega = S_omega * (Ry(theta) on coin).
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_position_qubits')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 11:
        raise ValueError('n_position_qubits must be an integer in 1..11')
    boundary = instance.get('boundary', 'open')
    if boundary not in ('open', 'periodic'):
        raise ValueError('boundary must be open or periodic')
    if boundary == 'periodic' and n < 2:
        raise ValueError('periodic chain needs n_position_qubits >= 2')
    theta = instance.get('coin_angle', math.pi / 2)
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError('coin_angle must be a finite real number')
    steps = instance.get('edge_configs')
    if not isinstance(steps, list) or len(steps) < 1 or len(steps) > 64:
        raise ValueError('edge_configs must be a list of 1..64 configurations')
    N = 1 << n
    E = N - 1 if boundary == 'open' else N
    for cfg in steps:
        if not isinstance(cfg, list) or len(cfg) != E:
            raise ValueError('each edge configuration must be a list of length %d' % E)
        for v in cfg:
            if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
                raise ValueError('edge entries must be 0 or 1')
    nq = n + 1
    coin = QuantumRegister(1, 'coin')
    pos = QuantumRegister(n, 'pos')
    qc = QuantumCircuit(coin, pos)
    for cfg in steps:
        qc.ry(float(theta), 0)
        for x in range(E):
            if cfg[x] == 1:
                # basis index = coin + 2*position
                a = 2 * x
                b = 2 * ((x + 1) % N) + 1
                _transpose(qc, a, b, nq)
    return qc
