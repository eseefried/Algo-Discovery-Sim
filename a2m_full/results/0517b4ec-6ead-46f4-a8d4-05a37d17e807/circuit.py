from qiskit import QuantumCircuit, QuantumRegister
import math


def _pos_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(name + ' must be a positive integer')
    return value


def _angle_list(instance, key, n):
    vals = instance.get(key)
    if not isinstance(vals, (list, tuple)) or len(vals) != n:
        raise ValueError(key + ' must be a list of length rows*cols')
    out = []
    for x in vals:
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
            raise ValueError(key + ' entries must be finite real numbers')
        out.append(float(x))
    return out


def build_circuit(instance):
    """Controlled (U_a^dagger V): ancilla = qubit 0, lattice site (r,c) = qubit 1 + r*cols + c.

    V = prod_{edges} CZ * H^{(x)n}  (eq_3, cluster-state preparation).
    U_a = prod_sites P(phi) Ry(theta), so U_a|0> = cos(t/2)|0> + e^{i phi} sin(t/2)|1>.
    U_a^dagger = prod_sites Ry(-theta) P(-phi).
    Every gate is controlled on the ancilla (eq_4 Hadamard-test structure).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    rows = _pos_int(instance.get('rows'), 'rows')
    cols = _pos_int(instance.get('cols'), 'cols')
    if rows * cols + 1 > 12:
        raise ValueError('total qubits (rows*cols + 1) must be at most 12')
    n = rows * cols
    theta = _angle_list(instance, 'theta', n)
    phi = _angle_list(instance, 'phi', n)

    anc = QuantumRegister(1, 'anc')
    lat = QuantumRegister(n, 'lat')
    qc = QuantumCircuit(anc, lat)
    a = anc[0]

    # controlled V: controlled-H on every site, then controlled-CZ on every edge
    for q in range(n):
        qc.ch(a, lat[q])
    for r in range(rows):
        for c in range(cols):
            q = r * cols + c
            if c + 1 < cols:
                qc.ccz(a, lat[q], lat[q + 1])
            if r + 1 < rows:
                qc.ccz(a, lat[q], lat[q + cols])

    # controlled U_a^dagger: P(-phi) first, then Ry(-theta)
    for q in range(n):
        qc.cp(-phi[q], a, lat[q])
        qc.cry(-theta[q], a, lat[q])
    return qc
