from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import XGate, ZGate


def _int_param(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    if v < lo or v > hi:
        raise ValueError(key + " out of range")
    return v


def _marked_coin(qc, pos, coin, p, m):
    # eq_2: Grover coin for d=2, C = 2|+><+| - I = X, applied at every node
    qc.x(coin[0])
    # eq_3: at the marked node the coin is -I; undo X there, then add phase -1
    qc.append(XGate().control(p, ctrl_state=m), list(pos) + [coin[0]])
    zero_bits = [pos[k] for k in range(p) if not ((m >> k) & 1)]
    for q in zero_bits:
        qc.x(q)
    qc.append(ZGate().control(p - 1), list(pos))
    for q in zero_bits:
        qc.x(q)


def _shift(qc, pos, coin, p):
    # eq_3: S|x,0> = |x+1,0>, S|x,1> = |x-1,1> (mod 2^p)
    for i in range(p - 1, -1, -1):
        # increment bit i if coin==0 and all lower bits are 1
        cs_inc = ((1 << i) - 1) << 1
        qc.append(XGate().control(i + 1, ctrl_state=cs_inc), [coin[0]] + [pos[k] for k in range(i)] + [pos[i]])
        # decrement bit i if coin==1 and all lower bits are 0
        qc.append(XGate().control(i + 1, ctrl_state=1), [coin[0]] + [pos[k] for k in range(i)] + [pos[i]])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    p = _int_param(instance, "position_qubits", 2, 11)
    n = 1 << p
    m = _int_param(instance, "marked_node", 0, n - 1)
    t = _int_param(instance, "steps", 0, 1000)
    pos = QuantumRegister(p, "pos")
    coin = QuantumRegister(1, "coin")
    qc = QuantumCircuit(pos, coin)
    for _ in range(t):
        _marked_coin(qc, pos, coin, p, m)
        _shift(qc, pos, coin, p)
    return qc
