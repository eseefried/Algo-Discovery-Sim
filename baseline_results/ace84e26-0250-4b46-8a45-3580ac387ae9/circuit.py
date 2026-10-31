"""Single-qudit permutation-class ('parity') algorithm for a ququart.

Implements the operation  F^dagger . U_sigma . F  (eq_5) on one qudit of
dimension d = 2**n, encoded in n qubits.  For the paper's ququart, d = 4 and
n = 2.  U_sigma is one of the 2d dihedral permutations (eq_3):
    shift      sigma^+_m(k) = k + m  (mod d)
    reflection sigma^-_m(k) = m - k  (mod d)
The runner prepares the input |1> and measures; ideal outcome is 1 for the
shift class and d-1 for the reflection class (eq_5).

Register layout (eq_1): computational label k = sum_i 2**i * bit_i, with Qiskit
qubit 0 the least significant bit.  For d = 4 this means q[0] = polarization
bit p (H=0, V=1) and q[1] = spatial-mode bit s, so k = 2*s + p.
"""
from __future__ import annotations

import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _validate(instance):
    """Validate the instance dictionary and return (d, n, m, perm_class)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    if "d" not in instance or "m" not in instance or "perm_class" not in instance:
        raise ValueError("instance must contain keys 'd', 'm' and 'perm_class'")
    d = instance["d"]
    if isinstance(d, bool) or not isinstance(d, int):
        raise ValueError("d must be an integer")
    if d < 2 or (d & (d - 1)) != 0:
        raise ValueError("d must be a power of two >= 2 (ququart: d=4)")
    n = d.bit_length() - 1
    if n > MAX_QUBITS:
        raise ValueError("d = 2**n requires n <= %d qubits" % MAX_QUBITS)
    m = instance["m"]
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError("m must be an integer")
    if m < 0 or m >= d:
        raise ValueError("m must satisfy 0 <= m < d")
    cls = instance["perm_class"]
    if not isinstance(cls, str):
        raise ValueError("perm_class must be a string")
    cls_l = cls.strip().lower()
    if cls_l in ("shift", "+", "even", "cyclic"):
        perm_class = "shift"
    elif cls_l in ("reflection", "-", "odd", "anticyclic"):
        perm_class = "reflection"
    else:
        raise ValueError("perm_class must be 'shift' ('+') or 'reflection' ('-')")
    return d, n, m, perm_class


def _add_power_of_two(qc, qubits, i):
    """Apply |x> -> |x + 2**i mod 2**n> via an incrementer on qubits[i:]."""
    sub = qubits[i:]
    r = len(sub)
    for j in range(r - 1, 0, -1):
        qc.mcx(sub[:j], sub[j])
    qc.x(sub[0])


def _add_constant(qc, qubits, c, d):
    """Apply |x> -> |x + c mod d> (d = 2**n) using incrementers (eq_3, shifts)."""
    c = c % d
    n = len(qubits)
    for i in range(n):
        if (c >> i) & 1:
            _add_power_of_two(qc, qubits, i)


def _permutation_oracle(qc, qubits, perm_class, m, d):
    """Black-box permutation unitary U_sigma |k> = |sigma(k)>  (eq_3).

    shift:      k -> k + m (mod d)
    reflection: k -> m - k (mod d), realized as bitwise complement
                k -> d-1-k followed by addition of (m+1) mod d.
    """
    if perm_class == "reflection":
        for q in qubits:
            qc.x(q)
        _add_constant(qc, qubits, m + 1, d)
    else:
        _add_constant(qc, qubits, m, d)


def build_circuit(instance):
    """Return the unitary F^dagger U_sigma F on n = log2(d) qubits (eq_5).

    instance keys:
        d          : qudit dimension, power of two (4 for the ququart)
        perm_class : 'shift' ('+') or 'reflection' ('-')
        m          : permutation parameter in Z_d
    """
    d, n, m, perm_class = _validate(instance)
    q = QuantumRegister(n, "q")
    qc = QuantumCircuit(q, name="perm_parity_d%d_%s_m%d" % (d, perm_class, m))
    qubits = list(range(n))
    # eq_2: Fourier transform F|j> = d^{-1/2} sum_k omega^{jk}|k>, omega = exp(2 pi i / d).
    # QFTGate(n) uses exactly this convention with qubit 0 as the least significant bit.
    qc.append(QFTGate(n), qubits)
    # eq_3 / eq_4: single query of the permutation black box.
    _permutation_oracle(qc, qubits, perm_class, m, d)
    # eq_5: inverse Fourier transform maps |psi_1> -> |1> and |psi_{d-1}> -> |d-1>.
    qc.append(QFTGate(n).inverse(), qubits)
    return qc
