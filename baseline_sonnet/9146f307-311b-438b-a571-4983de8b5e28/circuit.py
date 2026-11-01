from qiskit import QuantumCircuit, QuantumRegister
import math


def _apply_gate(qc, reg, spec):
    """Append one explicit single-qubit gate U_i to the system register."""
    if not isinstance(spec, dict):
        raise ValueError('each gate spec must be an object')
    name = spec.get('name')
    q = spec.get('qubit')
    if not isinstance(name, str):
        raise ValueError('gate name must be a string')
    if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= len(reg):
        raise ValueError('gate qubit out of range')
    qb = reg[q]
    fixed = {'h': qc.h, 'x': qc.x, 'y': qc.y, 'z': qc.z, 's': qc.s, 't': qc.t, 'sdg': qc.sdg, 'tdg': qc.tdg}
    param = {'rx': qc.rx, 'ry': qc.ry, 'rz': qc.rz, 'p': qc.p}
    if name in fixed:
        fixed[name](qb)
    elif name in param:
        angle = spec.get('angle')
        if isinstance(angle, bool) or not isinstance(angle, (int, float)) or not math.isfinite(angle):
            raise ValueError('parametrized gate needs a finite numeric angle')
        param[name](float(angle), qb)
    else:
        raise ValueError('unsupported gate name')


def build_circuit(instance):
    """Implement W_sigma = U_{sigma(n)} o ... o U_{sigma(1)} (eq_1).

    instance: {'num_qubits': m, 'sigma': [sigma(1),...,sigma(n)] (1-indexed),
               'gates': [U_1,...,U_n] each {'name':..., 'qubit':..., 'angle':...}}
    U_{sigma(1)} is applied first.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    m = instance.get('num_qubits')
    sigma = instance.get('sigma')
    gates = instance.get('gates')
    if isinstance(m, bool) or not isinstance(m, int) or m < 1 or m > 12:
        raise ValueError('num_qubits must be an integer in 1..12')
    if not isinstance(sigma, list) or not isinstance(gates, list):
        raise ValueError('sigma and gates must be lists')
    n = len(gates)
    if n < 1 or n > 32 or len(sigma) != n:
        raise ValueError('need 1..32 gates and sigma of equal length')
    for s in sigma:
        if isinstance(s, bool) or not isinstance(s, int):
            raise ValueError('sigma entries must be integers')
    if sorted(sigma) != list(range(1, n + 1)):
        raise ValueError('sigma must be a permutation of 1..n')
    reg = QuantumRegister(m, 'system')
    qc = QuantumCircuit(reg)
    # eq_1: apply U_{sigma(1)} first, ..., U_{sigma(n)} last
    for k in range(n):
        _apply_gate(qc, reg, gates[sigma[k] - 1])
    return qc
