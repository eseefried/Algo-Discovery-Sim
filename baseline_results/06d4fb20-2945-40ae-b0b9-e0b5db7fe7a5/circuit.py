from __future__ import annotations

'''Grover oracle with a quantumly accessible classical memory (QROM-style XOR lookup).

Qubit layout (Qiskit little-endian, qubit 0 = least significant bit):
  qubits 0 .. n-1        : address register, qubit i holds bit a_i of x = sum_i 2^i a_i
  qubits n .. n+m-1      : data register, qubit n+j holds bit j of D[x] (expected |0...0> on input)

Operation returned: (Diffusion * O_t)^k on addr (+) data, or O_t^k when oracle_only is true.
No state preparation and no measurement are included.
'''

import math
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a JSON object (dict)')
    required = ['n', 'm', 'database', 'target', 'iterations']
    for key in required:
        if key not in instance:
            raise ValueError('missing instance key: ' + key)
    n = instance['n']
    m = instance['m']
    database = instance['database']
    target = instance['target']
    iterations = instance['iterations']
    oracle_only = instance['oracle_only'] if 'oracle_only' in instance else False
    if not _is_int(n) or n < 1:
        raise ValueError('n must be a positive integer')
    if not _is_int(m) or m < 1:
        raise ValueError('m must be a positive integer')
    if n + m > MAX_QUBITS:
        raise ValueError('n + m exceeds the qubit cap of %d' % MAX_QUBITS)
    if not isinstance(database, list) or len(database) != 2 ** n:
        raise ValueError('database must be a list of length 2**n')
    for rec in database:
        if not _is_int(rec) or rec < 0 or rec >= 2 ** m:
            raise ValueError('database records must be integers in [0, 2**m)')
    if not _is_int(target) or target < 0 or target >= 2 ** m:
        raise ValueError('target must be an integer in [0, 2**m)')
    if not _is_int(iterations) or iterations < 1:
        raise ValueError('iterations must be a positive integer')
    if not isinstance(oracle_only, bool):
        raise ValueError('oracle_only must be a boolean')
    return n, m, list(database), target, iterations, oracle_only


def _lookup(qc, addr, data, database, n, m):
    '''eq_1 / eq_2: U_D |x>|y> = |x>|y XOR D[x]>, realised as a product over stored 1-bits of
    X on data bit j controlled on the address register being exactly |x>.'''
    for x in range(len(database)):
        rec = database[x]
        if rec == 0:
            continue
        zero_lines = [addr[i] for i in range(n) if ((x >> i) & 1) == 0]
        for q in zero_lines:
            qc.x(q)
        controls = [addr[i] for i in range(n)]
        for j in range(m):
            if (rec >> j) & 1:
                qc.mcx(controls, data[j])
        for q in zero_lines:
            qc.x(q)


def _phase_flip_on_value(qc, reg, value, size):
    '''Applies I - 2|value><value| on the register reg of the given size (up to no phase).'''
    zero_lines = [reg[i] for i in range(size) if ((value >> i) & 1) == 0]
    for q in zero_lines:
        qc.x(q)
    if size == 1:
        qc.z(reg[0])
    else:
        last = reg[size - 1]
        qc.h(last)
        qc.mcx([reg[i] for i in range(size - 1)], last)
        qc.h(last)
    for q in zero_lines:
        qc.x(q)


def _oracle(qc, addr, data, database, target, n, m):
    '''eq_3: O_t = U_D^dagger (I (x) (I - 2|t><t|)) U_D ; U_D is self-inverse.'''
    _lookup(qc, addr, data, database, n, m)
    _phase_flip_on_value(qc, data, target, m)
    _lookup(qc, addr, data, database, n, m)


def _diffusion(qc, addr, n):
    '''eq_4: 2|s><s| - I = H^n (2|0><0| - I) H^n on the address register (global phase ignored).'''
    for i in range(n):
        qc.h(addr[i])
    _phase_flip_on_value(qc, addr, 0, n)
    for i in range(n):
        qc.h(addr[i])


def build_circuit(instance):
    n, m, database, target, iterations, oracle_only = _validate(instance)
    addr = QuantumRegister(n, 'addr')
    data = QuantumRegister(m, 'data')
    qc = QuantumCircuit(addr, data)
    for _ in range(iterations):
        _oracle(qc, addr, data, database, target, n, m)
        if not oracle_only:
            _diffusion(qc, addr, n)
    return qc
