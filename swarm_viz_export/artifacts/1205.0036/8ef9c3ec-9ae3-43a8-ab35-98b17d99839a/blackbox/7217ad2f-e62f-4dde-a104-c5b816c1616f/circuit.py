from qiskit import QuantumCircuit, QuantumRegister


def _parse(instance):
    """Validate the instance and return the three X-mask bits for t1, t2, t3."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object")
    for key in instance:
        if key not in ("k", "side", "x_mask"):
            raise ValueError("unknown instance key: " + str(key))
    for key in ("k", "side"):
        if key in instance:
            v = instance[key]
            if isinstance(v, bool) or not isinstance(v, int) or v != 2:
                raise ValueError(key + " must equal 2 (only the 2x2 grid is implemented)")
    mask = instance.get("x_mask", [1, 1, 1])
    if not isinstance(mask, (list, tuple)) or len(mask) != 3:
        raise ValueError("x_mask must be a list of 3 bits")
    out = []
    for m in mask:
        if isinstance(m, bool):
            out.append(int(m))
        elif isinstance(m, int) and m in (0, 1):
            out.append(m)
        else:
            raise ValueError("x_mask entries must be 0 or 1")
    return out


def build_circuit(instance):
    """2x2 grid, sites row-major: c=(0,0)=q0, t1=(0,1)=q1, t2=(1,0)=q2, t3=(1,1)=q3.

    Implements eq_3 (applied in time order, rightmost operator first):
    CX(c,t1), CX(t1,t3), CX(c,t1), CX(t1,t3), CX(c,t1), CX(c,t2).
    With the full mask this is the fanout of eq_1; per-target masks give C(X^m1 x X^m2 x X^m3) of eq_2.
    """
    m1, m2, m3 = _parse(instance)
    c = QuantumRegister(1, "c")
    t = QuantumRegister(3, "t")
    qc = QuantumCircuit(c, t)
    ctrl, t1, t2, t3 = 0, 1, 2, 3
    if m3:
        # XOR x onto the diagonal site t3 through t1; t1 is restored to y1 (eq_4 trace).
        qc.cx(ctrl, t1)
        qc.cx(t1, t3)
        qc.cx(ctrl, t1)
        qc.cx(t1, t3)
    if m1:
        qc.cx(ctrl, t1)
    if m2:
        qc.cx(ctrl, t2)
    return qc
