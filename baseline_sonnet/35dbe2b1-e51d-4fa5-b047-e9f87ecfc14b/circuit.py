import math
from qiskit import QuantumCircuit, QuantumRegister


def _as_int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' must be an integer in [' + str(lo) + ', ' + str(hi) + ']')
    return v


def _as_real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + ' must be a finite real number')
    return float(v)


def _term_step(qc, pauli, angle):
    # Implements exp(-i * angle * P) for a Pauli string P (eq_1 factor e^{-i H_j tau}, angle = c_j * tau).
    # Leftmost character acts on the highest qubit index (Qiskit label convention).
    n = len(pauli)
    active = [(n - 1 - i, ch) for i, ch in enumerate(pauli) if ch != 'I']
    if not active:
        qc.global_phase -= angle
        return
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.sdg(q)
            qc.h(q)
    qubits = [q for q, _ in active]
    for a, b in zip(qubits[:-1], qubits[1:]):
        qc.cx(a, b)
    qc.rz(2.0 * angle, qubits[-1])
    for a, b in reversed(list(zip(qubits[:-1], qubits[1:]))):
        qc.cx(a, b)
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.h(q)
            qc.s(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('num_qubits'), 'num_qubits', 1, 12)
    t = _as_real(instance.get('time'), 'time')
    r = _as_int(instance.get('steps'), 'steps', 1, 1000)
    terms = instance.get('terms')
    if not isinstance(terms, list) or len(terms) == 0 or len(terms) > 500:
        raise ValueError('terms must be a list of 1 to 500 entries')
    parsed = []
    for term in terms:
        if not isinstance(term, dict):
            raise ValueError('each term must be a dict')
        p = term.get('pauli')
        if not isinstance(p, str) or len(p) != n or any(ch not in 'IXYZ' for ch in p):
            raise ValueError('pauli must be a length-num_qubits string over IXYZ')
        c = _as_real(term.get('coeff'), 'coeff')
        parsed.append((p, c))
    if r * len(parsed) > 5000:
        raise ValueError('steps * number of terms too large')
    qc = QuantumCircuit(QuantumRegister(n, 'system'))
    tau = t / r
    for _ in range(r):
        for p, c in parsed:
            _term_step(qc, p, c * tau)
    return qc
