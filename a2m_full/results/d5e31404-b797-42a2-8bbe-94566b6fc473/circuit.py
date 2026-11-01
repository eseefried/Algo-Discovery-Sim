from qiskit import QuantumCircuit, QuantumRegister
import math


def _anf(tt):
    """Moebius transform: truth table -> ANF coefficients a_S (index S is a bitmask)."""
    a = [int(v) for v in tt]
    for i in range(3):
        for x in range(8):
            if (x >> i) & 1:
                a[x] ^= a[x ^ (1 << i)]
    return a


def build_circuit(instance):
    """Return H^3 U_f H^3 on 3 qubits. instance: {'truth_table': [8 bits], 'include_hadamards': bool (optional)}.
    truth_table[x] = f(x), x = x0 + 2*x1 + 4*x2, qubit i holds x_i."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    tt = instance.get('truth_table')
    if not isinstance(tt, (list, tuple)) or len(tt) != 8:
        raise ValueError('truth_table must be a list of 8 bits')
    for v in tt:
        if isinstance(v, float) or not isinstance(v, (int, bool)) or v not in (0, 1):
            raise ValueError('truth_table entries must be 0 or 1')
    had = instance.get('include_hadamards', True)
    if not isinstance(had, bool):
        raise ValueError('include_hadamards must be a bool')
    qc = QuantumCircuit(QuantumRegister(3, 'q'))
    if had:
        for i in range(3):
            qc.h(i)
    # eq_1 / eq_4: oracle as product of Z, CZ, CCZ according to ANF
    a = _anf(tt)
    for s in range(8):
        if not a[s]:
            continue
        qs = [i for i in range(3) if (s >> i) & 1]
        if len(qs) == 0:
            qc.global_phase += math.pi
        elif len(qs) == 1:
            qc.z(qs[0])
        elif len(qs) == 2:
            qc.cz(qs[0], qs[1])
        else:
            qc.ccz(qs[0], qs[1], qs[2])
    if had:
        for i in range(3):
            qc.h(i)
    return qc
