from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, RYGate
import math


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    f = instance.get("f_values")
    t = instance.get("t")
    if not isinstance(f, (list, tuple)):
        raise ValueError("f_values must be a list")
    if isinstance(t, bool) or not isinstance(t, int) or t < 1:
        raise ValueError("t must be a positive integer")
    big_n = len(f)
    if big_n < 2 or (big_n & (big_n - 1)) != 0:
        raise ValueError("len(f_values) must be a power of two >= 2")
    n = big_n.bit_length() - 1
    if t + n + 1 > 12:
        raise ValueError("total qubits t+n+1 must be <= 12")
    vals = []
    for v in f:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError("f values must be real numbers")
        v = float(v)
        if (not math.isfinite(v)) or v < 0.0 or v > 1.0:
            raise ValueError("f values must lie in [0,1]")
        vals.append(v)
    return vals, t, n


def _state_prep(vals, n):
    # eq_1, eq_2: A = U_f (H^n on idx). idx qubits 0..n-1 (little-endian x), ancilla n.
    qc = QuantumCircuit(n + 1)
    qc.h(list(range(n)))
    for x, v in enumerate(vals):
        angle = 2.0 * math.asin(math.sqrt(v))
        if angle == 0.0:
            continue
        zeros = [i for i in range(n) if not ((x >> i) & 1)]
        for i in zeros:
            qc.x(i)
        qc.append(RYGate(angle).control(n), list(range(n)) + [n])
        for i in zeros:
            qc.x(i)
    return qc


def _grover_gate(a_circ, n):
    # eq_3: Q' = A S0 A^dagger S_chi (time order: S_chi, A^dagger, S0, A); Q = -Q'.
    m = n + 1
    qc = QuantumCircuit(m)
    qc.z(n)
    qc.compose(a_circ.inverse(), inplace=True)
    qc.x(list(range(m)))
    qc.h(n)
    qc.mcx(list(range(n)), n)
    qc.h(n)
    qc.x(list(range(m)))
    qc.compose(a_circ, inplace=True)
    return qc.to_gate(label="Qprime")


def build_circuit(instance):
    vals, t, n = _parse(instance)
    qc = QuantumCircuit(t + n + 1)
    system = list(range(t, t + n + 1))
    a_circ = _state_prep(vals, n)
    # eq_4: H on phase register, then A on idx+anc
    qc.h(list(range(t)))
    qc.compose(a_circ, qubits=system, inplace=True)
    cq = _grover_gate(a_circ, n).control(1)
    # eq_4: controlled-Q^(2^j) from phase qubit j
    for j in range(t):
        for _ in range(2 ** j):
            qc.append(cq, [j] + system)
        if j == 0:
            # the -1 in Q = -Q' is a Z on the control for odd power 1
            qc.z(0)
    # eq_4: inverse QFT on phase register (little-endian)
    qc.append(QFTGate(t).inverse(), list(range(t)))
    return qc
