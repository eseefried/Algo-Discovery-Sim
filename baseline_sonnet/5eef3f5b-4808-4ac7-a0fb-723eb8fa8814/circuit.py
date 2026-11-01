from qiskit import QuantumCircuit
import math

MAX_WORD = 1000
PAULI = ("X", "Y", "Z")
VGATES = ("V1", "V2", "V3", "V1dg", "V2dg", "V3dg")


def build_circuit(instance):
    """Single-qubit circuit for U = g_k ... g_1 (eq_5), where g_1 acts first.

    instance: {"word": [labels]}, labels in X,Y,Z,V1,V2,V3,V1dg,V2dg,V3dg.
    V_k = (I + 2i*sigma_k)/sqrt(5) = exp(i*a*sigma_k) with a = atan(2),
    i.e. R_sigma(-2a) (eq_3, corrected labelling). V_k^dagger = R_sigma(+2a).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    word = instance.get("word")
    if not isinstance(word, list):
        raise ValueError("word must be a list of gate labels")
    if len(word) > MAX_WORD:
        raise ValueError("word too long")
    for g in word:
        if not isinstance(g, str) or (g not in PAULI and g not in VGATES):
            raise ValueError("invalid gate label")
    a = math.atan(2.0)
    qc = QuantumCircuit(1, name="pauli_v_word")
    for g in word:
        if g == "X":
            qc.x(0)
        elif g == "Y":
            qc.y(0)
        elif g == "Z":
            qc.z(0)
        else:
            axis = g[1]
            theta = 2.0 * a if g.endswith("dg") else -2.0 * a
            if axis == "1":
                qc.rx(theta, 0)
            elif axis == "2":
                qc.ry(theta, 0)
            else:
                qc.rz(theta, 0)
    return qc
