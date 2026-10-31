'''Fast-signal assisted adiabatic quantum evolution for the 3-bit exact cover
problem (EC3), discretized with a first-order Trotter product formula.

build_circuit(instance) returns the unitary operation (eq_5)
    U = prod_{k=M}^{1} exp(-i f(t_k) V dt) exp(-i s_k dt H_P) exp(-i (1-s_k) dt H_B)
(k = M applied last), with H_B = sum_i (1 - X_i)/2 (eq_2), H_P the EC3
clause-penalty Hamiltonian (eq_3), s_k = k/M (eq_1), and V = sum_i P_i a
global single-qubit Pauli to which the fast signal f(t_k) couples (eq_4).
Input-state preparation (|+>^n) and measurement are NOT included.

Qubit layout: qubit index i-1 holds EC3 bit x_i (|0> <-> x_i = 0).
'''
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_STEPS = 2000
SIGNAL_TYPES = ('none', 'regular', 'random', 'custom')
PAULIS = ('X', 'Y', 'Z')


def _check_int(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError(f'{name} must be an integer')
    value = int(value)
    if value < lo or value > hi:
        raise ValueError(f'{name} must be in [{lo}, {hi}], got {value}')
    return value


def _check_float(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError(f'{name} must be a real number')
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f'{name} must be finite')
    return value


def _parse_clauses(raw, n):
    '''EC3 clauses as triples of distinct 1-based bit indices; returned 0-based.'''
    if not isinstance(raw, (list, tuple)) or len(raw) == 0:
        raise ValueError('clauses must be a non-empty list of triples')
    clauses = []
    for clause in raw:
        if not isinstance(clause, (list, tuple)) or len(clause) != 3:
            raise ValueError('each EC3 clause must be a triple of bit indices')
        idx = tuple(_check_int(v, 'clause index', 1, n) - 1 for v in clause)
        if len(set(idx)) != 3:
            raise ValueError('clause indices must be distinct')
        clauses.append(idx)
    return clauses


def _ising_coefficients(clauses, n):
    '''eq_3: H_P = sum_{(a,b,c)} (x_a + x_b + x_c - 1)^2 with x_i = (1 - Z_i)/2.

    Expanding each clause gives
        1 - (Z_a + Z_b + Z_c)/2 + (Z_a Z_b + Z_a Z_c + Z_b Z_c)/2,
    so H_P = const + sum_i h_i Z_i + sum_{i<j} J_ij Z_i Z_j.
    '''
    const = 0.0
    h = [0.0] * n
    couplings = {}
    for a, b, c in clauses:
        const += 1.0
        for i in (a, b, c):
            h[i] -= 0.5
        for i, j in ((a, b), (a, c), (b, c)):
            key = (min(i, j), max(i, j))
            couplings[key] = couplings.get(key, 0.0) + 0.5
    return const, h, couplings


def _signal_values(signal, m):
    '''eq_4: sampled fast-signal amplitudes f(t_k), k = 1..M (placeholder forms).'''
    if signal is None:
        return [0.0] * m, 'X'
    if not isinstance(signal, dict):
        raise ValueError('signal must be a dict or null')
    kind = signal.get('type', 'none')
    if kind not in SIGNAL_TYPES:
        raise ValueError(f'signal type must be one of {SIGNAL_TYPES}')
    pauli = signal.get('pauli', 'X')
    if pauli not in PAULIS:
        raise ValueError(f'signal pauli must be one of {PAULIS}')
    if kind == 'none':
        return [0.0] * m, pauli
    if kind == 'custom':
        values = signal.get('values')
        if not isinstance(values, (list, tuple)) or len(values) != m:
            raise ValueError('custom signal requires values with exactly M entries')
        return [_check_float(v, 'signal value') for v in values], pauli
    amplitude = _check_float(signal.get('amplitude', 0.0), 'signal amplitude')
    if kind == 'regular':
        # Regular alternating-sign sequence f(t_k) = A (-1)^k.
        return [amplitude * (1.0 if k % 2 == 0 else -1.0) for k in range(1, m + 1)], pauli
    # Random telegraph sequence f(t_k) = A r_k, r_k uniform in {-1, +1}, seeded.
    seed = _check_int(signal.get('seed', 0), 'signal seed', 0, 2 ** 32 - 1)
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, size=m)
    return [amplitude * (2.0 * float(b) - 1.0) for b in bits], pauli


def _apply_hb(qc, theta, n):
    '''eq_2: exp(-i theta H_B), H_B = sum_i (1 - X_i)/2.

    exp(-i theta (1 - X_i)/2) = exp(-i theta/2) * exp(+i theta X_i/2) = phase * RX(-theta).
    '''
    if theta == 0.0:
        return
    for i in range(n):
        qc.rx(-theta, i)
    qc.global_phase -= 0.5 * theta * n


def _apply_hp(qc, theta, const, h, couplings):
    '''eq_3: exp(-i theta H_P) exactly (all terms are diagonal and commute).

    exp(-i theta h Z) = RZ(2 theta h); exp(-i theta J ZZ) = RZZ(2 theta J).
    '''
    if theta == 0.0:
        return
    qc.global_phase -= theta * const
    for i, hi in enumerate(h):
        if hi != 0.0:
            qc.rz(2.0 * theta * hi, i)
    for (i, j), jij in sorted(couplings.items()):
        if jij != 0.0:
            qc.rzz(2.0 * theta * jij, i, j)


def _apply_signal(qc, phi, pauli, n):
    '''eq_4: exp(-i phi V), V = sum_i P_i, as RP(2 phi) on every qubit.'''
    if phi == 0.0:
        return
    for i in range(n):
        if pauli == 'X':
            qc.rx(2.0 * phi, i)
        elif pauli == 'Y':
            qc.ry(2.0 * phi, i)
        else:
            qc.rz(2.0 * phi, i)


def build_circuit(instance):
    '''Build the Trotterized fast-signal-assisted adiabatic evolution (eq_5).'''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _check_int(instance.get('n'), 'n', 1, MAX_QUBITS)
    clauses = _parse_clauses(instance.get('clauses'), n)
    total_time = _check_float(instance.get('T'), 'T')
    if total_time <= 0.0:
        raise ValueError('T must be positive')
    m = _check_int(instance.get('M'), 'M', 1, MAX_STEPS)
    dt = total_time / m
    f_values, pauli = _signal_values(instance.get('signal'), m)
    const, h, couplings = _ising_coefficients(clauses, n)

    reg = QuantumRegister(n, 'q')
    qc = QuantumCircuit(reg, name='fast_signal_aqc_ec3')
    # eq_5 / eq_1: k = 1..M in time order, s_k = t_k / T = k / M,
    # H(s_k) = (1 - s_k) H_B + s_k H_P; each step is split H_B -> H_P -> signal.
    for k in range(1, m + 1):
        s_k = k / m
        _apply_hb(qc, (1.0 - s_k) * dt, n)
        _apply_hp(qc, s_k * dt, const, h, couplings)
        _apply_signal(qc, f_values[k - 1] * dt, pauli, n)
    return qc
