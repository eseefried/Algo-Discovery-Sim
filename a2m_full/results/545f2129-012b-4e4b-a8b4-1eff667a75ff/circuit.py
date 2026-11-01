import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _isint(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _default_m(n, weights, signed):
    # smallest accumulator size that avoids overflow for all inputs
    if signed:
        xl, xh = -(2 ** (n - 1)), 2 ** (n - 1) - 1
    else:
        xl, xh = 0, 2 ** n - 1
    lo = sum(min(w * xl, w * xh) for w in weights)
    hi = sum(max(w * xl, w * xh) for w in weights)
    if lo >= 0:
        return max(1, hi.bit_length())
    return max(hi.bit_length(), (-lo - 1).bit_length()) + 1


def build_circuit(instance):
    """Weighted sum into accumulator via Draper QFT phase addition.
    instance: {'n': bits per input, 'weights': [ints], 'm': optional accumulator size,
    'signed_inputs': optional bool}.
    Qubits: input j bit i -> index j*n+i; accumulator bit l -> index k*n+l."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    n = instance.get('n')
    weights = instance.get('weights')
    m = instance.get('m')
    signed = instance.get('signed_inputs')
    if signed is None:
        signed = False
    if not isinstance(signed, bool):
        raise ValueError('signed_inputs must be a boolean')
    if not _isint(n) or n < 1 or n > 10:
        raise ValueError('n must be an integer in 1..10')
    if not isinstance(weights, list) or len(weights) == 0 or len(weights) > 12:
        raise ValueError('weights must be a non-empty list')
    if not all(_isint(w) for w in weights) or any(abs(w) > 4096 for w in weights):
        raise ValueError('weights must be integers with |w| <= 4096')
    k = len(weights)
    if m is None:
        m = _default_m(n, weights, signed)
    elif not _isint(m) or m < 1:
        raise ValueError('m must be a positive integer')
    if k * n + m > 12:
        raise ValueError('total qubits exceed 12')
    xs = [QuantumRegister(n, 'x' + str(j)) for j in range(k)]
    acc = QuantumRegister(m, 'A')
    qc = QuantumCircuit(*xs, acc)
    acc_idx = list(range(k * n, k * n + m))
    mod = 2 ** m
    qc.append(QFTGate(m), acc_idx)
    for j in range(k):
        for i in range(n):
            coef = weights[j] * (-(2 ** (n - 1)) if (signed and i == n - 1) else 2 ** i)
            for l in range(m):
                # QFTGate (with swaps): qubit l carries phase 2*pi*a*2^l/2^m
                val = (coef * (2 ** l)) % mod
                if val:
                    qc.cp(2.0 * math.pi * val / mod, xs[j][i], acc[l])
    qc.append(QFTGate(m).inverse(), acc_idx)
    return qc
