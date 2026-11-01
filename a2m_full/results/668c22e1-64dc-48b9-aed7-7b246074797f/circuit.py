from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate
import math


def _finite(v, name, bound):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or abs(v) > bound:
        raise ValueError('invalid ' + name)
    return float(v)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _energy(x, b, w):
    # eq_1: E(x) = -sum_i b_i x_i - sum_{i<j} w_ij x_i x_j
    e = 0.0
    for i, bi in enumerate(b):
        e -= bi * x[i]
    for i, j, wij in w:
        e -= wij * x[i] * x[j]
    return e


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    nv = instance.get('n_visible')
    nh = instance.get('n_hidden')
    if not _is_int(nv) or not _is_int(nh) or nv < 1 or nh < 1:
        raise ValueError('n_visible and n_hidden must be positive integers')
    n = nv + nh
    if n > 6 or n + 1 > 12:
        raise ValueError('too many units (max 6 units plus 1 ancilla)')
    b_raw = instance.get('biases')
    if not isinstance(b_raw, list) or len(b_raw) != n:
        raise ValueError('biases must be a list of length n_visible+n_hidden')
    b = [_finite(v, 'bias', 10.0) for v in b_raw]
    w_raw = instance.get('weights', [])
    if not isinstance(w_raw, list):
        raise ValueError('weights must be a list of [i, j, w]')
    w = []
    seen = set()
    for t in w_raw:
        if not isinstance(t, (list, tuple)) or len(t) != 3:
            raise ValueError('weight entries are [i, j, w]')
        i, j = t[0], t[1]
        if not _is_int(i) or not _is_int(j) or i < 0 or j < 0 or i >= n or j >= n or i == j:
            raise ValueError('invalid weight indices')
        a, c = min(i, j), max(i, j)
        if (a, c) in seen:
            raise ValueError('duplicate weight pair')
        seen.add((a, c))
        w.append((a, c, _finite(t[2], 'weight', 10.0)))
    clamp = instance.get('clamp_visible')
    x_fix = [0] * n
    free = list(range(n))
    if clamp is not None:
        if not isinstance(clamp, list) or len(clamp) != nv:
            raise ValueError('clamp_visible must be a list of length n_visible')
        for v in clamp:
            if not _is_int(v) or v not in (0, 1):
                raise ValueError('clamp_visible entries must be 0 or 1')
        for i in range(nv):
            x_fix[i] = clamp[i]
        free = list(range(nv, n))
    freeset = set(free)
    f = len(free)
    q = [0.5] * n
    q_raw = instance.get('q')
    if q_raw is None:
        # eq_2: classical mean-field marginals (damped fixed point) on the free units
        beff = {}
        for i in free:
            s = b[i]
            for a, c, wij in w:
                if a == i and c not in freeset:
                    s += wij * x_fix[c]
                if c == i and a not in freeset:
                    s += wij * x_fix[a]
            beff[i] = s
        for _ in range(500):
            for i in free:
                s = beff[i]
                for a, c, wij in w:
                    if a == i and c in freeset:
                        s += wij * q[c]
                    if c == i and a in freeset:
                        s += wij * q[a]
                new = 1.0 / (1.0 + math.exp(-s))
                val = 0.5 * q[i] + 0.5 * new
                q[i] = min(1.0 - 1e-6, max(1e-6, val))
    else:
        if not isinstance(q_raw, list) or len(q_raw) != n:
            raise ValueError('q must be a list of length n')
        for i in range(n):
            v = _finite(q_raw[i], 'q', 1.0)
            if not (0.0 < v < 1.0):
                raise ValueError('q entries must lie strictly in (0,1)')
            q[i] = v
    # classical table of ratios r(x) = exp(-E(x)) / Q(x) over free assignments
    ratios = []
    for m in range(2 ** f):
        x = list(x_fix)
        qm = 1.0
        for k, idx in enumerate(free):
            bit = (m >> k) & 1
            x[idx] = bit
            qm *= q[idx] if bit else (1.0 - q[idx])
        ratios.append(math.exp(-_energy(x, b, w)) / qm)
    kmin = max(ratios)
    kappa = instance.get('kappa')
    if kappa is None:
        kappa = kmin
    else:
        kappa = _finite(kappa, 'kappa', 1e12)
        if kappa < kmin * (1.0 - 1e-12):
            raise ValueError('kappa too small: exp(-E) <= kappa Q violated')
        kappa = max(kappa, kmin)
    vis = QuantumRegister(nv, 'vis')
    hid = QuantumRegister(nh, 'hid')
    anc = QuantumRegister(1, 'anc')
    qc = QuantumCircuit(vis, hid, anc)
    qubits = list(vis) + list(hid)
    # clamped visible units (data term, eq_5)
    for i in range(n):
        if i not in freeset and x_fix[i] == 1:
            qc.x(qubits[i])
    # mean-field product state Ry(theta_i)|0>, q_i = sin^2(theta_i/2)  (eq_2)
    for i in free:
        theta = 2.0 * math.asin(math.sqrt(q[i]))
        qc.ry(theta, qubits[i])
    # multiplexed ancilla rotation (eq_3)
    targets = [qubits[i] for i in free] + [anc[0]]
    for m in range(2 ** f):
        s = min(1.0, ratios[m] / kappa)
        phi = 2.0 * math.asin(math.sqrt(s))
        if phi == 0.0:
            continue
        qc.append(RYGate(phi).control(f, ctrl_state=m), targets)
    return qc
