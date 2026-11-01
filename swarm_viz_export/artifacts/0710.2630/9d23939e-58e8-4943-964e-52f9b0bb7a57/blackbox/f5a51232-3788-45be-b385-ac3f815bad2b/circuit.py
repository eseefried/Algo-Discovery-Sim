from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, RXGate
import math


def _edge(qc, u, v, theta, pc):
    # exp(i*theta*(|u><v|+|v><u|)) on vertex qubits 0..2, controlled by phase qubit pc
    diff = u ^ v
    p = (diff & -diff).bit_length() - 1
    others = [q for q in range(3) if q != p and (diff >> q) & 1]
    for q in others:
        qc.cx(p, q)
    up = u
    if (u >> p) & 1:
        for q in others:
            up ^= 1 << q
    cq = [q for q in range(3) if q != p]
    state = 0
    for idx, q in enumerate(cq):
        if (up >> q) & 1:
            state |= 1 << idx
    state |= 1 << len(cq)
    cq = cq + [pc]
    gate = RXGate(-2.0 * theta).control(len(cq), ctrl_state=state)
    qc.append(gate, cq + [p])
    for q in reversed(others):
        qc.cx(p, q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    x = instance.get('x')
    m = instance.get('phase_qubits')
    s = instance.get('s')
    steps = instance.get('trotter_steps')
    if not isinstance(x, (list, tuple)) or len(x) != 3:
        raise ValueError('x must be a length-3 list of bits')
    for b in x:
        if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
            raise ValueError('x entries must be 0 or 1')
    if isinstance(m, bool) or not isinstance(m, int) or m < 1 or m > 9:
        raise ValueError('phase_qubits must be an integer in 1..9')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 4:
        raise ValueError('trotter_steps must be an integer in 1..4')
    if isinstance(s, bool) or not isinstance(s, (int, float)) or not math.isfinite(s) or s == 0 or abs(s) > 1.5:
        raise ValueError('s must be a nonzero finite number with |s|<=1.5')
    vecs = ((0.0, 1.0), (1.0, 1.0), (1.0, -1.0))
    # vertex indices: root=0, rows=1,2, inputs=3,4,5
    edges = [(0, 1, 1.0)]
    for i in range(3):
        if x[i] == 1:
            for j in range(2):
                w = vecs[i][j]
                if w != 0.0:
                    edges.append((1 + j, 3 + i, w))
    qc = QuantumCircuit(3 + m)
    phase = list(range(3, 3 + m))
    for q in phase:
        qc.h(q)
    dt = float(s) / steps
    for k in range(m):
        pc = 3 + k
        n = steps * (2 ** k)
        for _ in range(n):
            for (u, v, w) in edges:
                _edge(qc, u, v, w * dt / 2.0, pc)
            for (u, v, w) in reversed(edges):
                _edge(qc, u, v, w * dt / 2.0, pc)
    qc.append(QFTGate(m).inverse(), phase)
    return qc
