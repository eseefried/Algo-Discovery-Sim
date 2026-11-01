from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _phase_about_basis(qc, qubits, value, phi):
    # eq_4: R_phi(|value>) = I + (e^{i phi}-1)|value><value|
    zeros = [q for i, q in enumerate(qubits) if not ((value >> i) & 1)]
    for q in zeros:
        qc.x(q)
    if len(qubits) == 1:
        qc.p(phi, qubits[0])
    else:
        qc.mcp(phi, list(qubits[:-1]), qubits[-1])
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    """Return k iterations of G_delta = -R_s(pi+delta) R_w(pi+delta) on n qubits.

    instance keys: n_qubits (1..12), marked (0..2^n-1), iterations (0..1000), delta (finite real).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('n_qubits', 'marked', 'iterations', 'delta'):
        if key not in instance:
            raise ValueError('missing key: ' + key)
    n = instance['n_qubits']
    marked = instance['marked']
    k = instance['iterations']
    delta = instance['delta']
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError('n_qubits must be an integer in 1..12')
    if not _is_int(marked) or marked < 0 or marked >= 2 ** n:
        raise ValueError('marked must be an integer in 0..2^n-1')
    if not _is_int(k) or k < 0 or k > 1000:
        raise ValueError('iterations must be an integer in 0..1000')
    if isinstance(delta, bool) or not isinstance(delta, (int, float)) or not math.isfinite(delta):
        raise ValueError('delta must be a finite real number')
    phi = math.pi + float(delta)
    reg = QuantumRegister(n, 'search')
    qc = QuantumCircuit(reg)
    qubits = list(reg)
    for _ in range(k):
        # R_w(pi+delta): phase error on the marked state
        _phase_about_basis(qc, qubits, marked, phi)
        # R_s(pi+delta) = H^n R_phi(|0..0>) H^n
        for q in qubits:
            qc.h(q)
        _phase_about_basis(qc, qubits, 0, phi)
        for q in qubits:
            qc.h(q)
        # overall minus sign of G_delta
        qc.global_phase += math.pi
    return qc
