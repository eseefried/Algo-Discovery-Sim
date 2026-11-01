import math
from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Build H^{x3} U_f H^{x3} (or U_f only) for f given by its ANF.

    instance: {"n": 3, "anf_terms": [[1],[2,3]], "include_hadamards": true}
    Each ANF term is a list of distinct variable labels in {1,2,3}; f is the XOR
    of the products of those variables. An empty list is the constant 1.
    Repeated terms cancel under XOR. Variable x_j maps to qubit index 3-j so
    that x = 4 x_1 + 2 x_2 + x_3 matches Qiskit little-endian ordering.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n", 3)
    if isinstance(n, bool) or not isinstance(n, int) or n != 3:
        raise ValueError("only n=3 is supported")
    terms = instance.get("anf_terms")
    if not isinstance(terms, (list, tuple)):
        raise ValueError("anf_terms must be a list of terms")
    inc = instance.get("include_hadamards", True)
    if not isinstance(inc, bool):
        raise ValueError("include_hadamards must be a bool")
    active = set()
    for t in terms:
        if not isinstance(t, (list, tuple)):
            raise ValueError("each term must be a list of labels")
        for j in t:
            if isinstance(j, bool) or not isinstance(j, int) or j < 1 or j > 3:
                raise ValueError("labels must be integers in 1..3")
        if len(set(t)) != len(t):
            raise ValueError("repeated label inside a term")
        key = tuple(sorted(t))
        if key in active:
            active.remove(key)
        else:
            active.add(key)
    qc = QuantumCircuit(QuantumRegister(3, "q"))
    if inc:
        for i in range(3):
            qc.h(i)
    # U_f = prod_S (-1)^{c_S prod_{j in S} x_j}  (ANF decomposition)
    for key in sorted(active):
        idx = [3 - j for j in key]
        if len(idx) == 0:
            qc.global_phase += math.pi
        elif len(idx) == 1:
            qc.z(idx[0])
        elif len(idx) == 2:
            qc.cz(idx[0], idx[1])
        else:
            qc.ccz(idx[0], idx[1], idx[2])
    if inc:
        for i in range(3):
            qc.h(i)
    return qc
