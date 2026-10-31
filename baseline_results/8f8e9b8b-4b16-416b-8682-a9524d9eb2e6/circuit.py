"""Coined quantum walk on a finite chain with dynamic percolation (1D).

For a user-supplied sequence of edge configurations K_1..K_t the circuit is
the product unitary  U_{K_t} ... U_{K_1}  with  U_K = S_K (I_N x C)  (eq_3),
where S_K is the reflecting conditional shift of eq_2.  Averaging over
configurations (the random unitary map Phi of eq_3) is a classical task for
the runner: build one circuit per sampled configuration sequence.

Qubit layout (Qiskit little-endian, eq_1): qubit 0 = coin (|0>=L, |1>=R),
qubits 1..n = position bits, x = sum_k pos[k] 2^k, n = ceil(log2 N).
The basis integer is 2*x + c, i.e. |x> (x) |c> with the coin least significant.
Positions x >= N (padding when N is not a power of two) are never reached from
valid positions; on them the circuit only flips the coin each step (unitary).
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
COIN_NAMES = ("H", "X", "Y", "Z", "I")


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + " must be an integer")
    return value


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n_sites = _as_int(instance.get("N"), "N")
    if n_sites < 2:
        raise ValueError("N must be >= 2")
    n_pos = (n_sites - 1).bit_length()
    if n_pos + 1 > MAX_QUBITS:
        raise ValueError("instance needs more than 12 qubits")
    coin = instance.get("coin", "H")
    if coin not in COIN_NAMES:
        raise ValueError("coin must be one of " + ", ".join(COIN_NAMES))
    configs = instance.get("configs")
    if not isinstance(configs, list) or len(configs) == 0:
        raise ValueError("configs must be a non-empty list of edge configurations")
    clean = []
    for step, cfg in enumerate(configs):
        if not isinstance(cfg, list) or len(cfg) != n_sites - 1:
            raise ValueError("configs[%d] must have length N-1 = %d" % (step, n_sites - 1))
        bits = []
        for e, b in enumerate(cfg):
            if isinstance(b, bool):
                bits.append(1 if b else 0)
            elif isinstance(b, int) and b in (0, 1):
                bits.append(b)
            else:
                raise ValueError("configs[%d][%d] must be 0 or 1" % (step, e))
        clean.append(bits)
    if "p" in instance:
        p = instance["p"]
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0.0 <= p <= 1.0:
            raise ValueError("p must be a number in [0, 1]")
    return n_sites, n_pos, coin, clean


def _apply_coin(qc, coin_qubit, coin):
    """eq_3 / eq_6: the coin operator I_N (x) C acting on the coin qubit."""
    if coin == "H":
        qc.h(coin_qubit)
    elif coin == "X":
        qc.x(coin_qubit)
    elif coin == "Y":
        qc.y(coin_qubit)
    elif coin == "Z":
        qc.z(coin_qubit)
    # "I": identity coin, nothing to apply


def _swap_pair(qc, pos, coin_qubit, x, n_pos):
    """Transposition |x,R> <-> |x+1,L>, all other basis states fixed (eq_2).

    CNOTs from the coin into the position bits where x and x+1 differ map
    |x,1> -> |x+1,1> while leaving |x+1,0> unchanged; a multi-controlled X on
    the coin conditioned on position == x+1 then exchanges exactly these two
    states; the CNOT layer is undone afterwards.
    """
    y = x + 1
    diff = [k for k in range(n_pos) if ((x ^ y) >> k) & 1]
    zeros = [pos[k] for k in range(n_pos) if not ((y >> k) & 1)]
    for k in diff:
        qc.cx(coin_qubit, pos[k])
    for q in zeros:
        qc.x(q)
    qc.mcx(list(pos), coin_qubit)
    for q in zeros:
        qc.x(q)
    for k in diff:
        qc.cx(coin_qubit, pos[k])


def _apply_shift(qc, pos, coin_qubit, config, n_pos):
    """eq_2: S_K = (I (x) X) . prod_{(x,x+1) in K} SWAP(|x,R>, |x+1,L>).

    Present edge: |x,R> -> |x+1,L> -> |x+1,R| and |x+1,L> -> |x,R> -> |x,L>.
    Absent edge / chain end: state untouched by the swaps, coin flipped
    (reflection).  The transpositions are disjoint, so their order is free.
    """
    for x, present in enumerate(config):
        if present:
            _swap_pair(qc, pos, coin_qubit, x, n_pos)
    qc.x(coin_qubit)


def build_circuit(instance):
    """Return U_{K_t} ... U_{K_1} for instance["configs"] = [K_1, ..., K_t].

    Each K_s is a list of N-1 bits, bit x = 1 iff edge (x, x+1) is present.
    """
    n_sites, n_pos, coin, configs = _validate(instance)
    coin_reg = QuantumRegister(1, "coin")
    pos = QuantumRegister(n_pos, "pos")
    qc = QuantumCircuit(coin_reg, pos, name="percolation_walk")
    c = coin_reg[0]
    for config in configs:
        # eq_3: U_K = S_K (I_N x C), coin first then shift
        _apply_coin(qc, c, coin)
        _apply_shift(qc, pos, c, config, n_pos)
    return qc
