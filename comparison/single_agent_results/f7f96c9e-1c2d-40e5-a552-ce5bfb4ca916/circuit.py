from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        if isinstance(v, float) and v == int(v) and not isinstance(v, bool):
            return int(v)
        raise ValueError(name + ' must be an integer')
    return v


def build_circuit(instance):
    """Controlled weighted sum in the Fourier domain.

    instance: {'n': accumulator qubits, 'weights': list of classical integer weights}.
    One single-qubit input per weight. Layout: inp qubits 0..m-1 (x_j = qubit j-1),
    acc qubits m..m+n-1 (little-endian: acc bit t is qubit m+t).
    Operation: |x>|a> -> |x>|(a + sum_j w_j x_j) mod 2^n>.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    if 'n' not in instance or 'weights' not in instance:
        raise ValueError('instance needs n and weights')
    n = _as_int(instance['n'], 'n')
    weights = instance['weights']
    if not isinstance(weights, (list, tuple)):
        raise ValueError('weights must be a list')
    m = len(weights)
    if n < 1 or m < 1:
        raise ValueError('n and number of weights must be positive')
    if n + m > 12:
        raise ValueError('total qubits exceed 12')
    ws = [_as_int(w, 'weight') for w in weights]
    inp = QuantumRegister(m, 'inp')
    acc = QuantumRegister(n, 'acc')
    qc = QuantumCircuit(inp, acc)
    acc_idx = list(range(m, m + n))
    # eq_1: QFT on accumulator (QFTGate includes bit reversal; little-endian acc)
    qc.append(QFTGate(n), acc_idx)
    # eq_2/eq_3: controlled Phi(w_j); phase on acc bit t is 2*pi*w/2^(n-t)
    # (spec qubit l = n-t in big-endian numbering, R_l angle 2*pi*c/2^l)
    for j in range(m):
        wm = ws[j] % (2 ** n)
        if wm == 0:
            continue
        for t in range(n):
            if (wm * (2 ** t)) % (2 ** n) == 0:
                continue
            angle = 2.0 * math.pi * wm / (2 ** (n - t))
            qc.cp(angle, j, m + t)
    # inverse QFT on the same indices
    qc.append(QFTGate(n).inverse(), acc_idx)
    return qc
