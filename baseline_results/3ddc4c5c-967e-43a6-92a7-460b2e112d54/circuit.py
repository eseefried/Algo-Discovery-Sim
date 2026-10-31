"""One-ancilla Repeat-Until-Success (RUS) primitive: single-attempt unitary.

Qubit layout (Qiskit little-endian):
  qubit 0 : target t  (receives e^{-i theta X} on RUS success)
  qubit 1 : ancilla a (runner prepares |0>, measures in Z after this circuit)

Conventions: rx(lam) = exp(-i lam X / 2), so e^{-i phi X} = rx(2 phi).
The controlled-(-iX) = controlled-exp(-i pi X / 2) is realised as CX(a->t) then Sdg on a
(the phase -i is attached to the control=|1> branch).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_angle(value, name):
    """Validate a real, finite angle supplied in the instance."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return x


def build_circuit(instance):
    """Return the pre-measurement unitary of one RUS attempt.

    instance keys (exactly one form):
      {"phi": float}                 -> squaring primitive, phi1 = phi2 = phi  (eq_2)
      {"phi1": float, "phi2": float} -> product-of-tangents primitive          (eq_4)
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    allowed = {"phi", "phi1", "phi2"}
    unknown = set(instance.keys()) - allowed
    if unknown:
        raise ValueError(f"unknown instance keys: {sorted(unknown)}")
    if "phi" in instance:
        if "phi1" in instance or "phi2" in instance:
            raise ValueError("supply either 'phi' or both 'phi1' and 'phi2', not a mixture")
        phi1 = _as_angle(instance["phi"], "phi")
        phi2 = phi1
    elif "phi1" in instance and "phi2" in instance:
        phi1 = _as_angle(instance["phi1"], "phi1")
        phi2 = _as_angle(instance["phi2"], "phi2")
    else:
        raise ValueError("instance must contain 'phi' or both 'phi1' and 'phi2'")

    n_qubits = 2  # one target + one ancilla
    if n_qubits > MAX_QUBITS:
        raise ValueError("qubit budget exceeded")

    t = QuantumRegister(1, "t")
    a = QuantumRegister(1, "a")
    qc = QuantumCircuit(t, a, name="rus_attempt")

    # eq_2 / eq_4 step 1: ancilla pre-rotation e^{-i phi1 X} = rx(2 phi1)
    qc.rx(2.0 * phi1, a[0])

    # eq_2 step 2: controlled-(e^{-i pi X/2}) = controlled-(-iX), ancilla control, target target.
    # CX applies X on t when a=|1>; Sdg on a supplies the -i phase on the a=|1> branch.
    qc.cx(a[0], t[0])
    qc.sdg(a[0])

    # eq_2 / eq_4 step 3: ancilla post-rotation e^{+i phi2 X} = rx(-2 phi2)
    qc.rx(-2.0 * phi2, a[0])

    # Measurement of a (eq_3) and repeat-on-failure (eq_6) are performed by the runner.
    return qc
