from qiskit import QuantumCircuit, QuantumRegister
import math


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n_address")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 11:
        raise ValueError("n_address must be an integer in 1..11")
    db = instance.get("database")
    if not isinstance(db, (list, tuple)) or len(db) != 2 ** n:
        raise ValueError("database must be a list of length 2**n_address")
    for v in db:
        if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
            raise ValueError("database entries must be 0 or 1")
    k = instance.get("iterations")
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 64:
        raise ValueError("iterations must be an integer in 0..64")
    marked = sum(db)
    if marked < 1 or marked >= 2 ** n:
        raise ValueError("need at least one marked and one unmarked entry")
    return n, [int(v) for v in db], k


def _lookup(qc, addr, data, db):
    # eq_1: U_M |x>|b> = |x>|b xor d(x)>, little-endian address bits
    for x, bit in enumerate(db):
        if bit:
            zeros = [addr[i] for i in range(len(addr)) if not (x >> i) & 1]
            for q in zeros:
                qc.x(q)
            qc.mcx(list(addr), data)
            for q in zeros:
                qc.x(q)


def _phase_oracle(qc, addr, data, db):
    # eq_2 (modified): U_M Z_D U_M = Z_D (x) O, then Z_D cancels the extra Z
    _lookup(qc, addr, data, db)
    qc.z(data)
    _lookup(qc, addr, data, db)
    qc.z(data)


def _diffusion(qc, addr):
    # eq_3: 2|s><s|-1 = - H X (MCZ) X H
    for q in addr:
        qc.h(q)
    for q in addr:
        qc.x(q)
    if len(addr) == 1:
        qc.z(addr[0])
    else:
        qc.h(addr[-1])
        qc.mcx(list(addr[:-1]), addr[-1])
        qc.h(addr[-1])
    for q in addr:
        qc.x(q)
    for q in addr:
        qc.h(q)
    qc.global_phase += math.pi


def build_circuit(instance):
    n, db, k = _parse(instance)
    a = QuantumRegister(n, "A")
    d = QuantumRegister(1, "D")
    qc = QuantumCircuit(a, d)
    addr = list(a)
    data = d[0]
    for _ in range(k):
        _phase_oracle(qc, addr, data, db)
        _diffusion(qc, addr)
    return qc
