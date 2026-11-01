from qiskit import QuantumCircuit, QuantumRegister


def _chk(v, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError("invalid parameter")
    return v


def _mcz(qc, q):
    if len(q) == 1:
        qc.z(q[0])
    else:
        qc.h(q[-1])
        qc.mcx(q[:-1], q[-1])
        qc.h(q[-1])


def _inc(c, ctl, met):
    # controlled +1 on little-endian metric register (no overflow: register is large enough)
    for k in range(len(met) - 1, -1, -1):
        c.mcx([ctl] + met[:k], met[k])


def _metric_circuit(N, Q, gens, rec, path, err, met, total):
    # eq_2: shift-register trellis output and Hamming-distance accumulation
    c = QuantumCircuit(total)
    for t in range(1, N + 1):
        s = QuantumCircuit(total)
        for j, g in enumerate(gens):
            for k in range(Q):
                if (g >> (Q - 1 - k)) & 1 and t - k >= 1:
                    s.cx(path[t - 1 - k], err[j])
            if (rec[t - 1] >> j) & 1:
                s.x(err[j])
        c.compose(s, qubits=list(range(total)), inplace=True)
        for e in err:
            _inc(c, e, met)
        c.compose(s.inverse(), qubits=list(range(total)), inplace=True)
    return c


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    N = _chk(instance.get("N"), 1, 8)
    Q = _chk(instance.get("Q"), 2, 6)
    gens = instance.get("generators")
    rec = instance.get("received")
    if not isinstance(gens, list) or not 1 <= len(gens) <= 4:
        raise ValueError("generators must be a list of 1..4 ints")
    n = len(gens)
    for g in gens:
        _chk(g, 1, 2 ** Q - 1)
    if not isinstance(rec, list) or len(rec) != N:
        raise ValueError("received must have length N")
    for r in rec:
        _chk(r, 0, 2 ** n - 1)
    T = _chk(instance.get("threshold"), 1, n * N + 1)
    R = _chk(instance.get("iterations"), 0, 64)
    prep = instance.get("prepare_uniform", True)
    if not isinstance(prep, bool):
        raise ValueError("prepare_uniform must be bool")
    m = (n * N).bit_length()
    total = N + n + m
    if total > 12:
        raise ValueError("too many qubits")
    qr_path = QuantumRegister(N, "path")
    qr_err = QuantumRegister(n, "err")
    qr_met = QuantumRegister(m, "metric")
    qc = QuantumCircuit(qr_path, qr_err, qr_met)
    path = list(range(N))
    err = list(range(N, N + n))
    met = list(range(N + n, total))
    comp = _metric_circuit(N, Q, gens, rec, path, err, met, total)
    comp_inv = comp.inverse()
    allq = list(range(total))
    if prep:
        qc.h(path)  # eq_1
    for _ in range(R):
        # eq_3: threshold phase oracle (-1)^[M<T]
        qc.compose(comp, qubits=allq, inplace=True)
        for v in range(min(T, 2 ** m)):
            zeros = [met[i] for i in range(m) if not (v >> i) & 1]
            if zeros:
                qc.x(zeros)
            _mcz(qc, met)
            if zeros:
                qc.x(zeros)
        qc.compose(comp_inv, qubits=allq, inplace=True)
        # eq_4: diffusion about uniform path state
        qc.h(path)
        qc.x(path)
        _mcz(qc, path)
        qc.x(path)
        qc.h(path)
    return qc
