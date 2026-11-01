from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Bit-flip oracle O_f: |x>|b> -> |x>|b xor f(x)> (eq_5).

    instance: {"n": int in [1, 11], "truth_table": list of 2^n values in {0, 1}}.
    truth_table[x] = f(x), where x = sum_i x_i 2^i and x_i sits on qubit i.
    Qubits 0..n-1 hold x; qubit n is the answer qubit b.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > 11:
        raise ValueError("n must satisfy 1 <= n <= 11 (total qubits <= 12)")
    tt = instance.get("truth_table")
    if not isinstance(tt, (list, tuple)):
        raise ValueError("truth_table must be a list")
    if len(tt) != 2 ** n:
        raise ValueError("truth_table must have length 2^n")
    vals = []
    for v in tt:
        if isinstance(v, bool):
            vals.append(int(v))
        elif isinstance(v, int) and v in (0, 1):
            vals.append(v)
        else:
            raise ValueError("truth_table entries must be 0 or 1")
    qx = QuantumRegister(n, "x")
    qb = QuantumRegister(1, "b")
    qc = QuantumCircuit(qx, qb)
    controls = [qx[i] for i in range(n)]
    for x, v in enumerate(vals):
        if v != 1:
            continue
        zeros = [i for i in range(n) if ((x >> i) & 1) == 0]
        for i in zeros:
            qc.x(qx[i])
        qc.mcx(controls, qb[0])
        for i in zeros:
            qc.x(qx[i])
    return qc
