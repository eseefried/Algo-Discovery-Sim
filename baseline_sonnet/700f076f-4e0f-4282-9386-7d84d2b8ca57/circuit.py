import math
from qiskit import QuantumCircuit, QuantumRegister


def _int_param(instance, key, lo, hi):
    if key not in instance:
        raise ValueError('missing parameter: ' + key)
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    if v < lo or v > hi:
        raise ValueError(key + ' out of range')
    return v


def _mcz(qc, qubits):
    # phase -1 on the all-ones state of the given qubits
    if len(qubits) == 1:
        qc.z(qubits[0])
    else:
        t = qubits[-1]
        qc.h(t)
        qc.mcx(list(qubits[:-1]), t)
        qc.h(t)


def _oracle(qc, qubits, w):
    # eq_1: O_w = I - 2|w><w| ; bit i of w acts on qubit i (little endian)
    zeros = [q for i, q in enumerate(qubits) if not (w >> i) & 1]
    for q in zeros:
        qc.x(q)
    _mcz(qc, qubits)
    for q in zeros:
        qc.x(q)


def _diffusion(qc, qubits):
    # eq_2: 2|s><s| - I = -(H^n (I - 2|0><0|) H^n)
    for q in qubits:
        qc.h(q)
    for q in qubits:
        qc.x(q)
    _mcz(qc, qubits)
    for q in qubits:
        qc.x(q)
    for q in qubits:
        qc.h(q)
    qc.global_phase = qc.global_phase + math.pi


def _iterations(guess_n):
    # eq_4: k = floor(pi / (4 arcsin(1/sqrt(guess_n))))
    val = math.pi / (4.0 * math.asin(1.0 / math.sqrt(guess_n)))
    return int(math.floor(val + 1e-12))


def build_circuit(instance):
    """Grover iterations G^k on n index qubits; no state preparation.

    instance keys: n (1..12), marked (0..2^n-1), guess_N (2..4096, optional,
    defaults to the true N = 2^n).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int_param(instance, 'n', 1, 12)
    w = _int_param(instance, 'marked', 0, 2 ** n - 1)
    if 'guess_N' in instance:
        guess_n = _int_param(instance, 'guess_N', 2, 4096)
    else:
        guess_n = 2 ** n
        if guess_n < 2:
            raise ValueError('invalid size')
    k = _iterations(guess_n)
    reg = QuantumRegister(n, 'index')
    qc = QuantumCircuit(reg)
    qubits = list(range(n))
    for _ in range(k):
        _oracle(qc, qubits, w)
        _diffusion(qc, qubits)
    return qc
