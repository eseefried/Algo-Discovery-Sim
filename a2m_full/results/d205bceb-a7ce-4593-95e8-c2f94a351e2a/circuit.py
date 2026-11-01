import math
from qiskit import QuantumCircuit, QuantumRegister


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + " must be a finite real number")
    return float(x)


def _int(x, name):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError(name + " must be an integer")
    return x


def _vec(v, length, name):
    if not isinstance(v, (list, tuple)) or len(v) != length:
        raise ValueError(name + " must be a list of length " + str(length))
    return [_num(x, name) for x in v]


def _zz_layer(qc, J, dt):
    # eq_1 ZZ terms: exp(-i J dt Z Z) = RZZ(2 J dt)
    for j in range(len(J)):
        qc.rzz(2.0 * J[j] * dt, j, j + 1)


def _x_layer(qc, h, dt, frac):
    # eq_1 X terms: exp(-i h dt X) = RX(2 h dt)
    for j in range(len(h)):
        qc.rx(2.0 * h[j] * dt * frac, j)


def build_circuit(instance):
    """Trotterized exp(-i H t) of the open 1D transverse-field Ising chain on a patch.

    instance keys: n (2..8), J (n-1 floats), h (n floats), t (>0), steps (1..64),
    order (1 or 2), basis ('Z' or 'X'), q (0-indexed measured qubit, used only for X basis rotation).
    Site j is qubit j (qubit 0 = leftmost chain site).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int(instance.get("n"), "n")
    if n < 2 or n > 8:
        raise ValueError("n must be in 2..8")
    J = _vec(instance.get("J"), n - 1, "J")
    h = _vec(instance.get("h"), n, "h")
    t = _num(instance.get("t"), "t")
    if t <= 0:
        raise ValueError("t must be positive")
    steps = _int(instance.get("steps"), "steps")
    if steps < 1 or steps > 64:
        raise ValueError("steps must be in 1..64")
    order = _int(instance.get("order"), "order")
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    basis = instance.get("basis")
    if basis not in ("Z", "X"):
        raise ValueError("basis must be 'Z' or 'X'")
    q = _int(instance.get("q"), "q")
    if q < 0 or q >= n:
        raise ValueError("q out of range")
    dt = t / steps
    reg = QuantumRegister(n, "s")
    qc = QuantumCircuit(reg)
    for _ in range(steps):
        if order == 1:
            _zz_layer(qc, J, dt)
            _x_layer(qc, h, dt, 1.0)
        else:
            _x_layer(qc, h, dt, 0.5)
            _zz_layer(qc, J, dt)
            _x_layer(qc, h, dt, 0.5)
    if basis == "X":
        qc.h(q)  # eq_3 projector basis change: X-basis readout becomes Z-basis
    return qc
