from qiskit import QuantumCircuit, QuantumRegister
import math


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' must be an integer in [' + str(lo) + ', ' + str(hi) + ']')
    return v


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + ' must be a finite real number')
    return float(v)


def build_circuit(instance):
    """First-order Trotter circuit (eq_1): (exp(-iAt/n) exp(-iBt/n))^n.
    A = -J sum_edges Z_i Z_j, B = -g sum_i X_i (assumed illustrative example).
    Qubit i of register 'sys' is site i; qubit 0 is least significant."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    N = _int(instance.get('num_qubits'), 'num_qubits', 2, 12)
    n = _int(instance.get('trotter_number'), 'trotter_number', 1, 2000)
    t = _real(instance.get('time'), 'time')
    J = _real(instance.get('J'), 'J')
    g = _real(instance.get('g'), 'g')
    periodic = instance.get('periodic', False)
    if not isinstance(periodic, bool):
        raise ValueError('periodic must be a bool')
    qr = QuantumRegister(N, 'sys')
    qc = QuantumCircuit(qr)
    edges = [(i, i + 1) for i in range(N - 1)]
    if periodic and N > 2:
        edges.append((N - 1, 0))
    dt = t / n
    # exp(-i A dt) = exp(+i J dt ZZ) = RZZ(-2 J dt); exp(-i B dt) = exp(+i g dt X) = RX(-2 g dt)
    for _ in range(n):
        for a, b in edges:
            qc.rzz(-2.0 * J * dt, a, b)
        for q in range(N):
            qc.rx(-2.0 * g * dt, q)
    return qc
