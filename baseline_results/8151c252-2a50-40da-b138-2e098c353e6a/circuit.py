"""Simon's algorithm (circuit model) as a measurement-free unitary operation.

Registers: input register x (n qubits) and output register y (n qubits).
Bit convention: the specification writes |x_1 x_2 ... x_n> with x_1 the most
significant bit; Qiskit qubit 0 is the least significant bit, so x_i lives on
qubit (n - i) of the input register and y_i on qubit (n - i) of the output
register.  The hidden string s is given as the string "s_1 s_2 ... s_n".

Oracle family (eq_2, eq_5): let j be the first index with s_j = 1 (pivot).
    f(x) = x xor (x_j * s)
so f(x) = x if x_j = 0 and f(x) = x xor s if x_j = 1.  This satisfies Simon's
promise (eq_1): f(x) = f(x xor s) and distinct cosets map to distinct values
(the value is the coset representative with bit j cleared).  For s = 0^n the
oracle is f(x) = x (1-to-1 case).  For n = 2, s = 11 the construction is
exactly eq_5: f(x1, x2) = (0, x1 xor x2), U_f = CNOT_{x1,y2} CNOT_{x2,y2}.
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _parse_instance(instance):
    """Validate the instance dictionary and return (n, s_bits, include_hadamards)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("'n' must be an integer")
    if n < 1:
        raise ValueError("'n' must be at least 1")
    if 2 * n > MAX_QUBITS:
        raise ValueError("2*n qubits exceed the cap of %d" % MAX_QUBITS)
    s = instance.get("s")
    if not isinstance(s, str) or len(s) != n:
        raise ValueError("'s' must be a bit string of length n")
    for c in s:
        if c not in ("0", "1"):
            raise ValueError("'s' must contain only '0' and '1'")
    s_bits = [int(c) for c in s]  # s_bits[i] = s_{i+1}, index 0 is the MSB s_1
    include_h = instance.get("include_hadamards", True)
    if not isinstance(include_h, bool):
        raise ValueError("'include_hadamards' must be a boolean")
    for key in instance:
        if key not in ("n", "s", "include_hadamards"):
            raise ValueError("unknown instance key: %s" % str(key))
    return n, s_bits, include_h


def _apply_oracle(qc, xr, yr, s_bits):
    """Append U_f (eq_2) for f(x) = x xor (x_j * s), eq_5 for n=2, s=11.

    Step A: y_i ^= x_i for all i != j   (copy x into y; the pair of CNOTs
            x_j -> y_j from the copy and from the mask step cancel and are
            omitted).
    Step B: y_i ^= x_j for all i != j with s_i = 1  (adds x_j * s).
    """
    n = len(s_bits)
    pivot = None
    for i in range(n):
        if s_bits[i] == 1:
            pivot = i
            break
    # Step A
    for i in range(n):
        if i != pivot:
            qc.cx(xr[n - 1 - i], yr[n - 1 - i])
    # Step B
    if pivot is not None:
        for i in range(n):
            if s_bits[i] == 1 and i != pivot:
                qc.cx(xr[n - 1 - pivot], yr[n - 1 - i])


def build_circuit(instance):
    """Return the Simon operation (H^n x I) U_f (H^n x I) as a QuantumCircuit (eq_3).

    instance keys:
      n (int): number of input bits, 1 <= n <= 6.
      s (str): hidden string "s_1...s_n" (s_1 most significant).
      include_hadamards (bool, optional, default True): if False only U_f is
          returned.
    Qubits 0..n-1 form the input register (x_i on qubit n-i), qubits n..2n-1
    the output register (y_i on qubit n + n - i).
    """
    n, s_bits, include_h = _parse_instance(instance)
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(n, "y")
    qc = QuantumCircuit(xr, yr, name="simon_n%d_s%s" % (n, "".join(str(b) for b in s_bits)))
    # eq_3: first Hadamard layer on the input register
    if include_h:
        for q in xr:
            qc.h(q)
    # eq_2 / eq_5: oracle
    _apply_oracle(qc, xr, yr, s_bits)
    # eq_3: second Hadamard layer on the input register
    if include_h:
        for q in xr:
            qc.h(q)
    return qc
