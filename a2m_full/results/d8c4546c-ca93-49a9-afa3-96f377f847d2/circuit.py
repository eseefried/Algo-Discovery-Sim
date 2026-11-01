from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate


def _validate(instance):
    if not isinstance(instance, dict) or 'permutation' not in instance:
        raise ValueError('instance must be a dict with key permutation')
    p = instance['permutation']
    if not isinstance(p, (list, tuple)) or len(p) != 4:
        raise ValueError('permutation must have length 4')
    out = []
    for v in p:
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError('permutation entries must be ints')
        out.append(v)
    if sorted(out) != [0, 1, 2, 3]:
        raise ValueError('not a permutation of 0..3')
    return out


def _cycles(perm):
    seen = [False] * 4
    cycles = []
    for s in range(4):
        if seen[s]:
            continue
        cyc = []
        x = s
        while not seen[x]:
            seen[x] = True
            cyc.append(x)
            x = perm[x]
        if len(cyc) > 1:
            cycles.append(cyc)
    return cycles


def _cswap_single_bit(qc, a, b):
    # a, b differ in exactly one bit; qubit 0 = ctrl, qubit 1 = bit0, qubit 2 = bit1
    diff = a ^ b
    tbit = 0 if diff == 1 else 1
    kbit = 1 - tbit
    v = (a >> kbit) & 1
    cs = 1 | (v << 1)
    qc.append(XGate().control(2, ctrl_state=cs), [0, kbit + 1, tbit + 1])


def _cswap(qc, a, b):
    # controlled transposition |a> <-> |b> on the sys register
    if a ^ b == 3:
        # CX(bit0 -> bit1) maps x -> x ^ (2 if x&1 else 0); conjugation relabels the pair
        def f(x):
            return x ^ (2 if (x & 1) else 0)
        qc.cx(1, 2)
        _cswap_single_bit(qc, f(a), f(b))
        qc.cx(1, 2)
    else:
        _cswap_single_bit(qc, a, b)


def build_circuit(instance):
    """Hadamard-test operation: H(ctrl), controlled-U_sigma (one query), H(ctrl).
    Qubit 0 = ctrl; qubits 1,2 = sys with x = 2*q2 + q1."""
    perm = _validate(instance)
    qc = QuantumCircuit(3)
    qc.h(0)
    # U_sigma|x> = |sigma(x)>: cycle (c0 c1 ... ck-1) with c_i -> c_{i+1}
    # equals swaps (c_{k-2},c_{k-1}), ..., (c_0,c_1) applied in that order
    for cyc in _cycles(perm):
        for i in range(len(cyc) - 2, -1, -1):
            _cswap(qc, cyc[i], cyc[i + 1])
    qc.h(0)
    return qc
