"""MAJ3 span-program graph spectral test (phase estimation on a Trotterized exp(iAs))."""
import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RXGate

# Span program for MAJ3 in R^2: target t=(1,0); v1=(1,1), v2=(1,-1), v3=(0,1).
# Column 0 is the target t (the root vertex, always present); column i is input i.
# Each column lists (row, weight) entries of the biadjacency matrix B.
_COLS = (((0, 1),), ((0, 1), (1, 1)), ((0, 1), (1, -1)), ((1, 1),))


def _check_int(value, lo, hi, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < lo or value > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return value


def _edges(x):
    # eq_2/eq_3: graph G(x) keeps only columns of inputs with x_i=1, plus the target column.
    edges = []
    for col, entries in enumerate(_COLS):
        if col == 0 or x[col - 1] == 1:
            for row, w in entries:
                edges.append((row, col, w))
    return edges


def _apply_edge(qc, ctrl, row, col, angle):
    # Controlled exp(i*theta*(|a><b|+|b><a|)), a=|side0,idx=row>, b=|side1,idx=col>,
    # implemented as RX(angle), angle=-2*theta, on the side qubit (qubit 2).
    diff = [k for k in (0, 1) if ((row >> k) & 1) != ((col >> k) & 1)]
    for k in diff:
        qc.cx(2, k)
    state = 1 | (row << 1)  # control order [ctrl, idx0, idx1]: ctrl=1, idx bits = row bits
    gate = RXGate(angle).control(3, ctrl_state=state)
    qc.append(gate, [ctrl, 0, 1, 2])
    for k in reversed(diff):
        qc.cx(2, k)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    x = instance.get("x")
    if not isinstance(x, list) or len(x) != 3:
        raise ValueError("x must be a list of 3 bits")
    for b in x:
        _check_int(b, 0, 1, "x bit")
    m = _check_int(instance.get("phase_qubits"), 1, 6, "phase_qubits")
    steps = _check_int(instance.get("trotter_steps"), 1, 4, "trotter_steps")
    t = instance.get("time")
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or t <= 0 or t > 1.2:
        raise ValueError("time must be a finite number in (0, 1.2] so that time*||A|| < pi")
    edges = _edges(x)
    vq = QuantumRegister(3, "v")
    pq = QuantumRegister(m, "p")
    qc = QuantumCircuit(vq, pq)
    for k in range(m):
        qc.h(3 + k)
    dt = float(t) / steps
    for k in range(m):
        # eq_4: controlled U^(2^k), U = one Trotterized step-product of exp(i A time)
        for _ in range(steps * (2 ** k)):
            for row, col, w in edges:
                _apply_edge(qc, 3 + k, row, col, -2.0 * w * dt)
    # eq_5 readout: inverse QFT on phase register (outcome 0 = zero-eigenvalue bin)
    qc.append(QFTGate(m).inverse(), list(range(3, 3 + m)))
    return qc
