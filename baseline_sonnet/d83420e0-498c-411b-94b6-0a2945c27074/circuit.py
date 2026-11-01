from qiskit import QuantumCircuit, QuantumRegister
import math


def _int_in(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [" + str(lo) + ", " + str(hi) + "]")
    return v


def _flip_state(qc, qubits, value):
    """Apply I - 2|value><value| on qubits (qubit k holds bit k of value)."""
    zeros = [q for k, q in enumerate(qubits) if not (value >> k) & 1]
    for q in zeros:
        qc.x(q)
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        qc.mcp(math.pi, list(qubits[:-1]), qubits[-1])
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    """Return G^L with G = -A S_0 A^dagger S_g (eq_2); A = H^n."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n", "marked", "L"):
        if key not in instance:
            raise ValueError("missing key " + key)
    n = _int_in(instance["n"], "n", 1, 12)
    L = _int_in(instance["L"], "L", 0, 256)
    marked = instance["marked"]
    if not isinstance(marked, (list, tuple)) or len(marked) == 0:
        raise ValueError("marked must be a non-empty list")
    marked = [_int_in(m, "marked element", 0, 2 ** n - 1) for m in marked]
    if len(set(marked)) != len(marked):
        raise ValueError("marked states must be distinct")
    reg = QuantumRegister(n, "search")
    qc = QuantumCircuit(reg)
    qubits = list(reg)
    for _ in range(L):
        # oracle S_g = I - 2 sum_{g} |g><g|
        for m in marked:
            _flip_state(qc, qubits, m)
        # A^dagger (A = Hadamard layer)
        for q in qubits:
            qc.h(q)
        # S_0 = I - 2|0><0|
        _flip_state(qc, qubits, 0)
        # A
        for q in qubits:
            qc.h(q)
        # overall minus sign of G
        qc.global_phase += math.pi
    return qc
