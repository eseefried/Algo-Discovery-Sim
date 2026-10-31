"""Two-query Bernstein-Vazirani identification of an affine Boolean function.

f(x) = a.x xor b  (eq_1), queried through the bit-flip oracle U_f (eq_2).
Query 1 (eq_3): (H^n x I) U_f (H^n x I) on |0^n>|-> leaves (-1)^b |a>|->.
Query 2 (eq_4, modified): U_f applied with the input register already in |a>
and a fresh |0> ancilla gives |f(a)> = |parity(a) xor b>, so b = z xor parity(a).

Qubit layout: qubits 0..n-1 = input x (qubit i holds x_i, x_0 least significant),
qubit n = first ancilla (expected in |1>, the circuit applies H to make |->),
qubit n+1 = second ancilla (expected in |0>), present only if two_query is true.
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in ("n", "a", "b", "two_query"):
        if key not in instance:
            raise ValueError("missing key: " + key)
    n = instance["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    a = instance["a"]
    if not isinstance(a, (list, tuple)) or len(a) != n:
        raise ValueError("a must be a list of exactly n bits")
    a_bits = []
    for v in a:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError("entries of a must be 0 or 1")
        a_bits.append(int(v))
    b = instance["b"]
    if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
        raise ValueError("b must be 0 or 1")
    two_query = instance["two_query"]
    if not isinstance(two_query, bool):
        raise ValueError("two_query must be a boolean")
    total = n + 1 + (1 if two_query else 0)
    if total > MAX_QUBITS:
        raise ValueError("total qubits exceed cap of 12")
    return n, a_bits, int(b), two_query


def _apply_oracle(qc, inputs, target, a_bits, b):
    """Bit-flip oracle U_f|x>|y> = |x>|y xor f(x)> for f(x) = a.x xor b (eq_1, eq_2)."""
    for i, ai in enumerate(a_bits):
        if ai == 1:
            qc.cx(inputs[i], target)
    if b == 1:
        qc.x(target)


def build_circuit(instance):
    """Return the (one- or two-query) affine identification circuit (eq_3, eq_4)."""
    n, a_bits, b, two_query = _validate(instance)
    inp = QuantumRegister(n, "x")
    anc1 = QuantumRegister(1, "y")
    regs = [inp, anc1]
    if two_query:
        anc2 = QuantumRegister(1, "z")
        regs.append(anc2)
    qc = QuantumCircuit(*regs, name="affine_bv")
    # Query 1 (eq_3): H on input register and on the |1> ancilla -> |+>^n |->
    for q in inp:
        qc.h(q)
    qc.h(anc1[0])
    # phase-kickback oracle call (eq_2)
    _apply_oracle(qc, inp, anc1[0], a_bits, b)
    # final Hadamards: input register becomes |a> up to global phase (-1)^b
    for q in inp:
        qc.h(q)
    if two_query:
        # Query 2 (eq_4, modified): evaluate f at x_0 = a into a fresh |0> ancilla
        # giving |f(a)> = |parity(a) xor b>; classically b = z xor parity(a).
        _apply_oracle(qc, inp, anc2[0], a_bits, b)
    return qc
