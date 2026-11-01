from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate
import math


def _qutrit_dft(qc, lo, hi):
    """3x3 DFT H_3 on qutrit levels 0=|hi0,lo0>, 1=|hi0,lo1>, 2=|hi1,lo1>.
    H_3 = H_{12} . R01 . S_{12} . H_{12} (time order H, S, R01, H); |hi1,lo0> is untouched."""
    qc.ch(lo, hi)
    qc.cp(math.pi / 2, lo, hi)
    qc.x(hi)
    qc.cz(hi, lo)
    qc.cry(2.0 * math.acos(1.0 / math.sqrt(3.0)), hi, lo)
    qc.x(hi)
    qc.ch(lo, hi)


def _twiddle(qc, lo, hi, digits, n):
    """Generalized controlled phase exp(2 pi i x_l y'/N), x_l=sum 2^k x_k, y'=lo+lo*hi in {0,1,2}."""
    big_n = 3 * (2 ** n)
    for k in range(n):
        theta = 2.0 * math.pi * (2 ** k) / big_n
        qc.cp(theta, digits[k], lo)
        qc.mcp(theta, [digits[k], lo], hi)


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    for key in instance:
        if key not in ('n_qubits', 'inverse'):
            raise ValueError('unknown key ' + str(key))
    n = instance.get('n_qubits')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 10:
        raise ValueError('n_qubits must be an integer in 1..10')
    inv = instance.get('inverse', False)
    if not isinstance(inv, bool):
        raise ValueError('inverse must be a boolean')
    qutrit = QuantumRegister(2, 'qutrit')
    digits = QuantumRegister(n, 'qubits')
    qc = QuantumCircuit(qutrit, digits)
    lo = qutrit[0]
    hi = qutrit[1]
    dig = list(digits)
    _qutrit_dft(qc, lo, hi)
    _twiddle(qc, lo, hi, dig, n)
    qc.append(QFTGate(n), dig)
    if inv:
        return qc.inverse()
    return qc
