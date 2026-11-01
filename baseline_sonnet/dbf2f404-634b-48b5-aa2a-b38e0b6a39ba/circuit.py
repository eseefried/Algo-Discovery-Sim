import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _get_int(instance, key, lo, hi):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' out of range [' + str(lo) + ',' + str(hi) + ']')
    return v


def _increment(qc, qubits, n, sign):
    # Cyclic shift |x> -> |x+sign mod 2^n> via QFT, phases exp(sign*2*pi*i*k/N), inverse QFT.
    # sign=+1 gives S, sign=-1 gives S^dagger.
    qc.append(QFTGate(n), qubits)
    for q in range(n):
        qc.p(sign * 2.0 * math.pi * (2 ** q) / (2 ** n), qubits[q])
    qc.append(QFTGate(n).inverse(), qubits)


def build_circuit(instance):
    """Coinless staggered walk on a cycle of N=2**num_qubits sites, U=(U1 U0)^steps."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _get_int(instance, 'num_qubits', 2, 12)
    steps = _get_int(instance, 'steps', 0, 64)
    site = QuantumRegister(n, 'site')
    qc = QuantumCircuit(site)
    qubits = list(range(n))
    for _ in range(steps):
        # U0 (eq_1, eq_2 tessellation 0): reflection 2|+><+| - I on LSB = X on qubit 0
        qc.x(0)
        # U1 (eq_1, eq_2 tessellation 1): S X0 S^dagger (apply S^dagger first)
        _increment(qc, qubits, n, -1)
        qc.x(0)
        _increment(qc, qubits, n, 1)
    return qc
