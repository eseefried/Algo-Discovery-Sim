# Equation to Qiskit

Implements the ideal gate-level Grover search operator (eq_3 with the eq_4 default iteration count) for a single marked basis state on n qubits (2 <= n <= 12, n = 4 in the paper's instance): optional Hadamard layer creating |s>, then r repetitions of the phase oracle O_w (X-conjugated multi-controlled Z) followed by the diffusion operator D (H, O_0, H). The pulse-level Ising spin-chain model (eq_1, eq_2), the 2*pi*k Rabi-frequency condition (eq_5) and the fidelity figure of merit (eq_6) are not implemented; they describe the Hamiltonian simulation the paper performs, which is not a unitary circuit construction within this scope.

Source equation run: `68e0108c-483d-4849-9710-256d7bae804f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'spin' with 4 qubits (indices 0..3); total qubits = 4
- Qiskit qubit 3 = specification spin 1 (most significant bit x_1); qubit 2 = spin 2; qubit 1 = spin 3; qubit 0 = spin 4 (least significant bit x_4)
- Basis state |x>, x = sum_k x_k 2^(4-k), with |0> = spin up and |1> = spin down; marked item w = 1111 = 15
- Runner input: |0000> (all qubits in |0>); with prepare_superposition=true the circuit applies H on all qubits then 3 Grover iterations, giving |<1111|psi>|^2 = sin^2(7 theta) ~ 0.961 (eq_4)

## Assumptions

- Single marked item w; the paper's choice of marked state is unknown and w = 1111 is the instance choice from the specification.
- Three Grover iterations (eq_4 r_opt for N = 16) are used in the example; the paper may have simulated a different number.
- Spin up encodes bit 0 and spin down bit 1; the runner supplies |0...0> as input.
- Multi-controlled Z is realised with QuantumCircuit.mcp(pi, controls, target), a standard library gate rather than an opaque dense unitary.
- Global phase of the diffusion operator is ignored.

## Unresolved issues

- The Ising spin-chain pulse-level realisation (eq_1, eq_2), the 2*pi*k Rabi-frequency condition (eq_5) and the fidelity scan (eq_6) remain unimplemented because physical parameters and the paper's pulse sequence are missing.
- Whether the paper's fidelity is a squared overlap and how the ideal reference state is defined during pulses cannot be resolved from the abstract.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Drift Ising Hamiltonian H_0 of the spin chain is part of the pulse-level Hamiltonian simulation, not of the gate-level Grover construction chosen for implementation; not realised as a circuit.
- `eq_2`: out_of_scope; no code location. Time-dependent RF pulse Hamiltonian requires time-ordered Hamiltonian integration and physical parameters (omega_k, J, J', Omega) that are not available; not implemented.
- `eq_3`: implemented; _phase_flip (oracle O_w), _diffusion (D), build_circuit (H layer for |s> and the loop applying G = D O_w). Uniform superposition via H on every qubit, phase oracle via X-conjugated multi-controlled phase pi, diffusion via H^n O_0 H^n (equal to D up to global phase -1), Grover iterate repeated r times.
- `eq_4`: implemented; build_circuit, comment '# eq_4: r_opt = floor(pi/4 * sqrt(N))' (default value of iterations). Default iteration count r_opt = floor(pi/4 sqrt(2^n)) is used when 'iterations' is absent; for n = 4 this gives r = 3. The success-probability formula itself is analytic background and not computed in the circuit.
- `eq_5`: out_of_scope; no code location. The 2*pi*k Rabi-frequency condition concerns the pulse-level realisation and the numerical fidelity scan; no pulse model is implemented.
- `eq_6`: out_of_scope; no code location. Fidelity between ideal and pulse-driven states requires Hamiltonian simulation and state comparison, which is excluded (no simulation or operator construction in the module).

## Specification changes

- eq_1, eq_2, eq_5, eq_6: Scope narrowed from the pulse-level spin-chain simulation of Grover's algorithm to the ideal gate-level Grover operator only. Reason: The pulse-level model needs numerical Larmor frequencies, couplings, pulse durations and the paper's pulse sequence (all listed as missing), and the fidelity/2*pi*k analysis is a simulation result rather than a unitary circuit construction.
- eq_3: Qubit ordering: specification spin k (spin 1 = MSB) is mapped to Qiskit qubit n - k so that Qiskit qubit 0 is the LSB; marked bitstrings are read with spin 1 as the leftmost character. Reason: Qiskit's little-endian convention differs from the spin-chain labelling x = sum_k x_k 2^(n-k) in the specification.
- eq_3: Diffusion operator realised as H^n (1 - 2|0><0|) H^n, which equals -D (global phase -1 relative to D = 2|s><s| - 1). Reason: Standard circuit realisation; a global phase does not change the algorithm's state or success probability.
- eq_3, eq_4: Generalised from n = 4 (N = 16) to any 2 <= n <= 12 with arbitrary single marked state and optional user-supplied iteration count r (default r_opt of eq_4); the H layer preparing |s> is optional (prepare_superposition flag, default true). Reason: Required to accept varying valid instance parameters under the 12-qubit cap; the |s> preparation is part of the Grover algorithm but may be disabled if the runner prepares the superposition itself.
