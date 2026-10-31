"""Second-order product-formula simulation of a single-qubit Markovian channel.

Scoped construction (from the math specification):
  L = L_1 + L_2                                             (eq_3)
  L_1(rho) = -i[(omega/2) X, rho]                           (coherent piece)
  L_2(rho) = gamma (s- rho s+ - 1/2 {s+ s-, rho})           (amplitude damping)
  S_2(tau) = e^{tau L_1/2} e^{tau L_2} e^{tau L_1/2}        (eq_4)
  T_t ~= S_2(t/n)^n

Each dissipative step e^{tau L_2} is realised exactly by the one-ancilla
Stinespring dilation (eq_5, eq_6):
  U_AD = CNOT_{A->S} . C_S[Ry(theta)]_A,  theta = 2 arcsin sqrt(p),
  p = 1 - exp(-gamma tau),
with the ancilla prepared in |0> and traced out afterwards.

Because the returned circuit must be unitary and measurement-free (no reset),
one fresh ancilla qubit is used for each of the n dissipative steps instead of
resetting a single reused ancilla.

Qubit layout: qubit 0 = system S; qubits 1..n = ancillas A_1..A_n where A_k is
consumed by the k-th Trotter step (1-indexed). All ancillas must be supplied in
|0>; the simulated channel on S is obtained by tracing out all ancillas.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12


def _as_real(instance, key):
    """Fetch a finite real number from the instance dict or raise ValueError."""
    if key not in instance:
        raise ValueError("missing required parameter '%s'" % key)
    value = instance[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("parameter '%s' must be a real number" % key)
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("parameter '%s' must be finite" % key)
    return value


def _as_positive_int(instance, key):
    """Fetch a positive integer from the instance dict or raise ValueError."""
    if key not in instance:
        raise ValueError("missing required parameter '%s'" % key)
    value = instance[key]
    if isinstance(value, bool):
        raise ValueError("parameter '%s' must be an integer" % key)
    if isinstance(value, float):
        if not value.is_integer():
            raise ValueError("parameter '%s' must be an integer" % key)
        value = int(value)
    if not isinstance(value, int):
        raise ValueError("parameter '%s' must be an integer" % key)
    if value < 1:
        raise ValueError("parameter '%s' must be >= 1" % key)
    return value


def _validate(instance):
    """Validate the instance and return (omega, gamma, t, n)."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a JSON object / dict")
    omega = _as_real(instance, "omega")
    gamma = _as_real(instance, "gamma")
    t = _as_real(instance, "t")
    n = _as_positive_int(instance, "n")
    if gamma < 0.0:
        raise ValueError("damping rate gamma must be non-negative")
    if t < 0.0:
        raise ValueError("evolution time t must be non-negative")
    # One system qubit plus one fresh ancilla per Trotter step.
    total_qubits = n + 1
    if total_qubits > MAX_QUBITS:
        raise ValueError(
            "n = %d steps needs %d qubits (1 system + n ancillas), exceeding the cap of %d"
            % (n, total_qubits, MAX_QUBITS)
        )
    return omega, gamma, t, n


def _damping_angle(gamma, tau):
    """eq_5 / eq_6: p = 1 - exp(-gamma tau), theta = 2 arcsin(sqrt(p))."""
    p = 1.0 - math.exp(-gamma * tau)
    if p < 0.0:
        p = 0.0
    if p > 1.0:
        p = 1.0
    return 2.0 * math.asin(math.sqrt(p))


def _coherent_half_step(qc, system, omega, tau):
    """eq_3 (L_1) and eq_4: e^{(tau/2) L_1}(rho) = U rho U^dagger with
    U = exp(-i (tau/2) (omega/2) X) = Rx(omega * tau / 2)."""
    qc.rx(omega * tau / 2.0, system)


def _dissipative_step(qc, system, ancilla, theta):
    """eq_5 / eq_6: one-ancilla Stinespring dilation of e^{tau L_2}.

    U_AD = CNOT_{A->S} . C_S[Ry(theta)]_A acting on |0>_A (x) |psi>_S gives
    (<0|_A (x) I) U_AD (|0>_A (x) I) = K_0 = |0><0| + sqrt(1-p)|1><1|,
    (<1|_A (x) I) U_AD (|0>_A (x) I) = K_1 = sqrt(p)|0><1|,
    with sqrt(p) = sin(theta/2).
    """
    qc.cry(theta, system, ancilla)
    qc.cx(ancilla, system)


def build_circuit(instance):
    """Build the unitary dilation of S_2(t/n)^n for the instance generator.

    instance keys:
      omega : real, coefficient of the Hamiltonian H = (omega/2) X
      gamma : real >= 0, amplitude-damping rate
      t     : real >= 0, total evolution time
      n     : int >= 1, number of second-order Trotter steps (n + 1 <= 12)

    Qubit 0 is the system; qubits 1..n are fresh |0> ancillas, ancilla k being
    used in Trotter step k. Tracing out the ancillas yields S_2(t/n)^n(rho_0).
    """
    omega, gamma, t, n = _validate(instance)
    tau = t / float(n)  # eq_4: tau = t / n
    theta = _damping_angle(gamma, tau)

    sys_reg = QuantumRegister(1, "s")
    anc_reg = QuantumRegister(n, "a")
    qc = QuantumCircuit(sys_reg, anc_reg, name="lindblad_trotter2")
    system = sys_reg[0]

    # eq_4: S_2(tau)^n = [ e^{tau L_1/2} e^{tau L_2} e^{tau L_1/2} ]^n
    for k in range(n):
        _coherent_half_step(qc, system, omega, tau)
        _dissipative_step(qc, system, anc_reg[k], theta)
        _coherent_half_step(qc, system, omega, tau)

    return qc
