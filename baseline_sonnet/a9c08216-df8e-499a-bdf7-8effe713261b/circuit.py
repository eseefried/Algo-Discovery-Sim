from qiskit import QuantumCircuit, QuantumRegister
import math


def _int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    return v


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + " must be a finite real number")
    return float(v)


def _phase_on_ones(qc, qubits, angle):
    # diag(1,...,1,exp(i*angle)) on the all-ones state of the given qubits
    if len(qubits) == 1:
        qc.p(angle, qubits[0])
    else:
        qc.mcp(angle, qubits[:-1], qubits[-1])


def _phase_on_marked(qc, qubits, marked, angle):
    # exp(i*angle*|w><w|) with qubit q holding bit q of w (little-endian)
    flips = [q for q in range(len(qubits)) if not (marked >> q) & 1]
    for q in flips:
        qc.x(qubits[q])
    _phase_on_ones(qc, qubits, angle)
    for q in flips:
        qc.x(qubits[q])


def _phase_on_uniform(qc, qubits, angle):
    # exp(i*angle*|s><s|) = H^n X^n [phase on |1..1>] X^n H^n
    for q in qubits:
        qc.h(q)
        qc.x(q)
    _phase_on_ones(qc, qubits, angle)
    for q in qubits:
        qc.x(q)
        qc.h(q)


def build_circuit(instance):
    """Trotterized exp(-i H t), H = -gamma*L - |w><w| on K_N, N=2^n (eq_3).
    instance keys: n, marked, gamma, t, steps."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n", "marked", "gamma", "t", "steps"):
        if key not in instance:
            raise ValueError("missing key: " + key)
    n = _int(instance["n"], "n")
    if n < 1 or n > 12:
        raise ValueError("n must be in 1..12")
    N = 2 ** n
    marked = _int(instance["marked"], "marked")
    if marked < 0 or marked >= N:
        raise ValueError("marked must be in 0..N-1")
    gamma = _real(instance["gamma"], "gamma")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    t = _real(instance["t"], "t")
    steps = _int(instance["steps"], "steps")
    if steps < 1 or steps > 2000:
        raise ValueError("steps must be in 1..2000")
    reg = QuantumRegister(n, "v")
    qc = QuantumCircuit(reg)
    qubits = list(range(n))
    dt = t / steps
    # H = -gamma*N*I + gamma*N*|s><s| - |w><w|; identity part -> global phase
    qc.global_phase = gamma * N * t
    for _ in range(steps):
        # exp(+i dt/2 |w><w|) exp(-i gamma N dt |s><s|) exp(+i dt/2 |w><w|)
        _phase_on_marked(qc, qubits, marked, dt / 2.0)
        _phase_on_uniform(qc, qubits, -gamma * N * dt)
        _phase_on_marked(qc, qubits, marked, dt / 2.0)
    return qc
