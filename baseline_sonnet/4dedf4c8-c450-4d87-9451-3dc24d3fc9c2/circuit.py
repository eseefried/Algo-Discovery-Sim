import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UGate, PhaseGate


def _check_int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(name + ' out of range')
    return v


def _check_block(b):
    if not isinstance(b, (list, tuple)) or len(b) != 4:
        raise ValueError('each block must be [theta, phi, lam, alpha]')
    out = []
    for x in b:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError('block entries must be real numbers')
        if not math.isfinite(x):
            raise ValueError('block entries must be finite')
        out.append(float(x))
    return out


def build_circuit(instance):
    """Product of N controlled unitaries, control register A (n_a qubits), target B (1 qubit).

    instance: {'n_a': int, 'gates': [{'blocks': [[theta, phi, lam, alpha] * d_A]} ...]}
    Gates are applied in list order (first entry acts first).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n_a = _check_int(instance.get('n_a'), 'n_a', 1, 11)
    d_a = 2 ** n_a
    gates = instance.get('gates')
    if not isinstance(gates, (list, tuple)):
        raise ValueError('gates must be a list')
    # eq_4 bound (d_A is a power of two): N <= 2 d_A - 1
    if len(gates) < 1 or len(gates) > 2 * d_a - 1:
        raise ValueError('number of controlled unitaries must be in [1, 2 d_A - 1]')
    parsed = []
    for g in gates:
        if not isinstance(g, dict):
            raise ValueError('each gate must be a dict')
        blocks = g.get('blocks')
        if not isinstance(blocks, (list, tuple)) or len(blocks) != d_a:
            raise ValueError('each gate needs d_A blocks')
        parsed.append([_check_block(b) for b in blocks])
    A = QuantumRegister(n_a, 'A')
    B = QuantumRegister(1, 'B')
    qc = QuantumCircuit(A, B)
    ctrl = list(range(n_a))
    tgt = n_a
    for blocks in parsed:  # eq_2: ordered product of CU_k
        for i, (th, ph, lam, al) in enumerate(blocks):  # eq_1: block i of CU_k
            zeros = [j for j in ctrl if not ((i >> j) & 1)]
            for j in zeros:
                qc.x(j)
            qc.append(UGate(th, ph, lam).control(n_a), ctrl + [tgt])
            if n_a == 1:
                qc.p(al, 0)
            else:
                qc.append(PhaseGate(al).control(n_a - 1), ctrl)
            for j in zeros:
                qc.x(j)
    return qc
