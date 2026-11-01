from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(x):
    if x is None:
        return math.inf
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError('weights must be numbers or null (infinity)')
    if x != x or x < 0:
        raise ValueError('weights must be nonnegative')
    return float(x)


def _phase_flip_basis(qc, m, k):
    # Flip the sign of computational basis state |k> on m index qubits.
    zeros = [i for i in range(m) if not ((k >> i) & 1)]
    for i in zeros:
        qc.x(i)
    if m == 1:
        qc.z(0)
    else:
        qc.mcp(math.pi, list(range(1, m)), 0)
    for i in zeros:
        qc.x(i)


def _diffusion(qc, m):
    # H^m (I - 2|0><0|) H^m = I - 2|s><s|, equals -(2|s><s|-I) up to global phase.
    for i in range(m):
        qc.h(i)
    for i in range(m):
        qc.x(i)
    if m == 1:
        qc.z(0)
    else:
        qc.mcp(math.pi, list(range(1, m)), 0)
    for i in range(m):
        qc.x(i)
    for i in range(m):
        qc.h(i)


def build_circuit(instance):
    """Grover iterations marking k with cost[k] = d1_row[k] + w_col[k] < threshold (eq_3 oracle)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    d1 = instance.get('d1_row')
    wc = instance.get('w_col')
    if not isinstance(d1, list) or not isinstance(wc, list):
        raise ValueError('d1_row and w_col must be lists')
    n = len(d1)
    if n != len(wc) or n < 2 or (n & (n - 1)) != 0:
        raise ValueError('n must be a power of two >= 2 and lists must match')
    m = n.bit_length() - 1
    if m > 12:
        raise ValueError('too many qubits')
    th = instance.get('threshold')
    if isinstance(th, bool) or not isinstance(th, (int, float)) or th != th or math.isinf(th):
        raise ValueError('threshold must be a finite number')
    r = instance.get('iterations')
    if isinstance(r, bool) or not isinstance(r, int) or r < 0 or r > 64:
        raise ValueError('iterations must be an integer in [0, 64]')
    costs = [_num(d1[k]) + _num(wc[k]) for k in range(n)]
    marked = [k for k in range(n) if costs[k] < th]
    reg = QuantumRegister(m, 'k')
    qc = QuantumCircuit(reg)
    for _ in range(r):
        for k in marked:
            _phase_flip_basis(qc, m, k)
        _diffusion(qc, m)
    return qc
