from qiskit import QuantumCircuit, QuantumRegister


def _check_bit(v, name):
    if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
        raise ValueError(name + " must be 0 or 1")
    return v


def build_circuit(instance):
    """Operation H^n . U_f . H^n on n input qubits + 1 target qubit.

 instance: {"n": int in 1..11, "a": list of n bits, "b": 0 or 1}
 Qubit i (0<=i<n) is input bit x_i; qubit n is the oracle target.
 f(x) = XOR_i a[i]*x_i xor b.
 """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n + 1 > 12:
        raise ValueError("n must be an integer in 1..11")
    a = instance.get("a")
    if not isinstance(a, list) or len(a) != n:
        raise ValueError("a must be a list of n bits")
    a = [_check_bit(v, "a[i]") for v in a]
    b = _check_bit(instance.get("b"), "b")

    x = QuantumRegister(n, "x")
    t = QuantumRegister(1, "t")
    qc = QuantumCircuit(x, t)

    # eq_2: Hadamards on the input register before the query
    qc.h(x)
    # eq_1: XOR oracle U_f|x>|y> = |x>|y xor f(x)>, f(x)=a.x xor b
    for i in range(n):
        if a[i] == 1:
            qc.cx(x[i], t[0])
    if b == 1:
        qc.x(t[0])
    # eq_2: final Hadamards, mapping the phase state to (-1)^b |a>
    qc.h(x)
    return qc
