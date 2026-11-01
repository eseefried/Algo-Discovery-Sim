from qiskit import QuantumCircuit, QuantumRegister


def _transposition(qc, n, a, b):
    # Swap basis states |a> and |b>: CX conjugation makes them differ in one bit t, then a multi-controlled X on t.
    d = a ^ b
    t = (d & -d).bit_length() - 1
    others = [k for k in range(n) if k != t]
    diffs = [k for k in others if (d >> k) & 1]
    alpha = (a >> t) & 1
    for k in diffs:
        qc.cx(t, k)
    ap = a
    for k in diffs:
        ap ^= alpha << k
    zeros = [k for k in others if not ((ap >> k) & 1)]
    for k in zeros:
        qc.x(k)
    if others:
        qc.mcx(others, t)
    else:
        qc.x(t)
    for k in zeros:
        qc.x(k)
    for k in reversed(diffs):
        qc.cx(t, k)


def build_circuit(instance):
    """Permutation operator U_sigma|j> = |sigma(j)> on n qubits (eq_1). Qubit 0 is the LSB of j."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_qubits', 2)
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 4:
        raise ValueError('num_qubits must be an integer in 1..4')
    dim = 2 ** n
    perm = instance.get('permutation')
    if not isinstance(perm, (list, tuple)) or len(perm) != dim:
        raise ValueError('permutation must be a list of length 2**num_qubits')
    for v in perm:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('permutation entries must be integers')
    if sorted(perm) != list(range(dim)):
        raise ValueError('permutation must be a permutation of 0..2**num_qubits-1')
    reg = QuantumRegister(n, 'q')
    qc = QuantumCircuit(reg)
    seen = [False] * dim
    for start in range(dim):
        if seen[start]:
            continue
        cycle = []
        j = start
        while not seen[j]:
            seen[j] = True
            cycle.append(j)
            j = perm[j]
        # cycle c0->c1->...->c_{k-1}->c0; apply swaps (c_{k-2},c_{k-1}) first down to (c0,c1)
        for i in range(len(cycle) - 2, -1, -1):
            _transposition(qc, n, cycle[i], cycle[i + 1])
    return qc
