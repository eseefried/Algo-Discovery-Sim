import math
from qiskit import QuantumCircuit, QuantumRegister


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _flip_all_ones(qc, n):
    # Phase -1 on |1...1> of the n index qubits.
    if n == 1:
        qc.z(0)
    else:
        qc.mcp(math.pi, list(range(n - 1)), n - 1)


def _oracle(qc, n, marked):
    # Phase oracle O = I - 2|marked><marked| (eq_1 oracle step).
    zeros = [i for i in range(n) if not (marked >> i) & 1]
    for i in zeros:
        qc.x(i)
    _flip_all_ones(qc, n)
    for i in zeros:
        qc.x(i)


def _diffusion(qc, n):
    # H X (C^{n-1}Z) X H = I - 2|s><s|, s uniform superposition.
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.x(i)
    _flip_all_ones(qc, n)
    for i in range(n):
        qc.x(i)
    for i in range(n):
        qc.h(i)


def build_circuit(instance):
    """Grover iterate G^k on n index qubits. instance keys: n (1..12), marked (0..2^n-1),
    optional iterations (int >= 0) XOR guessed_size (int >= 1). If neither is given,
    k is derived from N=2^n."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if not _is_int(n) or n < 1 or n > 12:
        raise ValueError('n must be an integer in 1..12')
    N = 2 ** n
    marked = instance.get('marked')
    if not _is_int(marked) or marked < 0 or marked >= N:
        raise ValueError('marked must be an integer in [0, 2^n)')
    has_k = 'iterations' in instance and instance['iterations'] is not None
    has_g = 'guessed_size' in instance and instance['guessed_size'] is not None
    if has_k and has_g:
        raise ValueError('give only one of iterations or guessed_size')
    if has_k:
        k = instance['iterations']
        if not _is_int(k) or k < 0:
            raise ValueError('iterations must be a nonnegative integer')
    else:
        if has_g:
            g = instance['guessed_size']
            if not _is_int(g) or g < 1 or g > 2 ** 24:
                raise ValueError('guessed_size must be an integer in 1..2^24')
        else:
            g = N
        # eq_2: k_opt ~ (pi/4) sqrt(N')
        k = int(math.floor(math.pi / 4.0 * math.sqrt(g)))
    if k > 1000:
        raise ValueError('too many iterations (cap 1000)')
    reg = QuantumRegister(n, 'index')
    qc = QuantumCircuit(reg, name='grover_iterate')
    for _ in range(k):
        _oracle(qc, n, marked)
        _diffusion(qc, n)
        # (I-2|s><s|)O = -G with G=(2|s><s|-I)O; restore the global phase
        qc.global_phase += math.pi
    return qc
