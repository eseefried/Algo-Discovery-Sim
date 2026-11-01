import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate


def _quad_phase(qc, weights, c, scale):
    # Applies diag exp(i*scale*(sum_k w_k b_k - c)^2) using P, CP and global phase.
    n = len(weights)
    for k in range(n):
        w = weights[k]
        ang = scale * (w * w - 2.0 * c * w)
        if ang != 0.0:
            qc.p(ang, k)
    for k in range(n):
        for l in range(k + 1, n):
            ang = 2.0 * scale * weights[k] * weights[l]
            if ang != 0.0:
                qc.cp(ang, k, l)
    qc.global_phase += scale * c * c


def _num(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(name + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(name + ' must be finite')
    return v


def build_circuit(instance):
    """Trotterized QHO evolution (T then V per step, r steps) on n position qubits."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_qubits')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError('n_qubits must be an integer in [1, 12]')
    r = instance.get('trotter_steps')
    if isinstance(r, bool) or not isinstance(r, int) or r < 1 or r > 1000:
        raise ValueError('trotter_steps must be an integer in [1, 1000]')
    t = _num(instance.get('time'), 'time')
    N = 2 ** n
    if 'delta' in instance and instance['delta'] is not None:
        delta = _num(instance['delta'], 'delta')
        if delta <= 0.0:
            raise ValueError('delta must be positive')
    else:
        delta = math.sqrt(2.0 * math.pi / N)
    dk = 2.0 * math.pi / (N * delta)
    s = t / r
    qc = QuantumCircuit(n, name='qho_trotter')
    pos_w = [float(2 ** k) for k in range(n)]
    c = (N - 1) / 2.0
    mom_w = [float(2 ** k) for k in range(n - 1)] + [-float(2 ** (n - 1))]
    qubits = list(range(n))
    for _ in range(r):
        # kinetic factor exp(-i T s) = F^dag diag(exp(-i s k^2/2)) F
        qc.append(QFTGate(n).inverse(), qubits)
        _quad_phase(qc, mom_w, 0.0, -s * dk * dk / 2.0)
        qc.append(QFTGate(n), qubits)
        # potential factor exp(-i V s), x_j = delta*(j-(N-1)/2)
        _quad_phase(qc, pos_w, c, -s * delta * delta / 2.0)
    return qc
