from qiskit import QuantumCircuit


def _num_pairs(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key != 'num_pairs':
            raise ValueError('unknown instance key: ' + str(key))
    p = instance.get('num_pairs')
    if isinstance(p, bool) or not isinstance(p, int):
        raise ValueError('num_pairs must be an integer')
    if p < 1 or 2 * p + 2 > 12:
        raise ValueError('num_pairs must satisfy 1 <= num_pairs <= 5')
    return p


def build_circuit(instance):
    """Long-range CNOT(c->t) on a line: c=0, ancillas 1..2p, t=2p+1."""
    p = _num_pairs(instance)
    n = 2 * p + 2
    c = 0
    t = n - 1
    qc = QuantumCircuit(n, name='long_range_cnot')
    # eq_2: local Bell pairs (2i-1, 2i), i = 1..p, via H then CNOT
    for i in range(p):
        qc.h(2 * i + 1)
        qc.cx(2 * i + 1, 2 * i + 2)
    # eq_3: entanglement swapping, Bell measurement deferred.
    # e is the current right end of the merged pair whose left end is qubit 1.
    e = 2
    for i in range(1, p):
        nxt = 2 * i + 1
        new = 2 * i + 2
        qc.cx(e, nxt)
        qc.h(e)
        qc.cx(nxt, new)  # coherent X^w correction
        qc.cz(e, new)    # coherent Z^z correction
        e = new
    u = 1
    v = e
    # eq_4: CNOT gate teleportation with deferred corrections
    qc.cx(c, u)
    qc.cx(u, v)  # coherent X^m correction on v, v now copies c in Z basis
    qc.cx(v, t)  # CNOT applied locally next to t
    qc.h(v)      # X-basis disentangling of the copy
    qc.cz(v, c)  # coherent Z^s correction on c
    # Return the uniformly superposed (formerly measured) ancillas to |0>
    for q in range(1, n - 1):
        qc.h(q)
    return qc
