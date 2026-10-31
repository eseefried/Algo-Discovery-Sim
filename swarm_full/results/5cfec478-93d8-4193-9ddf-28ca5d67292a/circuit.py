import math
from qiskit import QuantumCircuit


def build_circuit(instance):
    """Apply U^k with U = exp(-i*phi*n.sigma/2) on one qubit, then an optional basis change."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    for key in ('phi', 'k', 'axis', 'basis'):
        if key not in instance:
            raise ValueError('missing key: ' + key)
    phi = instance['phi']
    k = instance['k']
    axis = instance['axis']
    basis = instance['basis']
    if isinstance(phi, bool) or not isinstance(phi, (int, float)) or not math.isfinite(phi):
        raise ValueError('phi must be a finite real number')
    if isinstance(k, bool) or not isinstance(k, int) or k < 0 or k > 1024:
        raise ValueError('k must be an integer in [0, 1024]')
    if not isinstance(axis, (list, tuple)) or len(axis) != 3:
        raise ValueError('axis must have 3 components')
    comps = []
    for a in axis:
        if isinstance(a, bool) or not isinstance(a, (int, float)) or not math.isfinite(a):
            raise ValueError('axis components must be finite reals')
        comps.append(float(a))
    nrm = math.sqrt(comps[0] ** 2 + comps[1] ** 2 + comps[2] ** 2)
    if nrm < 1e-12:
        raise ValueError('axis must be nonzero')
    if basis not in ('Z', 'X', 'Y'):
        raise ValueError('basis must be Z, X or Y')
    nx, ny, nz = comps[0] / nrm, comps[1] / nrm, comps[2] / nrm
    theta = math.acos(max(-1.0, min(1.0, nz)))
    az = math.atan2(ny, nx) if (abs(nx) > 1e-15 or abs(ny) > 1e-15) else 0.0
    qc = QuantumCircuit(1, name='repeated_gate')
    # eq_2: k literal repetitions of U = Rz(az) Ry(theta) Rz(phi) Ry(-theta) Rz(-az)
    for _ in range(k):
        qc.rz(-az, 0)
        qc.ry(-theta, 0)
        qc.rz(float(phi), 0)
        qc.ry(theta, 0)
        qc.rz(az, 0)
    # basis change before a computational-basis readout (done by the runner)
    if basis == 'X':
        qc.h(0)
    elif basis == 'Y':
        qc.sdg(0)
        qc.h(0)
    return qc
