from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate
import math


def build_circuit(instance):
    """Lackadaisical phase-flip-coin walk step U^t on K_N, N=2^n, one marked vertex.

    instance keys: n_vertex_qubits (1..6), self_loops (0 or 1),
    marked_vertex (0..2^n-1), steps (0..100).
    Layout: vertex qubits 0..n-1 (bit i of v at qubit i), coin qubits n..2n-1
    (bit i of the XOR offset c at qubit n+i). Arc (v,c) -> (v xor c, c); c=0 is a self-loop.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    vals = []
    for name in ('n_vertex_qubits', 'self_loops', 'marked_vertex', 'steps'):
        x = instance.get(name)
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError('missing or non-integer parameter: ' + name)
        vals.append(x)
    n, l, w, t = vals
    if n < 1 or n > 6:
        raise ValueError('n_vertex_qubits must be in 1..6 (total qubits <= 12)')
    if l not in (0, 1):
        raise ValueError('self_loops must be 0 or 1')
    if w < 0 or w >= 2 ** n:
        raise ValueError('marked_vertex out of range')
    if t < 0 or t > 100:
        raise ValueError('steps must be in 0..100')

    vertex = QuantumRegister(n, 'vertex')
    coin = QuantumRegister(n, 'coin')
    qc = QuantumCircuit(vertex, coin)
    vq = [vertex[i] for i in range(n)]
    cq = [coin[i] for i in range(n)]

    # Coin basis change A: A|0> = |s_c>, uniform over allowed offsets
    prep = QuantumCircuit(n)
    if l == 1:
        for i in range(n):
            prep.h(i)
    else:
        for k in range(n - 1, -1, -1):
            theta = 2.0 * math.asin(math.sqrt((2.0 ** k) / (2.0 ** (k + 1) - 1.0)))
            if k == n - 1:
                prep.ry(theta, k)
            else:
                prep.ry(math.pi / 2.0, k)
                upper = list(range(k + 1, n))
                prep.append(RYGate(theta - math.pi / 2.0).control(len(upper), ctrl_state=0), upper + [k])
    prep_inv = prep.inverse()

    for _ in range(t):
        # Coin: C = A D A^dagger, D = -(I - 2 P[c=0 and v != w])  (eq_2)
        qc.compose(prep_inv, qubits=cq, inplace=True)
        # phase flip on c=0
        for q in cq:
            qc.x(q)
        if n == 1:
            qc.z(cq[0])
        else:
            qc.h(cq[-1])
            qc.mcx(cq[:-1], cq[-1])
            qc.h(cq[-1])
        for q in cq:
            qc.x(q)
        # second phase flip on (c=0 and v=w): cancels the first on the marked vertex
        for q in cq:
            qc.x(q)
        for i in range(n):
            if not (w >> i) & 1:
                qc.x(vq[i])
        allq = cq + vq
        qc.h(allq[-1])
        qc.mcx(allq[:-1], allq[-1])
        qc.h(allq[-1])
        for i in range(n):
            if not (w >> i) & 1:
                qc.x(vq[i])
        for q in cq:
            qc.x(q)
        qc.global_phase += math.pi
        qc.compose(prep, qubits=cq, inplace=True)
        # Shift S: (v,c) -> (v xor c, c)  (eq_1)
        for i in range(n):
            qc.cx(cq[i], vq[i])
    return qc
