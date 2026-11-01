from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np


def _get_int(instance, key, lo, hi):
    if key not in instance:
        raise ValueError('missing key: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, np.integer)):
        raise ValueError(key + ' must be an integer')
    v = int(v)
    if v < lo or v > hi:
        raise ValueError(key + ' out of range')
    return v


def _phase_on_basis_state(qc, qubits, value, angle):
    # Applies diag(1,...,exp(i*angle) on |value>,...,1) = I + (e^{i angle}-1)|value><value|.
    # Bit i of value is qubit qubits[i] (little endian).
    zeros = [q for i, q in enumerate(qubits) if not (value >> i) & 1]
    for q in zeros:
        qc.x(q)
    qc.mcp(angle, list(qubits[:-1]), qubits[-1])
    for q in zeros:
        qc.x(q)


def _w_factor(qc, qubits, marked, dt):
    # eq_2/eq_3: exp(-i dt |w><w|); at dt=pi this equals the oracle I-2|w><w|
    _phase_on_basis_state(qc, qubits, marked, -dt)


def _s_factor(qc, qubits, dt):
    # eq_2/eq_3: exp(-i dt |s><s|) = H^n exp(-i dt |0><0|) H^n; at dt=pi it equals I-2|s><s|
    for q in qubits:
        qc.h(q)
    _phase_on_basis_state(qc, qubits, 0, -dt)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    """Lie-Trotter Grover evolution: m steps of (W(dt) S(dt)), S applied first in each step.

    instance keys: n (3..6), marked (0..2^n-1), steps (0..200), dt (finite real).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _get_int(instance, 'n', 3, 6)
    marked = _get_int(instance, 'marked', 0, 2 ** n - 1)
    steps = _get_int(instance, 'steps', 0, 200)
    if 'dt' not in instance:
        raise ValueError('missing key: dt')
    dt = instance['dt']
    if isinstance(dt, bool) or not isinstance(dt, (int, float, np.integer, np.floating)):
        raise ValueError('dt must be real')
    dt = float(dt)
    if not math.isfinite(dt):
        raise ValueError('dt must be finite')
    reg = QuantumRegister(n, 'search')
    qc = QuantumCircuit(reg)
    qubits = list(reg)
    for _ in range(steps):
        _s_factor(qc, qubits, dt)
        _w_factor(qc, qubits, marked, dt)
    return qc
