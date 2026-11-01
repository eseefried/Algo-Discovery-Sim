from qiskit import QuantumCircuit, QuantumRegister


def _increment(qc, pos):
    """Unconditional modular increment v -> v+1 on little-endian position qubits."""
    for k in range(len(pos) - 1, -1, -1):
        if k == 0:
            qc.x(pos[0])
        else:
            qc.mcx(list(pos[:k]), pos[k])


def build_circuit(instance):
    """Build U^t, U = S (I_N (x) C), on the cycle C_N with N = 2**position_qubits.

    instance keys: position_qubits (int, 2..11), steps (int, 0..200),
    coin ('grover' or 'hadamard').
    Layout: qubits 0..n-1 position (little-endian), qubit n coin.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('position_qubits', 2)
    steps = instance.get('steps', 1)
    coin = instance.get('coin', 'grover')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2 or n + 1 > 12:
        raise ValueError('position_qubits must be an integer in [2, 11]')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0 or steps > 200:
        raise ValueError('steps must be an integer in [0, 200]')
    if coin not in ('grover', 'hadamard'):
        raise ValueError('coin must be grover or hadamard')
    pos = QuantumRegister(n, 'pos')
    cn = QuantumRegister(1, 'coin')
    qc = QuantumCircuit(pos, cn)
    p = list(range(n))
    c = n
    for _ in range(steps):
        # eq_2: coin operator on coin qubit (Grover coin 2|s><s|-I = X on 2 dims)
        if coin == 'grover':
            qc.x(c)
        else:
            qc.h(c)
        # eq_1: shift S|v,c> = |v+(-1)^c, c>.
        # Conjugating the position by X when c=1 turns -1 into +1 since ~(~v+1)=v-1.
        for q in p:
            qc.cx(c, q)
        _increment(qc, p)
        for q in p:
            qc.cx(c, q)
    return qc
