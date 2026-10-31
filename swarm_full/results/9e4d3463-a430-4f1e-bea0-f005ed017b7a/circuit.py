from qiskit import QuantumCircuit, QuantumRegister
import math

_MAX_QUBITS = 12
_MAX_GATES = 4096


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _read_params(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    m = instance.get('num_qubits')
    if not _is_int(m) or m < 1 or m > _MAX_QUBITS:
        raise ValueError('num_qubits must be an integer in [1, 12]')
    phi = instance.get('phi')
    if isinstance(phi, bool) or not isinstance(phi, (int, float)):
        raise ValueError('phi must be a real number')
    phi = float(phi)
    if not math.isfinite(phi):
        raise ValueError('phi must be finite')
    counts = instance.get('gate_counts')
    if counts is None:
        # standard Kitaev distribution n_j = 2^j (reference case)
        counts = [2 ** j for j in range(m)]
    if not isinstance(counts, (list, tuple)) or len(counts) != m:
        raise ValueError('gate_counts must be a list of length num_qubits')
    for n in counts:
        if not _is_int(n) or n < 0:
            raise ValueError('gate_counts entries must be non-negative integers')
    total = sum(counts)
    if total < 1 or total > _MAX_GATES:
        raise ValueError('total gate number N must be in [1, 4096]')
    return m, phi, [int(n) for n in counts]


def build_circuit(instance):
    """Apply n_j phase gates P(phi) to probe qubit j (eq_1/eq_2 distribution stage).

    Qubit j acquires relative phase n_j*phi; total resource N = sum_j n_j.
    No state preparation or measurement is included.
    """
    m, phi, counts = _read_params(instance)
    q = QuantumRegister(m, 'q')
    qc = QuantumCircuit(q)
    for j in range(m):
        # each of the n_j gates is applied individually, so N counts physical gate uses
        for _ in range(counts[j]):
            qc.p(phi, q[j])
    return qc
