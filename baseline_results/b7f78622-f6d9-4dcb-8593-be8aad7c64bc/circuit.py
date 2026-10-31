"""Trine-POVM via a 3-step discrete-time quantum walk (Naimark dilation).

Registers (little-endian Qiskit convention):
  qubit 0            : coin / polarisation qubit, |0> = |H>, |1> = |V>
  qubits 1 .. n      : position register, x = sum_i 2**i * pos[i], pos[0] = qubit 1

The circuit implements U = U_3 U_2 U_1 of eq_3 with U_t = S (sum_x C_x^(t) (x) |x><x|)
(eq_2) and the coin schedule of eq_4.  With the walker prepared at x = 0 and the
position register read out afterwards, outcome x in {0,1,2} corresponds to the trine
element E_x = (2/3)|psi_x><psi_x| (eq_1).  No state preparation or measurement is
included here.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import HGate, RYGate, XGate

MAX_QUBITS = 12


def _validate(instance):
    """Return (num_position_qubits, trine_phase) or raise ValueError."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    allowed = {"num_position_qubits", "trine_phase"}
    for key in instance:
        if key not in allowed:
            raise ValueError("unknown instance key: %s" % str(key))
    n = instance.get("num_position_qubits", 2)
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("num_position_qubits must be an integer")
    if n < 2:
        raise ValueError("num_position_qubits must be >= 2 to hold positions 0,1,2")
    if 1 + n > MAX_QUBITS:
        raise ValueError("total qubits 1 + num_position_qubits exceeds %d" % MAX_QUBITS)
    phi = instance.get("trine_phase", 0.0)
    if isinstance(phi, bool) or not isinstance(phi, (int, float)):
        raise ValueError("trine_phase must be a real number")
    phi = float(phi)
    if not math.isfinite(phi):
        raise ValueError("trine_phase must be finite")
    return n, phi


def _shift(qc, coin, pos):
    """eq_2: S = |H><H| (x) I + |V><V| (x) (x -> x+1 mod 2**n).

    Controlled incrementer on the position register, controlled on coin = |1> = |V>.
    Most significant target first so that every step uses the *old* lower bits.
    """
    n = len(pos)
    for i in range(n - 1, 0, -1):
        controls = [coin] + [pos[j] for j in range(i)]
        qc.mcx(controls, pos[i])
    qc.cx(coin, pos[0])


def _site_coin(qc, gate, x, coin, pos):
    """eq_2: apply coin unitary `gate` to the coin qubit only at position |x>.

    ctrl_state = x is interpreted little-endian over the control list pos[0..n-1],
    matching the binary encoding x = sum_i 2**i * pos[i].
    """
    n = len(pos)
    cg = gate.control(n, ctrl_state=x)
    qc.append(cg, list(pos) + [coin])


def build_circuit(instance):
    """Build the trine-POVM quantum-walk dilation unitary (eq_2, eq_3, eq_4)."""
    n, phi = _validate(instance)

    coin_reg = QuantumRegister(1, "coin")
    pos_reg = QuantumRegister(n, "pos")
    qc = QuantumCircuit(coin_reg, pos_reg, name="trine_walk")
    coin = coin_reg[0]
    pos = [pos_reg[i] for i in range(n)]

    # Optional rotation of the trine plane about the Bloch z-axis:
    # measuring E'_k = W E_k W^dag with W = diag(1, e^{i phi}) is done by applying
    # W^dag to the coin before the (x-z plane) walk.
    if phi != 0.0:
        qc.p(-phi, coin)

    # Coin matrices of eq_4 (ordered basis |H>, |V>).
    # C2_0 = [[sqrt(2/3), -sqrt(1/3)], [sqrt(1/3), sqrt(2/3)]] = RY(theta),
    # theta/2 = arccos(sqrt(2/3)).
    theta = 2.0 * math.acos(math.sqrt(2.0 / 3.0))
    c2_0 = RYGate(theta)
    c2_1 = XGate()
    c3_1 = HGate()

    # Step 1 (eq_4): C1_0 = I, then shift S.
    _shift(qc, coin, pos)

    # Step 2 (eq_4): C2_0 at x=0, sigma_x at x=1, then shift S.
    _site_coin(qc, c2_0, 0, coin, pos)
    _site_coin(qc, c2_1, 1, coin, pos)
    _shift(qc, coin, pos)

    # Step 3 (eq_4): identity at x=0 and x=2, Hadamard at x=1, then shift S.
    _site_coin(qc, c3_1, 1, coin, pos)
    _shift(qc, coin, pos)

    # eq_3: position readout of this circuit's output (done by the runner) yields
    # E_x = K_x^dag K_x with K_x = (I (x) <x|) U (I (x) |0>), x in {0,1,2}.
    return qc
