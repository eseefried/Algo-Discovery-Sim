from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Return H^n . O_f . H^n with phase oracle O_f|x> = (-1)^{f(x)}|x>.

    instance: {"n": int in 1..8, "truth_table": list of 2^n ints in {0,1}},
    where truth_table[x] = f(x) and x = sum_i x_i 2^i (qubit i holds x_i).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 8:
        raise ValueError("n must be an integer in 1..8")
    tt = instance.get("truth_table")
    if not isinstance(tt, list) or len(tt) != 2 ** n:
        raise ValueError("truth_table must be a list of length 2^n")
    for v in tt:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError("truth_table entries must be 0 or 1")
    reg = QuantumRegister(n, "x")
    qc = QuantumCircuit(reg)
    # step 1: Hadamards on the input register (eq_2)
    for q in range(n):
        qc.h(q)
    # step 2: phase oracle (-1)^{f(x)} (eq_2); flip the phase of each basis state x with f(x)=1
    for x, v in enumerate(tt):
        if v != 1:
            continue
        zeros = [q for q in range(n) if not (x >> q) & 1]
        for q in zeros:
            qc.x(q)
        if n == 1:
            qc.p(math.pi, 0)
        else:
            qc.mcp(math.pi, list(range(n - 1)), n - 1)
        for q in zeros:
            qc.x(q)
    # step 3: final Hadamards (eq_2)
    for q in range(n):
        qc.h(q)
    return qc
