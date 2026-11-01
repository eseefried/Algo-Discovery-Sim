from qiskit import QuantumCircuit
import math


def _num(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + " must be a finite real number")
    return float(v)


def _int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(name + " must be an integer")
    return v


def build_circuit(instance):
    """Trotterized exp(-i H t), H = -gamma*A - epsilon|w><w|, 2x2 periodic honeycomb (8 sites).

    Site index s = x + 2*y + 4*b with qubits 0,1,2 = bits of s. Honeycomb A(x,y) -> (x, y, x^y),
    B(u,v) -> (u, v, 1^u^v). A(x,y) neighbours are B(x,y), B(x+1,y), B(x,y+1) (mod 2),
    which are exactly the three single-bit flips, so A = X0 + X1 + X2 (cube graph).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    gamma = _num(instance.get("gamma"), "gamma")
    eps = _num(instance.get("epsilon"), "epsilon")
    t = _num(instance.get("t"), "t")
    w = _int(instance.get("marked_site"), "marked_site")
    r = _int(instance.get("trotter_steps", 1), "trotter_steps")
    if gamma <= 0.0:
        raise ValueError("gamma must be positive")
    if t < 0.0:
        raise ValueError("t must be nonnegative")
    if w < 0 or w > 7:
        raise ValueError("marked_site must be in 0..7")
    if r < 1 or r > 500:
        raise ValueError("trotter_steps must be in 1..500")
    n = 3
    dt = t / r
    qc = QuantumCircuit(n)
    for _ in range(r):
        # half step of hopping: exp(+i gamma dt/2 X) = RX(-gamma dt)
        for q in range(n):
            qc.rx(-gamma * dt, q)
        # marking: exp(+i eps dt |w><w|) = phase eps*dt on |w>
        zeros = [q for q in range(n) if ((w >> q) & 1) == 0]
        for q in zeros:
            qc.x(q)
        qc.mcp(eps * dt, [0, 1], 2)
        for q in zeros:
            qc.x(q)
        # second half step of hopping
        for q in range(n):
            qc.rx(-gamma * dt, q)
    return qc
