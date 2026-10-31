# Equation to Qiskit

Qiskit implementation of the scoped construction: second-order symmetric Trotter (Suzuki) splitting of the single-qubit Lindbladian L = L_1 + L_2 with L_1 the coherent X-rotation term (H = omega X/2) and L_2 amplitude damping at rate gamma. Each of the n steps applies Rx(omega*tau/2) on the system, then the exact one-ancilla Stinespring dilation of the amplitude-damping step (system-controlled Ry(theta) on a fresh ancilla followed by CNOT ancilla->system, theta = 2 arcsin sqrt(1-exp(-gamma*tau))), then Rx(omega*tau/2) again. Because the returned object must be a measurement-free unitary circuit (no reset), one fresh ancilla is allocated per dissipative step instead of resetting a single ancilla; total qubits n+1 <= 12. The channel S_2(t/n)^n(rho_0) is obtained by tracing out all ancillas, which the runner must prepare in |0>.

Source equation run: `6735ecfd-c1fb-44a1-85e8-8819e20b46a4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 (register s[0]): system qubit S carrying rho; runner prepares rho_0 (instance choice |+><+|) here
- qubit 1 (register a[0]): ancilla A_1, must be |0> at input; consumed by the dissipative part of Trotter step 1 and traced out afterwards
- qubit 2 (register a[1]): ancilla A_2, must be |0> at input; consumed by the dissipative part of Trotter step 2 and traced out afterwards
- general n: qubits 1..n are ancillas A_1..A_n, one per Trotter step; total qubits n+1 <= 12 so n <= 11
- Qiskit little-endian convention: qubit 0 is the least significant computational-basis bit

## Assumptions

- All ancilla qubits (indices 1..n) are supplied in |0> by the runner; the simulated channel on qubit 0 is obtained by tracing out qubits 1..n.
- The coherent half step uses Rx(omega*tau/2) = exp(-i (tau/2) (omega/2) X), matching H = (omega/2) X.
- The controlled-Ry gate (qc.cry) is considered an O(1) composition of single-qubit and CNOT gates; no further gate-level compilation is performed.
- Parameter validation: omega, gamma, t finite reals with gamma >= 0 and t >= 0; n a positive integer with n + 1 <= 12.
- No simulation or verification has been performed; correctness claims are based on the algebraic derivation in the docstrings.

## Unresolved issues

- The paper's general method for approximating arbitrary single-qubit channels with one ancilla is not reconstructed; only the two-Kraus amplitude-damping instance is exactly dilated.
- The error constant C in eq_4 and the resulting formula for n given epsilon are not available, so n must be chosen by the user.
- Whether the original algorithm uses ancilla reset, measurement, or classical randomness between steps is unknown; this implementation substitutes fresh ancillas.

## Equation mapping

- `eq_1`: background; no code location. Definition of the target semigroup T_t = e^{tL} in GKSL form; it is the object being approximated, not directly constructed in the circuit.
- `eq_2`: background; no code location. Induced (1->1) norm used only in the error analysis / choice of n; the module takes n as an input and performs no norm computation.
- `eq_3`: implemented; _coherent_half_step (L_1 as Rx(omega*tau/2)) and _dissipative_step (L_2 via its exact dilation); module docstring. The two-term split L = L_1 + L_2 is realised by alternating the coherent Rx half-steps and the amplitude-damping dilation.
- `eq_4`: implemented; build_circuit: loop 'for k in range(n)' with comment '# eq_4', tau = t / n. The symmetric second-order product S_2(tau)^n is built step by step; the error bound and choice of n are not computed in code (n is supplied).
- `eq_5`: implemented; _damping_angle (p = 1 - exp(-gamma*tau)) and docstring of _dissipative_step (Kraus operators K_0, K_1). The Kraus form of the amplitude-damping step determines p and hence the rotation angle theta of the dilation.
- `eq_6`: implemented; _dissipative_step: qc.cry(theta, system, ancilla); qc.cx(ancilla, system). One-ancilla Stinespring dilation U_AD = CNOT_{A->S} . C_S[Ry(theta)]_A with theta = 2 arcsin sqrt(p); ancilla starts in |0> and is traced out by the runner.

## Specification changes

- eq_6: Instead of reusing a single ancilla that is reset to |0> before each dissipative step, the circuit allocates n fresh ancilla qubits (one per Trotter step), giving n+1 qubits in total and the constraint n <= 11. Reason: The deliverable must be a measurement-free unitary QuantumCircuit without reset or dynamic circuits; using n fresh |0> ancillas is unitarily equivalent (after tracing out all ancillas) to reset-and-reuse of one ancilla.
- eq_4, eq_2: The number of Trotter steps n is taken as an instance parameter rather than derived from epsilon via the bound n = O((||L|| t)^{3/2}/epsilon^{1/2}). Reason: The constant C in the error bound is not available from the abstract, and the module must not perform norm/operator computations; the instance fixes n = 2 as in the specification.
- eq_3, eq_5: Scope narrowed to the specific instance generator (X-rotation plus amplitude damping); arbitrary single-qubit Lindbladians and the paper's general one-ancilla channel approximation are not implemented. Reason: The abstract does not specify the general decomposition or the arbitrary-channel approximation method; the specification already restricted to this exactly dilatable instance.
