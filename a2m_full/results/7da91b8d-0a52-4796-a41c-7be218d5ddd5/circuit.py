from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Hadamard-test influence operation.

    instance: {"n": int 1..11, "target": int in [0,n), "truth_table": list of 2^n ints in {0,1}}
    truth_table[x] = f(x), where bit j of x is x_j and is held by qubit j.
    Qubits 0..n-1 are the input register; qubit n is the ancilla.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    t = instance.get('target')
    tt = instance.get('truth_table')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n + 1 > 12:
        raise ValueError('n must be an integer in 1..11')
    if isinstance(t, bool) or not isinstance(t, int) or t < 0 or t >= n:
        raise ValueError('target must be an integer in [0, n)')
    if not isinstance(tt, (list, tuple)) or len(tt) != 2 ** n:
        raise ValueError('truth_table must have length 2^n')
    for v in tt:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError('truth_table entries must be 0 or 1')
    xr = QuantumRegister(n, 'x')
    ar = QuantumRegister(1, 'a')
    qc = QuantumCircuit(xr, ar)
    anc = n
    # eq_2: CX(a->x_i) before the oracle
    qc.cx(anc, t)
    # eq_2: phase oracle U_f |x> = (-1)^f(x) |x>, one phase flip per f(x)=1 input
    for x in range(2 ** n):
        if tt[x] != 1:
            continue
        zeros = [j for j in range(n) if not (x >> j) & 1]
        for j in zeros:
            qc.x(j)
        if n == 1:
            qc.p(3.141592653589793, 0)
        else:
            qc.mcp(3.141592653589793, list(range(n - 1)), n - 1)
        for j in zeros:
            qc.x(j)
    # eq_2: CX(a->x_i) after the oracle
    qc.cx(anc, t)
    # eq_4: final Hadamard on the ancilla before the runner's readout
    qc.h(anc)
    return qc
