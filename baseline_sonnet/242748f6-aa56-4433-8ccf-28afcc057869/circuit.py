from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be a finite real number')
    return float(x)


def build_circuit(instance):
    """System qubit 0, probe k at qubit 1+k. Iteration k: U3 pulse on S, then CRX(2*eps_k) S->P_k."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    eps = instance.get('epsilons')
    if not isinstance(eps, list) or len(eps) < 1:
        raise ValueError('epsilons must be a non-empty list')
    n = len(eps)
    if n + 1 > 12:
        raise ValueError('at most 11 iterations (12 qubits total)')
    pulses = instance.get('pulses')
    if pulses is None:
        pulses = [[0.0, 0.0, 0.0] for _ in range(n)]
    if not isinstance(pulses, list) or len(pulses) != n:
        raise ValueError('pulses must be a list with one [theta, phi, lam] per iteration')
    eps = [_num(e, 'epsilon') for e in eps]
    for e in eps:
        if e <= 0:
            raise ValueError('epsilon must be positive')
    clean = []
    for p in pulses:
        if not isinstance(p, (list, tuple)) or len(p) != 3:
            raise ValueError('each pulse needs three angles')
        clean.append([_num(a, 'pulse angle') for a in p])
    S = QuantumRegister(1, 'S')
    P = QuantumRegister(n, 'P')
    qc = QuantumCircuit(S, P)
    for k in range(n):
        th, ph, lam = clean[k]
        qc.u(th, ph, lam, S[0])  # U_k pulse on system
        qc.crx(2.0 * eps[k], S[0], P[k])  # exp(-i eps |1><1|_S (x) X_P)
    return qc
