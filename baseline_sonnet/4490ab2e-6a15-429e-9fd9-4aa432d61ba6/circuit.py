from qiskit import QuantumCircuit, QuantumRegister
import math


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _lattice_edges(rows, cols):
    # open-boundary square lattice; site (i, j) -> qubit i*cols + j
    edges = []
    for i in range(rows):
        for j in range(cols):
            k = i * cols + j
            if j + 1 < cols:
                edges.append((k, k + 1))
            if i + 1 < rows:
                edges.append((k, k + cols))
    return edges


def build_circuit(instance):
    """Hadamard test of <alpha|G> for a square-lattice graph state G.

    Data qubits 0..n-1 (n = rows*cols), ancilla qubit n.
    |alpha_i> = P(phi_i) Ry(theta_i) |0>.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    rows = instance.get('rows')
    cols = instance.get('cols')
    for v in (rows, cols):
        if not isinstance(v, int) or isinstance(v, bool) or v < 1:
            raise ValueError('rows and cols must be positive integers')
    if rows * cols + 1 > 12:
        raise ValueError('total qubits (rows*cols + 1) must be at most 12')
    n = rows * cols
    theta = instance.get('theta')
    phi = instance.get('phi')
    for arr in (theta, phi):
        if not isinstance(arr, list) or len(arr) != n or not all(_num(x) for x in arr):
            raise ValueError('theta and phi must be lists of n finite numbers')
    imag = instance.get('imaginary_part', False)
    if not isinstance(imag, bool):
        raise ValueError('imaginary_part must be a bool')

    data = QuantumRegister(n, 'q')
    anc = QuantumRegister(1, 'a')
    qc = QuantumCircuit(data, anc)
    a = n

    qc.h(a)
    # controlled H layer (graph-state preparation from |0>), eq_2
    for k in range(n):
        qc.ch(a, k)
    # controlled CZ on every lattice edge (CCZ with ancilla), eq_2
    for (u, v) in _lattice_edges(rows, cols):
        qc.ccz(a, u, v)
    # controlled V^dagger = Ry(-theta) P(-phi), eq_3 (product-state overlap)
    for k in range(n):
        qc.cp(-float(phi[k]), a, k)
        qc.cry(-float(theta[k]), a, k)
    # eq_4: Im part via S^dagger on ancilla
    if imag:
        qc.sdg(a)
    qc.h(a)
    return qc
