from qiskit import QuantumCircuit, QuantumRegister
import math

MAX_POWER = 1024
MAX_STAGE = 10


def _is_real(value):
    return (not isinstance(value, bool)) and isinstance(value, (int, float)) and math.isfinite(value)


def _is_int(value):
    return (not isinstance(value, bool)) and isinstance(value, int)


def build_circuit(instance):
    """U^k for the amplitude-error gate U = Rx(pi*(1+epsilon)) on one qubit.

    instance keys: epsilon (float, |epsilon|<=0.5); exactly one of
    stage (int 0..10, k=2^stage) or power (int 0..1024, k=power);
    undo_ideal_pulse (bool, optional): append a known X if k is odd.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    allowed = {'epsilon', 'stage', 'power', 'undo_ideal_pulse'}
    for key in instance:
        if key not in allowed:
            raise ValueError('unknown instance key: %s' % (key,))
    if 'epsilon' not in instance:
        raise ValueError('epsilon is required')
    eps = instance['epsilon']
    if not _is_real(eps) or abs(eps) > 0.5:
        raise ValueError('epsilon must be a finite real with |epsilon| <= 0.5')
    has_stage = 'stage' in instance
    has_power = 'power' in instance
    if has_stage == has_power:
        raise ValueError('provide exactly one of stage or power')
    if has_stage:
        j = instance['stage']
        if not _is_int(j) or j < 0 or j > MAX_STAGE:
            raise ValueError('stage must be an int in 0..%d' % MAX_STAGE)
        k = 2 ** j
    else:
        k = instance['power']
        if not _is_int(k) or k < 0 or k > MAX_POWER:
            raise ValueError('power must be an int in 0..%d' % MAX_POWER)
    undo = instance.get('undo_ideal_pulse', False)
    if not isinstance(undo, bool):
        raise ValueError('undo_ideal_pulse must be a bool')

    q = QuantumRegister(1, 'q')
    qc = QuantumCircuit(q)
    # eq_1: noisy pi pulse, theta = pi*(1+epsilon), U = exp(-i*theta/2*sigma_x)
    theta = math.pi * (1.0 + float(eps))
    # eq_2: U^k as k sequential black-box placements (k queries)
    for _ in range(k):
        qc.rx(theta, 0)
    # eq_2: odd k leaves an ideal pi pulse (-i X); undo it with a known X
    if undo and (k % 2 == 1):
        qc.x(0)
    return qc
