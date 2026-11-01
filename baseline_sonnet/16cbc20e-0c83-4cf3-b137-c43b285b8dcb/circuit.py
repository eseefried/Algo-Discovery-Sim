from qiskit import QuantumCircuit
import math


def _phase_on_basis_state(qc, angle, n, value):
    """Apply exp(i*angle*|value><value|) on qubits 0..n-1 (qubit 0 is the LSB)."""
    zeros = [q for q in range(n) if not ((value >> q) & 1)]
    for q in zeros:
        qc.x(q)
    if n == 1:
        qc.p(angle, 0)
    else:
        qc.mcp(angle, list(range(n - 1)), n - 1)
    for q in zeros:
        qc.x(q)


def _phase_on_uniform(qc, angle, n):
    """Apply exp(i*angle*|s><s|), |s>=H^n|0>, as H^n (phase on |0..0>) H^n."""
    for q in range(n):
        qc.h(q)
    _phase_on_basis_state(qc, angle, n, 0)
    for q in range(n):
        qc.h(q)


def _real(instance, key):
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + " must be a real number")
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + " must be finite")
    return v


def _integer(instance, key):
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    return v


def build_circuit(instance):
    """Trotterized exp(-i H t), H = -gamma*A_{K_N} - |w><w|, N = 2**n.

    instance keys: n_qubits (1..12), marked (0..N-1), gamma (>0), time (>=0), trotter_steps (>=1).
    Uses A = N|s><s| - I, so
    -iHt = i*gamma*N*t|s><s| + i*t|w><w| - i*gamma*t*I.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n_qubits", "marked", "gamma", "time", "trotter_steps"):
        if key not in instance:
            raise ValueError("missing key: " + key)
    n = _integer(instance, "n_qubits")
    if n < 1 or n > 12:
        raise ValueError("n_qubits must be in 1..12")
    big_n = 2 ** n
    w = _integer(instance, "marked")
    if w < 0 or w >= big_n:
        raise ValueError("marked out of range")
    gamma = _real(instance, "gamma")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    t = _real(instance, "time")
    if t < 0:
        raise ValueError("time must be non-negative")
    r = _integer(instance, "trotter_steps")
    if r < 1 or r > 10000:
        raise ValueError("trotter_steps must be in 1..10000")
    qc = QuantumCircuit(n, name="ctqw_search_complete_graph")
    dt = t / r
    for _ in range(r):
        _phase_on_uniform(qc, gamma * big_n * dt, n)
        _phase_on_basis_state(qc, dt, n, w)
    qc.global_phase = -gamma * t
    return qc
