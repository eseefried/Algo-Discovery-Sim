'''Szegedy-type unitary quantization of a finite-graph open quantum walk (OQW).

Registers (tensor order internal x node1 x node2; Qiskit little-endian inside
each register, qubit 0 of the circuit is the least significant internal bit):
  internal : m qubits, the OQW internal (coin-like) space, d = 2**m
  node1    : nb = ceil(log2 n) qubits, source node j (basis state |j>)
  node2    : nb qubits, destination node i (basis state |i>)

Scope restriction (reported in specification_changes): the Kraus operators
are B_i^j = sqrt(p_ij) * V_i^j with V_i^j a tensor product of single-qubit
gates from {I, X, Y, Z, H, S, T}, one letter per internal qubit.  The Kraus
constraint of eq_1, sum_i B_i^j^dag B_i^j = I, then reads sum_i p_ij = 1 for
every source node j and is validated.

The returned circuit is U**steps with (eq_3)
    U   = S R_A,
    R_A = U_A (I x I x (2|0><0| - I)) U_A^dagger,
where U_A is the controlled Stinespring dilation realising the isometry A of
eq_2:  U_A |xi>|j>|0> = sum_i (B_i^j|xi>) |j>|i> = A(|xi>|j>).
Optionally (key "prepend_isometry") U_A itself is prepended so that the
runner-supplied |xi_0>|j_0>|0> is mapped to |Psi_0> = A(|xi_0>|j_0>) (eq_6).
'''
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import HGate, RYGate, SGate, TGate, XGate, YGate, ZGate

_TOL = 1e-9
_SUM_TOL = 1e-6
_MAX_QUBITS = 12
_MAX_STEPS = 1000
_ALLOWED = 'IXYZHST'


