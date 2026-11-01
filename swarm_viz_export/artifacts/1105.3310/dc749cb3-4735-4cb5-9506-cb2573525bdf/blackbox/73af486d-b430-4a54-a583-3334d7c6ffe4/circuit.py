from qiskit import QuantumCircuit

_KEYS = ("0", "1", "2", "3", "12", "13", "23")


def _read_coefficients(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    for k in instance:
        if k not in ("coefficients", "n", "d", "q"):
            raise ValueError("unknown instance key: %r" % (k,))
    if instance.get("n", 3) != 3 or instance.get("d", 2) != 2 or instance.get("q", 2) != 2:
        raise ValueError("only n=3, d=2, q=2 is supported")
    raw = instance.get("coefficients", {})
    if not isinstance(raw, dict):
        raise ValueError("coefficients must be a dict")
    coeffs = {k: 0 for k in _KEYS}
    for key, val in raw.items():
        if key not in coeffs:
            raise ValueError("invalid monomial key: %r" % (key,))
        if isinstance(val, bool):
            val = int(val)
        if not isinstance(val, int) or val not in (0, 1):
            raise ValueError("coefficients must be 0 or 1")
        coeffs[key] = val
    return coeffs


def build_circuit(instance):
    """Qubits: 0=a0 (c_0); 1,2,3=a1..a3 (c_1..c_3); (4,5)=(x2,x3) block 1;
    (6,7)=(x1,x3) block 2; (8,9)=(x1,x2) block 3.
    Output basis state: q0=c_0,q1..q3=c_i, block qubit for partner j of i = c_ij."""
    c = _read_coefficients(instance)
    qc = QuantumCircuit(10)
    # eq_4: first Hadamard layer
    for q in range(10):
        qc.h(q)
    # eq_5: constant term
    if c["0"]:
        qc.z(0)
    # eq_2/eq_3: derivative phase (-1)^(c_i*b + l.x') as uncontrolled Z gates
    for i in (1, 2, 3):
        if c[str(i)]:
            qc.z(i)
        base = 2 + 2 * i
        others = [j for j in (1, 2, 3) if j != i]
        for k, j in enumerate(others):
            key = str(min(i, j)) + str(max(i, j))
            if c[key]:
                qc.z(base + k)
    # eq_4: final Hadamard layer
    for q in range(10):
        qc.h(q)
    return qc
