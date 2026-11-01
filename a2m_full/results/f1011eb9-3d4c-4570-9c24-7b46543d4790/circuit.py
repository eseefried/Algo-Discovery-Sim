from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Trotterized exp(-i H t), H=-gamma*(N|s><s|-I)-|w><w|, on n qubits (little-endian vertex index)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')

    def is_num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)

    def is_int(x):
        return isinstance(x, int) and not isinstance(x, bool)

    n = instance.get('n')
    w = instance.get('w')
    t = instance.get('t')
    if not is_int(n) or n < 1 or n > 12:
        raise ValueError('n must be an integer in [1, 12]')
    size = 2 ** n
    if not is_int(w) or w < 0 or w >= size:
        raise ValueError('w must be an integer in [0, 2^n)')
    if not is_num(t) or t < 0:
        raise ValueError('t must be a finite non-negative number')
    gamma = instance.get('gamma', 1.0 / size)
    if not is_num(gamma) or gamma <= 0:
        raise ValueError('gamma must be a finite positive number')
    steps = instance.get('steps', 8)
    if not is_int(steps) or steps < 1 or steps > 200:
        raise ValueError('steps must be an integer in [1, 200]')
    order = instance.get('order', 2)
    if not is_int(order) or order not in (1, 2):
        raise ValueError('order must be 1 or 2')

    reg = QuantumRegister(n, 'q')
    qc = QuantumCircuit(reg, name='ctqw_search_Kn')
    qubits = list(reg)

    def phase_on_pattern(bits, theta):
        # diag phase exp(i*theta) on the basis state whose bit i (qubit i) is bits[i]
        zeros = [qubits[i] for i in range(n) if bits[i] == 0]
        for q in zeros:
            qc.x(q)
        if n == 1:
            qc.p(theta, qubits[0])
        else:
            qc.mcp(theta, qubits[:-1], qubits[-1])
        for q in zeros:
            qc.x(q)

    def apply_s(phi):
        # exp(i*phi*|s><s|) = H^n exp(i*phi*|0><0|) H^n
        for q in qubits:
            qc.h(q)
        phase_on_pattern([0] * n, phi)
        for q in qubits:
            qc.h(q)

    wbits = [(w >> i) & 1 for i in range(n)]
    a = gamma * size * t / steps
    b = t / steps
    for _ in range(steps):
        if order == 1:
            apply_s(a)
            phase_on_pattern(wbits, b)
        else:
            apply_s(a / 2.0)
            phase_on_pattern(wbits, b)
            apply_s(a / 2.0)
    # identity term +gamma*I in H gives exp(-i*gamma*t) global phase
    qc.global_phase = -gamma * t
    return qc
