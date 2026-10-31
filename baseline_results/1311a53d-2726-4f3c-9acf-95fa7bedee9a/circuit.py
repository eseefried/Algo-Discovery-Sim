"""Ideal Toffoli (CCNOT) operation on three qubits of a register.

Implements eq_1 / eq_2 of the specification: the target qubit is flipped iff
both control qubits are 1.  Register convention (eq_1): c_1 is the most
significant bit, t the least significant, x = 4*c_1 + 2*c_2 + t.  Because
Qiskit qubit 0 is the least significant bit, the default layout is
t -> qubit 0, c_2 -> qubit 1, c_1 -> qubit 2.

Scope: logical (ideal) target gate only.  The transmon Hamiltonian,
propagator, fidelity functional and Differential-Evolution optimisation
(eq_3 - eq_6) are not reconstructible from the abstract and are not
implemented here.
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _get_int(instance, key, low, high):
    """Fetch a required integer field and check it lies in [low, high]."""
    if key not in instance:
        raise ValueError("missing required key: " + key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(key + " must be an integer")
    if value < low or value > high:
        raise ValueError(key + " must lie in [" + str(low) + ", " + str(high) + "]")
    return value


def _toffoli_single_shot(qc, c1, c2, t):
    """eq_1 / eq_2: one Toffoli gate, |c1 c2 t> -> |c1, c2, t XOR (c1 AND c2)>."""
    qc.ccx(c1, c2, t)


def _toffoli_decomposed(qc, a, b, c):
    """eq_2 realised by the standard sequential H/T/CX decomposition.

    This is the conventional 'decomposed into single- and two-qubit gates'
    baseline that the abstract contrasts with a single-shot implementation.
    Controls a, b; target c.  Exactly equal to CCX (no relative phases).
    """
    qc.h(c)
    qc.cx(b, c)
    qc.tdg(c)
    qc.cx(a, c)
    qc.t(c)
    qc.cx(b, c)
    qc.tdg(c)
    qc.cx(a, c)
    qc.t(b)
    qc.t(c)
    qc.h(c)
    qc.cx(a, b)
    qc.t(a)
    qc.tdg(b)
    qc.cx(a, b)


def build_circuit(instance):
    """Build the ideal Toffoli operation described by `instance`.

    instance keys:
      num_qubits   : int in [3, 12], total register size
      control_1    : int, qubit index of c_1 (spec: most significant logical bit)
      control_2    : int, qubit index of c_2
      target       : int, qubit index of t (spec: least significant logical bit)
      implementation (optional): 'single_shot' (one CCX, default) or
                                 'decomposed' (H/T/CX sequence)
    All three indices must be distinct.  Qubits not listed are left idle.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    n = _get_int(instance, "num_qubits", 3, MAX_QUBITS)
    c1 = _get_int(instance, "control_1", 0, n - 1)
    c2 = _get_int(instance, "control_2", 0, n - 1)
    t = _get_int(instance, "target", 0, n - 1)
    if len({c1, c2, t}) != 3:
        raise ValueError("control_1, control_2 and target must be distinct qubits")

    mode = "single_shot"
    if "implementation" in instance:
        mode = instance["implementation"]
        if mode not in ("single_shot", "decomposed"):
            raise ValueError("implementation must be 'single_shot' or 'decomposed'")

    qreg = QuantumRegister(n, "q")
    qc = QuantumCircuit(qreg, name="toffoli")
    if mode == "single_shot":
        _toffoli_single_shot(qc, c1, c2, t)
    else:
        _toffoli_decomposed(qc, c1, c2, t)
    return qc
