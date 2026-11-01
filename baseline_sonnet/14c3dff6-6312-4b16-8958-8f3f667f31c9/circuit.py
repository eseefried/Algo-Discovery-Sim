from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _phase_on_all_ones(qc, qubits, angle):
    # diag phase exp(i*angle) on |1...1> of the given qubits
    if len(qubits) == 1:
        qc.p(angle, qubits[0])
    else:
        qc.mcp(angle, qubits[:-1], qubits[-1])


def _marked_phase(qc, qubits, w, angle):
    # exp(i*angle*|w><w|); qubit i holds bit i of w (little-endian)
    for i, q in enumerate(qubits):
        if not (w >> i) & 1:
            qc.x(q)
    _phase_on_all_ones(qc, qubits, angle)
    for i, q in enumerate(qubits):
        if not (w >> i) & 1:
            qc.x(q)


def _uniform_phase(qc, qubits, angle):
    # exp(i*angle*|s><s|) = H^n exp(i*angle*|0><0|) H^n
    for q in qubits:
        qc.h(q)
    for q in qubits:
        qc.x(q)
    _phase_on_all_ones(qc, qubits, angle)
    for q in qubits:
        qc.x(q)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Approximate exp(-i H T), H = -gamma*L - |w><w| on K_N, N = 2^n (eq_1, eq_2)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_qubits')
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError('n_qubits must be an integer in [1, 12]')
    N = 2 ** n
    w = instance.get('marked')
    if not _is_int(w) or w < 0 or w >= N:
        raise ValueError('marked must be an integer in [0, 2^n - 1]')
    gamma = instance.get('gamma')
    if gamma is None:
        gamma = 1.0 / N
    if not _is_num(gamma) or gamma < 0:
        raise ValueError('gamma must be a finite nonnegative number')
    T = instance.get('time')
    if not _is_num(T) or T < 0:
        raise ValueError('time must be a finite nonnegative number')
    r = instance.get('trotter_steps')
    if r is None:
        r = 1
    if not _is_int(r) or r < 1 or r > 1000:
        raise ValueError('trotter_steps must be an integer in [1, 1000]')
    gamma = float(gamma)
    T = float(T)
    reg = QuantumRegister(n, 'vertex')
    qc = QuantumCircuit(reg)
    qubits = list(range(n))
    dt = T / r
    # identity part of H: -gamma*N*I  ->  global phase exp(+i*gamma*N*T)
    qc.global_phase = gamma * N * T
    for _ in range(r):
        # exp(+i*dt*|w><w|) half step, exp(-i*gamma*N*dt*|s><s|) full step, half step
        _marked_phase(qc, qubits, w, dt / 2.0)
        _uniform_phase(qc, qubits, -gamma * N * dt)
        _marked_phase(qc, qubits, w, dt / 2.0)
    return qc
