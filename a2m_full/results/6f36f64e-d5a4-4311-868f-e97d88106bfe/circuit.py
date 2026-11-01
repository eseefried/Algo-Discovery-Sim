import math
from qiskit import QuantumCircuit


def _read_real(instance, key, required, fallback):
    if key not in instance:
        if required:
            raise ValueError('missing parameter: ' + key)
        return fallback
    v = instance[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + ' must be finite')
    return v


def build_circuit(instance):
    """Group-commutator approximation of exp(-i*(a*b + shift) X) on one qubit.

    Uses e^{sA} e^{tB} e^{-sA} e^{-tB} ~ exp(st[A,B]) with A=-i a Z, B=-i b' Y,
    [Z,Y] = -2iX and b' = -b/2, giving exp(-i a b X) up to O(|a|,|b|)^3 error.
    Qubit 0 is the target. No ancillas, no measurement.
    """
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    a = _read_real(instance, 'a', True, 0.0)
    b = _read_real(instance, 'b', True, 0.0)
    shift = _read_real(instance, 'shift', False, 0.0)
    if abs(a) > 1.0 or abs(b) > 1.0:
        raise ValueError('|a| and |b| must be <= 1 (small-angle regime)')
    if abs(shift) > 10.0:
        raise ValueError('|shift| must be <= 10')
    qc = QuantumCircuit(1, name='prod_commutator')
    # operator order: Rz(2a) Ry(-b) Rz(-2a) Ry(b); circuit applies right-to-left
    qc.ry(b, 0)
    qc.rz(-2.0 * a, 0)
    qc.ry(-b, 0)
    qc.rz(2.0 * a, 0)
    # additive composition (eq_4): exact commuting X rotation exp(-i shift X)
    if shift != 0.0:
        qc.rx(2.0 * shift, 0)
    return qc
