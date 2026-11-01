from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _as_int(value, name, low):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    if value < low:
        raise ValueError(name + ' must be >= ' + str(low))
    return value


def build_circuit(instance):
    """Controlled weighted sum |x>|s> -> |x>|s + sum_i w_i x_i mod 2^n_acc>.

    instance keys: n_acc (int), n_x (int), weights (list of ints), signed (optional bool).
    If signed is true, each x_i is two's complement (top bit has weight -2^(n_x-1)).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n_acc = _as_int(instance.get('n_acc'), 'n_acc', 1)
    n_x = _as_int(instance.get('n_x'), 'n_x', 1)
    weights = instance.get('weights')
    if not isinstance(weights, list) or len(weights) < 1:
        raise ValueError('weights must be a non-empty list')
    for w in weights:
        if isinstance(w, bool) or not isinstance(w, int):
            raise ValueError('weights must be integers')
        if abs(w) > 1000000:
            raise ValueError('weight too large')
    signed = instance.get('signed', False)
    if not isinstance(signed, bool):
        raise ValueError('signed must be a bool')
    m = len(weights)
    if m * n_x + n_acc > 12:
        raise ValueError('total qubits exceed 12')
    xregs = [QuantumRegister(n_x, 'x' + str(i)) for i in range(m)]
    acc = QuantumRegister(n_acc, 'acc')
    qc = QuantumCircuit(*xregs, acc)
    modulus = 2 ** n_acc
    acc_qubits = list(acc)
    # eq_1: enter Fourier domain on the accumulator
    qc.append(QFTGate(n_acc), acc_qubits)
    # eq_2/eq_3: controlled Draper phase additions of w_i * 2^j
    for i in range(m):
        for j in range(n_x):
            sign = -1 if (signed and j == n_x - 1) else 1
            coeff = (sign * weights[i] * (2 ** j)) % modulus
            if coeff == 0:
                continue
            for t in range(n_acc):
                angle = 2.0 * math.pi * coeff * (2 ** t) / modulus
                qc.cp(angle, xregs[i][j], acc[t])
    qc.append(QFTGate(n_acc).inverse(), acc_qubits)
    return qc
