'''Baseline amplitude-amplified hypercube edge tester for Boolean monotonicity (eq_5).

Search register = x (n qubits, x_{j+1} on qubit j) + i (k = ceil(log2 n) qubits, little-endian
integer i meaning direction i+1, i.e. flip qubit x[i]).  A = H on all search qubits prepares the
uniform superposition over (padded) hypercube edges.  S_{V_f} (eq_3) marks violated edges using
the bit-flip query oracle O_f on two answer qubits a0, a1 and a CZ between them; everything is
uncomputed.  The Grover iterate G = -A S_0 A^dagger S_{V_f} is repeated instance['iterations']
times.  This realises the O(sqrt(n/eps)) baseline, NOT the paper's O~(n^{1/4} eps^{-1/2}) bound.
No input preparation beyond A and no measurement are included.
'''
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
ANSWER_QUBITS = 2


def _check_int(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(name + ' must be an integer')
    if value < minimum:
        raise ValueError(name + ' must be >= ' + str(minimum))
    return value


def _parse_function(instance, n):
    '''Return ('coordinate', j) for f(x) = 1 - x_{j+1}, or ('table', bits) for a truth table.

    Truth-table index convention: bit j (LSB = bit 0) of the index equals x_{j+1}, i.e. the
    bit carried by qubit j of the x register (Qiskit little-endian).
    '''
    spec = instance.get('f')
    if not isinstance(spec, dict):
        raise ValueError('instance[f] must be a dict describing the Boolean function')
    kind = spec.get('type')
    if kind == 'negated_coordinate':
        j = _check_int(spec.get('index'), 'f.index', 1)
        if j > n:
            raise ValueError('f.index must lie in 1..n')
        return 'coordinate', j - 1
    if kind == 'truth_table':
        values = spec.get('values')
        if not isinstance(values, list) or len(values) != 2 ** n:
            raise ValueError('f.values must be a list of length 2**n')
        bits = []
        for v in values:
            if isinstance(v, bool) or v not in (0, 1):
                raise ValueError('f.values entries must be 0 or 1')
            bits.append(int(v))
        return 'table', bits
    raise ValueError('f.type must be negated_coordinate or truth_table')


def _mcx(qc, controls, target):
    if len(controls) == 0:
        qc.x(target)
    elif len(controls) == 1:
        qc.cx(controls[0], target)
    else:
        qc.mcx(controls, target)


def _apply_oracle(qc, x_qubits, target, kind, data):
    '''Bit-flip query oracle O_f: |x>|b> -> |x>|b xor f(x)>   (eq_3).'''
    n = len(x_qubits)
    if kind == 'coordinate':
        qc.x(target)
        qc.cx(x_qubits[data], target)
        return
    for idx in range(2 ** n):
        if data[idx] != 1:
            continue
        zeros = [x_qubits[j] for j in range(n) if not (idx >> j) & 1]
        for q in zeros:
            qc.x(q)
        _mcx(qc, list(x_qubits), target)
        for q in zeros:
            qc.x(q)


def _direction_pattern(qc, i_qubits, i):
    '''X gates mapping direction value i to the all-ones pattern on the i register.'''
    for b, q in enumerate(i_qubits):
        if not (i >> b) & 1:
            qc.x(q)


def _apply_direction_flip(qc, x_qubits, i_qubits, n):
    '''Controlled x -> x xor e_i for i in 0..n-1; padded directions i >= n do nothing.'''
    for i in range(n):
        _direction_pattern(qc, i_qubits, i)
        _mcx(qc, list(i_qubits), x_qubits[i])
        _direction_pattern(qc, i_qubits, i)


def _apply_xi_into(qc, x_qubits, i_qubits, target, n):
    '''target -> target xor x_i, controlled on the direction register.'''
    for i in range(n):
        _direction_pattern(qc, i_qubits, i)
        _mcx(qc, list(i_qubits) + [x_qubits[i]], target)
        _direction_pattern(qc, i_qubits, i)


def _apply_marking(qc, x_qubits, i_qubits, a0, a1, n, kind, data):
    '''Phase oracle S_{V_f} of eq_5: phase -1 exactly on violated edges (eq_3).

    After the forward computation a0 = f(x) xor x_i and a1 = f(x) xor f(x xor e_i).
    The edge (x, x xor e_i) is violated iff a0 = a1 = 1 (lower endpoint has value 1,
    upper endpoint value 0), so a CZ(a0, a1) realises S_{V_f}; all work is uncomputed.
    Uses four applications of O_f per iteration (two forward, two uncompute).
    '''
    _apply_oracle(qc, x_qubits, a0, kind, data)
    _apply_direction_flip(qc, x_qubits, i_qubits, n)
    _apply_oracle(qc, x_qubits, a1, kind, data)
    _apply_direction_flip(qc, x_qubits, i_qubits, n)
    qc.cx(a0, a1)
    _apply_xi_into(qc, x_qubits, i_qubits, a0, n)
    qc.cz(a0, a1)
    _apply_xi_into(qc, x_qubits, i_qubits, a0, n)
    qc.cx(a0, a1)
    _apply_direction_flip(qc, x_qubits, i_qubits, n)
    _apply_oracle(qc, x_qubits, a1, kind, data)
    _apply_direction_flip(qc, x_qubits, i_qubits, n)
    _apply_oracle(qc, x_qubits, a0, kind, data)


def _apply_diffusion(qc, qubits):
    '''Grover diffusion -A S_0 A^dagger with A = H^{(n+k)} on the search register (eq_5).'''
    for q in qubits:
        qc.h(q)
    for q in qubits:
        qc.x(q)
    last = qubits[-1]
    qc.h(last)
    _mcx(qc, list(qubits[:-1]), last)
    qc.h(last)
    for q in qubits:
        qc.x(q)
    for q in qubits:
        qc.h(q)


def build_circuit(instance):
    '''Build the amplitude-amplified edge-tester operation (eq_5) for a given instance.

    instance = {'n': int >= 1, 'iterations': int >= 0,
                'f': {'type': 'negated_coordinate', 'index': j}  (f(x) = 1 - x_j, 1-based)
                  or {'type': 'truth_table', 'values': [2**n bits]}}
    '''
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _check_int(instance.get('n'), 'n', 1)
    iterations = _check_int(instance.get('iterations'), 'iterations', 0)
    k = (n - 1).bit_length()
    total = n + k + ANSWER_QUBITS
    if total > MAX_QUBITS:
        raise ValueError('instance needs ' + str(total) + ' qubits, cap is ' + str(MAX_QUBITS))
    kind, data = _parse_function(instance, n)
    x_reg = QuantumRegister(n, 'x')
    a_reg = QuantumRegister(ANSWER_QUBITS, 'a')
    if k > 0:
        i_reg = QuantumRegister(k, 'i')
        qc = QuantumCircuit(x_reg, i_reg, a_reg, name='edge_tester_aa')
        i_qubits = list(i_reg)
    else:
        qc = QuantumCircuit(x_reg, a_reg, name='edge_tester_aa')
        i_qubits = []
    x_qubits = list(x_reg)
    a0 = a_reg[0]
    a1 = a_reg[1]
    search = x_qubits + i_qubits
    # A: uniform superposition over (padded) hypercube edges |x>|i>  (eq_5)
    for q in search:
        qc.h(q)
    # Grover iterate G = -A S_0 A^dagger S_{V_f}, repeated T times  (eq_5)
    for _ in range(iterations):
        _apply_marking(qc, x_qubits, i_qubits, a0, a1, n, kind, data)
        _apply_diffusion(qc, search)
    return qc
