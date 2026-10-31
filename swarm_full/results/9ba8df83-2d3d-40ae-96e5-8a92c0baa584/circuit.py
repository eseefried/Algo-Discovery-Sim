import math
from qiskit import QuantumCircuit, QuantumRegister


def _real(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(name + ' must be a finite real number')
    return float(value)


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def _ising_layer(qc, n, j_nn, j_nnn, tau):
    # eq_1: exp(-i H_J tau) with Iz = Z/2 -> exp(-i J tau/4 ZZ) = RZZ(J tau/2)
    if tau == 0.0:
        return
    for i in range(n - 1):
        if j_nn != 0.0:
            qc.rzz(j_nn * tau / 2.0, i, i + 1)
    for i in range(n - 2):
        if j_nnn != 0.0:
            qc.rzz(j_nnn * tau / 2.0, i, i + 2)


def _all_ones_phase(qc, n):
    # phase -1 on |1...1>
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)


def _oracle(qc, n, marked):
    zeros = [q for q in range(n) if not (marked >> q) & 1]
    for q in zeros:
        qc.x(q)
    _all_ones_phase(qc, n)
    for q in zeros:
        qc.x(q)


def _diffusion(qc, n):
    # inversion about the mean (up to a global phase): H X (CZ..Z) X H
    for q in range(n):
        qc.h(q)
        qc.x(q)
    _all_ones_phase(qc, n)
    for q in range(n):
        qc.x(q)
        qc.h(q)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _integer(instance.get('n_qubits', 4), 'n_qubits')
    if n < 2 or n > 12:
        raise ValueError('n_qubits must be between 2 and 12')
    marked = _integer(instance.get('marked', 0), 'marked')
    if marked < 0 or marked >= 2 ** n:
        raise ValueError('marked out of range')
    iterations = instance.get('iterations', None)
    if iterations is None:
        iterations = int(math.floor(math.pi / 4.0 * math.sqrt(2 ** n)))
    iterations = _integer(iterations, 'iterations')
    if iterations < 0 or iterations > 100:
        raise ValueError('iterations must be in 0..100')
    j_nn = _real(instance.get('j_nn', 0.0), 'j_nn')
    j_nnn = _real(instance.get('j_nnn', 0.0), 'j_nnn')
    omega = instance.get('omega', None)
    if omega is None:
        tau = 0.0
    else:
        omega = _real(omega, 'omega')
        if omega <= 0.0:
            raise ValueError('omega must be positive')
        tau = math.pi / omega
    reg = QuantumRegister(n, 'spins')
    qc = QuantumCircuit(reg)
    for _ in range(iterations):
        _oracle(qc, n, marked)
        _ising_layer(qc, n, j_nn, j_nnn, tau)
        _diffusion(qc, n)
        _ising_layer(qc, n, j_nn, j_nnn, tau)
    return qc
