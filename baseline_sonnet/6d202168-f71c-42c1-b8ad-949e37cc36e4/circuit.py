from qiskit import QuantumCircuit
import math


def _mul(A, B):
    t = {(1, 2): (3, 1j), (2, 1): (3, -1j), (2, 3): (1, 1j), (3, 2): (1, -1j), (3, 1): (2, 1j), (1, 3): (2, -1j)}
    res = {}
    for ka, ca in A.items():
        for kb, cb in B.items():
            ph = ca * cb
            out = []
            for x, y in zip(ka, kb):
                if x == 0:
                    out.append(y)
                elif y == 0:
                    out.append(x)
                elif x == y:
                    out.append(0)
                else:
                    z, f = t[(x, y)]
                    out.append(z)
                    ph = ph * f
            key = tuple(out)
            res[key] = res.get(key, 0) + ph
    return res


def _ladder(n, p, dagger):
    # Jordan-Wigner: a_p = (X_p + iY_p)/2 * Z_{<p}; a_p^dag = (X_p - iY_p)/2 * Z_{<p}
    kx = tuple([3] * p + [1] + [0] * (n - p - 1))
    ky = tuple([3] * p + [2] + [0] * (n - p - 1))
    sgn = -1j if dagger else 1j
    return {kx: 0.5 + 0j, ky: 0.5 * sgn}


def _scale(A, c):
    return {k: v * c for k, v in A.items()}


def _add(H, A):
    for k, v in A.items():
        H[k] = H.get(k, 0) + v


def _to_int(x, lo, hi, name):
    try:
        f = float(x)
    except (TypeError, ValueError):
        raise ValueError(name + " must be numeric")
    if not math.isfinite(f) or f != math.floor(f) or f < lo or f > hi:
        raise ValueError(name + " out of range")
    return int(f)


def _to_real(x, name):
    try:
        f = float(x)
    except (TypeError, ValueError):
        raise ValueError(name + " must be numeric")
    if not math.isfinite(f):
        raise ValueError(name + " must be finite")
    return f


def _hamiltonian_paulis(n, one_body, two_body):
    # eq_1: H = sum h_pq a_p^dag a_q + 1/2 sum h_pqrs a_p^dag a_q^dag a_r a_s, mapped to Pauli strings
    H = {}
    for e in one_body:
        if not isinstance(e, list) or len(e) != 3:
            raise ValueError("one_body entries are [p,q,value]")
        p = _to_int(e[0], 0, n - 1, "p")
        q = _to_int(e[1], 0, n - 1, "q")
        v = _to_real(e[2], "h_pq")
        _add(H, _scale(_mul(_ladder(n, p, True), _ladder(n, q, False)), v))
    for e in two_body:
        if not isinstance(e, list) or len(e) != 5:
            raise ValueError("two_body entries are [p,q,r,s,value]")
        p = _to_int(e[0], 0, n - 1, "p")
        q = _to_int(e[1], 0, n - 1, "q")
        r = _to_int(e[2], 0, n - 1, "r")
        s = _to_int(e[3], 0, n - 1, "s")
        v = _to_real(e[4], "h_pqrs")
        op = _mul(_mul(_mul(_ladder(n, p, True), _ladder(n, q, True)), _ladder(n, r, False)), _ladder(n, s, False))
        _add(H, _scale(op, 0.5 * v))
    terms = []
    const = 0.0
    for k in sorted(H.keys()):
        c = H[k]
        if abs(c) < 1e-12:
            continue
        if abs(c.imag) > 1e-9:
            raise ValueError("Hamiltonian is not Hermitian (complex Pauli coefficient)")
        if all(l == 0 for l in k):
            const += c.real
        else:
            terms.append((k, c.real))
    return terms, const


def _pauli_rotation(qc, key, coeff, dt):
    # exp(-i coeff dt P) via basis change, CX ladder and RZ(2 coeff dt)
    sup = [i for i, l in enumerate(key) if l != 0]
    for i in sup:
        if key[i] == 1:
            qc.h(i)
        elif key[i] == 2:
            qc.sdg(i)
            qc.h(i)
    for a, b in zip(sup[:-1], sup[1:]):
        qc.cx(a, b)
    qc.rz(2.0 * coeff * dt, sup[-1])
    for a, b in reversed(list(zip(sup[:-1], sup[1:]))):
        qc.cx(a, b)
    for i in sup:
        if key[i] == 1:
            qc.h(i)
        elif key[i] == 2:
            qc.h(i)
            qc.s(i)


def build_circuit(instance):
    """Instance: n_orbitals, time, steps, one_body [[p,q,h]], two_body [[p,q,r,s,h]]."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _to_int(instance.get("n_orbitals"), 1, 12, "n_orbitals")
    r = _to_int(instance.get("steps"), 1, 50, "steps")
    t = _to_real(instance.get("time"), "time")
    one_body = instance.get("one_body", [])
    two_body = instance.get("two_body", [])
    if not isinstance(one_body, list) or not isinstance(two_body, list):
        raise ValueError("one_body and two_body must be lists")
    if len(one_body) > 144 or len(two_body) > 100:
        raise ValueError("too many integrals")
    if two_body and n < 2:
        raise ValueError("two-body terms need at least 2 orbitals")
    order = instance.get("order", 1)
    if _to_int(order, 1, 1, "order") != 1:
        raise ValueError("only first-order Trotter is supported")
    terms, const = _hamiltonian_paulis(n, one_body, two_body)
    if len(terms) > 2000:
        raise ValueError("too many Pauli terms")
    qc = QuantumCircuit(n)
    dt = t / r
    # eq_2: (prod_j exp(-i H_j t/r))^r
    for _ in range(r):
        for key, c in terms:
            _pauli_rotation(qc, key, c, dt)
    qc.global_phase = -const * t
    return qc
