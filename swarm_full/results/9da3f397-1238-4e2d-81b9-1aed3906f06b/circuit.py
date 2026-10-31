from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _int_param(instance, key, lo, hi):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' out of range')
    return v


def build_circuit(instance):
    """Lazy quantum walk: t x (coin on 2 coin qubits, then coin-conditioned shift -1/0/+1/0 mod 2^n).
    Layout: qubits 0,1 = coin (qubit 0 LSB); qubits 2..n+1 = position (LSB first)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int_param(instance, 'position_qubits', 2, 10)
    t = _int_param(instance, 'steps', 0, 1000)
    coin_type = instance.get('coin', 'dft')
    if coin_type not in ('dft', 'hadamard'):
        raise ValueError('coin must be dft or hadamard')
    N = 2 ** n
    if 2 * t + 1 > N:
        raise ValueError('position register too small: need 2*steps+1 <= 2^position_qubits')
    coin = QuantumRegister(2, 'coin')
    pos = QuantumRegister(n, 'pos')
    qc = QuantumCircuit(coin, pos)
    cq = [coin[0], coin[1]]
    pq = [pos[i] for i in range(n)]
    for _ in range(t):
        # coin operator
        if coin_type == 'dft':
            qc.append(QFTGate(2), cq)
        else:
            qc.h(coin[0])
            qc.h(coin[1])
        # conditional shift in the Fourier basis of the position register
        qc.append(QFTGate(n), pq)
        for value, sign in ((0, -1), (2, 1)):
            flips = [cq[b] for b in range(2) if not ((value >> b) & 1)]
            for q in flips:
                qc.x(q)
            for m in range(n):
                qc.mcp(sign * 2.0 * math.pi * (2 ** m) / N, cq, pq[m])
            for q in flips:
                qc.x(q)
        qc.append(QFTGate(n).inverse(), pq)
    return qc
