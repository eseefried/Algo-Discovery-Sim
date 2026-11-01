from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _is_real(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def build_circuit(instance):
    """Level-one QAOA operation U = exp(-i beta B) exp(-i gamma C) for E3LIN2.

    instance: {"n": int 1..12, "equations": [[a,b,c,bit],...],
               "gamma": float, "beta": float, optional "D": int max occurrence}
    Qubit j encodes variable x_j (Z eigenvalue (-1)^x_j). No state prep.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if not _is_int(n) or n < 3 or n > 12:
        raise ValueError("n must be an integer in [3, 12]")
    eqs = instance.get("equations")
    if not isinstance(eqs, (list, tuple)) or len(eqs) < 1 or len(eqs) > 200:
        raise ValueError("equations must be a list of 1..200 entries")
    gamma = instance.get("gamma")
    beta = instance.get("beta")
    if not _is_real(gamma) or not _is_real(beta):
        raise ValueError("gamma and beta must be finite real numbers")
    gamma = float(gamma)
    beta = float(beta)
    clauses = []
    counts = [0] * n
    for eq in eqs:
        if not isinstance(eq, (list, tuple)) or len(eq) != 4:
            raise ValueError("each equation must be [a, b, c, bit]")
        a, b, c, bit = eq
        for v in (a, b, c):
            if not _is_int(v) or v < 0 or v >= n:
                raise ValueError("variable index out of range")
        if len({a, b, c}) != 3:
            raise ValueError("equation variables must be distinct")
        if not _is_int(bit) or bit not in (0, 1):
            raise ValueError("right-hand side bit must be 0 or 1")
        for v in (a, b, c):
            counts[v] += 1
        clauses.append((a, b, c, bit))
    if "D" in instance:
        d = instance["D"]
        if not _is_int(d) or d < 1:
            raise ValueError("D must be a positive integer")
        if max(counts) > d:
            raise ValueError("a variable occurs in more than D equations")
    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    # Phase separation: exp(-i gamma (1 + s Z Z Z)/2) per clause
    for a, b, c, bit in clauses:
        s = -1.0 if bit == 1 else 1.0
        qc.cx(a, c)
        qc.cx(b, c)
        qc.rz(gamma * s, c)  # exp(-i gamma s/2 Z_a Z_b Z_c)
        qc.cx(b, c)
        qc.cx(a, c)
    qc.global_phase += -gamma * len(clauses) / 2.0  # the constant 1/2 in each C_k
    # Mixer: exp(-i beta X) = RX(2 beta) on each qubit
    for j in range(n):
        qc.rx(2.0 * beta, j)
    return qc
