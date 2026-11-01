from qiskit import QuantumCircuit, QuantumRegister
import math


def build_circuit(instance):
    """Second-order Trotter unitary U_r = (prod_{j=1..L} e^{-i c_j P_j t/2r} prod_{j=L..1} e^{-i c_j P_j t/2r})^r.

    instance: {"n_qubits": int 1..12, "time": float, "steps": int 1..1000,
               "terms": [{"pauli": str of length n over IXYZ (rightmost char = qubit 0), "coeff": float}, ...]}
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n_qubits")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 12:
        raise ValueError("n_qubits must be an integer in 1..12")
    t = instance.get("time")
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t):
        raise ValueError("time must be a finite real number")
    r = instance.get("steps")
    if isinstance(r, bool) or not isinstance(r, int) or r < 1 or r > 1000:
        raise ValueError("steps must be an integer in 1..1000")
    terms = instance.get("terms")
    if not isinstance(terms, list) or len(terms) == 0 or len(terms) > 200:
        raise ValueError("terms must be a list of 1..200 entries")
    parsed = []
    for item in terms:
        if not isinstance(item, dict):
            raise ValueError("each term must be a dict")
        label = item.get("pauli")
        coeff = item.get("coeff")
        if not isinstance(label, str) or len(label) != n:
            raise ValueError("pauli label must be a string of length n_qubits")
        for ch in label:
            if ch not in "IXYZ":
                raise ValueError("pauli label may only contain I, X, Y, Z")
        if isinstance(coeff, bool) or not isinstance(coeff, (int, float)) or not math.isfinite(coeff):
            raise ValueError("coeff must be a finite real number")
        parsed.append((label, float(coeff)))

    qc = QuantumCircuit(QuantumRegister(n, "q"))

    def apply_pauli_exp(label, theta):
        # implements exp(-i * theta * P) for Pauli string P
        active = [(i, label[n - 1 - i]) for i in range(n) if label[n - 1 - i] != "I"]
        if len(active) == 0:
            qc.global_phase = qc.global_phase - theta
            return
        for i, p in active:
            if p == "X":
                qc.h(i)
            elif p == "Y":
                qc.sdg(i)
                qc.h(i)
        qs = [i for i, _ in active]
        pairs = list(zip(qs[:-1], qs[1:]))
        for a, b in pairs:
            qc.cx(a, b)
        qc.rz(2.0 * theta, qs[-1])
        for a, b in reversed(pairs):
            qc.cx(a, b)
        for i, p in active:
            if p == "X":
                qc.h(i)
            elif p == "Y":
                qc.h(i)
                qc.s(i)

    tau = float(t) / (2.0 * r)
    for _ in range(r):
        for label, c in parsed:
            apply_pauli_exp(label, c * tau)
        for label, c in reversed(parsed):
            apply_pauli_exp(label, c * tau)
    return qc