def _check_int(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    if value < low or value > high:
        raise ValueError(name + ' out of range [' + str(low) + ', ' + str(high) + ']')
    return value


def _check_prob(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + ' must be a real number')
    p = float(value)
    if math.isnan(p) or p < -_TOL or p > 1.0 + _TOL:
        raise ValueError(name + ' must lie in [0, 1]')
    return min(max(p, 0.0), 1.0)


def _single_gate(label):
    '''Single-qubit factor of the unitary part V_i^j of a Kraus operator.'''
    if label == 'X':
        return XGate()
    if label == 'Y':
        return YGate()
    if label == 'Z':
        return ZGate()
    if label == 'H':
        return HGate()
    if label == 'S':
        return SGate()
    if label == 'T':
        return TGate()
    raise ValueError('unsupported gate label ' + str(label))


def _parse(instance):
    '''Validate the instance and return (n, nb, m, steps, prepend, probs, labels).

    probs[j][i]  = p_ij  (so that B_i^j = sqrt(p_ij) V_i^j),
    labels[j][i] = string of m letters describing V_i^j.
    The node-wise Kraus constraint of eq_1 is enforced as sum_i p_ij = 1.
    '''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object / dict')
    n = _check_int(instance.get('nodes'), 'nodes', 2, 2 ** 5)
    m = _check_int(instance.get('internal_qubits'), 'internal_qubits', 1, _MAX_QUBITS)
    steps = _check_int(instance.get('steps'), 'steps', 0, _MAX_STEPS)
    prepend = instance.get('prepend_isometry', False)
    if not isinstance(prepend, bool):
        raise ValueError('prepend_isometry must be a boolean')
    nb = (n - 1).bit_length()
    if m + 2 * nb > _MAX_QUBITS:
        raise ValueError('total qubits ' + str(m + 2 * nb) + ' exceeds cap ' + str(_MAX_QUBITS))
    kraus = instance.get('kraus')
    if not isinstance(kraus, list) or len(kraus) != n:
        raise ValueError('kraus must be a list with one row per source node')
    probs = []
    labels = []
    for j in range(n):
        row = kraus[j]
        if not isinstance(row, list) or len(row) != n:
            raise ValueError('kraus[' + str(j) + '] must list one entry per destination node')
        pj = []
        lj = []
        for i in range(n):
            entry = row[i]
            if not isinstance(entry, dict):
                raise ValueError('kraus entries must be objects with prob and unitary')
            p = _check_prob(entry.get('prob'), 'kraus[' + str(j) + '][' + str(i) + '].prob')
            u = entry.get('unitary')
            if not isinstance(u, str) or len(u) != m:
                raise ValueError('unitary label must be a string of length internal_qubits')
            for c in u:
                if c not in _ALLOWED:
                    raise ValueError('unitary label letters must be from ' + _ALLOWED)
            pj.append(p)
            lj.append(u)
        if abs(sum(pj) - 1.0) > _SUM_TOL:
            raise ValueError('Kraus constraint violated at source node ' + str(j))
        probs.append(pj)
        labels.append(lj)
    return n, nb, m, steps, prepend, probs, labels


def _append_dilation(ua, internal, node1, node2, n, nb, m, probs, labels):
    '''Controlled Stinespring dilation U_A of the Kraus isometry A (eq_2).

    For every source node j (controlled on node1 == j):
      1. prepare sum_i sqrt(p_ij) |i> on node2 (binary tree of controlled RY),
      2. for every i apply V_i^j to the internal register controlled on
         node1 == j and node2 == i.
    Hence U_A |xi>|j>|0> = sum_i sqrt(p_ij) (V_i^j |xi>) |j>|i> = A(|xi>|j>).
    '''
    for j in range(n):
        pj = probs[j]
        ctrl_j = [node1[k] for k in range(nb)]
        for q in range(nb - 1, -1, -1):
            high = nb - 1 - q
            for pre in range(2 ** high):
                mass0 = 0.0
                mass1 = 0.0
                for i in range(n):
                    if (i >> (q + 1)) == pre:
                        if (i >> q) & 1:
                            mass1 += pj[i]
                        else:
                            mass0 += pj[i]
                if mass0 + mass1 <= _TOL:
                    continue
                theta = 2.0 * math.atan2(math.sqrt(mass1), math.sqrt(mass0))
                if abs(theta) <= _TOL:
                    continue
                ctrls = ctrl_j + [node2[k] for k in range(q + 1, nb)]
                cs = j | (pre << nb)
                ua.append(RYGate(theta).control(len(ctrls), ctrl_state=cs), ctrls + [node2[q]])
        for i in range(n):
            if pj[i] <= _TOL:
                continue
            ctrls = ctrl_j + [node2[k] for k in range(nb)]
            cs = j | (i << nb)
            for k in range(m):
                c = labels[j][i][k]
                if c == 'I':
                    continue
                ua.append(_single_gate(c).control(2 * nb, ctrl_state=cs), ctrls + [internal[k]])


def _append_zero_reflection(qc, node2, nb):
    '''Apply (2|0><0| - I) on the node2 register, exactly including sign.'''
    if nb == 1:
        qc.z(node2[0])
        return
    for k in range(nb):
        qc.x(node2[k])
    qc.append(ZGate().control(nb - 1), [node2[k] for k in range(nb)])
    for k in range(nb):
        qc.x(node2[k])
    qc.global_phase = qc.global_phase + math.pi


def build_circuit(instance):
    '''Return the unitary U**steps (eq_3) for the OQW described by instance.'''
    n, nb, m, steps, prepend, probs, labels = _parse(instance)
    internal = QuantumRegister(m, 'internal')
    node1 = QuantumRegister(nb, 'node1')
    node2 = QuantumRegister(nb, 'node2')
    qc = QuantumCircuit(internal, node1, node2)
    ua = QuantumCircuit(internal, node1, node2)
    _append_dilation(ua, internal, node1, node2, n, nb, m, probs, labels)
    ua_dag = ua.inverse()
    if prepend:
        qc.compose(ua, inplace=True)
    for _step in range(steps):
        # R_A = U_A (I x I x (2|0><0| - I)) U_A^dagger  (eq_3)
        qc.compose(ua_dag, inplace=True)
        _append_zero_reflection(qc, node2, nb)
        qc.compose(ua, inplace=True)
        # S: swap the two node registers  (eq_3)
        for k in range(nb):
            qc.swap(node1[k], node2[k])
    return qc
