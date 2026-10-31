from qiskit import QuantumCircuit, QuantumRegister
import math


def _int(x, lo, hi):
    if isinstance(x, bool) or not isinstance(x, int) or x < lo or x > hi:
        raise ValueError('invalid integer')
    return x


def _num(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError('invalid number')
    return float(x)


def _apply(qc, m, g):
    # eq_1 building block: one explicit gate U_i acting on the data register
    if not isinstance(g, dict):
        raise ValueError('gate must be an object')
    kind = g.get('kind')
    qs = g.get('qubits')
    ps = g.get('params', [])
    if not isinstance(qs, list) or not isinstance(ps, list):
        raise ValueError('qubits and params must be lists')
    qs = [_int(q, 0, m - 1) for q in qs]
    if len(set(qs)) != len(qs):
        raise ValueError('repeated qubit')
    ps = [_num(p) for p in ps]
    if kind == 'u' and len(qs) == 1 and len(ps) == 3:
        qc.u(ps[0], ps[1], ps[2], qs[0])
    elif kind == 'cp' and len(qs) == 2 and len(ps) == 1:
        qc.cp(ps[0], qs[0], qs[1])
    elif kind == 'rzz' and len(qs) == 2 and len(ps) == 1:
        qc.rzz(ps[0], qs[0], qs[1])
    elif kind == 'cx' and len(qs) == 2 and len(ps) == 0:
        qc.cx(qs[0], qs[1])
    else:
        raise ValueError('unsupported gate specification')


def build_circuit(instance):
    """Apply gates U_1..U_n in the order sigma(1),...,sigma(n) (eq_1)."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    m = _int(instance.get('num_qubits'), 1, 12)
    gates = instance.get('gates')
    sigma = instance.get('sigma')
    if not isinstance(gates, list) or not isinstance(sigma, list):
        raise ValueError('gates and sigma must be lists')
    n = len(gates)
    if n < 1 or n > 64 or len(sigma) != n:
        raise ValueError('invalid number of gates or sigma length')
    s = [_int(v, 1, n) for v in sigma]
    if len(set(s)) != n:
        raise ValueError('sigma is not a permutation')
    qr = QuantumRegister(m, 'data')
    qc = QuantumCircuit(qr)
    for k in range(n):
        _apply(qc, m, gates[s[k] - 1])
    return qc
