import math
from qiskit import QuantumCircuit, QuantumRegister


def _pauli_string_rotation(qc, i, j, kind, angle):
    """Apply exp(-i*angle/2 * P) with P = X_i Z...Z X_j (kind 'x') or Y_i Z...Z Y_j (kind 'y'), i<j."""
    if kind == 'y':
        qc.sdg(i)
        qc.sdg(j)
    qc.h(i)
    qc.h(j)
    for k in range(i, j):
        qc.cx(k, k + 1)
    qc.rz(angle, j)
    for k in range(j - 1, i - 1, -1):
        qc.cx(k, k + 1)
    qc.h(i)
    qc.h(j)
    if kind == 'y':
        qc.s(i)
        qc.s(j)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def build_circuit(instance):
    """Build a first-order Trotter circuit for the fermionic walk exp(-i t H), H = sum_{(i,j) in E} (a_i^dag a_j + h.c.).

    instance: {'num_vertices': N (2..12), 'edges': [[i,j],...], 'time': t, 'trotter_steps': r}
    Qubit k = occupation of vertex k (one-hot). Particle number is conserved; the weight-2 sector is the
    antisymmetric two-fermion space where |i,j>_- corresponds to qubits i and j set.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_vertices')
    if not _is_int(n) or n < 2 or n > 12:
        raise ValueError('num_vertices must be an integer in [2, 12]')
    edges = instance.get('edges')
    if not isinstance(edges, (list, tuple)):
        raise ValueError('edges must be a list of pairs')
    t = instance.get('time')
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t):
        raise ValueError('time must be a finite real number')
    r = instance.get('trotter_steps')
    if not _is_int(r) or r < 1 or r > 200:
        raise ValueError('trotter_steps must be an integer in [1, 200]')
    seen = set()
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError('each edge must be a pair')
        a, b = e
        if not _is_int(a) or not _is_int(b) or a < 0 or b < 0 or a >= n or b >= n:
            raise ValueError('edge endpoints must be vertex indices')
        if a == b:
            raise ValueError('self loops not allowed')
        key = (min(a, b), max(a, b))
        if key in seen:
            raise ValueError('duplicate edge')
        seen.add(key)
    edge_list = sorted(seen)
    if len(edge_list) > 66:
        raise ValueError('too many edges')
    reg = QuantumRegister(n, 'v')
    qc = QuantumCircuit(reg)
    dt = float(t) / r
    for _ in range(r):
        for (i, j) in edge_list:
            _pauli_string_rotation(qc, i, j, 'x', dt)
            _pauli_string_rotation(qc, i, j, 'y', dt)
    return qc
