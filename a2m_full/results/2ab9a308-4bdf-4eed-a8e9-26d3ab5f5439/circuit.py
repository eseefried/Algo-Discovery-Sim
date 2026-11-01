import math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UGate

_TOL = 1e-9
_MAX_N = 4


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > _MAX_N:
        raise ValueError('n must be an integer in 1..4')
    dim = 1 << n
    try:
        re = np.array(instance['unitary_real'], dtype=float)
        if 'unitary_imag' in instance:
            im = np.array(instance['unitary_imag'], dtype=float)
        else:
            im = np.zeros((dim, dim))
    except (KeyError, TypeError, ValueError):
        raise ValueError('unitary_real/unitary_imag must be numeric dim x dim arrays')
    if re.shape != (dim, dim) or im.shape != (dim, dim):
        raise ValueError('unitary must have shape (2^n, 2^n)')
    u = re + 1j * im
    if not np.all(np.isfinite(u)):
        raise ValueError('unitary entries must be finite')
    if not np.allclose(u.conj().T @ u, np.eye(dim), atol=1e-8):
        raise ValueError('matrix is not unitary')
    return n, u


def _cost(a):
    # eq_3 proxy c(.): number of non-negligible off-diagonal entries
    nz = np.abs(a) > _TOL
    return int(nz.sum() - np.count_nonzero(np.diag(nz)))


def _search(u, n):
    # eq_2/eq_3: greedy heuristic for Q (XOR mask) then P (transpositions)
    dim = 1 << n
    idx = np.arange(dim)
    best_m = 0
    best_c = _cost(u)
    for m in range(1, dim):
        perm = idx ^ m
        c = _cost(u[np.ix_(perm, perm)]) + bin(m).count('1')
        if c < best_c:
            best_c = c
            best_m = m
    perm = idx ^ best_m
    a = u[np.ix_(perm, perm)]
    swaps = []
    cur = _cost(a)
    for _ in range(dim * dim):
        found = None
        limit = cur
        for x in range(dim):
            for y in range(x + 1, dim):
                p = idx.copy()
                p[x] = y
                p[y] = x
                b = a[np.ix_(p, p)]
                c = _cost(b)
                if c + 1 < limit:
                    limit = c + 1
                    found = (x, y, b, c)
        if found is None:
            break
        swaps.append((found[0], found[1]))
        a = found[2]
        cur = found[3]
    return best_m, swaps, a


def _decompose(a):
    # two-level (Givens) elimination: G_m...G_1 A = D
    dim = a.shape[0]
    a = a.astype(complex).copy()
    gates = []
    for c in range(dim - 1):
        for r in range(c + 1, dim):
            b = a[r, c]
            if abs(b) < 1e-12:
                continue
            x = a[c, c]
            nr = math.sqrt(abs(x) ** 2 + abs(b) ** 2)
            g = np.array([[np.conj(x), np.conj(b)], [-b, x]]) / nr
            rows = a[[c, r], :]
            a[[c, r], :] = g @ rows
            gates.append((c, r, g))
    return gates, np.angle(np.diag(a))


def _apply_1q(qc, ctrls, t, v):
    # apply 2x2 unitary v (exactly, incl. phase) to qubit t under all-ones controls
    a, b, c, d = v[0, 0], v[0, 1], v[1, 0], v[1, 1]
    th = 2.0 * math.atan2(abs(c), abs(a))
    if abs(c) < 1e-12:
        g = float(np.angle(a))
        ph = 0.0
        lam = float(np.angle(d)) - g
    elif abs(a) < 1e-12:
        g = 0.0
        ph = float(np.angle(c))
        lam = float(np.angle(-b))
    else:
        g = float(np.angle(a))
        ph = float(np.angle(c)) - g
        lam = float(np.angle(-b)) - g
    if ctrls:
        qc.append(UGate(th, ph, lam).control(len(ctrls)), list(ctrls) + [t])
        if abs(g) > 1e-12:
            if len(ctrls) == 1:
                qc.p(g, ctrls[0])
            else:
                qc.mcp(g, list(ctrls[:-1]), ctrls[-1])
    else:
        qc.u(th, ph, lam, t)
        qc.global_phase += g


def _emit(qc, q, n, i, j, m, use_x):
    # act with 2x2 matrix m on span{|i>,|j>} (basis order i, j); identity elsewhere
    diff = i ^ j
    t = (diff & -diff).bit_length() - 1
    others = [d for d in range(n) if d != t]
    flips = [d for d in others if (diff >> d) & 1]
    it = (i >> t) & 1
    for d in flips:
        qc.cx(q[t], q[d], ctrl_state=1 - it)
    zeros = [d for d in others if not (i >> d) & 1]
    for d in zeros:
        qc.x(q[d])
    ctrls = [q[d] for d in others]
    if use_x:
        if ctrls:
            qc.mcx(ctrls, q[t])
        else:
            qc.x(q[t])
    else:
        v = m if it == 0 else m[::-1, ::-1]
        _apply_1q(qc, ctrls, q[t], v)
    for d in zeros:
        qc.x(q[d])
    for d in reversed(flips):
        qc.cx(q[t], q[d], ctrl_state=1 - it)


def _diag(qc, q, n, phases):
    for k in range(1 << n):
        ph = float(phases[k])
        if abs(ph) < 1e-12:
            continue
        zeros = [d for d in range(n) if not (k >> d) & 1]
        for d in zeros:
            qc.x(q[d])
        if n == 1:
            qc.p(ph, q[0])
        else:
            qc.mcp(ph, [q[d] for d in range(1, n)], q[0])
        for d in zeros:
            qc.x(q[d])


def _xor_mask(qc, q, n, mask):
    for d in range(n):
        if (mask >> d) & 1:
            qc.x(q[d])


def build_circuit(instance):
    """Return W = Q^T P^T C_U' P Q (time order Q, P, C_U', P^T, Q^T) for the given U."""
    n, u = _parse(instance)
    mask, swaps, up = _search(u, n)
    gates, phases = _decompose(up)
    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q)
    xm = np.array([[0, 1], [1, 0]], dtype=complex)
    # Q (first in time)
    _xor_mask(qc, q, n, mask)
    # P = T_s ... T_1, so T_1 acts first
    for (x, y) in swaps:
        _emit(qc, q, n, x, y, xm, True)
    # C_U': U' = G_1^dag ... G_m^dag D, so D first then G_m^dag ... G_1^dag
    _diag(qc, q, n, phases)
    for (c, r, g) in reversed(gates):
        _emit(qc, q, n, c, r, g.conj().T, False)
    # P^T = T_1 ... T_s, so T_s acts first
    for (x, y) in reversed(swaps):
        _emit(qc, q, n, x, y, xm, True)
    # Q^T = Q (XOR involution)
    _xor_mask(qc, q, n, mask)
    return qc
