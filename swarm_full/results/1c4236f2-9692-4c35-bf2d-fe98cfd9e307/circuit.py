from qiskit import QuantumCircuit, QuantumRegister
import math


def _as_int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + ' must be an integer')
    return v


def build_circuit(instance):
    """Path superposition with probability-dependent phase (eq_1).

    instance keys: constraint_length K>=2, num_frames N>=1,
    generators: list of ints in [1, 2^K-1] (bit j acts on window position j),
    received: N lists of len(generators) bits, gamma: real phase scale.
    Path bits x_0..x_{M-1}, M=(K-1)+N, qubit i holds x_i.
    Frame t window is x_t..x_{t+K-1}.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('constraint_length', 'num_frames', 'generators', 'received', 'gamma'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    K = _as_int(instance['constraint_length'], 'constraint_length')
    N = _as_int(instance['num_frames'], 'num_frames')
    if K < 2 or N < 1:
        raise ValueError('need K>=2 and N>=1')
    M = K - 1 + N
    if M > 12:
        raise ValueError('too many qubits (max 12)')
    gens = instance['generators']
    if not isinstance(gens, (list, tuple)) or len(gens) == 0:
        raise ValueError('generators must be a non-empty list')
    gens = [_as_int(g, 'generator') for g in gens]
    for g in gens:
        if g < 1 or g >= (1 << K):
            raise ValueError('generator out of range')
    rec = instance['received']
    if not isinstance(rec, (list, tuple)) or len(rec) != N:
        raise ValueError('received must have N frames')
    for fr in rec:
        if not isinstance(fr, (list, tuple)) or len(fr) != len(gens):
            raise ValueError('each received frame must have one bit per generator')
        for b in fr:
            if _as_int(b, 'received bit') not in (0, 1):
                raise ValueError('received bits must be 0/1')
    gv = instance['gamma']
    if isinstance(gv, bool) or not isinstance(gv, (int, float)):
        raise ValueError('gamma must be real')
    gamma = float(gv)
    if not math.isfinite(gamma):
        raise ValueError('gamma must be finite')

    path = QuantumRegister(M, 'x')
    qc = QuantumCircuit(path)
    # uniform superposition over all legal paths (start memory + input bits)
    for i in range(M):
        qc.h(path[i])
    # phase phi = -gamma * Hamming distance(path output, received)
    for t in range(N):
        for k, g in enumerate(gens):
            r = rec[t][k]
            qs = [t + j for j in range(K) if (g >> j) & 1]
            tgt = qs[-1]
            others = qs[:-1]
            for c in others:
                qc.cx(path[c], path[tgt])
            # parity p; mismatch indicator is p (r=0) or 1-p (r=1)
            if r == 0:
                qc.p(-gamma, path[tgt])
            else:
                qc.p(gamma, path[tgt])
                qc.global_phase = qc.global_phase - gamma
            for c in reversed(others):
                qc.cx(path[c], path[tgt])
    return qc
