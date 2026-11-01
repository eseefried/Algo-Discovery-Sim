import math
from qiskit import QuantumCircuit, QuantumRegister

_CLIFFORD = ("h", "s", "sdg", "x", "y", "z")
_ROT = ("r", "rdg")


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for key in instance:
        if key not in ("n", "word"):
            raise ValueError("unknown instance key")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 2 or n > 1024 or n % 2 != 0:
        raise ValueError("n must be an even integer in [2, 1024]")
    word = instance.get("word")
    if not isinstance(word, (list, tuple)):
        raise ValueError("word must be a list of gate names")
    if len(word) > 500:
        raise ValueError("word too long")
    for tok in word:
        if not isinstance(tok, str) or (tok not in _CLIFFORD and tok not in _ROT):
            raise ValueError("invalid gate token")
    return n, list(word)


def build_circuit(instance):
    """Build the 1-qubit circuit for U = F_1 F_2 ... F_k (matrix-product order).

    Tokens: h, s, sdg, x, y, z (Clifford); r = Rz(pi/n); rdg = Rz(-pi/n).
    The circuit applies F_k first and F_1 last (eq_5 ordering).
    """
    n, word = _validate(instance)
    theta = math.pi / n  # eq_1: rotation angle pi/n
    q = QuantumRegister(1, "q")
    qc = QuantumCircuit(q)
    for tok in reversed(word):
        if tok == "h":
            qc.h(0)
        elif tok == "s":
            qc.s(0)
        elif tok == "sdg":
            qc.sdg(0)
        elif tok == "x":
            qc.x(0)
        elif tok == "y":
            qc.y(0)
        elif tok == "z":
            qc.z(0)
        elif tok == "r":
            qc.rz(theta, 0)  # eq_1: diag(e^{-i pi/2n}, e^{i pi/2n})
        else:
            qc.rz(-theta, 0)
    return qc
