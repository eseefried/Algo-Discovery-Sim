'''Discrete-time quantum walk (DTQW) perfect state transfer of ONE unknown coin qubit
on a one-dimensional line, from site x = 0 to site x = d (scoped reconstruction).

Qubit layout (Qiskit little-endian, qubit 0 = least significant bit):
  qubits 0 .. n_p-1 : position register P storing y = x + 1 as an unsigned integer,
                      qubit m holds bit m of y, n_p = (d + 2).bit_length()
  qubit  n_p        : coin register C, which initially carries the unknown qubit |phi>
Sender site x = 0 is y = 1 (basis state 0...01 on P); receiver site x = d is y = d + 1.
The circuit is the bare operation U = X_C . U_T ... U_1 (T = d + 2); no state preparation
or measurement is included.
'''
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

MAX_QUBITS = 12


def _validate(instance):
    '''Validate the instance dict and return (d, apply_correction, n_p).'''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object (dict)')
    if 'd' not in instance:
        raise ValueError('instance must contain the integer target site d')
    d = instance['d']
    if isinstance(d, bool) or not isinstance(d, int):
        raise ValueError('d must be an integer')
    if d < 1:
        raise ValueError('d must be >= 1')
    apply_correction = True
    if 'apply_correction' in instance:
        apply_correction = instance['apply_correction']
        if not isinstance(apply_correction, bool):
            raise ValueError('apply_correction must be a boolean')
    # eq_1 register sizing: positions x in [-1, d+1] -> y in [0, d+2]
    n_p = (d + 2).bit_length()
    if n_p + 1 > MAX_QUBITS:
        raise ValueError('instance needs %d qubits, exceeding the cap of %d' % (n_p + 1, MAX_QUBITS))
    return d, apply_correction, n_p


def _shift(qc, pos, coin):
    '''eq_2: coin-conditioned shift S: y -> y + 1 if coin = 0, y -> y - 1 if coin = 1.

    QFT-basis adder: after QFTGate(n) the Fourier amplitude of |k> must acquire
    exp(2 pi i s k / 2^n) with s = 1 - 2c.  This is split into an unconditional +1
    phase p(2 pi 2^m / 2^n) on Fourier qubit m and a coin-controlled -2 phase
    cp(-4 pi 2^m / 2^n), followed by the inverse QFT on the same qubits.
    '''
    n = len(pos)
    qubits = [pos[m] for m in range(n)]
    qc.append(QFTGate(n), qubits)
    for m in range(n):
        ang = 2.0 * math.pi * float(2 ** m) / float(2 ** n)
        qc.p(ang, pos[m])
        qc.cp(-2.0 * ang, coin, pos[m])
    qc.append(QFTGate(n).inverse(), qubits)


def _flip_coin_at(qc, pos, coin, y):
    '''eq_3 / eq_5 coin operator: C_t(x) = X at the single site with label y, I elsewhere.'''
    n = len(pos)
    zero_bits = [pos[m] for m in range(n) if ((y >> m) & 1) == 0]
    for q in zero_bits:
        qc.x(q)
    qc.mcx([pos[m] for m in range(n)], coin)
    for q in zero_bits:
        qc.x(q)


def _walk_step(qc, pos, coin, flip_site_y):
    '''eq_3: U_t = S (sum_x |x><x| (x) C_t(x)); flip_site_y None means C_t(x) = I for all x.'''
    if flip_site_y is not None:
        _flip_coin_at(qc, pos, coin, flip_site_y)
    _shift(qc, pos, coin)


def build_circuit(instance):
    '''Build the DTQW perfect-state-transfer operation for the given instance.

    instance keys:
      d                : int >= 1, receiver site (transfer distance)
      apply_correction : optional bool (default True), apply V^dagger = X on the coin at the end
    '''
    d, apply_correction, n_p = _validate(instance)
    pos = QuantumRegister(n_p, 'pos')
    coin = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pos, coin, name='dtqw_pst_d%d' % d)
    c = coin[0]
    total_steps = d + 2  # T = d + 2
    # eq_5 coin schedule (with corrected final flip site):
    #   t = 1      : C = I everywhere
    #   t = 2      : C = X at x = -1 (y = 0)
    #   3..T-1     : C = I everywhere
    #   t = T      : C = X at x = T - 1 = d + 1 (y = d + 2)   [spec eq_5 wrote x = T - 2]
    for t in range(1, total_steps + 1):
        flip_y = None
        if t == 2:
            flip_y = 0
        elif t == total_steps:
            flip_y = d + 2
        _walk_step(qc, pos, c, flip_y)
    if apply_correction:
        # eq_4 / eq_6: transfer delivers X|phi>, so V = X; apply V^dagger = X to recover |phi>
        qc.x(c)
    return qc
