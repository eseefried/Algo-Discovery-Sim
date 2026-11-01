from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """Simon's algorithm operation: H^n on x, oracle U_f, H^n on x.
    instance: {"n": int in [2,6], "s": bitstring of length n, nonzero, s[0] is the most significant bit (qubit n-1)}.
    Oracle: j = lowest set bit of s; output bit k (for the k-th index i != j) = x_i XOR s_i*x_j.
    This is 2-to-1 with f(x)=f(y) iff y in {x, x^s}.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 6:
        raise ValueError("n must be an integer in [2, 6]")
    s = instance.get("s")
    if not isinstance(s, str) or len(s) != n or any(c not in "01" for c in s):
        raise ValueError("s must be a bitstring of length n")
    bits = [int(s[n - 1 - i]) for i in range(n)]
    if sum(bits) == 0:
        raise ValueError("s must be nonzero")
    j = min(i for i in range(n) if bits[i] == 1)
    xr = QuantumRegister(n, "x")
    yr = QuantumRegister(n, "y")
    qc = QuantumCircuit(xr, yr)
    for i in range(n):
        qc.h(xr[i])
    qc.barrier()
    # oracle U_f|x>|y> = |x>|y xor f(x)>
    others = [i for i in range(n) if i != j]
    for k, i in enumerate(others):
        qc.cx(xr[i], yr[k])
        if bits[i] == 1:
            qc.cx(xr[j], yr[k])
    qc.barrier()
    for i in range(n):
        qc.h(xr[i])
    return qc
