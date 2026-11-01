import math
from qiskit import QuantumCircuit, QuantumRegister


def _apply_clifford_word(qc, word):
    """Apply a Clifford word left-to-right in time order on qubit 0."""
    for ch in word:
        if ch == 'H':
            qc.h(0)
        elif ch == 'S':
            qc.s(0)
        elif ch == 'D':
            qc.sdg(0)
        elif ch == 'X':
            qc.x(0)
        elif ch == 'Y':
            qc.y(0)
        elif ch == 'Z':
            qc.z(0)
        else:
            raise ValueError('invalid Clifford letter: use only H,S,D,X,Y,Z')


def build_circuit(instance):
    """Circuit for C_k Rz(pi/n) C_{k-1} ... Rz(pi/n) C_0 (eq_2, eq_3).

    instance: {"n": positive even int, "cliffords": [word_0, ..., word_k]}
    with k >= 0 rotations; word_i are strings over 'HSDXYZ' (may be empty).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError('n must be an integer')
    if n <= 0 or n % 2 != 0 or n > 1000000:
        raise ValueError('n must be a positive even integer')
    words = instance.get('cliffords')
    if not isinstance(words, list) or len(words) < 1 or len(words) > 101:
        raise ValueError('cliffords must be a list of 1..101 strings')
    for w in words:
        if not isinstance(w, str) or len(w) > 64:
            raise ValueError('each Clifford word must be a string of length <= 64')
    for w in words:
        for ch in w:
            if ch not in 'HSDXYZ':
                raise ValueError('invalid Clifford letter: use only H,S,D,X,Y,Z')
    q = QuantumRegister(1, 'q')
    qc = QuantumCircuit(q)
    last = len(words) - 1
    for i, w in enumerate(words):
        _apply_clifford_word(qc, w)
        if i < last:
            # Rz(pi/n) = diag(exp(-i pi/(2n)), exp(i pi/(2n)))
            qc.rz(math.pi / n, 0)
    return qc
