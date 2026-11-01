from math import pi
from qiskit import QuantumCircuit, QuantumRegister


def build_circuit(instance):
    """One PQF step W on (data, ancilla); ancilla is expected in |0> from the runner.

    instance: {"t_power": int in {1,2,3,5,6,7}, "apply_correction": bool}
    alpha = t_power*pi/4, G = diag(e^{i alpha}, e^{-i alpha}) = Rz(-2 alpha).
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    j = instance.get('t_power', 1)
    corr = instance.get('apply_correction', False)
    if isinstance(j, bool) or not isinstance(j, int):
        raise ValueError('t_power must be an integer')
    if j < 1 or j > 7 or j % 4 == 0:
        raise ValueError('t_power must be in {1,2,3,5,6,7}')
    if not isinstance(corr, bool):
        raise ValueError('apply_correction must be a bool')
    alpha = j * pi / 4.0
    data = QuantumRegister(1, 'data')
    anc = QuantumRegister(1, 'anc')
    qc = QuantumCircuit(data, anc)
    # eq_1: W = (I_data x H_anc) * controlled-G * (I_data x H_anc)
    qc.h(1)
    qc.crz(-2.0 * alpha, 1, 0)
    qc.h(1)
    # optional deferred-measurement form of the outcome-1 byproduct C_{k,1} = Z
    if corr:
        qc.cz(1, 0)
    return qc
