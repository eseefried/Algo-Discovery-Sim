'''Coherent rejection-sampling preparation of an (unnormalised, flagged) Gibbs state
for a small restricted Boltzmann machine (RBM).

The returned circuit implements the unitary
    |0>^{n_v+n_h} |0>_f  ->  sum_{v,h} sqrt(Q(v,h)) |v,h> ( sqrt(1-r(v,h)) |0>_f + sqrt(r(v,h)) |1>_f )
with r(v,h) = exp(-E(v,h)) / (kappa' Q(v,h)) in [0,1], optionally followed by
Grover / amplitude-amplification rounds that boost the flag=1 branch.
Post-selecting flag=1 leaves the state register in the coherent Gibbs state
sum_{v,h} sqrt(P(v,h)) |v,h> (eq_postselect).

Qubit layout (Qiskit index 0 = least significant bit):
    qubit i            (0 <= i < n_v)        : visible unit v_{i+1}, |1> = on
    qubit n_v + j      (0 <= j < n_h)        : hidden unit h_{j+1},  |1> = on
    qubit n_v + n_h                           : rejection-sampling flag f
'''
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate

MAX_QUBITS = 12
RATIO_TOLERANCE = 1e-9


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError('%s must be an integer' % name)
    return int(value)


def _as_float_list(value, length, name):
    if value is None:
        raise ValueError('%s is required' % name)
    try:
        arr = [float(x) for x in value]
    except (TypeError, ValueError):
        raise ValueError('%s must be a sequence of real numbers' % name)
    if len(arr) != length:
        raise ValueError('%s must have length %d' % (name, length))
    for x in arr:
        if not math.isfinite(x):
            raise ValueError('%s must contain only finite values' % name)
    return arr


def _config_bits(index, n):
    '''Bit k of index is the value of qubit k (little-endian).'''
    return [(index >> k) & 1 for k in range(n)]


def _energy(v_bits, h_bits, w, a, b):
    '''eq_energy: E(v,h) = -sum a_i v_i - sum b_j h_j - sum w_ij v_i h_j.'''
    e = 0.0
    for i, vi in enumerate(v_bits):
        e -= a[i] * vi
    for j, hj in enumerate(h_bits):
        e -= b[j] * hj
    for i, vi in enumerate(v_bits):
        for j, hj in enumerate(h_bits):
            e -= w[i][j] * vi * hj
    return e


def _proposal_prob(v_bits, h_bits, mu, nu):
    '''eq_proposal_state (classical part): product distribution Q(v,h).'''
    q = 1.0
    for i, vi in enumerate(v_bits):
        q *= mu[i] if vi == 1 else (1.0 - mu[i])
    for j, hj in enumerate(h_bits):
        q *= nu[j] if hj == 1 else (1.0 - nu[j])
    return q


def _prepare_proposal(qc, state_qubits, means):
    '''eq_proposal_state (quantum part): |psi_Q> = prod_k R_y(2 arcsin sqrt(mean_k)) |0>.'''
    for q, m in zip(state_qubits, means):
        qc.ry(2.0 * math.asin(math.sqrt(m)), q)


def _rejection_rotation(qc, state_qubits, flag_qubit, ratios):
    '''eq_rejection_rotation: for every configuration (v,h) rotate the flag by
    2 arcsin sqrt(r(v,h)) conditioned on the state register being |v,h>.
    The ratio is evaluated classically and encoded exactly by multi-controlled
    R_y gates, replacing the b-bit fixed-point ratio register of the spec.'''
    n = len(state_qubits)
    for idx in range(2 ** n):
        bits = _config_bits(idx, n)
        r = min(1.0, max(0.0, ratios[idx]))
        theta = 2.0 * math.asin(math.sqrt(r))
        if theta == 0.0:
            continue
        zero_controls = [state_qubits[k] for k in range(n) if bits[k] == 0]
        for q in zero_controls:
            qc.x(q)
        qc.append(RYGate(theta).control(n), list(state_qubits) + [flag_qubit])
        for q in zero_controls:
            qc.x(q)


def _reflect_about_zero(qc, qubits):
    '''Phase -1 on |0...0> over the given qubits (S_0 of amplitude amplification).'''
    for q in qubits:
        qc.x(q)
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        qc.h(qubits[-1])
        qc.mcx(qubits[:-1], qubits[-1])
        qc.h(qubits[-1])
    for q in qubits:
        qc.x(q)


