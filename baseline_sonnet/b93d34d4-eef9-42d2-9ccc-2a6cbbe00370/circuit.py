from qiskit import QuantumCircuit
import math


def _real(instance, key):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + ' must be finite')
    return v


def _int(instance, key):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    return v


def build_circuit(instance):
    """Logical single-qubit operation of a walker on a two-vertex graph.

    Encoding (eq_2): circuit qubit q holds the logical qubit; |0>_L = walker at
    vertex 1, |1>_L = walker at vertex 2.
    Parameters: num_qubits, target, J, t_hop, delta, t_pot.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance, 'num_qubits')
    if n < 1 or n > 12:
        raise ValueError('num_qubits must be in 1..12')
    target = _int(instance, 'target')
    if target < 0 or target >= n:
        raise ValueError('target out of range')
    J = _real(instance, 'J')
    t_hop = _real(instance, 't_hop')
    delta = _real(instance, 'delta')
    t_pot = _real(instance, 't_pot')
    if t_hop < 0 or t_pot < 0:
        raise ValueError('evolution times must be nonnegative')
    qc = QuantumCircuit(n)
    # eq_3: H_X = -J(a1^dag a2 + h.c.) -> exp(-i H_X t) = exp(i J t X_L) = RX(theta), theta = -2 J t
    theta = -2.0 * J * t_hop
    qc.rx(theta, target)
    # eq_4: H_Z = (Delta/2)(n1 - n2) -> exp(-i phi Z_L / 2), phi = Delta t (hopping off)
    phi = delta * t_pot
    qc.rz(phi, target)
    return qc
