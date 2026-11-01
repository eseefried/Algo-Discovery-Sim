import math
from qiskit import QuantumCircuit, QuantumRegister


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + " must be an integer in [%d, %d]" % (lo, hi))
    return v


def _table(v, name, n, bits):
    if not isinstance(v, (list, tuple)) or len(v) != n:
        raise ValueError(name + " must be a list of length %d" % n)
    return [_int(x, name, 0, 2 ** bits - 1) for x in v]


def _mcz(qc, qs):
    # multi-controlled Z on all qubits in qs
    if len(qs) == 1:
        qc.z(qs[0])
    else:
        qc.h(qs[-1])
        qc.mcx(list(qs[:-1]), qs[-1])
        qc.h(qs[-1])


def _load(qc, idx, tgt, values, bits):
    # eq_1: |i>|0> -> |i>|value_i> by index-controlled X gates (self-inverse, also unloads)
    for i, v in enumerate(values):
        zeros = [idx[j] for j in range(len(idx)) if not (i >> j) & 1]
        for b in range(bits):
            if (v >> b) & 1:
                if zeros:
                    qc.x(zeros)
                qc.mcx(list(idx), tgt[b])
                if zeros:
                    qc.x(zeros)


def _oracle(qc, data, q, bits):
    # eq_2: phase flip (-1) when the data register equals the query q
    zeros = [data[b] for b in range(bits) if not (q >> b) & 1]
    if zeros:
        qc.x(zeros)
    _mcz(qc, list(data))
    if zeros:
        qc.x(zeros)


def _diffuse(qc, idx):
    qc.h(list(idx))
    qc.x(list(idx))
    _mcz(qc, list(idx))
    qc.x(list(idx))
    qc.h(list(idx))


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    k = _int(instance.get("k"), "k", 1, 4)
    nb = _int(instance.get("name_bits"), "name_bits", 1, 4)
    mb = _int(instance.get("number_bits"), "number_bits", 1, 4)
    if k + nb + mb > 12:
        raise ValueError("total qubits exceed 12")
    n = 2 ** k
    names = _table(instance.get("names"), "names", n, nb)
    nums = _table(instance.get("numbers"), "numbers", n, mb)
    field = instance.get("search")
    if field not in ("name", "number"):
        raise ValueError("search must be 'name' or 'number'")
    use_name = field == "name"
    bits = nb if use_name else mb
    data_vals = names if use_name else nums
    q = _int(instance.get("query"), "query", 0, 2 ** bits - 1)
    t = instance.get("iterations")
    if t is None:
        m = data_vals.count(q)
        if m == 0:
            raise ValueError("query matches no entry")
        theta = math.asin(math.sqrt(m / n))
        t = max(0, int(round(math.pi / (4 * theta) - 0.5)))
    else:
        t = _int(t, "iterations", 0, 64)
    idx = QuantumRegister(k, "index")
    nreg = QuantumRegister(nb, "name")
    mreg = QuantumRegister(mb, "number")
    qc = QuantumCircuit(idx, nreg, mreg)
    data = nreg if use_name else mreg
    for _ in range(t):
        _load(qc, idx, nreg, names, nb)
        _load(qc, idx, mreg, nums, mb)
        _oracle(qc, data, q, bits)
        _load(qc, idx, mreg, nums, mb)
        _load(qc, idx, nreg, names, nb)
        _diffuse(qc, idx)
    return qc
