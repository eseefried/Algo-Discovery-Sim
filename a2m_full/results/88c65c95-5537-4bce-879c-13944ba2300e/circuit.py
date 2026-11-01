import math
from qiskit import QuantumCircuit


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    k = instance.get('iterations')
    tt = instance.get('truth_table')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError('n must be an integer >= 2')
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 16:
        raise ValueError('iterations must be an integer in [0,16]')
    m = (n - 1).bit_length()
    if 2 * n + m + 3 > 12:
        raise ValueError('too many qubits: need 2n+ceil(log2 n)+3 <= 12')
    if not isinstance(tt, list) or len(tt) != 2 ** n:
        raise ValueError('truth_table must be a list of length 2^n')
    for v in tt:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError('truth_table entries must be 0 or 1')
    return n, m, k, list(tt)


def _oracle(qc, y, target, tt):
    # XOR oracle: target ^= f(y); y[j] is bit j of the argument
    for v, val in enumerate(tt):
        if val == 1:
            qc.mcx(list(y), target, ctrl_state=v)


def _force(qc, x, ireg, y, b):
    # Y ^= (x with bit i forced to b); self-inverse (all gates are XORs onto Y)
    n = len(x)
    m = len(ireg)
    for j in range(n):
        qc.cx(x[j], y[j])
    for j in range(n):
        qc.mcx(list(ireg) + [x[j]], y[j], ctrl_state=j | (1 << m))
        if b == 1:
            qc.mcx(list(ireg), y[j], ctrl_state=j)


def _checker(total, x, ireg, y, a, f, tt):
    u = QuantumCircuit(total)
    for q in list(x) + list(ireg):
        u.h(q)
    for b in (0, 1):
        _force(u, x, ireg, y, b)
        _oracle(u, y, a[b], tt)
        _force(u, x, ireg, y, b)
    # flag = f(lo) AND NOT f(hi): controls [a0,a1], state a0=1,a1=0 -> ctrl_state=1
    u.mcx([a[0], a[1]], f, ctrl_state=1)
    for b in (1, 0):
        _force(u, x, ireg, y, b)
        _oracle(u, y, a[b], tt)
        _force(u, x, ireg, y, b)
    return u


def build_circuit(instance):
    """Grover iterations Q=-U S0 U^dag S_flag around the monotonicity edge checker."""
    n, m, k, tt = _validate(instance)
    total = 2 * n + m + 3
    x = list(range(n))
    ireg = list(range(n, n + m))
    y = list(range(n + m, 2 * n + m))
    a = [2 * n + m, 2 * n + m + 1]
    f = 2 * n + m + 2
    qc = QuantumCircuit(total)
    u = _checker(total, x, ireg, y, a, f, tt)
    ud = u.inverse()
    # U_check (state preparation of the amplitude-amplification operator)
    qc.compose(u, inplace=True)
    allq = list(range(total))
    for _ in range(k):
        qc.z(f)  # S_flag
        qc.compose(ud, inplace=True)
        for q in allq:
            qc.x(q)
        qc.h(allq[-1])
        qc.mcx(allq[:-1], allq[-1])
        qc.h(allq[-1])
        for q in allq:
            qc.x(q)
        qc.compose(u, inplace=True)
        qc.global_phase = qc.global_phase + math.pi
    return qc
