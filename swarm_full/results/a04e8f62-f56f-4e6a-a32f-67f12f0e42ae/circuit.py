from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be a finite real number')
    return float(x)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_qubits')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('num_qubits must be an integer in 1..12')
    r = instance.get('steps')
    if isinstance(r, bool) or not isinstance(r, int) or r < 1 or r > 1000:
        raise ValueError('steps must be an integer in 1..1000')
    t = _num(instance.get('time'), 'time')
    raw = instance.get('terms')
    if not isinstance(raw, list) or len(raw) == 0 or len(raw) > 200:
        raise ValueError('terms must be a list of 1..200 entries')
    terms = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError('each term must be a dict')
        p = item.get('pauli')
        if not isinstance(p, str) or len(p) != n:
            raise ValueError('pauli must be a string of length num_qubits')
        for ch in p:
            if ch not in 'IXYZ':
                raise ValueError('pauli characters must be in IXYZ')
        terms.append((p, _num(item.get('coeff'), 'coeff')))
    return n, terms, t, r


def _pauli_rotation(qc, pauli, theta):
    # Implements exp(-i * theta/2 * P); rightmost character acts on qubit 0.
    n = len(pauli)
    active = []
    for q in range(n):
        ch = pauli[n - 1 - q]
        if ch != 'I':
            active.append((q, ch))
    if not active:
        qc.global_phase = qc.global_phase - theta / 2.0
        return
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.sdg(q)
            qc.h(q)
    qubits = [q for q, _ in active]
    last = qubits[-1]
    for q in qubits[:-1]:
        qc.cx(q, last)
    qc.rz(theta, last)
    for q in reversed(qubits[:-1]):
        qc.cx(q, last)
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.h(q)
            qc.s(q)


def build_circuit(instance):
    """First-order Trotter circuit for H=sum_j c_j P_j (eq_1)."""
    n, terms, t, r = _parse(instance)
    sys = QuantumRegister(n, 'sys')
    qc = QuantumCircuit(sys)
    dt = t / r
    for _ in range(r):
        for pauli, c in terms:
            _pauli_rotation(qc, pauli, 2.0 * c * dt)
    return qc
