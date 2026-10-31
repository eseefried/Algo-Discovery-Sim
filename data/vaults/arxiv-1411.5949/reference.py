"""Reference: Draper-style QFT adder (Sec. 3-4). QFT on the target register, controlled phase
rotations from the operand register, inverse QFT. No ancillas; overflow wraps mod 2^m."""

from math import pi

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate


def build_circuit(spec):
    m = spec["m"]
    a = list(range(m))
    b = list(range(m, 2 * m))
    qc = QuantumCircuit(2 * m)
    qc.append(QFTGate(m), b)
    for i in range(m):              # a_i has weight 2^i
        for j in range(m):          # Fourier qubit j of b carries phase 2*pi*x*2^j / 2^m
            if i + j < m:
                qc.cp(2 * pi * 2 ** (i + j) / 2**m, a[i], b[j])
    qc.append(QFTGate(m).inverse(), b)
    return qc
