import math

from qiskit import QuantumCircuit


def _real_param(instance, key):
    if not isinstance(instance, dict) or key not in instance:
        raise ValueError('instance must be a dict containing ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + ' must be finite')
    return v


def build_circuit(instance):
    """U_tot = CZ (I x Rz(phi)) (Rx(theta) x I) on the dual-rail logical space.

    Layout (eq_2): basis index = 2*q0 + q1, logical qubit 0 is the left tensor
    factor / most significant bit. In Qiskit: logical qubit 0 -> circuit qubit 1,
    logical qubit 1 -> circuit qubit 0.
    """
    theta = _real_param(instance, 'theta')
    phi = _real_param(instance, 'phi')
    qc = QuantumCircuit(2, name='bosonic_walker_dual_rail')
    # eq_3: Rx(theta) = exp(-i theta X/2) on logical qubit 0 (hopping between its two rails)
    qc.rx(theta, 1)
    # eq_4: Rz(phi) = diag(exp(-i phi/2), exp(i phi/2)) on logical qubit 1 (rail detuning)
    qc.rz(phi, 0)
    # eq_5: CZ = diag(1,1,1,-1) = exp(-i U t |11><11|) at U t = pi (on-site interaction phase)
    qc.cz(1, 0)
    return qc
