"""Scoped Qiskit reconstruction: dual-rail position-encoded qubits on a Bose-Hubbard graph.

Each graph vertex is one physical qubit (hard-core truncation: occupation 0 or 1).
Logical qubit k uses physical qubits 2k (rail 0, vertex v_0^(k)) and 2k+1 (rail 1, vertex v_1^(k)).
|0_L>_k  <->  boson on rail 0  <->  q[2k]=1, q[2k+1]=0
|1_L>_k  <->  boson on rail 1  <->  q[2k]=0, q[2k+1]=1
All gates are exact exponentials exp(-i H t) of piecewise-constant Bose-Hubbard segments (eq_1)
restricted to the hard-core subspace. hbar = 1.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_PHYSICAL_QUBITS = 12
MAX_LOGICAL_QUBITS = 6


def _check_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError('parameter ' + name + ' must be a real number')
    out = float(value)
    if not math.isfinite(out):
        raise ValueError('parameter ' + name + ' must be finite')
    return out


def _check_logical_index(value, num_logical, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError('parameter ' + name + ' must be an integer logical qubit index')
    if value < 0 or value >= num_logical:
        raise ValueError('logical qubit index ' + name + ' out of range')
    return value


def _rails(k):
    # eq_2: dual-rail position encoding; vertex v_0^(k) -> qubit 2k, vertex v_1^(k) -> qubit 2k+1
    return 2 * k, 2 * k + 1


def _apply_tunnel(qc, k, hop_j, time_t):
    # eq_3 (segment of eq_1 with only the intra-pair edge active):
    # H_X = -J (a0^dag a1 + a1^dag a0). For hard-core bosons a0^dag a1 + h.c. = (X0 X1 + Y0 Y1)/2,
    # so exp(-i H_X t) = exp(+i J t X0X1 / 2) exp(+i J t Y0Y1 / 2) = RXX(-J t) RYY(-J t)
    # (XX and YY commute). On span{|01>,|10>} this is exp(i J t X) = R_X(theta), theta = -2 J t.
    v0, v1 = _rails(k)
    angle = -hop_j * time_t
    qc.rxx(angle, v0, v1)
    qc.ryy(angle, v0, v1)


def _apply_bias(qc, k, eps, time_t):
    # eq_4 (segment of eq_1 with all edges off):
    # H_Z = (eps/2)(n_v0 - n_v1); exp(-i H_Z t) = P(-eps t/2) on rail 0 and P(+eps t/2) on rail 1,
    # which equals R_Z(theta) with theta = eps t on the logical dual-rail subspace.
    v0, v1 = _rails(k)
    qc.p(-0.5 * eps * time_t, v0)
    qc.p(0.5 * eps * time_t, v1)


def _apply_collide(qc, k, l, int_u, tau):
    # eq_5: collisional controlled phase. Net effect of transfer T, on-site wait tau (phase -U tau on the
    # doubly occupied vertex) and inverse transfer: CPHASE(phi) with phi = -U tau on |1_L 1_L>, i.e. a
    # conditional phase when both walkers sit on their rail-1 vertices. Implemented directly as
    # cp(-U tau) between the two rail-1 qubits (see specification_changes: transfer T and double
    # occupancy are not modelled in the hard-core truncation).
    _, v1_k = _rails(k)
    _, v1_l = _rails(l)
    qc.cp(-int_u * tau, v1_k, v1_l)


def build_circuit(instance):
    """Build the dual-rail Bose-Hubbard gate sequence as a unitary QuantumCircuit.

    instance = {
      'num_logical_qubits': n (1..6),
      'operations': [
        {'type': 'tunnel',  'qubit': k, 'J': J, 't': t},            # eq_3, logical R_X(-2 J t)
        {'type': 'bias',    'qubit': k, 'epsilon': eps, 't': t},    # eq_4, logical R_Z(eps t)
        {'type': 'collide', 'qubit_a': k, 'qubit_b': l, 'U': U, 'tau': tau}  # eq_5, CPHASE(-U tau)
      ]
    }
    Physical qubit 2k is rail 0 (v_0^(k)), qubit 2k+1 is rail 1 (v_1^(k)) of logical qubit k.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    if 'num_logical_qubits' not in instance:
        raise ValueError('instance must contain num_logical_qubits')
    num_logical = instance['num_logical_qubits']
    if isinstance(num_logical, bool) or not isinstance(num_logical, int):
        raise ValueError('num_logical_qubits must be an integer')
    if num_logical < 1 or num_logical > MAX_LOGICAL_QUBITS:
        raise ValueError('num_logical_qubits must be between 1 and ' + str(MAX_LOGICAL_QUBITS))
    num_physical = 2 * num_logical
    if num_physical > MAX_PHYSICAL_QUBITS:
        raise ValueError('too many physical qubits')
    if 'operations' not in instance:
        raise ValueError('instance must contain operations')
    operations = instance['operations']
    if not isinstance(operations, list):
        raise ValueError('operations must be a list')

    vertices = QuantumRegister(num_physical, 'v')
    qc = QuantumCircuit(vertices, name='bose_hubbard_dual_rail')

    for idx, op in enumerate(operations):
        tag = 'operations[' + str(idx) + ']'
        if not isinstance(op, dict) or 'type' not in op:
            raise ValueError(tag + ' must be a dict with a type field')
        kind = op['type']
        if kind == 'tunnel':
            for key in ('qubit', 'J', 't'):
                if key not in op:
                    raise ValueError(tag + ' missing ' + key)
            k = _check_logical_index(op['qubit'], num_logical, tag + '.qubit')
            hop_j = _check_number(op['J'], tag + '.J')
            time_t = _check_number(op['t'], tag + '.t')
            if time_t < 0.0:
                raise ValueError(tag + '.t must be non-negative')
            _apply_tunnel(qc, k, hop_j, time_t)
        elif kind == 'bias':
            for key in ('qubit', 'epsilon', 't'):
                if key not in op:
                    raise ValueError(tag + ' missing ' + key)
            k = _check_logical_index(op['qubit'], num_logical, tag + '.qubit')
            eps = _check_number(op['epsilon'], tag + '.epsilon')
            time_t = _check_number(op['t'], tag + '.t')
            if time_t < 0.0:
                raise ValueError(tag + '.t must be non-negative')
            _apply_bias(qc, k, eps, time_t)
        elif kind == 'collide':
            for key in ('qubit_a', 'qubit_b', 'U', 'tau'):
                if key not in op:
                    raise ValueError(tag + ' missing ' + key)
            k = _check_logical_index(op['qubit_a'], num_logical, tag + '.qubit_a')
            l = _check_logical_index(op['qubit_b'], num_logical, tag + '.qubit_b')
            if k == l:
                raise ValueError(tag + ' qubit_a and qubit_b must differ')
            int_u = _check_number(op['U'], tag + '.U')
            tau = _check_number(op['tau'], tag + '.tau')
            if tau < 0.0:
                raise ValueError(tag + '.tau must be non-negative')
            _apply_collide(qc, k, l, int_u, tau)
        else:
            raise ValueError(tag + ' has unknown type ' + str(kind))

    return qc
