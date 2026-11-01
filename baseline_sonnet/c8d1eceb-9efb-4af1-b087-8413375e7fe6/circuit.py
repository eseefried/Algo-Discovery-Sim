from qiskit import QuantumCircuit, QuantumRegister
import math


def _real(v, name):
    try:
        x = float(v)
    except (TypeError, ValueError):
        raise ValueError(name + ' must be a real number')
    if not math.isfinite(x):
        raise ValueError(name + ' must be finite')
    return x


def build_circuit(instance):
    """Controlled Trotter evolution of H = sum_j (eps_j - G/2)(1 - Z_j) - (G/2)(XX+YY).

    Qubits: 0,1 = system (pair occupation of levels 0,1; |1> = occupied), 2 = control ancilla.
    instance keys: epsilon (list of 2 reals), G (real), time (real), trotter_steps (int 1..100).
    """
    if type(instance) is not dict:
        raise ValueError('instance must be a JSON object')
    eps = instance.get('epsilon')
    if type(eps) is not list or len(eps) != 2:
        raise ValueError('epsilon must be a list of two reals')
    e0 = _real(eps[0], 'epsilon[0]')
    e1 = _real(eps[1], 'epsilon[1]')
    g = _real(instance.get('G'), 'G')
    t = _real(instance.get('time'), 'time')
    n = instance.get('trotter_steps')
    if type(n) is not int or n < 1 or n > 100:
        raise ValueError('trotter_steps must be an integer in 1..100')
    # eq_3 coefficients: H = sum_j a_j (1 - Z_j) - (G/2)(XX + YY), a_j = eps_j - G/2
    a = [e0 - g / 2.0, e1 - g / 2.0]
    const = a[0] + a[1]
    dt = t / n
    sysr = QuantumRegister(2, 'q')
    anc = QuantumRegister(1, 'a')
    qc = QuantumCircuit(sysr, anc)
    # exchange block exp(+i G dt/2 (XX+YY)) = RXX(-G dt) RYY(-G dt); XX and YY commute
    pair = QuantumCircuit(2)
    pair.rxx(-g * dt, 0, 1)
    pair.ryy(-g * dt, 0, 1)
    cpair = pair.to_gate().control(1)
    for _ in range(n):
        # constant part of H: phase exp(-i const dt) on ancilla |1>
        qc.p(-const * dt, 2)
        # diagonal part: exp(+i a_j dt Z_j) = RZ(-2 a_j dt), controlled on ancilla
        qc.crz(-2.0 * a[0] * dt, 2, 0)
        qc.crz(-2.0 * a[1] * dt, 2, 1)
        # XY exchange part
        qc.append(cpair, [2, 0, 1])
    return qc
