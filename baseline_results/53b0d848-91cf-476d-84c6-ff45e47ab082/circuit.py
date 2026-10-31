"""Single-ancilla Stinespring dilation circuit for one generalized extreme qubit channel.

Implements eq_3 (dilation U_k with one ancilla) for a channel of Kraus rank <= 2
(eq_2) on a single system qubit (d = 2).  Canonical Kraus form (eq_2, RSW form):
    K_0 = diag(cos v0, cos v1),   K_1 = sin v1 |0><1| + sin v0 |1><0|
so that K_0^dag K_0 + K_1^dag K_1 = 1.  The dilation acts as
    |0>_S|0>_A -> cos v0 |0>_S|0>_A + sin v0 |1>_S|1>_A
    |1>_S|0>_A -> cos v1 |1>_S|0>_A + sin v1 |0>_S|1>_A
and is realised by Ry(2 v0) on A, controlled-Ry(2(v1 - v0)) S->A, CNOT A->S.
Amplitude damping (eq_6, U_1) is v0 = 0, v1 = arcsin(sqrt(gamma)).
The unitary extreme channel X.X (eq_6, U_2) is the 'unitary' channel type.

Layout: qubit 0 = system S (channel input/output), qubit 1 = ancilla A
(must be supplied in |0> by the runner and traced out afterwards).
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
SUPPORTED_DIMENSION = 2
PAULI_LABELS = ("I", "X", "Y", "Z")


def _as_real(value, name):
    """Validate a finite real number taken from the instance."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("parameter '%s' must be a real number" % name)
    out = float(value)
    if not math.isfinite(out):
        raise ValueError("parameter '%s' must be finite" % name)
    return out


def _channel_angles(channel):
    """Return (v0, v1) for a rank-2 extreme channel, or None for a unitary channel.

    eq_2: Kraus operators K_0 = diag(cos v0, cos v1), K_1 = sin v1 |0><1| + sin v0 |1><0|.
    """
    if not isinstance(channel, dict) or "type" not in channel:
        raise ValueError("instance['channel'] must be a dict with a 'type' key")
    ctype = channel["type"]
    if ctype == "amplitude_damping":
        # eq_6: K_0 = |0><0| + sqrt(1-gamma)|1><1|, K_1 = sqrt(gamma)|0><1|
        if "gamma" not in channel:
            raise ValueError("amplitude_damping channel requires 'gamma'")
        gamma = _as_real(channel["gamma"], "gamma")
        if gamma < 0.0 or gamma > 1.0:
            raise ValueError("gamma must lie in [0, 1]")
        return 0.0, math.asin(math.sqrt(gamma))
    if ctype == "extreme":
        if "v0" not in channel or "v1" not in channel:
            raise ValueError("extreme channel requires 'v0' and 'v1'")
        return _as_real(channel["v0"], "v0"), _as_real(channel["v1"], "v1")
    if ctype == "unitary":
        if "pauli" not in channel or channel["pauli"] not in PAULI_LABELS:
            raise ValueError("unitary channel requires 'pauli' in %s" % (PAULI_LABELS,))
        return None
    raise ValueError("unknown channel type '%s'" % str(ctype))


def build_circuit(instance):
    """Build the dilation unitary U_k (eq_3) for one generalized extreme qubit channel.

    instance = {"d": 2, "channel": {...}} with channel one of
      {"type": "amplitude_damping", "gamma": g}        (eq_6, U_1)
      {"type": "extreme", "v0": a, "v1": b}            (eq_2 canonical form)
      {"type": "unitary", "pauli": "X"}                (eq_6, U_2)
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "d" not in instance or isinstance(instance["d"], bool) or not isinstance(instance["d"], int):
        raise ValueError("instance must provide integer 'd'")
    d = instance["d"]
    if d != SUPPORTED_DIMENSION:
        raise ValueError("only qubit channels (d = 2) are supported in this module")
    if "channel" not in instance:
        raise ValueError("instance must provide 'channel'")
    angles = _channel_angles(instance["channel"])

    n_system = 1
    n_ancilla = 1
    if n_system + n_ancilla > MAX_QUBITS:
        raise ValueError("qubit budget exceeded")

    system = QuantumRegister(n_system, "s")
    ancilla = QuantumRegister(n_ancilla, "a")
    qc = QuantumCircuit(system, ancilla, name="extreme_channel_dilation")
    s = system[0]
    a = ancilla[0]

    if angles is None:
        # eq_6 (U_2 = X_S tensor 1_A): unitary (Kraus rank 1) extreme channel, no ancilla action.
        pauli = instance["channel"]["pauli"]
        if pauli == "X":
            qc.x(s)
        elif pauli == "Y":
            qc.y(s)
        elif pauli == "Z":
            qc.z(s)
        else:
            qc.id(s)
        qc.id(a)
        return qc

    v0, v1 = angles
    # eq_3: isometry |psi>_S|0>_A -> sum_i (K_i |psi>)_S |i>_A.
    # Step 1: ancilla rotation conditioned on system basis state:
    #   S=0 -> Ry(2 v0) on A  (|0>_A -> cos v0 |0> + sin v0 |1>)
    #   S=1 -> Ry(2 v1) on A  (|0>_A -> cos v1 |0> + sin v1 |1>)
    if v0 != 0.0:
        qc.ry(2.0 * v0, a)
    if v1 - v0 != 0.0:
        qc.cry(2.0 * (v1 - v0), s, a)
    # Step 2: K_1 is off-diagonal, so flip the system whenever ancilla records index 1.
    qc.cx(a, s)
    return qc
