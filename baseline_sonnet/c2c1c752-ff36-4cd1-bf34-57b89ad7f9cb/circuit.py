import math
from qiskit import QuantumCircuit, QuantumRegister


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in [1, 12]')
    tt = instance.get('truth_table')
    if not isinstance(tt, (list, tuple)) or len(tt) != 2 ** n:
        raise ValueError('truth_table must be a list of length 2**n')
    out = []
    for v in tt:
        if isinstance(v, bool):
            v = int(v)
        if not isinstance(v, int) or v not in (0, 1):
            raise ValueError('truth_table entries must be 0 or 1')
        out.append(v)
    return n, out


def _phase_flip_basis_state(qc, n, x):
    # Apply -1 to the computational basis state |x> (qubit q holds bit q of x).
    zeros = [q for q in range(n) if not ((x >> q) & 1)]
    for q in zeros:
        qc.x(q)
    if n == 1:
        qc.z(0)
    else:
        qc.mcp(math.pi, list(range(n - 1)), n - 1)
    for q in zeros:
        qc.x(q)


def build_circuit(instance):
    """Bernstein-Vazirani circuit H^n O_f H^n (eq_1) with phase oracle O_f|x>=(-1)^{f(x)}|x>.

    instance: {'n': int, 'truth_table': [f(0),...,f(2^n-1)]}, where index x has
    bit (i-1) equal to variable x_i, stored on qubit i-1.
    """
    n, tt = _validate(instance)
    qr = QuantumRegister(n, 'x')
    qc = QuantumCircuit(qr)
    qc.h(qr)
    for x in range(2 ** n):
        if tt[x] == 1:
            _phase_flip_basis_state(qc, n, x)
    qc.h(qr)
    return qc
