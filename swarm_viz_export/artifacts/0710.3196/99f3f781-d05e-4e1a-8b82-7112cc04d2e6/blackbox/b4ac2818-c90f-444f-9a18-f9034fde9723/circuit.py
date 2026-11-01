import math
from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    return value


def _phase_flip_all_ones(qc, n):
    # CCC..Z on all n qubits: phase -1 on |1...1>
    qc.mcp(math.pi, list(range(n - 1)), n - 1)


def _oracle(qc, n, w):
    # eq_2/eq_3: O_w = X^{wbar} CCCZ X^{wbar}; qubit j holds bit j of w
    zeros = [j for j in range(n) if ((w >> j) & 1) == 0]
    for j in zeros:
        qc.x(j)
    _phase_flip_all_ones(qc, n)
    for j in zeros:
        qc.x(j)


def _diffusion(qc, n):
    # eq_2/eq_3: D = 2|s><s| - I = -(H^n X^n CCCZ X^n H^n); the -1 is restored as global phase
    for j in range(n):
        qc.h(j)
    for j in range(n):
        qc.x(j)
    _phase_flip_all_ones(qc, n)
    for j in range(n):
        qc.x(j)
    for j in range(n):
        qc.h(j)
    qc.global_phase = qc.global_phase + math.pi


def _zz_layer(qc, n, phi):
    # eq_5: E_phi = prod_j exp(-i phi Z_j Z_{j+2} / 4) = RZZ(phi/2) on (j, j+2)
    for j in range(n - 2):
        qc.rzz(phi / 2.0, j, j + 2)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _as_int(instance.get('n', 4), 'n')
    if n < 2 or n > 12:
        raise ValueError('n must be between 2 and 12')
    w = _as_int(instance.get('w', 5), 'w')
    if w < 0 or w >= 2 ** n:
        raise ValueError('w out of range')
    phi = instance.get('phi', 0.0)
    if isinstance(phi, bool) or not isinstance(phi, (int, float)) or not math.isfinite(phi):
        raise ValueError('phi must be a finite real number')
    phi = float(phi)
    if 'iterations' in instance and instance['iterations'] is not None:
        k = _as_int(instance['iterations'], 'iterations')
    else:
        # eq_4: k = round(pi/4 sqrt(N) - 1/2)
        k = int(math.floor(math.pi / 4.0 * math.sqrt(2 ** n) - 0.5 + 0.5))
    if k < 0 or k > 100:
        raise ValueError('iterations must be between 0 and 100')
    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(qr)
    for _ in range(k):
        _oracle(qc, n, w)
        _diffusion(qc, n)
        if phi != 0.0:
            _zz_layer(qc, n, phi)
    return qc
