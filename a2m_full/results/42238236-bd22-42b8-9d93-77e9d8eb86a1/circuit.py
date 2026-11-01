from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate, RYGate, RZGate
import math


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(name + " must be a real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def build_circuit(instance):
    """Coherent QPE of U=exp(-i(H-E_ref)t) for the 2-qubit HeH+ Hamiltonian.
    Qubits: sys[0]=q0 (Z0,X0,Y0), sys[1]=q1, anc[k] (qubit 2+k) controls U^(2^k).
    Instance keys: m (int, 1..10), g (6 reals), t (>0), e_ref (real)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    m = instance.get("m")
    if isinstance(m, bool) or not isinstance(m, int) or m < 1 or m + 2 > 12:
        raise ValueError("m must be an integer with 1 <= m <= 10")
    g = instance.get("g")
    if not isinstance(g, (list, tuple)) or len(g) != 6:
        raise ValueError("g must contain exactly 6 coefficients")
    g = [_num(v, "g") for v in g]
    t = _num(instance.get("t"), "t")
    if t <= 0:
        raise ValueError("t must be positive")
    e_ref = _num(instance.get("e_ref"), "e_ref")
    g0, g1, g2, g3, g4, g5 = g
    # After CX(q0->q1): q1 holds parity p, and
    # H' = g0 + g3 Zp + (g1 + g2 Zp) Z_q0 + (g4 - g5 Zp) X_q0  (eq_1, eq_2)
    blocks = []
    for p in (0, 1):
        s = 1 - 2 * p
        a = g1 + s * g2
        b = g4 - s * g5
        blocks.append((p, math.atan2(b, a), math.hypot(a, b)))
    sysr = QuantumRegister(2, "sys")
    anc = QuantumRegister(m, "anc")
    qc = QuantumCircuit(sysr, anc)
    qc.h(anc)
    qc.cx(sysr[0], sysr[1])
    for k in range(m):
        tau = t * (2 ** k)
        c = anc[k]
        # scalar part: exp(-i tau (g0 - E_ref)) and exp(-i tau g3 Zp) (eq_3)
        qc.p(tau * (e_ref - g0), c)
        qc.crz(2.0 * tau * g3, c, sysr[1])
        # block rotation exp(-i tau (a Z + b X)) = Ry(beta) Rz(2 tau r) Ry(-beta), per parity p
        for p, beta, r in blocks:
            qc.append(RYGate(-beta).control(1, ctrl_state=p), [sysr[1], sysr[0]])
        for p, beta, r in blocks:
            qc.append(RZGate(2.0 * tau * r).control(2, ctrl_state=1 + 2 * p), [c, sysr[1], sysr[0]])
        for p, beta, r in blocks:
            qc.append(RYGate(beta).control(1, ctrl_state=p), [sysr[1], sysr[0]])
    qc.cx(sysr[0], sysr[1])
    qc.append(QFTGate(m).inverse(), list(anc))
    return qc
