import math
from qiskit import QuantumCircuit

_ALLOWED = ("h", "s", "sdg", "t", "tdg", "x", "z", "w")


def _apply_word(qc, word, target, control):
    """Apply single-qubit word W (time order), optionally controlled (eq_5)."""
    for g in word:
        if control is None:
            if g == "h":
                qc.h(target)
            elif g == "s":
                qc.s(target)
            elif g == "sdg":
                qc.sdg(target)
            elif g == "t":
                qc.t(target)
            elif g == "tdg":
                qc.tdg(target)
            elif g == "x":
                qc.x(target)
            elif g == "z":
                qc.z(target)
            else:
                qc.global_phase += math.pi / 4
        else:
            if g == "h":
                qc.ch(control, target)
            elif g == "s":
                qc.cs(control, target)
            elif g == "sdg":
                qc.csdg(control, target)
            elif g == "t":
                qc.cp(math.pi / 4, control, target)
            elif g == "tdg":
                qc.cp(-math.pi / 4, control, target)
            elif g == "x":
                qc.cx(control, target)
            elif g == "z":
                qc.cz(control, target)
            else:
                qc.p(math.pi / 4, control)


def _two_level(qc, n, j, l, word):
    """Append E_(j,l) = P^dag C(W) P; W index 0 <-> |j>, index 1 <-> |l>."""
    if n == 1:
        _apply_word(qc, word, 0, None)
        return
    d = j ^ l
    perm = False
    if d == 3:
        perm = True
        j = j ^ ((j & 1) << 1)
        l = l ^ ((l & 1) << 1)
        d = j ^ l
    target = 0 if d == 1 else 1
    control = 1 - target
    cbit = (j >> control) & 1
    tbit = (j >> target) & 1
    if perm:
        qc.cx(0, 1)
    if cbit == 0:
        qc.x(control)
    if tbit == 1:
        qc.x(target)
    _apply_word(qc, word, target, control)
    if tbit == 1:
        qc.x(target)
    if cbit == 0:
        qc.x(control)
    if perm:
        qc.cx(0, 1)


def build_circuit(instance):
    """instance: {"n": 1|2, "factors": [{"pair": [j, l], "word": [gate names]}, ...]}.
    Factors are listed in circuit (time) order; the operator is E_m ... E_1 (eq_2)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n not in (1, 2):
        raise ValueError("n must be 1 or 2")
    factors = instance.get("factors")
    if not isinstance(factors, list) or len(factors) == 0 or len(factors) > 60:
        raise ValueError("factors must be a list of 1..60 entries")
    dim = 2 ** n
    parsed = []
    for f in factors:
        if not isinstance(f, dict):
            raise ValueError("bad factor")
        pair = f.get("pair")
        word = f.get("word")
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("pair must have two indices")
        j, l = pair
        for v in (j, l):
            if isinstance(v, bool) or not isinstance(v, int) or v < 0 or v >= dim:
                raise ValueError("pair index out of range")
        if j == l:
            raise ValueError("pair indices must differ")
        if not isinstance(word, list) or len(word) > 200:
            raise ValueError("word must be a list of at most 200 gates")
        for g in word:
            if g not in _ALLOWED:
                raise ValueError("unsupported gate in word")
        parsed.append((j, l, word))
    qc = QuantumCircuit(n)
    for j, l, word in parsed:
        _two_level(qc, n, j, l, word)
    return qc
