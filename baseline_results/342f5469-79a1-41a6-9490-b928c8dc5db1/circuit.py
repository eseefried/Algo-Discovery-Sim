"""Single-qubit robust phase estimation circuits for amplitude-error estimation.

Scoped construction: gate under test G(theta) = exp(-i theta X / 2) with
theta = pi/2 + epsilon (eq_1), applied k = 2**j times to one qubit, followed by
an optional Y-basis change (S^dagger, H) so that a computational-basis outcome 0
corresponds to the +y eigenstate (eq_3). The Z-basis variant applies no basis
change (eq_2). No state preparation or measurement is included.

Instance keys:
  "epsilon" (float): amplitude error, theta = pi/2 + epsilon; or
  "theta"   (float): rotation angle directly (overrides epsilon if both given)
  "k"       (int)  : number of gate repetitions; or
  "round"   (int)  : round index j >= 0, k = 2**j (used if "k" is absent)
  "basis"   (str)  : "Z" or "Y" (measurement basis variant)
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_REPETITIONS = 4096
MAX_ROUND = 12
NUM_SYSTEM_QUBITS = 1


def _as_int(value, name):
    """Return value as a Python int, rejecting bools and non-integers."""
    if isinstance(value, bool):
        raise ValueError(name + " must be an integer, not a bool")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    raise ValueError(name + " must be an integer")


def _as_float(value, name):
    """Return value as a finite float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a real number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(name + " must be finite")
    return out


def _resolve_theta(instance):
    """eq_1: theta = pi/2 + epsilon (or theta given directly)."""
    if "theta" in instance:
        return _as_float(instance["theta"], "theta")
    if "epsilon" in instance:
        epsilon = _as_float(instance["epsilon"], "epsilon")
        return 0.5 * math.pi + epsilon
    raise ValueError("instance must provide 'theta' or 'epsilon'")


def _resolve_k(instance):
    """Number of repetitions k; from 'k' directly or k = 2**round."""
    if "k" in instance:
        k = _as_int(instance["k"], "k")
    elif "round" in instance:
        j = _as_int(instance["round"], "round")
        if j < 0 or j > MAX_ROUND:
            raise ValueError("round must satisfy 0 <= round <= " + str(MAX_ROUND))
        k = 2 ** j
    else:
        raise ValueError("instance must provide 'k' or 'round'")
    if k < 1 or k > MAX_REPETITIONS:
        raise ValueError("k must satisfy 1 <= k <= " + str(MAX_REPETITIONS))
    return k


def _resolve_basis(instance):
    """Measurement-basis variant: 'Z' (eq_2) or 'Y' (eq_3)."""
    if "basis" not in instance:
        raise ValueError("instance must provide 'basis' ('Z' or 'Y')")
    basis = instance["basis"]
    if not isinstance(basis, str):
        raise ValueError("basis must be a string")
    basis = basis.strip().upper()
    if basis not in ("Z", "Y"):
        raise ValueError("basis must be 'Z' or 'Y'")
    return basis


def build_circuit(instance):
    """Build the unitary part of one robust-phase-estimation circuit.

    Returns a 1-qubit QuantumCircuit implementing G(theta)^k followed by the
    optional Y-basis change. Input state |0> and measurement are supplied by
    the runner.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    theta = _resolve_theta(instance)
    k = _resolve_k(instance)
    basis = _resolve_basis(instance)

    num_qubits = NUM_SYSTEM_QUBITS
    if num_qubits < 1 or num_qubits > MAX_QUBITS:
        raise ValueError("qubit count out of range")

    qr = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(qr, name="rpe_k%d_%s" % (k, basis))

    # eq_1: G(theta) = exp(-i theta X / 2) == rx(theta); applied k times.
    for _ in range(k):
        qc.rx(theta, qr[0])

    if basis == "Y":
        # eq_3: Y-basis readout. S^dagger then H maps |+y> -> |0>, so the
        # runner's computational-basis outcome 0 has probability (1 - sin(k theta))/2.
        qc.sdg(qr[0])
        qc.h(qr[0])
    # else: eq_2: Z-basis readout, no basis change; outcome 0 has
    # probability (1 + cos(k theta))/2 for input |0>.

    return qc
