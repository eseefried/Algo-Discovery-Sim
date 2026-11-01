from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Phase encoding exp(-i*phi*n) on an n-qubit little-endian Fock register,
    then optionally H on all qubits (readout basis rotation).
    instance keys: n_qubits (int 1..12), phi (finite real, radians),
    apply_readout_rotation (bool, optional, default True)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n_qubits")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n_qubits must be an integer in 1..12")
    phi = instance.get("phi")
    if isinstance(phi, bool) or not isinstance(phi, (int, float)):
        raise ValueError("phi must be a real number")
    phi = float(phi)
    if not math.isfinite(phi):
        raise ValueError("phi must be finite")
    rot = instance.get("apply_readout_rotation", True)
    if not isinstance(rot, bool):
        raise ValueError("apply_readout_rotation must be a bool")
    reg = QuantumRegister(n, "fock")
    qc = QuantumCircuit(reg)
    # eq_2: exp(-i*phi*nhat) = product_j P(-2^j * phi) on qubit j (bit j of n)
    for j in range(n):
        qc.p(-(2.0 ** j) * phi, reg[j])
    # eq_3: Hadamard rotation of the Fock register (measurement left to runner)
    if rot:
        for j in range(n):
            qc.h(reg[j])
    return qc
