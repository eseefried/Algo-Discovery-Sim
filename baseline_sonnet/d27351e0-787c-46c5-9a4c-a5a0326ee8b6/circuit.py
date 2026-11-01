from qiskit import QuantumCircuit, QuantumRegister
import math


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 11:
        raise ValueError('n must be an integer in 1..11')
    a = instance.get('a')
    if not isinstance(a, (list, tuple)) or len(a) != n:
        raise ValueError('a must be a list of n bits')
    for v in a:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError('a entries must be 0 or 1')
    b = instance.get('b')
    if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
        raise ValueError('b must be 0 or 1')
    return n, [int(v) for v in a], int(b)


def _phase_oracle(qc, a, b):
    # eq_2 with eq_1: U_f|x> = (-1)^(a.x xor b)|x>; Z on each qubit with a_i=1, plus global phase (-1)^b
    for i, ai in enumerate(a):
        if ai:
            qc.z(i)
    if b:
        qc.global_phase = qc.global_phase + math.pi


def _controlled_phase_oracle(qc, a, b, control):
    # controlled-U_f: CZ(control, x_i) for a_i=1; Z on control gives the (-1)^b factor when control=1
    for i, ai in enumerate(a):
        if ai:
            qc.cz(control, i)
    if b:
        qc.z(control)


def build_circuit(instance):
    n, a, b = _parse(instance)
    x = QuantumRegister(n, 'x')
    c = QuantumRegister(1, 'c')
    qc = QuantumCircuit(x, c)
    ctrl = n
    # Query 1 (eq_4): f(0^n)=b by phase kickback; x is still |0^n> here
    qc.h(ctrl)
    _controlled_phase_oracle(qc, a, b, ctrl)
    qc.h(ctrl)
    # Query 2 (eq_3): Bernstein-Vazirani on the input register
    for i in range(n):
        qc.h(i)
    _phase_oracle(qc, a, b)
    for i in range(n):
        qc.h(i)
    return qc
