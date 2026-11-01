from qiskit import QuantumCircuit, QuantumRegister
import math


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    coeffs = instance.get('coefficients')
    if not isinstance(coeffs, dict) or len(coeffs) == 0 or len(coeffs) > 16:
        raise ValueError('coefficients must be a non-empty dict of 2-character Pauli labels')
    terms = []
    for label in sorted(coeffs):
        if not isinstance(label, str) or len(label) != 2 or any(c not in 'IXYZ' for c in label):
            raise ValueError('invalid Pauli label: %r' % (label,))
        v = coeffs[label]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError('coefficient must be a finite real number')
        terms.append((label, float(v)))
    tau = instance.get('tau')
    if isinstance(tau, bool) or not isinstance(tau, (int, float)) or not math.isfinite(tau) or tau <= 0:
        raise ValueError('tau must be a positive finite number')
    steps = instance.get('trotter_steps')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1 or steps > 50:
        raise ValueError('trotter_steps must be an integer in [1, 50]')
    order = instance.get('order')
    if isinstance(order, bool) or order not in (1, 2):
        raise ValueError('order must be 1 or 2')
    return terms, float(tau), steps, order


def _apply_term(qc, label, theta):
    # Ancilla-controlled exp(-i theta P), P a Pauli string.
    # Circuit qubit 0 = ancilla; label[1] -> circuit qubit 1; label[0] -> circuit qubit 2.
    active = []
    for k, ch in enumerate(label):
        if ch != 'I':
            active.append((2 - k, ch))
    if not active:
        qc.p(-theta, 0)
        return
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.sdg(q)
            qc.h(q)
    target = active[0][0]
    others = [q for q, _ in active[1:]]
    for q in others:
        qc.cx(q, target)
    qc.crz(2.0 * theta, 0, target)
    for q in reversed(others):
        qc.cx(q, target)
    for q, ch in active:
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.h(q)
            qc.s(q)


def build_circuit(instance):
    """Controlled Trotterized exp(-i H tau); ancilla = qubit 0, system = qubits 1,2."""
    terms, tau, steps, order = _parse(instance)
    anc = QuantumRegister(1, 'anc')
    sysr = QuantumRegister(2, 'sys')
    qc = QuantumCircuit(anc, sysr)
    dt = tau / steps
    for _ in range(steps):
        if order == 1:
            for label, g in terms:
                _apply_term(qc, label, g * dt)
        else:
            for label, g in terms:
                _apply_term(qc, label, g * dt / 2.0)
            for label, g in reversed(terms):
                _apply_term(qc, label, g * dt / 2.0)
    return qc
