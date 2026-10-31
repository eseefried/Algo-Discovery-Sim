import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in instance:
        if key not in ('num_register_qubits', 'inverse'):
            raise ValueError('unknown instance key: ' + str(key))
    m = instance.get('num_register_qubits')
    if isinstance(m, bool) or not isinstance(m, int) or m < 1 or m > 10:
        raise ValueError('num_register_qubits must be an integer in 1..10')
    inv = instance.get('inverse', False)
    if not isinstance(inv, bool):
        raise ValueError('inverse must be a bool')
    return m, inv


def _qutrit_dft(qc, a, b):
    # eq_2: H_3 = DFT_3 on levels {0,1,2}; level = q_a + 2*q_b; level 3 fixed.
    # DFT_3 = S^dag R^dag D H12 (two-level decomposition); time order below.
    # H12: Hadamard on levels (1,2) via CX conjugation and controlled-H.
    qc.cx(b, a)
    qc.ch(a, b)
    qc.cx(b, a)
    # D = diag(1,-1,-i,1) on levels 0..3
    qc.x(b)
    qc.cz(a, b)
    qc.x(b)
    qc.x(a)
    qc.cp(-math.pi / 2, b, a)
    qc.x(a)
    # R^dag: rotation on levels (0,1), applied when q_b = 0
    qc.cry(2.0 * math.atan(math.sqrt(2.0)), b, a, ctrl_state=0)
    # S^dag: rotation on levels (1,2)
    qc.cx(b, a)
    qc.cry(math.pi / 2, a, b)
    qc.cx(b, a)


def build_circuit(instance):
    """Hybrid qutrit+qubits QFT (mixed radix 3*2^m). Output digit order k=k1+3*k2."""
    m, inv = _validate(instance)
    t = QuantumRegister(2, 't')
    r = QuantumRegister(m, 'r')
    qc = QuantumCircuit(t, r)
    n_total = 3 * (2 ** m)
    # Step 1 (eq_2): generalized Hadamard on the qutrit
    _qutrit_dft(qc, 0, 1)
    # Step 2 (eq_3): generalized controlled phase exp(2 pi i k1 j0 / N)
    for i in range(m):
        theta = 2.0 * math.pi * (2 ** i) / n_total
        qc.cp(theta, 0, 2 + i)
        qc.cp(2.0 * theta, 1, 2 + i)
    # Step 3 (eq_1): QFT of dimension 2^m on the qubit register
    qc.append(QFTGate(m), list(range(2, 2 + m)))
    if inv:
        return qc.inverse()
    return qc
