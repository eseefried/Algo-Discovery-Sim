"""Ternary SWAP gate (eq_6) synthesised from ternary controlled-X gates (eq_2)
on qubit-encoded qutrits.

Qutrit encoding: a qutrit occupies two qubits (q_low, q_high) with value
j = q_low + 2*q_high, j in {0,1,2}; the pattern |11> (j=3) is unused and is
mapped to itself by every gate so that all operations are permutations.

For pair p the first qutrit (q_1 of the specification, control of TCX_{1->2})
is on qubits (4p, 4p+1) and the second qutrit (q_2) on qubits (4p+2, 4p+3).
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
QUBITS_PER_PAIR = 4


def _transposition_01(qc, ctrl, t0, t1):
    """(Controlled) swap of |0>=|00> and |1>=|01> on target qutrit bits (t1 t0):
    flip t0 when t1 == 0.  ctrl is a qubit index or None (uncontrolled)."""
    qc.x(t1)
    if ctrl is None:
        qc.cx(t1, t0)
    else:
        qc.ccx(ctrl, t1, t0)
    qc.x(t1)


def _transposition_02(qc, ctrl, t0, t1):
    """(Controlled) swap of |0>=|00> and |2>=|10>: flip t1 when t0 == 0."""
    qc.x(t0)
    if ctrl is None:
        qc.cx(t0, t1)
    else:
        qc.ccx(ctrl, t0, t1)
    qc.x(t0)


def _controlled_shift(qc, ctrl, t0, t1, power):
    """eq_1: (controlled) X_3^power on the target qutrit (t0 low bit, t1 high bit).
    X_3 = (0 2)(0 1) and X_3^2 = (0 1)(0 2) as permutation products acting
    right-to-left; power 0 is the identity."""
    if power == 0:
        return
    if power == 1:
        _transposition_01(qc, ctrl, t0, t1)
        _transposition_02(qc, ctrl, t0, t1)
    elif power == 2:
        _transposition_02(qc, ctrl, t0, t1)
        _transposition_01(qc, ctrl, t0, t1)
    else:
        raise ValueError("power must be 0, 1 or 2")


def _tcx(qc, c0, c1, t0, t1, power):
    """eq_2: TCX^power with control qutrit (c0, c1) and target qutrit (t0, t1):
    |a>|b> -> |a>|b + power*a mod 3>.  With a = c0 + 2*c1 this equals
    C_{c0}(X_3^power) * C_{c1}(X_3^(2*power mod 3)); the two factors commute.
    power=1 is TCX, power=2 is TCX^{-1} = TCX^2."""
    _controlled_shift(qc, c0, t0, t1, power % 3)
    _controlled_shift(qc, c1, t0, t1, (2 * power) % 3)


def _negation(qc, q0, q1):
    """eq_6 one-qutrit factor F_3^2: |j> -> |-j mod 3>, i.e. |1>=|01> <-> |2>=|10>,
    which is a qubit SWAP inside the qutrit (|00> and |11> fixed)."""
    qc.swap(q0, q1)


def build_circuit(instance):
    """Return the ternary SWAP circuit (eq_6) acting on num_pairs qutrit pairs.

    instance keys:
      num_pairs : int in {1,2,3}; number of independent qutrit pairs (4 qubits each).
      variant   : 'A' -> SWAP_3 = (F_3^2 x I) TCX_{1->2} TCX_{2->1}^{-1} TCX_{1->2}  (eq_6)
                  'B' -> SWAP_3 = (I x F_3^2) TCX_{1->2}^{-1} TCX_{2->1} TCX_{1->2}^{-1}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    allowed = {"num_pairs", "variant"}
    for key in instance:
        if key not in allowed:
            raise ValueError("unknown instance key: %s" % str(key))
    num_pairs = instance.get("num_pairs", 1)
    variant = instance.get("variant", "A")
    if isinstance(num_pairs, bool) or not isinstance(num_pairs, int):
        raise ValueError("num_pairs must be an int")
    if num_pairs < 1:
        raise ValueError("num_pairs must be >= 1")
    if variant not in ("A", "B"):
        raise ValueError("variant must be 'A' or 'B'")
    n_qubits = QUBITS_PER_PAIR * num_pairs
    if n_qubits > MAX_QUBITS:
        raise ValueError("too many qubits: %d > %d" % (n_qubits, MAX_QUBITS))

    qr = QuantumRegister(n_qubits, "q")
    qc = QuantumCircuit(qr, name="ternary_swap_" + variant)

    for p in range(num_pairs):
        a0 = QUBITS_PER_PAIR * p        # qutrit 1 low bit
        a1 = QUBITS_PER_PAIR * p + 1    # qutrit 1 high bit
        b0 = QUBITS_PER_PAIR * p + 2    # qutrit 2 low bit
        b1 = QUBITS_PER_PAIR * p + 3    # qutrit 2 high bit
        if variant == "A":
            # eq_6, operators applied in time order (right-to-left in the formula):
            # |a,b> -> |a,a+b> -> |-b,a+b> -> |-b,a> -> |b,a>
            _tcx(qc, a0, a1, b0, b1, 1)   # TCX_{1->2}
            _tcx(qc, b0, b1, a0, a1, 2)   # TCX_{2->1}^{-1} = TCX_{2->1}^2
            _tcx(qc, a0, a1, b0, b1, 1)   # TCX_{1->2}
            _negation(qc, a0, a1)         # F_3^2 on qutrit 1
        else:
            # mirror variant: |a,b> -> |a,b-a> -> |b,b-a> -> |b,-a> -> |b,a>
            _tcx(qc, a0, a1, b0, b1, 2)   # TCX_{1->2}^{-1}
            _tcx(qc, b0, b1, a0, a1, 1)   # TCX_{2->1}
            _tcx(qc, a0, a1, b0, b1, 2)   # TCX_{1->2}^{-1}
            _negation(qc, b0, b1)         # F_3^2 on qutrit 2
    return qc
