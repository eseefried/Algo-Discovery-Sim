"""First-order Trotter (Lie-Trotter) circuit for a transverse-field Ising chain.

H = A + B,  A = J * sum_{k} X_k X_{k+1}  (open chain),  B = h * sum_k Z_k.
The operation returned is the ideal (noise-free) Trotterized unitary
    U_n(t) = ( e^{-i A t/n} e^{-i B t/n} )^n                      (eq_1)
The Trotter number n is either given in the instance or chosen from the
closed-form optimum of the error-tradeoff bound                   (eq_6).

Qubit convention: specification qubit k (1-indexed, k = 1 is the most
significant bit of |q_1 q_2 ... q_N>) is mapped to Qiskit qubit index N - k,
because Qiskit index 0 is the least significant bit.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
MAX_TROTTER_NUMBER = 2000


def _as_real(value, name):
    """Validate that value is a finite real number and return it as float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number, got {value!r}")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return out


def _as_positive_int(value, name, upper):
    """Validate that value is an integer in [1, upper] and return it."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    if value < 1 or value > upper:
        raise ValueError(f"{name} must be in [1, {upper}], got {value}")
    return int(value)


def optimal_trotter_number(coupling_j, field_h, time_t, epsilon, num_qubits):
    """eq_6: n* = sqrt(c_1 / c_2), rounded to the neighbouring integer that
    minimises the bound D(n) <= c_1/n + c_2 n (eq_5).

    c_1 = (t^2 / 2) * ||[A, B]||,  c_2 = 2 * epsilon.
    For the open TFIM chain, [A, B] = -2 i J h sum_k (Y_k X_{k+1} + X_k Y_{k+1}),
    so ||[A, B]|| <= 4 |J h| (N - 1), with equality for N = 2 (the two
    commuting Pauli strings Y X and X Y give spectral norm 2).
    """
    if epsilon <= 0.0:
        raise ValueError("epsilon must be strictly positive to define n*")
    comm_norm = 4.0 * abs(coupling_j * field_h) * (num_qubits - 1)
    c_1 = 0.5 * time_t * time_t * comm_norm  # Trotter-error coefficient (eq_2)
    c_2 = 2.0 * epsilon  # accumulated gate-error coefficient (eq_4)
    if c_1 == 0.0:
        # A and B commute (or t = 0): a single Trotter step is exact.
        return 1
    n_real = math.sqrt(c_1 / c_2)  # continuous optimum (eq_6)
    n_lo = max(1, int(math.floor(n_real)))
    n_hi = max(1, int(math.ceil(n_real)))
    d_lo = c_1 / n_lo + c_2 * n_lo
    d_hi = c_1 / n_hi + c_2 * n_hi
    n_star = n_lo if d_lo <= d_hi else n_hi
    if n_star > MAX_TROTTER_NUMBER:
        raise ValueError(
            f"optimal Trotter number {n_star} exceeds cap {MAX_TROTTER_NUMBER}; "
            "increase epsilon or reduce t"
        )
    return n_star


def build_circuit(instance):
    """Return the first-order Trotter circuit U_n(t) (eq_1) for the TFIM chain.

    instance keys:
      num_qubits : int in [2, 12]      (optional, default 2)
      J          : real coupling of A = J sum X_k X_{k+1}
      h          : real field of    B = h sum Z_k
      t          : real evolution time
      n          : positive int Trotter number   (either n or epsilon required)
      epsilon    : positive real per-gate error; if given and n is absent,
                   n is set to the eq_6 optimum n*.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")

    num_qubits = instance.get("num_qubits", 2)
    num_qubits = _as_positive_int(num_qubits, "num_qubits", MAX_QUBITS)
    if num_qubits < 2:
        raise ValueError("num_qubits must be at least 2 so that A = J X X exists")

    if "J" not in instance or "h" not in instance or "t" not in instance:
        raise ValueError("instance must contain 'J', 'h' and 't'")
    coupling_j = _as_real(instance["J"], "J")
    field_h = _as_real(instance["h"], "h")
    time_t = _as_real(instance["t"], "t")

    if "n" in instance and instance["n"] is not None:
        n_steps = _as_positive_int(instance["n"], "n", MAX_TROTTER_NUMBER)
    elif "epsilon" in instance and instance["epsilon"] is not None:
        epsilon = _as_real(instance["epsilon"], "epsilon")
        n_steps = optimal_trotter_number(coupling_j, field_h, time_t, epsilon, num_qubits)
    else:
        raise ValueError("instance must provide either 'n' or 'epsilon'")

    tau = time_t / n_steps  # elementary time slice t/n

    sys_reg = QuantumRegister(num_qubits, "sys")
    qc = QuantumCircuit(sys_reg, name=f"trotter1_tfim_n{n_steps}")

    # eq_1: U_n(t) = (e^{-iA tau} e^{-iB tau})^n.  In the operator product the
    # rightmost factor e^{-iB tau} acts first on the state, so each Trotter
    # step applies the B-layer before the A-layer in circuit (time) order.
    for _ in range(n_steps):
        # B-layer: e^{-i h tau Z_k} = RZ(2 h tau) on every qubit
        for q in range(num_qubits):
            qc.rz(2.0 * field_h * tau, sys_reg[q])
        # A-layer: e^{-i J tau X_k X_{k+1}} = RXX(2 J tau) on each chain bond.
        # Spec qubit k -> Qiskit index num_qubits - k; the bond set is unchanged.
        for q in range(num_qubits - 1):
            qc.rxx(2.0 * coupling_j * tau, sys_reg[q], sys_reg[q + 1])

    return qc
