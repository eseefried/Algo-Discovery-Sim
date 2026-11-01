from qiskit import QuantumCircuit


def build_circuit(instance):
    """Bell-basis encoding operation (eq_3), repeated over m control/target pairs.

    instance: {"m": int in [1, 6]}; "m" is optional and defaults to 1.
    Qubits 0..m-1 are controls, qubits m..2m-1 are targets (pair i = (i, m+i)).
    For input |a>|b> the output is 2^(-m/2) sum_x (-1)^(a.x) |x>|x xor b>.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    m = instance.get("m", 1)
    if isinstance(m, bool) or not isinstance(m, int):
        raise ValueError("m must be an integer")
    if m < 1 or 2 * m > 12:
        raise ValueError("m must satisfy 1 <= m <= 6")
    qc = QuantumCircuit(2 * m, name="bell_like_encoder")
    for i in range(m):
        # eq_3: (H on control) then CNOT control->target
        qc.h(i)
        qc.cx(i, m + i)
    return qc
