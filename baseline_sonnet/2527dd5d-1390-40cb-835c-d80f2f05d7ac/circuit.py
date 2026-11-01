from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
import math

_COINS = ("identity", "flip")
_FINALS = ("auto", "identity", "flip")


def _get_int(inst, key, lo, hi):
    if key not in inst:
        raise ValueError("missing parameter: " + key)
    v = inst[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + " must be an integer")
    if v < lo or v > hi:
        raise ValueError(key + " out of range")
    return v


def _apply_coin(qc, coin_idx, kind):
    # Coin operator C on the coin qubit (eq_2): identity or flip X.
    if kind == "flip":
        qc.x(coin_idx)


def _apply_shift(qc, coin_idx, pos_idx):
    # Conditional shift S (eq_1): coin 0 -> x+1, coin 1 -> x-1 (mod 2^n).
    # In the Fourier basis, x -> x+1 is phase exp(2*pi*i*k/N) on |k>.
    # Per position bit j: p(theta_j) unconditionally and cp(-2*theta_j) from coin,
    # giving +theta_j for coin 0 and -theta_j for coin 1.
    n = len(pos_idx)
    big_n = 2 ** n
    qc.append(QFTGate(n), pos_idx)
    for j, q in enumerate(pos_idx):
        theta = 2.0 * math.pi * (2 ** j) / big_n
        qc.p(theta, q)
        qc.cp(-2.0 * theta, coin_idx, q)
    qc.append(QFTGate(n).inverse(), pos_idx)


def build_circuit(instance):
    """Walk operation: (C_f on coin) * (S (C x I))^t. Qubit 0 = coin, qubits 1..n = position (qubit 1 is LSB)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _get_int(instance, "position_qubits", 1, 11)
    t = _get_int(instance, "steps", 0, 256)
    coin = instance.get("coin", "flip")
    final = instance.get("final_coin", "auto")
    if coin not in _COINS:
        raise ValueError("coin must be 'identity' or 'flip'")
    if final not in _FINALS:
        raise ValueError("final_coin must be 'auto', 'identity' or 'flip'")
    qc = QuantumCircuit(n + 1, name="qwalk_circle")
    coin_idx = 0
    pos_idx = list(range(1, n + 1))
    for _ in range(t):
        _apply_coin(qc, coin_idx, coin)
        _apply_shift(qc, coin_idx, pos_idx)
    # Final state-independent coin C_f (eq_3, eq_4)
    if final == "auto":
        if coin == "flip" and t % 2 == 1:
            qc.x(coin_idx)
    elif final == "flip":
        qc.x(coin_idx)
    return qc
