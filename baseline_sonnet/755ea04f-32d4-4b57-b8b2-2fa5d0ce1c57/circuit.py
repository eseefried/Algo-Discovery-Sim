from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def build_circuit(instance):
    """Draper-style QFT weighted-sum accumulator.

    instance keys:
      n_acc: int, accumulator qubits (modulus N = 2**n_acc)
      weights: list[int], classical weights w_j (negative allowed, taken mod N)
      input_bits: list[int], qubit count m_j of each input register x_j
    Layout (little-endian everywhere): acc = qubits 0..n-1, then x_0, x_1, ...
    Operation: |x_0>..|x_J>|b> -> |x_0>..|x_J>|(b + sum_j w_j x_j) mod N>.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_acc')
    weights = instance.get('weights')
    bits = instance.get('input_bits')
    if not _is_int(n) or n < 1:
        raise ValueError('n_acc must be a positive integer')
    if not isinstance(weights, list) or not isinstance(bits, list):
        raise ValueError('weights and input_bits must be lists')
    if len(weights) != len(bits) or len(weights) < 1:
        raise ValueError('weights and input_bits must be nonempty and of equal length')
    for w in weights:
        if not _is_int(w):
            raise ValueError('weights must be integers')
    for m in bits:
        if not _is_int(m) or m < 1:
            raise ValueError('input_bits entries must be positive integers')
    if n + sum(bits) > 12:
        raise ValueError('total qubits exceed 12')

    N = 2 ** n
    acc = QuantumRegister(n, 'acc')
    xregs = [QuantumRegister(m, 'x%d' % j) for j, m in enumerate(bits)]
    qc = QuantumCircuit(acc, *xregs)
    acc_q = list(range(n))

    # eq_1/eq_3: move accumulator to the Fourier domain
    qc.append(QFTGate(n), acc_q)

    # eq_2/eq_4: phase-domain accumulation of w_j * x_j mod N
    for j, m in enumerate(bits):
        for l in range(m):
            ctrl = xregs[j][l]
            for t in range(n):
                coeff = (weights[j] * (2 ** (l + t))) % N
                if coeff == 0:
                    continue
                qc.cp(2.0 * math.pi * coeff / N, ctrl, acc[t])

    # eq_3: return to the computational basis
    qc.append(QFTGate(n).inverse(), acc_q)
    return qc
