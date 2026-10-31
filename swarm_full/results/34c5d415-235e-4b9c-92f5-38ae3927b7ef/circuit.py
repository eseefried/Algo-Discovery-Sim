from qiskit import QuantumCircuit, QuantumRegister


def _increment(qc, n):
    # |x> -> |x+1 mod 2^n>
    for i in range(n - 1, 0, -1):
        qc.mcx(list(range(i)), i)
    qc.x(0)


def _decrement(qc, n):
    # inverse of _increment: |x> -> |x-1 mod 2^n>
    qc.x(0)
    for i in range(1, n):
        qc.mcx(list(range(i)), i)


def _h0(qc):
    # eq_2, a=0: pairs (2k,2k+1). 2|+><+| - I = X on the lowest bit.
    qc.x(0)


def _h1(qc, n):
    # eq_2, a=1: pairs (2k+1,2k+2 mod N) = shift of the a=0 pairing by one site.
    # H_1 = Inc X0 Dec (circuit order: Dec first, then X0, then Inc).
    _decrement(qc, n)
    qc.x(0)
    _increment(qc, n)


def build_circuit(instance):
    """Coinless 1D tessellation walk U^t, U = H_1 H_0, on N = 2^n_qubits sites (cycle)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n_qubits')
    t = instance.get('steps')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n > 12:
        raise ValueError('n_qubits must be an integer in [2, 12]')
    if isinstance(t, bool) or not isinstance(t, int) or t < 0 or t > 256:
        raise ValueError('steps must be an integer in [0, 256]')
    pos = QuantumRegister(n, 'pos')
    qc = QuantumCircuit(pos, name='coinless_walk')
    for _ in range(t):
        _h0(qc)      # first apply H_0
        _h1(qc, n)   # then H_1, so one step is U = H_1 H_0 (eq_1)
    return qc
