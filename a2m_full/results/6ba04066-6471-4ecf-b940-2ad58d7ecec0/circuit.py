from qiskit import QuantumCircuit


def _check_bit(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1):
        raise ValueError(name + ' must be the integer 0 or 1')
    return value


def build_circuit(instance):
    """Deutsch operation for Z_2: one oracle query then H on the control.

    Qubit 0 = x (control, phase-kickback register), qubit 1 = y (target).
    instance: {'f0': 0|1, 'f1': 0|1}, the two Z_2 elements (oracle values).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    if 'f0' not in instance or 'f1' not in instance:
        raise ValueError('instance requires f0 and f1')
    f0 = _check_bit(instance['f0'], 'f0')
    f1 = _check_bit(instance['f1'], 'f1')
    qc = QuantumCircuit(2)
    # eq_4: single query U_f|x>|y> = |x>|y xor f(x)>, built from X/CX
    if f0 == 1:
        qc.x(0)
        qc.cx(0, 1)
        qc.x(0)
    if f1 == 1:
        qc.cx(0, 1)
    # eq_4: Hadamard basis change reads the kicked-back phase (-1)^(f0+f1)
    qc.h(0)
    return qc