def build_circuit(instance):
    '''Build the flagged Gibbs-state preparation unitary for an RBM instance.

    instance keys:
        n_v, n_h   : positive integers (n_v + n_h + 1 <= 12)
        w          : n_v rows of n_h real weights w_ij
        a, b       : visible / hidden biases (lengths n_v, n_h)
        mu, nu     : proposal means in the open interval (0,1) (lengths n_v, n_h)
        kappa_prime: optional real >= max_{v,h} exp(-E)/Q (default: exact maximum)
        aa_rounds  : optional non-negative integer number of amplitude-amplification rounds
    '''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n_v = _as_int(instance.get('n_v'), 'n_v')
    n_h = _as_int(instance.get('n_h'), 'n_h')
    if n_v < 1 or n_h < 1:
        raise ValueError('n_v and n_h must be >= 1')
    n = n_v + n_h
    total = n + 1
    if total > MAX_QUBITS:
        raise ValueError('n_v + n_h + 1 = %d exceeds the cap of %d qubits' % (total, MAX_QUBITS))

    w_raw = instance.get('w')
    if w_raw is None:
        raise ValueError('w is required')
    try:
        rows = list(w_raw)
    except TypeError:
        raise ValueError('w must be a sequence of n_v rows')
    if len(rows) != n_v:
        raise ValueError('w must have n_v = %d rows' % n_v)
    w = [_as_float_list(row, n_h, 'w[%d]' % i) for i, row in enumerate(rows)]
    a = _as_float_list(instance.get('a'), n_v, 'a')
    b = _as_float_list(instance.get('b'), n_h, 'b')
    mu = _as_float_list(instance.get('mu'), n_v, 'mu')
    nu = _as_float_list(instance.get('nu'), n_h, 'nu')
    for m in mu + nu:
        if not (0.0 < m < 1.0):
            raise ValueError('proposal means mu, nu must lie strictly inside (0,1)')

    aa_raw = instance.get('aa_rounds', 0)
    aa_rounds = _as_int(aa_raw, 'aa_rounds')
    if aa_rounds < 0:
        raise ValueError('aa_rounds must be >= 0')

    # Classical preprocessing: unnormalised acceptance ratios exp(-E)/Q (eq_energy, eq_proposal_state).
    ratios_raw = []
    for idx in range(2 ** n):
        bits = _config_bits(idx, n)
        vb = bits[:n_v]
        hb = bits[n_v:]
        q = _proposal_prob(vb, hb, mu, nu)
        try:
            val = math.exp(-_energy(vb, hb, w, a, b)) / q
        except OverflowError:
            raise ValueError('weights too large: exp(-E) overflows')
        if not math.isfinite(val):
            raise ValueError('acceptance ratio is not finite')
        ratios_raw.append(val)
    kmax = max(ratios_raw)
    kappa_prime = instance.get('kappa_prime', None)
    if kappa_prime is None:
        kappa_prime = kmax
    else:
        try:
            kappa_prime = float(kappa_prime)
        except (TypeError, ValueError):
            raise ValueError('kappa_prime must be a real number')
        if not math.isfinite(kappa_prime) or kappa_prime <= 0.0:
            raise ValueError('kappa_prime must be a positive finite number')
        if kappa_prime < kmax * (1.0 - RATIO_TOLERANCE):
            raise ValueError('kappa_prime must be >= max_{v,h} exp(-E(v,h))/Q(v,h) = %g' % kmax)
    ratios = [r / kappa_prime for r in ratios_raw]

    vis = QuantumRegister(n_v, 'v')
    hid = QuantumRegister(n_h, 'h')
    flg = QuantumRegister(1, 'f')
    qc = QuantumCircuit(vis, hid, flg)
    state_qubits = list(range(n))
    flag = n
    all_qubits = list(range(total))

    # A = proposal preparation followed by the coherent rejection rotation.
    prep = QuantumCircuit(total)
    _prepare_proposal(prep, state_qubits, mu + nu)
    _rejection_rotation(prep, state_qubits, flag, ratios)
    qc.compose(prep, qubits=all_qubits, inplace=True)

    # eq_postselect (optional): amplitude amplification of the flag=1 branch,
    # Grover operator  A S_0 A^dagger S_f  with S_f = Z on the flag.
    for _ in range(aa_rounds):
        qc.z(flag)
        qc.compose(prep.inverse(), qubits=all_qubits, inplace=True)
        _reflect_about_zero(qc, all_qubits)
        qc.compose(prep, qubits=all_qubits, inplace=True)
    return qc
