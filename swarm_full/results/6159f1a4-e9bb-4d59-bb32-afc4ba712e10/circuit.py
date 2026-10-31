from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' must be an integer in [' + str(lo) + ',' + str(hi) + ']')
    return v


def _num(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + ' must be a finite real number')
    return float(v)


def _onsite(qc, s, gamma, tau):
    # exp(+i gamma tau X_s): intra-cell hopping A(x,y)<->B(x,y)
    qc.rx(-2.0 * gamma * tau, s)


def _shift_hop(qc, s, reg, gamma, tau):
    # hopping A(c)<->B(c-1) along one cell coordinate.
    # H = -gamma(|A><B| (x) S + h.c.), S|j>=|j+1> = QFT^dag diag(w^k) QFT.
    # exp(-iHt) = F^dag P^dag RX(-2 gamma t) P F, P = exp(i*2*pi*k/L * n_s)
    n = len(reg)
    length = 2 ** n
    qc.append(QFTGate(n), reg)
    for m, q in enumerate(reg):
        qc.cp(2.0 * math.pi * (2 ** m) / length, q, s)
    qc.rx(-2.0 * gamma * tau, s)
    for m, q in enumerate(reg):
        qc.cp(-2.0 * math.pi * (2 ** m) / length, q, s)
    qc.append(QFTGate(n).inverse(), reg)


def _mark(qc, qubits, bits, eps, tau):
    # exp(+i eps tau |w><w|): phase on the computational basis state w
    for q, b in zip(qubits, bits):
        if b == 0:
            qc.x(q)
    if len(qubits) == 1:
        qc.p(eps * tau, qubits[0])
    else:
        qc.mcp(eps * tau, qubits[1:], qubits[0])
    for q, b in zip(qubits, bits):
        if b == 0:
            qc.x(q)


def build_circuit(instance):
    """Trotterized CTQW on a periodic graphene lattice with an on-site marked site.
    instance keys: nx, ny (cell register sizes, 1..5), gamma, epsilon, time,
    trotter_steps (1..200), order (1 or 2), marked_site [sublattice, x, y]."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('nx', 'ny', 'gamma', 'epsilon', 'time', 'trotter_steps', 'order', 'marked_site'):
        if key not in instance:
            raise ValueError('missing key ' + key)
    nx = _int(instance['nx'], 'nx', 1, 10)
    ny = _int(instance['ny'], 'ny', 1, 10)
    if 1 + nx + ny > 12:
        raise ValueError('total qubits exceed 12')
    gamma = _num(instance['gamma'], 'gamma')
    eps = _num(instance['epsilon'], 'epsilon')
    t = _num(instance['time'], 'time')
    if gamma <= 0:
        raise ValueError('gamma must be positive')
    steps = _int(instance['trotter_steps'], 'trotter_steps', 1, 200)
    order = _int(instance['order'], 'order', 1, 2)
    w = instance['marked_site']
    if not isinstance(w, (list, tuple)) or len(w) != 3:
        raise ValueError('marked_site must be [sublattice, x, y]')
    sw = _int(w[0], 'sublattice', 0, 1)
    xw = _int(w[1], 'x', 0, 2 ** nx - 1)
    yw = _int(w[2], 'y', 0, 2 ** ny - 1)
    n = 1 + nx + ny
    reg = QuantumRegister(n, 'q')
    qc = QuantumCircuit(reg)
    s = reg[0]
    xr = [reg[1 + i] for i in range(nx)]
    yr = [reg[1 + nx + i] for i in range(ny)]
    allq = [reg[i] for i in range(n)]
    bits = [sw] + [(xw >> i) & 1 for i in range(nx)] + [(yw >> i) & 1 for i in range(ny)]
    dt = t / steps
    for _ in range(steps):
        if order == 1:
            _onsite(qc, s, gamma, dt)
            _shift_hop(qc, s, xr, gamma, dt)
            _shift_hop(qc, s, yr, gamma, dt)
            _mark(qc, allq, bits, eps, dt)
        else:
            h = dt / 2.0
            _onsite(qc, s, gamma, h)
            _shift_hop(qc, s, xr, gamma, h)
            _shift_hop(qc, s, yr, gamma, h)
            _mark(qc, allq, bits, eps, dt)
            _shift_hop(qc, s, yr, gamma, h)
            _shift_hop(qc, s, xr, gamma, h)
            _onsite(qc, s, gamma, h)
    return qc
