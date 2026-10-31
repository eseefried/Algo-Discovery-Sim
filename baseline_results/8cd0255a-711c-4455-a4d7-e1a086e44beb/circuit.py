"""Miter circuit for quantum circuit equivalence checking.

Given two circuits U and V on n qubits (as gate lists), build the difference
operator
    W = U^dagger V   (mode 'u_dag_v')  -> eq_3: W = e^{i theta} I  iff  U ~_gp V
    W = U V^dagger   (mode 'u_v_dag')  -> eq_4 (circuit part): W diagonal iff U = D V
The equivalence decision itself is classical post-processing on W and is not
part of the returned operation.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

_MAX_QUBITS = 12
_ONE_Q = ("x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "sxdg", "id")
_ONE_Q_P = ("rx", "ry", "rz", "p")
_TWO_Q = ("cx", "cy", "cz", "ch", "swap")
_TWO_Q_P = ("cp", "crx", "cry", "crz", "rxx", "rzz")
_THREE_Q = ("ccx", "cswap")


def _validate_gate(gate, n):
    """Validate one gate dictionary and return (name, qubits, params)."""
    if not isinstance(gate, dict):
        raise ValueError("each gate must be a dict with keys name, qubits, params")
    name = gate.get("name")
    qubits = gate.get("qubits")
    params = gate.get("params", [])
    if not isinstance(name, str):
        raise ValueError("gate name must be a string")
    name = name.lower()
    if not isinstance(qubits, list) or len(qubits) == 0:
        raise ValueError("gate qubits must be a non-empty list")
    for q in qubits:
        if isinstance(q, bool) or not isinstance(q, int) or q < 0 or q >= n:
            raise ValueError("gate qubit index out of range")
    if len(set(qubits)) != len(qubits):
        raise ValueError("gate qubit indices must be distinct")
    if not isinstance(params, list):
        raise ValueError("gate params must be a list")
    fparams = []
    for p in params:
        if isinstance(p, bool) or not isinstance(p, (int, float)):
            raise ValueError("gate params must be real numbers")
        fp = float(p)
        if not math.isfinite(fp):
            raise ValueError("gate params must be finite")
        fparams.append(fp)
    if name in _ONE_Q:
        nq, npar = 1, 0
    elif name in _ONE_Q_P:
        nq, npar = 1, 1
    elif name in _TWO_Q:
        nq, npar = 2, 0
    elif name in _TWO_Q_P:
        nq, npar = 2, 1
    elif name in _THREE_Q:
        nq, npar = 3, 0
    else:
        raise ValueError("unsupported gate name: " + name)
    if len(qubits) != nq:
        raise ValueError("gate " + name + " expects " + str(nq) + " qubits")
    if len(fparams) != npar:
        raise ValueError("gate " + name + " expects " + str(npar) + " params")
    return name, qubits, fparams


def _append_gate(qc, name, qubits, params):
    """Append one whitelisted standard gate to qc."""
    if name == "x":
        qc.x(qubits[0])
    elif name == "y":
        qc.y(qubits[0])
    elif name == "z":
        qc.z(qubits[0])
    elif name == "h":
        qc.h(qubits[0])
    elif name == "s":
        qc.s(qubits[0])
    elif name == "sdg":
        qc.sdg(qubits[0])
    elif name == "t":
        qc.t(qubits[0])
    elif name == "tdg":
        qc.tdg(qubits[0])
    elif name == "sx":
        qc.sx(qubits[0])
    elif name == "sxdg":
        qc.sxdg(qubits[0])
    elif name == "id":
        qc.id(qubits[0])
    elif name == "rx":
        qc.rx(params[0], qubits[0])
    elif name == "ry":
        qc.ry(params[0], qubits[0])
    elif name == "rz":
        qc.rz(params[0], qubits[0])
    elif name == "p":
        qc.p(params[0], qubits[0])
    elif name == "cx":
        qc.cx(qubits[0], qubits[1])
    elif name == "cy":
        qc.cy(qubits[0], qubits[1])
    elif name == "cz":
        qc.cz(qubits[0], qubits[1])
    elif name == "ch":
        qc.ch(qubits[0], qubits[1])
    elif name == "swap":
        qc.swap(qubits[0], qubits[1])
    elif name == "cp":
        qc.cp(params[0], qubits[0], qubits[1])
    elif name == "crx":
        qc.crx(params[0], qubits[0], qubits[1])
    elif name == "cry":
        qc.cry(params[0], qubits[0], qubits[1])
    elif name == "crz":
        qc.crz(params[0], qubits[0], qubits[1])
    elif name == "rxx":
        qc.rxx(params[0], qubits[0], qubits[1])
    elif name == "rzz":
        qc.rzz(params[0], qubits[0], qubits[1])
    elif name == "ccx":
        qc.ccx(qubits[0], qubits[1], qubits[2])
    elif name == "cswap":
        qc.cswap(qubits[0], qubits[1], qubits[2])
    else:
        raise ValueError("unsupported gate name: " + name)


def _build_sub(n, gates, label):
    """Build one of the compared circuits (U or V) from its gate list.

    Gates are listed in time order (first entry applied first), so the matrix
    product is read right-to-left, matching the eq_5 convention 'XZ = Z first'.
    """
    if not isinstance(gates, list):
        raise ValueError(label + " must be a list of gate dicts")
    qc = QuantumCircuit(QuantumRegister(n, "system"), name=label)
    for gate in gates:
        name, qubits, params = _validate_gate(gate, n)
        _append_gate(qc, name, qubits, params)
    return qc


def build_circuit(instance):
    """Return the miter circuit W for circuit-equivalence checking.

    instance keys:
      n    : number of qubits (1..12)
      u, v : gate lists, each entry {"name": str, "qubits": [int,...], "params": [float,...]}
      mode : 'u_dag_v' -> W = U^dagger V  (eq_3 test: W proportional to identity)
             'u_v_dag' -> W = U V^dagger  (eq_4 circuit test: W diagonal)
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = instance.get("n")
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > _MAX_QUBITS:
        raise ValueError("n must satisfy 1 <= n <= " + str(_MAX_QUBITS))
    mode = instance.get("mode", "u_dag_v")
    if mode not in ("u_dag_v", "u_v_dag"):
        raise ValueError("mode must be 'u_dag_v' or 'u_v_dag'")
    if "u" not in instance or "v" not in instance:
        raise ValueError("instance must contain gate lists 'u' and 'v'")
    qc_u = _build_sub(n, instance["u"], "U")
    qc_v = _build_sub(n, instance["v"], "V")

    qc = QuantumCircuit(QuantumRegister(n, "system"), name="miter_" + mode)
    if mode == "u_dag_v":
        # eq_3: W = U^dagger V -- apply V first, then U^dagger (time order).
        qc.compose(qc_v, qubits=range(n), inplace=True)
        qc.compose(qc_u.inverse(), qubits=range(n), inplace=True)
    else:
        # eq_4 (circuit part): W = U V^dagger -- apply V^dagger first, then U.
        qc.compose(qc_v.inverse(), qubits=range(n), inplace=True)
        qc.compose(qc_u, qubits=range(n), inplace=True)
    return qc
