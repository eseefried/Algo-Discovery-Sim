from qiskit import QuantumCircuit, QuantumRegister
import math


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _parse(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "phi" not in instance or "n" not in instance:
        raise ValueError("instance requires 'phi' and 'n'")
    phi = instance["phi"]
    if isinstance(phi, bool) or not isinstance(phi, (int, float)):
        raise ValueError("phi must be a real number")
    phi = float(phi)
    if not math.isfinite(phi):
        raise ValueError("phi must be finite")
    counts = instance["n"]
    if not isinstance(counts, (list, tuple)):
        raise ValueError("n must be a list of nonnegative integers")
    m = len(counts)
    if m < 1 or m > 12:
        raise ValueError("number of qubits M must be between 1 and 12")
    for c in counts:
        if not _is_int(c) or c < 0:
            raise ValueError("each n_k must be a nonnegative integer")
    total = sum(counts)
    if total < 1:
        raise ValueError("total gate count N must be positive")
    if total > 4096:
        raise ValueError("total gate count N too large")
    if "N" in instance:
        if not _is_int(instance["N"]) or instance["N"] != total:
            raise ValueError("N must equal sum of n_k")
    return phi, [int(c) for c in counts]


def build_circuit(instance):
    """Apply n_k phase gates diag(1, e^{i phi}) to qubit k (eq_1, eq_2, eq_3).

    The runner is expected to prepare |+>^M beforehand.
    """
    phi, counts = _parse(instance)
    m = len(counts)
    q = QuantumRegister(m, "q")
    qc = QuantumCircuit(q)
    # eq_1: sum(counts) == N gates distributed over qubits
    for k in range(m):
        # eq_2: n_k sequential applications of U = diag(1, e^{i phi}) on qubit k
        for _ in range(counts[k]):
            qc.p(phi, q[k])
    # eq_3: no entangling gates, so the output stays a product state
    return qc
