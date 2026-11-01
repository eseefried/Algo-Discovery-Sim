import math
from qiskit import QuantumCircuit, QuantumRegister


def _mcz(qc, qubits):
    """Multi-controlled Z (phase -1 on all-ones) over the listed qubits."""
    if len(qubits) == 1:
        qc.z(qubits[0])
        return
    qc.h(qubits[-1])
    qc.mcx(list(qubits[:-1]), qubits[-1])
    qc.h(qubits[-1])


def _oracle(qc, search, w):
    """eq_3: U_w = I - 2|w><w| on the search register (little-endian bits of w)."""
    n = len(search)
    for i in range(n):
        if not (w >> i) & 1:
            qc.x(search[i])
    _mcz(qc, list(search))
    for i in range(n):
        if not (w >> i) & 1:
            qc.x(search[i])


def _lossy_hop(qc, search, anc, theta):
    """eq_1/eq_2: V = (|0><0| (x) R_s + |1><1| (x) I)(Ry(theta) (x) I).
    R_s = 2|s><s| - I = H^n (2|0><0| - I) H^n.
    Controlled on anc=0, 2|0><0|-I has phase +1 on search=0 and -1 elsewhere.
    Implemented as a -1 phase on anc=0 times a -1 phase on (search=0, anc=0)."""
    n = len(search)
    qc.ry(theta, anc)
    for i in range(n):
        qc.h(search[i])
    qc.x(anc)
    qc.z(anc)
    for i in range(n):
        qc.x(search[i])
    _mcz(qc, list(search) + [anc])
    for i in range(n):
        qc.x(search[i])
    qc.x(anc)
    for i in range(n):
        qc.h(search[i])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 4:
        raise ValueError('n must be an integer in 2..4')
    N = 2 ** n
    w = instance.get('marked')
    if isinstance(w, bool) or not isinstance(w, int) or w < 0 or w >= N:
        raise ValueError('marked must be an integer in 0..N-1')
    T = instance.get('steps')
    if T is None:
        T = int(math.floor(math.pi / 4.0 * math.sqrt(N)))
    if isinstance(T, bool) or not isinstance(T, int) or T < 0:
        raise ValueError('steps must be a nonnegative integer')
    if n + T > 12:
        raise ValueError('total qubits n + steps must be at most 12')
    has_eps = instance.get('eps') is not None
    has_c = instance.get('c') is not None
    if has_eps == has_c:
        raise ValueError('provide exactly one of eps or c')
    if has_eps:
        eps = instance['eps']
        if isinstance(eps, bool) or not isinstance(eps, (int, float)):
            raise ValueError('eps must be a real number')
        eps = float(eps)
    else:
        c = instance['c']
        if isinstance(c, bool) or not isinstance(c, (int, float)) or c < 0:
            raise ValueError('c must be a nonnegative real number')
        eps = float(c) / math.sqrt(N)
    if not (eps >= 0.0 and eps <= 1.0):
        raise ValueError('eps must lie in [0, 1]')
    theta = 2.0 * math.asin(eps)
    sr = QuantumRegister(n, 'search')
    if T > 0:
        ar = QuantumRegister(T, 'anc')
        qc = QuantumCircuit(sr, ar)
    else:
        qc = QuantumCircuit(sr)
    search = [sr[i] for i in range(n)]
    for t in range(T):
        _oracle(qc, search, w)
        _lossy_hop(qc, search, ar[t], theta)
    return qc
