# Equation to Qiskit

Single-step (N=1) Naimark dilation of a two-outcome qubit measurement with M0=U0 diag(a,b) V and M1=U1 diag(sqrt(1-a^2),sqrt(1-b^2)) V on a system qubit and a probe qubit. The circuit applies V on the system, then a system-controlled RY on the probe (angles 2*arccos(a) for s=0 and 2*arccos(b) for s=1), then probe-controlled U0 (p=0) and U1 (p=1) on the system. It is unitary and has no input preparation or measurement. The output state is sum_k (M_k psi) (x) |k>_p.

Source equation run: `c96f7338-04cb-4948-bc96-f4bc56c36972`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system s (input state psi, little-endian least significant bit)
- qubit 1: probe p (input |0>); the output state is sum_k (M_k psi)_s (x) |k>_p
- Basis index = s + 2*p

## Assumptions

- a and b lie in [0,1], so theta in [0,pi] and sin(theta/2) = sqrt(1-a^2) is nonnegative (no sign issue).
- a == b is accepted as a valid but trivial case.
- Qiskit's RY convention RY(theta)|0> = cos(theta/2)|0> + sin(theta/2)|1> is used.
- The probe starts in |0>, prepared by the runner.
- Completeness of M0 and M1 holds by construction.

## Unresolved issues

- The paper's Hamiltonian normalization and exact pulse sequence for reaching arbitrary (theta0, theta1) are unavailable.
- The N-step continuous decomposition is not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: V gate, and U0/U1 parameters used in the controlled-U steps. The Kraus operators M0, M1 are realized through V, the singular values a, b, and the feedback unitaries U0, U1, with each unitary given as exp(i*gamma)*U(theta,phi,lam).
- `eq_2`: implemented; build_circuit: theta0 = 2*acos(a), theta1 = 2*acos(b). The controlled-RY angles are set so that the probe |0> amplitude equals the singular value.
- `eq_3`: background; no code location. The Hamiltonian exp(-i g t Z(x)Y) is not synthesized. Its Z-conditioned RY form is implemented directly as controlled-RY gates with arbitrary angles. The extra pulses that would reach theta0 != +-theta1 are not specified.
- `eq_4`: implemented; build_circuit: V, controlled-RY pair, then X-conjugated cu for U0 and cu for U1. This realizes sum_k (U_k (x) |k><k|) C (V psi (x) |0>) with C = sum_z |z><z| (x) RY(theta_z).
- `eq_5`: background; no code location. The Born-rule probabilities and post-measurement states are computed by the runner, not by the circuit.

## Specification changes

- eq_1, eq_4: Each unitary U0, U1, V is parametrized as exp(i*gamma)*U(theta,phi,lam), with gamma optional and defaulting to 0. U0 and U1 are applied as controlled-U gates (cu), which carry gamma as the controlled phase. Reason: A concrete gate-level parametrization is required. The controlled phase affects the relative phase between branches, so it must be explicit.
- eq_3: The Z(x)Y Hamiltonian evolution is replaced by directly parametrized controlled-RY gates. Reason: The paper's pulse sequence and normalization are not available, and the construction only needs conditioned probe rotations.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to a single dilation step (N=1). The two-singular-value proof and the N-step decomposition with fresh probes are not implemented. Reason: The specification marks these as missing information.
