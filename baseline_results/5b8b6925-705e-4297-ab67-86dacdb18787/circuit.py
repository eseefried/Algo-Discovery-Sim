"""Bell-like multi-term entangled basis generator (chosen construction of the spec).

Operation implemented: U = C_f (H^{(x)m} (x) I^{(x)(n-m)})   [eq_4, eq_5]
  - H on each of the m control qubits                        [eq_3]
  - C_f |k>|b> = |k>|b XOR f(k)>  (multi-qubit controlled XOR)  [eq_4]
Applied to a computational input |a>|b> the circuit outputs |B_{a,b}> [eq_5], a
superposition of exactly 2^m distinct terms with amplitudes +-1/sqrt(2^m) [eq_1];
since U is unitary the 2^n outputs are orthonormal [eq_2].

Qubit layout (Qiskit index 0 = least significant bit):
  target register  : Qiskit qubits 0 .. n-m-1   (target qubit 1 of the spec = index n-m-1, MSB of b)
  control register : Qiskit qubits n-m .. n-1   (control qubit 1 of the spec = index n-1, MSB of a)
With this layout the integer value of a basis state equals the big-endian reading of the
label string 'ab' used in the specification (a*2^(n-m) + b).

Instance format:
  {"n": int, "m": int, "f_table": [int, ...]}  with len(f_table) == 2^m and
  0 <= f_table[k] < 2^(n-m); k and f(k) are read as integers with the first spec qubit as MSB.
  Alternatively {"n": int, "m": int, "f": "parity"} selects f(k) = k_1 XOR ... XOR k_m written
  into the least significant target bit.
"""
from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _parity_table(m, n_target):
    table = []
    for k in range(2 ** m):
        parity = bin(k).count("1") % 2
        table.append(parity)
    return table


def _validate(instance):
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object (dict)")
    if "n" not in instance or "m" not in instance:
        raise ValueError("instance requires keys 'n' and 'm'")
    n = _as_int(instance["n"], "n")
    m = _as_int(instance["m"], "m")
    if n < 2 or n > MAX_QUBITS:
        raise ValueError(f"n must satisfy 2 <= n <= {MAX_QUBITS}")
    if m < 1 or m > n - 1:
        raise ValueError("m must satisfy 1 <= m <= n-1")
    n_target = n - m
    if "f_table" in instance:
        raw = instance["f_table"]
        if not isinstance(raw, list) or len(raw) != 2 ** m:
            raise ValueError("f_table must be a list of length 2^m")
        f_table = []
        for value in raw:
            v = _as_int(value, "f_table entry")
            if v < 0 or v >= 2 ** n_target:
                raise ValueError("f_table entries must lie in [0, 2^(n-m))")
            f_table.append(v)
    elif instance.get("f") == "parity":
        f_table = _parity_table(m, n_target)
    else:
        raise ValueError("instance requires 'f_table' (list) or 'f': 'parity'")
    if all(v == f_table[0] for v in f_table):
        raise ValueError("f must be non-constant for the basis to be entangled (eq_4 assumption)")
    return n, m, f_table


def _apply_hadamard_layer(qc, control_idx):
    # eq_3: H^{(x)m}|a> = 2^{-m/2} sum_k (-1)^{a.k} |k>
    for q in control_idx:
        qc.h(q)


def _apply_controlled_xor(qc, control_idx, target_idx, m, f_table):
    # eq_4: C_f |k>|b> = |k>|b XOR f(k)>, realised as, for every control string k,
    # X-conjugated multi-controlled X gates onto each target bit where f(k) has a 1.
    # control_idx[i] carries bit i of k (ascending significance); target_idx[t] carries bit t of f(k).
    n_target = len(target_idx)
    for k in range(2 ** m):
        fk = f_table[k]
        if fk == 0:
            continue
        zero_controls = [control_idx[i] for i in range(m) if ((k >> i) & 1) == 0]
        for q in zero_controls:
            qc.x(q)
        for t in range(n_target):
            if (fk >> t) & 1:
                qc.mcx(list(control_idx), target_idx[t])
        for q in zero_controls:
            qc.x(q)


def build_circuit(instance):
    """Return the unitary U = C_f (H^{(x)m} (x) I) of eq_4/eq_5 as a QuantumCircuit."""
    n, m, f_table = _validate(instance)
    n_target = n - m
    target = QuantumRegister(n_target, "target")
    control = QuantumRegister(m, "control")
    qc = QuantumCircuit(target, control, name="bell_like_basis")
    target_idx = list(range(0, n_target))
    control_idx = list(range(n_target, n))
    # eq_5: |B_{a,b}> = C_f (H^{(x)m} (x) I) |a>|b>
    _apply_hadamard_layer(qc, control_idx)
    _apply_controlled_xor(qc, control_idx, target_idx, m, f_table)
    return qc
