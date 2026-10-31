import math
from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def _phase_on_state(qc, qubits, state, phi):
    # Multiply the computational basis state |state> by exp(i*phi); all other basis states are unchanged.
    n = len(qubits)
    flips = [q for i, q in enumerate(qubits) if not (state >> i) & 1]
    for q in flips:
        qc.x(q)
    if n == 1:
        qc.p(phi, qubits[0])
    else:
        qc.mcp(phi, list(qubits[:-1]), qubits[-1])
    for q in flips:
        qc.x(q)


def build_circuit(instance):
    """Grover-type iteration with systematic phase error beta (baseline, eq_2 with beta perturbation).
    instance: {n_qubits, marked, iterations, beta}"""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('n_qubits', 'marked', 'iterations', 'beta'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    n = _as_int(instance['n_qubits'], 'n_qubits')
    marked = _as_int(instance['marked'], 'marked')
    iters = _as_int(instance['iterations'], 'iterations')
    beta = instance['beta']
    if isinstance(beta, bool) or not isinstance(beta, (int, float)):
        raise ValueError('beta must be a real number')
    beta = float(beta)
    if not math.isfinite(beta):
        raise ValueError('beta must be finite')
    if n < 1 or n > 12:
        raise ValueError('n_qubits must be in 1..12')
    if marked < 0 or marked >= 2 ** n:
        raise ValueError('marked out of range')
    if iters < 0 or iters > 200:
        raise ValueError('iterations must be in 0..200')
    phi = math.pi + beta
    reg = QuantumRegister(n, 'search')
    qc = QuantumCircuit(reg)
    qubits = list(range(n))
    for _ in range(iters):
        # Oracle phase inversion with error: |marked> -> exp(i(pi+beta))|marked>
        _phase_on_state(qc, qubits, marked, phi)
        # Inversion about the uniform state with error: |s> -> exp(i(pi+beta))|s>
        for q in qubits:
            qc.h(q)
        _phase_on_state(qc, qubits, 0, phi)
        for q in qubits:
            qc.h(q)
    return qc
