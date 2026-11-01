import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import XGate


def _real(v, name):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(name + ' must be a finite real number')
    return float(v)


def _int(v, name, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError(name + ' must be an integer in [' + str(lo) + ',' + str(hi) + ']')
    return v


def _shift(qc, coin, pos, n):
    # Eq. eq_2: coin 0 -> x+1 mod N, coin 1 -> x-1 mod N
    # Process bits from high to low so controls see the original lower bits.
    for k in range(n - 1, -1, -1):
        lower = [pos[j] for j in range(k)]
        targets = [coin] + lower + [pos[k]]
        inc = XGate().control(k + 1, ctrl_state=((1 << k) - 1) << 1)
        qc.append(inc, targets)
        dec = XGate().control(k + 1, ctrl_state=1)
        qc.append(dec, targets)


def build_circuit(instance):
    """Walk operator U_T...U_1 on 1 coin qubit + n position qubits.
    instance: {'position_qubits': n, 'steps': T, 'coins': [[theta,phi,lam], ...] (length T)}
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance.get('position_qubits'), 'position_qubits', 1, 11)
    steps = _int(instance.get('steps'), 'steps', 0, 64)
    coins = instance.get('coins')
    if not isinstance(coins, list) or len(coins) != steps:
        raise ValueError('coins must be a list of length steps')
    parsed = []
    for c in coins:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            raise ValueError('each coin must be [theta, phi, lam]')
        parsed.append([_real(c[0], 'theta'), _real(c[1], 'phi'), _real(c[2], 'lam')])
    coin = QuantumRegister(1, 'coin')
    pos = QuantumRegister(n, 'pos')
    qc = QuantumCircuit(coin, pos)
    for t in range(steps):
        # Eq. eq_1: U_t = S (C_t x I)
        qc.u(parsed[t][0], parsed[t][1], parsed[t][2], coin[0])
        _shift(qc, coin[0], list(pos), n)
    return qc
