from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
import math


def build_circuit(instance):
    """Draper QFT constant adder |x> -> |x+a mod 2^n>, optionally controlled.

    instance: {"n": int, "a": int, "controlled": bool (optional)}
    Qubits 0..n-1: data register (qubit 0 least significant).
    Qubit n (only if controlled): control qubit.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    a = instance.get("a")
    controlled = instance.get("controlled", False)
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if isinstance(a, bool) or not isinstance(a, int):
        raise ValueError("a must be an integer")
    if not isinstance(controlled, bool):
        raise ValueError("controlled must be a boolean")
    extra = 1 if controlled else 0
    if n < 1 or n + extra > 12:
        raise ValueError("n must satisfy 1 <= n and n + control qubit <= 12")
    dim = 2 ** n
    if a < 0 or a >= dim:
        raise ValueError("a must satisfy 0 <= a < 2^n")

    qc = QuantumCircuit(n + extra)
    targets = list(range(n))
    # eq_1: QFT on the data register (QFTGate includes bit reversal, so Fourier index k has qubit q with weight 2^q)
    qc.append(QFTGate(n), targets)
    # eq_2: phase exp(2*pi*i*a*k/2^n) = product over qubits q of exp(2*pi*i*a*2^q*k_q/2^n)
    for q in range(n):
        angle = 2.0 * math.pi * ((a * (2 ** q)) % dim) / dim
        if controlled:
            qc.cp(angle, n, q)
        else:
            qc.p(angle, q)
    # eq_2: inverse QFT back to the computational basis
    qc.append(QFTGate(n).inverse(), targets)
    return qc
