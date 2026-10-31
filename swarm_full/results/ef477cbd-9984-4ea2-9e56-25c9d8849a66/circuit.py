from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, RYGate
import math

MAX_QUBITS = 12
MAX_COUNTING = 6


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    f = instance.get('f_values')
    m = instance.get('counting_qubits')
    if not isinstance(f, list) or len(f) < 2:
        raise ValueError('f_values must be a list of length >= 2')
    size = len(f)
    if size & (size - 1) != 0:
        raise ValueError('len(f_values) must be a power of two')
    n = size.bit_length() - 1
    if isinstance(m, bool) or not isinstance(m, int) or m < 1 or m > MAX_COUNTING:
        raise ValueError('counting_qubits must be an int in 1..6')
    if m + n + 1 > MAX_QUBITS:
        raise ValueError('too many qubits (cap is 12)')
    vals = []
    for v in f:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError('f_values must be numeric')
        v = float(v)
        if not math.isfinite(v) or v < 0.0 or v > 1.0:
            raise ValueError('f_values must lie in [0,1]')
        vals.append(v)
    return vals, n, m


def _state_prep(vals, n):
    # A|0>|0> = (1/sqrt N) sum_x |x>( sqrt(1-f(x))|0> + sqrt(f(x))|1> ); P(a=1)=mean(f)  (eq_1)
    qc = QuantumCircuit(n + 1)
    for q in range(n):
        qc.h(q)
    for x, v in enumerate(vals):
        theta = 2.0 * math.asin(math.sqrt(v))
        if abs(theta) > 1e-14:
            g = RYGate(theta).control(n, ctrl_state=x)
            qc.append(g, list(range(n)) + [n])
    return qc


def _iterate(vals, n):
    # Q = -A S0 A^dag S_chi with S0 = I-2|0><0|; the global -1 is applied later as a phase on the control.
    a_circ = _state_prep(vals, n)
    q = QuantumCircuit(n + 1)
    q.z(n)
    q.compose(a_circ.inverse(), inplace=True)
    for i in range(n + 1):
        q.x(i)
    q.h(n)
    q.mcx(list(range(n)), n)
    q.h(n)
    for i in range(n + 1):
        q.x(i)
    q.compose(a_circ, inplace=True)
    return q


def build_circuit(instance):
    vals, n, m = _validate(instance)
    qc = QuantumCircuit(m + n + 1)
    xs = list(range(m, m + n))
    anc = m + n
    reg = xs + [anc]
    qc.compose(_state_prep(vals, n), qubits=reg, inplace=True)
    for c in range(m):
        qc.h(c)
    cq = _iterate(vals, n).to_gate().control(1)
    for c in range(m):
        for _ in range(2 ** c):
            qc.append(cq, [c] + reg)
            qc.p(math.pi, c)
    qc.append(QFTGate(m).inverse(), list(range(m)))
    return qc
