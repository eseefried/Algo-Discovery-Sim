from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCXGate
import math


def _int_param(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError('parameter ' + key + ' must be an integer in [' + str(lo) + ', ' + str(hi) + ']')
    return v


def _prob_param(instance, key):
    v = instance.get(key, 0.0)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0.0 or v > 1.0:
        raise ValueError('parameter ' + key + ' must be a probability in [0, 1]')
    return float(v)


def _real_param(instance, key):
    v = instance.get(key, 0.0)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError('parameter ' + key + ' must be a finite real number')
    return float(v)


def build_circuit(instance):
    """DTQW operation. instance keys: n (position qubits), steps (T), p_s, q, theta0 (optional).
    Qubits: pos[0..n-1] (little endian), coin = n, spin ancillas n+1..n+T, spatial ancillas n+T+1..n+2T.
    Ancillas are assumed to start in |0>; they are the environment of the dephasing dilation."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int_param(instance, 'n', 1, 10)
    T = _int_param(instance, 'steps', 1, 5)
    if n + 1 + 2 * T > 12:
        raise ValueError('total qubits n+1+2*steps must not exceed 12')
    p_s = _prob_param(instance, 'p_s')
    q = _prob_param(instance, 'q')
    theta0 = _real_param(instance, 'theta0')

    pos = QuantumRegister(n, 'pos')
    coin = QuantumRegister(1, 'coin')
    aspin = QuantumRegister(T, 'aspin')
    aspace = QuantumRegister(T, 'aspace')
    qc = QuantumCircuit(pos, coin, aspin, aspace)
    c = coin[0]

    for t in range(T):
        # coin toss (eq_1): Hadamard on spin
        qc.h(c)
        # conditional shift (eq_1): spin 0 -> x+1, spin 1 -> x-1 (mod 2^n)
        # bit i of x+1 flips iff lower bits all 1; bit i of x-1 flips iff lower bits all 0.
        # process top bit first so lower bits are still the original values.
        for i in range(n - 1, -1, -1):
            controls = [c] + [pos[j] for j in range(i)]
            inc_state = 0
            for j in range(i):
                inc_state |= 1 << (j + 1)  # coin=0 (bit0 of state = 0), lower bits = 1
            qc.append(MCXGate(len(controls), ctrl_state=inc_state), controls + [pos[i]])
            dec_state = 1  # coin=1, lower bits = 0
            qc.append(MCXGate(len(controls), ctrl_state=dec_state), controls + [pos[i]])
        # optional quasi-stationary spin dephasing: fixed Z rotation per run
        if theta0 != 0.0:
            qc.rz(theta0, c)
        # spin dephasing dilation (eq_3): phase flip on coin with probability p_s
        if p_s > 0.0:
            qc.ry(2.0 * math.asin(math.sqrt(p_s)), aspin[t])
            qc.cz(aspin[t], c)
        # spatial dephasing dilation (eq_4): Z on least significant position qubit with probability q
        if q > 0.0:
            qc.ry(2.0 * math.asin(math.sqrt(q)), aspace[t])
            qc.cz(aspace[t], pos[0])
    return qc
