from qiskit import QuantumCircuit, QuantumRegister
import math


def _check_int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' out of range or not an integer')
    return v


def _mcz(qc, n):
    # CZ on all n qubits: H on top qubit, multi-controlled X, H (eq_3)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    if set(instance) - {'n', 'w', 'k', 'phi'}:
        raise ValueError('unknown instance key')
    n = _check_int(instance.get('n', 4), 'n', 2, 12)
    size = 2 ** n
    w = _check_int(instance.get('w', 5 % size), 'w', 0, size - 1)
    k_default = int(math.floor(math.pi / 4 * math.sqrt(size) - 0.5 + 0.5))  # eq_4, =3 for n=4
    k = _check_int(instance.get('k', k_default), 'k', 0, 100)
    phi = instance.get('phi', 0.0)
    if isinstance(phi, bool) or not isinstance(phi, (int, float)) or not math.isfinite(phi):
        raise ValueError('phi must be a finite real number')
    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q)
    # eq_1: uniform superposition layer, part of the unitary
    for i in range(n):
        qc.h(i)
    for _ in range(k):
        # eq_2/eq_3: oracle O_w = X^{wbar} MCZ X^{wbar}
        for i in range(n):
            if not (w >> i) & 1:
                qc.x(i)
        _mcz(qc, n)
        for i in range(n):
            if not (w >> i) & 1:
                qc.x(i)
        # eq_2/eq_3: diffusion D = -(H^n X^n MCZ X^n H^n)
        for i in range(n):
            qc.h(i)
            qc.x(i)
        _mcz(qc, n)
        for i in range(n):
            qc.x(i)
            qc.h(i)
        qc.global_phase += math.pi
        # eq_5: optional second-neighbour ZZ layer, exp(-i phi ZZ/4) = RZZ(phi/2)
        if phi != 0:
            for j in range(n - 2):
                qc.rzz(phi / 2.0, j, j + 2)
    return qc
