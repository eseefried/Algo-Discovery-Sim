from qiskit import QuantumCircuit, QuantumRegister


def _gf_mul(a, b, n, poly):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> n) & 1:
            a ^= poly
    return r


def _gf_trace(z, n, poly):
    t = z
    s = z
    for _ in range(n - 1):
        t = _gf_mul(t, t, n, poly)
        s ^= t
    return s & 1


def build_circuit(instance):
    """U_k for the MUB set: basis k vectors are U_k^dagger|j> = D_a H^{(x)n}|j>.

    instance: {"n": int 1..12, "k": int 0..2^n, "inverse": optional bool}
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    k = instance.get('k')
    inv = instance.get('inverse', False)
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 2 ** n:
        raise ValueError('k must be an integer in 0..2^n')
    if not isinstance(inv, bool):
        raise ValueError('inverse must be a bool')
    polys = {1: 0b11, 2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101,
             6: 0b1000011, 7: 0b10000011, 8: 0b100011011,
             9: 0b1000010001, 10: 0b10000001001,
             11: 0b100000000101, 12: 0b1000001010011}
    poly = polys[n]
    qc = QuantumCircuit(QuantumRegister(n, 'q'))
    if k > 0:
        a = k - 1
        pw = [1]
        for _ in range(2 * n - 2):
            pw.append(_gf_mul(pw[-1], 2, n, poly))
        # symmetric binary matrix M_a[i][j] = Tr(a x^(i+j)) over GF(2^n)
        # D_a^dagger = prod Sdg^{M_ii} * prod CZ^{M_ij}
        for i in range(n):
            if _gf_trace(_gf_mul(a, pw[2 * i], n, poly), n, poly):
                qc.sdg(i)
        for i in range(n):
            for j in range(i + 1, n):
                if _gf_trace(_gf_mul(a, pw[i + j], n, poly), n, poly):
                    qc.cz(i, j)
        for i in range(n):
            qc.h(i)
    if inv:
        return qc.inverse()
    return qc
