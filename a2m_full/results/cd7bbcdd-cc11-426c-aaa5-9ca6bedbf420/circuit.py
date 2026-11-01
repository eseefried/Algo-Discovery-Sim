from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RXGate
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _edges(M):
    # eq_2: simplex of K_M. index = clique*M + local position.
    edges = []
    for c in range(M + 1):
        for i in range(M):
            for j in range(i + 1, M):
                edges.append((c * M + i, c * M + j))
    # one connector edge per clique pair (i<j): c_ij = i*M+(j-1), c_ji = j*M+i
    for i in range(M + 1):
        for j in range(i + 1, M + 1):
            edges.append((i * M + (j - 1), j * M + i))
    return edges


def _two_level(qc, n, a, b, theta):
    # exp(i*theta*(|a><b|+|b><a|)) as CX network + multi-controlled RX(-2*theta)
    diff = a ^ b
    p = (diff & -diff).bit_length() - 1
    flips = [q for q in range(n) if q != p and (diff >> q) & 1]
    ap = a
    for q in flips:
        if (ap >> p) & 1:
            ap ^= 1 << q
    for q in flips:
        qc.cx(p, q)
    ctrls = [q for q in range(n) if q != p]
    state = 0
    for k, q in enumerate(ctrls):
        state |= ((ap >> q) & 1) << k
    gate = RXGate(-2.0 * theta).control(len(ctrls), ctrl_state=state)
    qc.append(gate, ctrls + [p])
    for q in reversed(flips):
        qc.cx(p, q)


def _phase_state(qc, n, x, angle):
    # multiply basis state |x> by exp(i*angle)
    zeros = [q for q in range(n) if not (x >> q) & 1]
    for q in zeros:
        qc.x(q)
    qc.mcp(angle, list(range(1, n)), 0)
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('M', 'marked', 'gamma', 't', 'steps'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    M = instance['M']
    marked = instance['marked']
    gamma = instance['gamma']
    t = instance['t']
    steps = instance['steps']
    if not _is_int(M) or M < 2 or M > 6:
        raise ValueError('M must be an integer in 2..6')
    N = M * (M + 1)
    n = max(1, (N - 1).bit_length())
    if n > 12:
        raise ValueError('too many qubits')
    if not isinstance(marked, list) or len(marked) == 0:
        raise ValueError('marked must be a nonempty list')
    for w in marked:
        if not _is_int(w) or w < 0 or w >= N:
            raise ValueError('marked vertex out of range')
    if len(set(marked)) != len(marked):
        raise ValueError('marked vertices must be distinct')
    if not _is_num(gamma) or gamma < 0:
        raise ValueError('gamma must be a finite number >= 0')
    if not _is_num(t) or t < 0:
        raise ValueError('t must be a finite number >= 0')
    if not _is_int(steps) or steps < 1 or steps > 64:
        raise ValueError('steps must be an integer in 1..64')
    reg = QuantumRegister(n, 'v')
    qc = QuantumCircuit(reg)
    edges = _edges(M)
    theta = float(gamma) * float(t) / steps
    phi = float(t) / steps
    for _ in range(steps):
        # exp(i*gamma*A*t/r), edge by edge
        for a, b in edges:
            _two_level(qc, n, a, b, theta)
        # exp(i*t/r * sum_w |w><w|)
        for w in marked:
            _phase_state(qc, n, w, phi)
    return qc
