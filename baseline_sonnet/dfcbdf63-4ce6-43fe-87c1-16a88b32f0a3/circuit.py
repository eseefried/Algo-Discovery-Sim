from qiskit import QuantumCircuit
import math


def _mux_ry(qc, angles, controls, target):
    """Uniformly controlled RY: angle angles[idx] where idx has controls[k] as bit k."""
    if not controls:
        qc.ry(angles[0], target)
        return
    half = len(angles) // 2
    a = [(angles[k] + angles[k + half]) / 2.0 for k in range(half)]
    b = [(angles[k] - angles[k + half]) / 2.0 for k in range(half)]
    c = controls[-1]
    rest = controls[:-1]
    _mux_ry(qc, a, rest, target)
    qc.cx(c, target)
    _mux_ry(qc, b, rest, target)
    qc.cx(c, target)


def _prep(n, P):
    """Isometry-completing unitary U: |i>|0> -> |i> sum_j sqrt(P[i][j]) |j> (eq_2, |phi_i>)."""
    N = 2 ** n
    qc = QuantumCircuit(2 * n)
    node = list(range(n))
    tgt = list(range(n, 2 * n))
    for k in range(n - 1, -1, -1):
        nm = 2 ** (n - 1 - k)
        angles = [0.0] * (N * nm)
        for i in range(N):
            for m in range(nm):
                w0 = 0.0
                w1 = 0.0
                for j in range(N):
                    if (j >> (k + 1)) == m:
                        if (j >> k) & 1:
                            w1 += P[i][j]
                        else:
                            w0 += P[i][j]
                if w0 + w1 > 0.0:
                    angles[i + N * m] = 2.0 * math.atan2(math.sqrt(w1), math.sqrt(w0))
        controls = node + tgt[k + 1:]
        _mux_ry(qc, angles, controls, tgt[k])
    return qc


def _walk_step(n, P):
    """One Szegedy step W = S (2 Pi - I), Pi = U (I x |0><0|) U^dagger (eq_2)."""
    prep = _prep(n, P)
    w = QuantumCircuit(2 * n)
    tgt = list(range(n, 2 * n))
    w.compose(prep.inverse(), qubits=list(range(2 * n)), inplace=True)
    # I - 2|0><0| on second register, then global phase pi gives 2|0><0| - I
    for q in tgt:
        w.x(q)
    if n == 1:
        w.z(tgt[0])
    else:
        w.h(tgt[-1])
        w.mcx(tgt[:-1], tgt[-1])
        w.h(tgt[-1])
    for q in tgt:
        w.x(q)
    w.global_phase += math.pi
    w.compose(prep, qubits=list(range(2 * n)), inplace=True)
    for i in range(n):
        w.swap(i, n + i)
    return w


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('num_node_qubits')
    steps = instance.get('steps')
    P = instance.get('transition_matrix')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or 2 * n > 12:
        raise ValueError('num_node_qubits must be an integer in 1..6')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0 or steps > 64:
        raise ValueError('steps must be an integer in 0..64')
    N = 2 ** n
    if not isinstance(P, list) or len(P) != N:
        raise ValueError('transition_matrix must have 2^n rows')
    M = []
    for row in P:
        if not isinstance(row, list) or len(row) != N:
            raise ValueError('transition_matrix must be 2^n by 2^n')
        r = []
        for x in row:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                raise ValueError('entries must be numbers')
            x = float(x)
            if not math.isfinite(x) or x < 0.0:
                raise ValueError('entries must be finite and nonnegative')
            r.append(x)
        if abs(sum(r) - 1.0) > 1e-9:
            raise ValueError('rows must sum to 1')
        M.append(r)
    qc = QuantumCircuit(2 * n)
    if steps == 0:
        return qc
    w = _walk_step(n, M)
    for _ in range(steps):
        qc.compose(w, qubits=list(range(2 * n)), inplace=True)
    return qc
