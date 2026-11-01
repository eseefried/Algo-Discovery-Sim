from qiskit import QuantumCircuit, QuantumRegister
import math


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    return v


def _as_float(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(name + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(name + ' must be finite')
    return v


def _marked_phase(qc, n, w, phi):
    # eq_2: e^{i phi |w><w|} = diag with phase e^{i phi} on |w> only.
    # Flip qubits where bit i of w is 0, apply multi-controlled phase on all-ones, unflip.
    zeros = [i for i in range(n) if ((w >> i) & 1) == 0]
    for i in zeros:
        qc.x(i)
    qc.mcp(phi, list(range(n - 1)), n - 1)
    for i in zeros:
        qc.x(i)


def _hop_half(qc, n, gamma, dt):
    # eq_3: e^{i gamma A dt/2} = tensor_i RX(-gamma*dt)
    for i in range(n):
        qc.rx(-gamma * dt, i)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('n'), 'n')
    marked = _as_int(instance.get('marked'), 'marked')
    r = _as_int(instance.get('steps'), 'steps')
    gamma = _as_float(instance.get('gamma'), 'gamma')
    T = _as_float(instance.get('T'), 'T')
    if n < 2 or n > 12:
        raise ValueError('n must be in 2..12')
    if marked < 0 or marked >= 2 ** n:
        raise ValueError('marked must be in [0, 2^n)')
    if r < 1 or r > 500:
        raise ValueError('steps must be in 1..500')
    if gamma <= 0.0:
        raise ValueError('gamma must be positive')
    if T <= 0.0:
        raise ValueError('T must be positive')
    dt = T / r
    v = QuantumRegister(n, 'v')
    qc = QuantumCircuit(v)
    for _ in range(r):
        _hop_half(qc, n, gamma, dt)
        _marked_phase(qc, n, marked, dt)
        _hop_half(qc, n, gamma, dt)
    return qc
