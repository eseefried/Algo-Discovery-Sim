import math
from qiskit import QuantumCircuit


def _mul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def _conj(q):
    return (q[0], -q[1], -q[2], -q[3])


def _gens():
    out = []
    for ax in (1, 2, 3):
        for s in (1, -1):
            v = [1, 0, 0, 0]
            v[ax] = 2 * s
            out.append(tuple(v))
    return out


def _axis(v):
    # eq_1: quaternion i,j,k <-> -iX,-iY,-iZ; returns (axis 1..3, sign) of the single non-real part
    for ax in (1, 2, 3):
        if v[ax] != 0:
            return ax, (1 if v[ax] > 0 else -1)
    raise ValueError('no axis')


def _reduce(q, k):
    # peel V-type left factors: q = g * q', q' = conj(g) q / 5 must be integral
    if k == 0:
        if sum(x * x for x in q) == 1:
            return [], q
        return None
    for g in _gens():
        p = _mul(_conj(g), q)
        if all(x % 5 == 0 for x in p):
            r = _reduce(tuple(x // 5 for x in p), k - 1)
            if r is not None:
                return [g] + r[0], r[1]
    return None


def _search(theta, eps, max_k):
    ch = math.cos(theta / 2.0)  # eq_2: target quaternion direction (cos, 0, 0, sin)
    sh = math.sin(theta / 2.0)
    thr = 1.0 - eps * eps / 2.0  # eq_5: dist = sqrt(2-2|p|) <= eps
    for k in range(max_k + 1):
        n = 5 ** k
        r = math.isqrt(n)
        scale = math.sqrt(n)
        found = []
        for a in range(-r, r + 1):
            for d in range(-r, r + 1):
                rem = n - a * a - d * d
                if rem < 0:
                    continue
                p = abs(a * ch + d * sh) / scale
                if p < thr - 1e-12:
                    continue
                for b in range(-r, r + 1):
                    t = rem - b * b  # eq_4: c^2 = 5^k - a^2 - d^2 - b^2
                    if t < 0:
                        continue
                    c = math.isqrt(t)
                    if c * c != t:
                        continue
                    for cc in sorted({c, -c}):
                        found.append((-p, (a, b, cc, d)))
        found.sort()
        for _, q in found:
            red = _reduce(q, k)
            if red is not None:
                return red
    raise ValueError('no Pauli+V approximation found within max_k and epsilon')


def build_circuit(instance):
    """Single-qubit Pauli+V approximation of Rz(theta); instance: theta, epsilon, optional max_k (0..4)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    theta = instance.get('theta')
    eps = instance.get('epsilon')
    max_k = instance.get('max_k', 3)
    for v in (theta, eps):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError('theta and epsilon must be finite numbers')
    if not (0.0 < eps <= 2.0):
        raise ValueError('epsilon must be in (0, 2]')
    if isinstance(max_k, bool) or not isinstance(max_k, int) or max_k < 0 or max_k > 4:
        raise ValueError('max_k must be an integer in 0..4')
    word, unit = _search(float(theta), float(eps), max_k)
    qc = QuantumCircuit(1)
    phase = 0.0
    # matrix U = G1 G2 ... Gk * unit, so the unit acts first and Gk ... G1 follow
    if unit[0] != 0:
        if unit[0] < 0:
            phase += math.pi
    else:
        ax, s = _axis(unit)
        if ax == 1:
            qc.x(0)
        elif ax == 2:
            qc.y(0)
        else:
            qc.z(0)
        phase -= s * math.pi / 2.0  # s*(-i sigma) = sigma times phase
    for g in reversed(word):
        ax, s = _axis(g)
        ang = 2.0 * math.atan2(2.0 * s, 1.0)  # (I - i s 2 sigma)/sqrt5 = R_sigma(ang)
        if ax == 1:
            qc.rx(ang, 0)
        elif ax == 2:
            qc.ry(ang, 0)
        else:
            qc.rz(ang, 0)
    qc.global_phase = phase
    return qc
