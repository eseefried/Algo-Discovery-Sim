from qiskit import QuantumCircuit, QuantumRegister


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    return v


def _gf2_rank(rows):
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    return len(basis)


def build_circuit(instance):
    """Bell-like basis generator. instance keys: n, m, optional fan, optional w.
    Qubits 0..m-1 are controls, qubits m..n-1 are targets.
    fan[i] = list of target indices (0..n-m-1) flipped by control i.
    w = list of m bits defining the type B sign g(c)=XOR_i w_i c_i."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _as_int(instance.get("n"), "n")
    m = _as_int(instance.get("m"), "m")
    if n < 3 or n > 12:
        raise ValueError("n must be in 3..12")
    if m < 1 or n - m < m:
        raise ValueError("need 1 <= m <= n-m for an injective fan map")
    t = n - m
    fan = instance.get("fan")
    if fan is None:
        fan = [[i] for i in range(m)]
        fan[m - 1] = list(range(m - 1, t))
    if not isinstance(fan, (list, tuple)) or len(fan) != m:
        raise ValueError("fan must have one entry per control")
    rows = []
    clean = []
    for lst in fan:
        if not isinstance(lst, (list, tuple)):
            raise ValueError("fan entries must be lists")
        mask = 0
        items = []
        for j in lst:
            j = _as_int(j, "fan target")
            if j < 0 or j >= t or (mask >> j) & 1:
                raise ValueError("invalid or duplicate fan target")
            mask |= 1 << j
            items.append(j)
        rows.append(mask)
        clean.append(items)
    if _gf2_rank(rows) != m:
        raise ValueError("fan map must be injective (rank m over GF(2))")
    w = instance.get("w")
    if w is None:
        w = [0] * m
    if not isinstance(w, (list, tuple)) or len(w) != m:
        raise ValueError("w must have length m")
    for x in w:
        if _as_int(x, "w entry") not in (0, 1):
            raise ValueError("w entries must be 0 or 1")
    ctrl = QuantumRegister(m, "ctrl")
    tgt = QuantumRegister(t, "tgt")
    qc = QuantumCircuit(ctrl, tgt)
    # eq_1: Hadamards turn |b> into sum_c (-1)^{b.c}|c>
    for i in range(m):
        qc.h(ctrl[i])
    # eq_1 type A fan: |c>|a> -> |c>|a xor f(c)>
    for i in range(m):
        for j in clean[i]:
            qc.cx(ctrl[i], tgt[j])
    # eq_4 type B: sign (-1)^{w.c}
    for i in range(m):
        if w[i]:
            qc.z(ctrl[i])
    return qc
