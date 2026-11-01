import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UGate


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _arg(z):
    return math.atan2(z.imag, z.real)


def _dft3(sign):
    # eq_2: (F_3)_{jk} = exp(sign*2*pi*i*j*k/3)/sqrt(3)
    s = 1.0 / math.sqrt(3.0)
    return [[complex(math.cos(2 * math.pi * ((j * k) % 3) / 3), sign * math.sin(2 * math.pi * ((j * k) % 3) / 3)) * s for k in range(3)] for j in range(3)]


def _givens(M):
    # Reduce M to a diagonal with two-level rotations G3*G2*G1*M = D
    m = [row[:] for row in M]
    ops = []
    for a, b, col in ((0, 1, 0), (0, 2, 0), (1, 2, 1)):
        x = m[a][col]
        y = m[b][col]
        r = math.hypot(abs(x), abs(y))
        g = [[x.conjugate() / r, y.conjugate() / r], [-y / r, x / r]]
        for k in range(3):
            u = m[a][k]
            v = m[b][k]
            m[a][k] = g[0][0] * u + g[0][1] * v
            m[b][k] = g[1][0] * u + g[1][1] * v
        ops.append((a, b, g))
    return ops, [m[k][k] for k in range(3)]


def _u3_params(V):
    # V = exp(i*al) * U3(th, ph, lam)
    eps = 1e-12
    if abs(V[0][0]) > eps:
        al = _arg(V[0][0])
        th = 2.0 * math.atan2(abs(V[1][0]), abs(V[0][0]))
        if abs(V[1][0]) > eps:
            ph = _arg(V[1][0]) - al
            lam = _arg(-V[0][1]) - al
        else:
            ph = 0.0
            lam = _arg(V[1][1]) - al
    else:
        al = _arg(V[1][0])
        th = math.pi
        ph = 0.0
        lam = _arg(-V[0][1]) - al
    return al, th, ph, lam


def _ctrl0(qc, ctrl, tgt, V):
    al, th, ph, lam = _u3_params(V)
    qc.append(UGate(th, ph, lam).control(1, ctrl_state=0), [ctrl, tgt])
    qc.x(ctrl)
    qc.p(al, ctrl)
    qc.x(ctrl)


def _two_level(qc, a, b, V, c0, c1):
    # 2x2 unitary V on coin basis states a,b (coin value = 2*c1 + c0)
    if (a, b) == (0, 1):
        _ctrl0(qc, c1, c0, V)
    elif (a, b) == (0, 2):
        _ctrl0(qc, c0, c1, V)
    else:
        qc.cx(c1, c0, ctrl_state=0)
        _ctrl0(qc, c0, c1, V)
        qc.cx(c1, c0, ctrl_state=0)


def _coin(qc, c0, c1, ops, diag):
    # eq_2: coin = G1^dag G2^dag G3^dag D ; D acts first. State |3> untouched.
    for k in range(3):
        phi = _arg(diag[k])
        flips = [q for q, bit in ((c0, k & 1), (c1, k >> 1)) if bit == 0]
        for q in flips:
            qc.x(q)
        qc.cp(phi, c1, c0)
        for q in flips:
            qc.x(q)
    for a, b, g in reversed(ops):
        gd = [[g[0][0].conjugate(), g[1][0].conjugate()], [g[0][1].conjugate(), g[1][1].conjugate()]]
        _two_level(qc, a, b, gd, c0, c1)


def _shift(qc, pos, c0, c1):
    # eq_1: coin |10> (R) -> T (increment); coin |00> (L) -> T^-1; |01> (S), |11> idle
    n = len(pos)
    qc.x(c0)
    for i in range(n - 1, -1, -1):
        qc.mcx([c1, c0] + pos[:i], pos[i])
    qc.x(c0)
    qc.x(c0)
    qc.x(c1)
    for i in range(n):
        qc.mcx([c1, c0] + pos[:i], pos[i])
    qc.x(c0)
    qc.x(c1)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_position_qubits')
    t = instance.get('steps')
    sign = instance.get('coin_sign', 1)
    if not _is_int(n) or n < 2 or n > 10:
        raise ValueError('n_position_qubits must be an integer in [2, 10]')
    if not _is_int(t) or t < 0 or t > 64:
        raise ValueError('steps must be an integer in [0, 64]')
    if not _is_int(sign) or sign not in (1, -1):
        raise ValueError('coin_sign must be +1 or -1')
    if n + 2 > 12:
        raise ValueError('too many qubits')
    pr = QuantumRegister(n, 'pos')
    cr = QuantumRegister(2, 'coin')
    qc = QuantumCircuit(pr, cr)
    pos = list(range(n))
    c0 = n
    c1 = n + 1
    ops, diag = _givens(_dft3(sign))
    for _ in range(t):
        _coin(qc, c0, c1, ops, diag)
        _shift(qc, pos, c0, c1)
    return qc
