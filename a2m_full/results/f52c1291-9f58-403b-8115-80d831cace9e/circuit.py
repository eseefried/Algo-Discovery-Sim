from qiskit import QuantumCircuit, QuantumRegister
import math


def _apply_tcx(qc, c1, t0, t1):
    """eq_2/eq_4: target trit t=2*t1+t0 shifted +1 mod 3 when control qutrit is 2 (c1=1).
    Step 1: controlled swap of trits 1<->2 (01<->10). Step 2: controlled swap of trits 0<->1 (00<->01),
    i.e. toggle t0 when t1=0. Composition maps 0->1, 1->2, 2->0 and fixes 11."""
    qc.cswap(c1, t0, t1)
    qc.x(t1)
    qc.ccx(c1, t1, t0)
    qc.x(t1)


def _apply_tcz(qc, c1, t0, t1):
    """eq_3: phase omega^t, t=2*t1+t0, on the target when control qutrit is 2 (c1=1).
    Phase exp(2 pi i (t0+2 t1)/3) is built from two controlled phases."""
    qc.cp(2.0 * math.pi / 3.0, c1, t0)
    qc.cp(4.0 * math.pi / 3.0, c1, t1)


def build_circuit(instance):
    """Layout (eq_1): qubits 0,1 = a0,a1 ; qubits 2,3 = b0,b1. Trit t=2*q1+q0.
    instance: {"gate": "TCX"|"TCZ", "control": "a"|"b", "power": int in 0..8}"""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    gate = instance.get("gate", "TCX")
    control = instance.get("control", "a")
    power = instance.get("power", 1)
    if gate not in ("TCX", "TCZ"):
        raise ValueError("gate must be 'TCX' or 'TCZ'")
    if control not in ("a", "b"):
        raise ValueError("control must be 'a' or 'b'")
    if isinstance(power, bool) or not isinstance(power, int) or power < 0 or power > 8:
        raise ValueError("power must be an integer in 0..8")
    a = QuantumRegister(2, "a")
    b = QuantumRegister(2, "b")
    qc = QuantumCircuit(a, b)
    if control == "a":
        c1, t0, t1 = a[1], b[0], b[1]
    else:
        c1, t0, t1 = b[1], a[0], a[1]
    for _ in range(power):
        if gate == "TCX":
            _apply_tcx(qc, c1, t0, t1)
        else:
            _apply_tcz(qc, c1, t0, t1)
    return qc
