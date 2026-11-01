import math
from qiskit import QuantumCircuit, QuantumRegister


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + " must be an integer")
    return value


def _mcz(qc, qubits):
    # Multi-controlled Z: phase -1 on the all-ones state of `qubits`.
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        t = qubits[-1]
        qc.h(t)
        qc.mcx(list(qubits[:-1]), t)
        qc.h(t)


def build_circuit(instance):
    """Controlled Grover iterate U^steps (eq_3 built from eq_1).

    instance: {"n_data": int in 1..11, "marked": int in 0..2^n_data-1, "steps": int in 0..1000}
    Qubits 0..n_data-1: data register (little-endian); qubit n_data: control.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _as_int(instance.get("n_data"), "n_data")
    if n < 1 or n > 11:
        raise ValueError("n_data must be in 1..11")
    w = _as_int(instance.get("marked"), "marked")
    if w < 0 or w >= 2 ** n:
        raise ValueError("marked out of range")
    steps = _as_int(instance.get("steps"), "steps")
    if steps < 0 or steps > 1000:
        raise ValueError("steps must be in 0..1000")
    data = QuantumRegister(n, "data")
    ctrl = QuantumRegister(1, "control")
    qc = QuantumCircuit(data, ctrl)
    dq = list(data)
    c = ctrl[0]
    for _ in range(steps):
        # Controlled oracle I - 2|w><w| (eq_1, right factor)
        zeros = [dq[i] for i in range(n) if not (w >> i) & 1]
        for q in zeros:
            qc.x(q)
        _mcz(qc, [c] + dq)
        for q in zeros:
            qc.x(q)
        # Controlled diffusion I - 2|s><s| = H^n X^n (I - 2|0..0><0..0|) X^n H^n (eq_1, left factor)
        for q in dq:
            qc.h(q)
            qc.x(q)
        _mcz(qc, [c] + dq)
        for q in dq:
            qc.x(q)
            qc.h(q)
        # Overall minus sign of G, controlled on the control qubit (eq_3)
        qc.p(math.pi, c)
    return qc
