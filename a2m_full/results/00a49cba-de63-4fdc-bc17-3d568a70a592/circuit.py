from qiskit import QuantumCircuit, QuantumRegister


def _nn_cx(qc, p, q):
    """CX(p -> q) using only gates on adjacent chain pairs (0,1),(1,2)."""
    if abs(p - q) == 1:
        qc.cx(p, q)
    else:
        # distance-2 pair is (0,2); route through the middle qubit 1
        qc.swap(1, q)
        qc.cx(p, 1)
        qc.swap(1, q)


def build_circuit(instance):
    """Toffoli on a 3-qubit linear chain; two controls, one target (instance['target'], default 2)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    allowed = {'num_qubits', 'target'}
    for k in instance:
        if k not in allowed:
            raise ValueError('unknown instance key: ' + str(k))
    n = instance.get('num_qubits', 3)
    if isinstance(n, bool) or not isinstance(n, int) or n != 3:
        raise ValueError('num_qubits must be 3')
    t = instance.get('target', 2)
    if isinstance(t, bool) or not isinstance(t, int) or t not in (0, 1, 2):
        raise ValueError('target must be 0, 1 or 2')
    controls = [q for q in range(3) if q != t]
    a = controls[0]
    b = controls[1]
    c = t
    qc = QuantumCircuit(QuantumRegister(3, 'q'))
    # eq_1: |x_a x_b x_c> -> |x_a x_b x_c xor (x_a x_b)>
    qc.h(c)
    _nn_cx(qc, b, c)
    qc.tdg(c)
    _nn_cx(qc, a, c)
    qc.t(c)
    _nn_cx(qc, b, c)
    qc.tdg(c)
    _nn_cx(qc, a, c)
    qc.t(b)
    qc.t(c)
    qc.h(c)
    _nn_cx(qc, a, b)
    qc.t(a)
    qc.tdg(b)
    _nn_cx(qc, a, b)
    return qc
