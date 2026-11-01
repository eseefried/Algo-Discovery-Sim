import math
from qiskit import QuantumCircuit, QuantumRegister


def _h12(qc):
    """Hadamard acting on qutrit levels 1 and 2 (levels 0 and 3 fixed)."""
    qc.cx(1, 0)
    qc.ch(0, 1)
    qc.cx(1, 0)


def _f3(qc):
    """Generalized Hadamard F_3 on qubits (0,1), identity on level 3 (eq_3).
    F_3 = H12 . Ry01(theta) . (1 + W), with W = diag(-1,i).H on levels 1,2."""
    _h12(qc)
    qc.x(1)
    qc.cp(math.pi, 0, 1)
    qc.x(1)
    qc.x(0)
    qc.cp(math.pi / 2, 0, 1)
    qc.x(0)
    theta = 2.0 * math.atan(math.sqrt(2.0))
    qc.x(1)
    qc.cry(theta, 1, 0)
    qc.x(1)
    _h12(qc)


def build_circuit(instance):
    """Hybrid QFT: one qutrit (2 qubits) plus m qubits. Z_N with N=3*2^m."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key not in ('num_qubits', 'inverse'):
            raise ValueError('unknown instance key')
    m = instance.get('num_qubits')
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError('num_qubits must be an integer')
    if m < 1 or m + 2 > 12:
        raise ValueError('num_qubits must be in 1..10')
    inverse = instance.get('inverse', False)
    if not isinstance(inverse, bool):
        raise ValueError('inverse must be a bool')
    qutrit = QuantumRegister(2, 'qutrit')
    qubits = QuantumRegister(m, 'qubit')
    qc = QuantumCircuit(qutrit, qubits)
    # eq_3: generalized Hadamard on the qutrit
    _f3(qc)
    # eq_4: qutrit -> qubit k controlled phases, exp(2 pi i l x_k / (3*2^k)), l=q0+2*q1
    for k in range(1, m + 1):
        t = 1 + k
        ang = 2.0 * math.pi / (3.0 * (2 ** k))
        qc.cp(ang, 0, t)
        qc.cp(2.0 * ang, 1, t)
    # eq_3 (H) and eq_5 (qubit-qubit controlled phases), no final swaps
    for i in range(1, m + 1):
        qi = 1 + i
        qc.h(qi)
        for j in range(i + 1, m + 1):
            qc.cp(2.0 * math.pi / (2 ** (j - i + 1)), 1 + j, qi)
    if inverse:
        qc = qc.inverse()
    return qc
