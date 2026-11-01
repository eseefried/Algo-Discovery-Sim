from qiskit import QuantumCircuit, QuantumRegister
import math


def _prep(qc, reg):
    # U: H on first qubit then CNOT fan-out (Bell state for n=2)
    qc.h(reg[0])
    for i in range(1, len(reg)):
        qc.cx(reg[0], reg[i])


def build_circuit(instance):
    """Swap-test unitary comparing U|0> (register A) with V|0> (register B)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if set(instance) - {"n", "v_variant", "theta"}:
        raise ValueError("unknown instance keys")
    n = instance.get("n", 2)
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or 1 + 2 * n > 12:
        raise ValueError("n must be an integer with 1 <= n <= 5")
    variant = instance.get("v_variant", "identical")
    if variant not in ("identical", "z", "x", "global_phase"):
        raise ValueError("invalid v_variant")
    theta = instance.get("theta", 0.0)
    if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
        raise ValueError("theta must be a finite real number")
    a = QuantumRegister(1, "a")
    A = QuantumRegister(n, "A")
    B = QuantumRegister(n, "B")
    qc = QuantumCircuit(a, A, B)
    # eq_3: I_a x U_A x V_B
    _prep(qc, A)
    _prep(qc, B)
    if variant == "z":
        qc.z(B[0])
    elif variant == "x":
        qc.x(B[0])
    elif variant == "global_phase":
        # P(theta) then X P(theta) X equals e^{i theta} * identity on this qubit
        qc.p(theta, B[0])
        qc.x(B[0])
        qc.p(theta, B[0])
        qc.x(B[0])
    # eq_3: H_a, CSWAP_{a;A,B}, H_a
    qc.h(a[0])
    for i in range(n):
        qc.cswap(a[0], A[i], B[i])
    qc.h(a[0])
    return qc
