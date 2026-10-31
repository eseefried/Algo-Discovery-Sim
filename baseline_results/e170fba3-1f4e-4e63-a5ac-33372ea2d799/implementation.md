# Equation to Qiskit

Qiskit module implementing fixed-point amplitude amplification (eq_1-eq_3, eq_6) as one unitary operation: A = H^{\otimes n} state preparation followed by l=(L-1)/2 generalized Grover iterations G(alpha_j,beta_j) = S_s(alpha_j) S_t(beta_j) with the Chebyshev phase schedule alpha_j = -beta_{l-j+1} = 2 acot(tan(2 pi j/L) sqrt(1-gamma^2)), 1/gamma = cosh(acosh(1/delta)/L). The partial-phase oracle S_t and the reflection S_s = A S_0 A^dagger are realised with X-conjugated multi-controlled phase gates (no ancilla). The scoped example is n=2, target |11>, L=3, delta=1/2. One sign-convention correction to eq_2 (S_t must carry e^{+i beta}) was required for eq_3's schedule to produce the fixed-point response and is reported.

Source equation run: `9963132b-7925-4b62-91b7-92f843822295`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- sys[0] = qubit 0: least-significant bit of the computational-basis label (Qiskit little-endian)
- sys[1] = qubit 1: most-significant bit for the n=2 example; target integer 3 = |11> = both qubits 1
- No ancilla qubits; multi-controlled phases are synthesised by Qiskit without extra qubits. Total qubits = n <= 12.
- Example: input |00> -> A=H⊗H gives lambda=1/4 -> one iteration G(alpha_1,beta_1) with L=3, delta=1/2 -> target weight P_3(1/4) ≈ 0.914 expected (eq_4, unverified here).

## Assumptions

- The Chebyshev phase schedule (eq_3) and success probability (eq_4) are recalled from the published fixed-point amplitude amplification method, not derived from the abstract; only the L=3 case was hand-checked for consistency.
- Each S_t application counts as one oracle query; the cost of A, A† and the multi-controlled phase synthesis is not counted.
- Target states are listed as integers (little-endian, qubit k = bit k) or as n-bit strings with leftmost character = qubit n-1.
- qc.mcp (MCPhaseGate) is available in Qiskit 2.6.1 and synthesises to standard gates without ancilla.

## Unresolved issues

- eq_3/eq_4 have not been checked against the paper for L > 3 (the implemented ordering yields the palindromic phase sequence alpha_l, ..., alpha_1, alpha_1, ..., alpha_l, which is the expected structure, but this is unverified).
- No simulation was run; the quoted expected value P_3(1/4) ≈ 0.914 is a hand computation.
- Whether the paper's construction requires an ancilla for the general-phase oracle is not resolved; here mcp is used directly on the system register.

## Equation mapping

- `eq_1`: implemented; build_circuit: block 'eq_1: |s> = A|0..0>' (qc.h on all qubits when apply_state_preparation is True). A = H^{⊗n} prepares the uniform superposition; lambda = |targets|/2^n is implicit in the target list.
- `eq_2`: implemented; _target_phase_oracle (S_t), _reflection_about_s (S_s = A S_0 A†), _apply_basis_state_phase. Partial-phase oracle and partial-phase reflection about |s> realised via X-conjugated mcp gates; overall minus sign of G dropped as global phase; S_t sign convention corrected to e^{+i beta}.
- `eq_3`: implemented; _fixed_point_phases and the iteration loop in build_circuit. Computes 1/gamma = cosh(acosh(1/delta)/L), alpha_j = 2 acot(tan(2 pi j/L) sqrt(1-gamma^2)), beta_j = -alpha_{l-j+1}, and applies G(alpha_1,beta_1) first through G(alpha_l,beta_l) last.
- `eq_4`: background; no code location. Closed-form success probability is a property of the output state, not a circuit element; it is only quoted in docstrings/notes as the expected value.
- `eq_5`: background; no code location. The fixed-point guarantee and query-complexity scaling are analytical consequences; the code only exposes L and delta as inputs and does not pick L from w.
- `eq_6`: implemented; example_instance_json / build_circuit with n=2, targets=[3], L=3, delta=0.5. The scoped tiny instance is exactly the example instance; the module also accepts other valid (n, targets, L, delta).

## Specification changes

- eq_2, eq_3: Sign convention of the oracle changed from S_t(beta) = I - (1 - e^{-i beta})|t><t| to S_t(beta) = I - (1 - e^{+i beta})|t><t| (the published convention), while keeping alpha_j = -beta_{l-j+1} from eq_3. Equivalently the oracle in iteration j applies phase e^{-i alpha_{l-j+1}} to targets. Reason: A hand evaluation of the 2D amplitude for L=3, delta=1/2, lambda=1/4 showed the specification's e^{-i beta} convention gives target probability ≈0.24 (< lambda), whereas e^{+i beta} gives ≈0.915, matching eq_4's prediction 1 - delta^2 T_3(T_{1/3}(2) sqrt(3/4))^2 ≈ 0.914.
- eq_2: The overall factor -1 in G(alpha,beta) = -S_s S_t is omitted. Reason: It is a global phase with no effect on measurement statistics; omitting it keeps the circuit in standard gates.
- eq_3: acot is evaluated on the branch (0, pi) via atan2(1, x); L = 1 (l = 0, no iterations) is accepted and yields just A. Reason: 2*acot(x) is only defined modulo 2 pi, so the branch choice is immaterial; L=1 is a degenerate but valid odd query count.
- eq_1, eq_6: The state-preparation unitary A = H^{⊗n} is included in the operation (optional via apply_state_preparation flag, default True) rather than supplied externally; A is fixed to Hadamards, so lambda = |targets|/2^n only. Reason: A is part of the algorithm's definition (also used inside S_s); the runner prepares |0...0>. General A is outside the scoped construction.
- eq_6: Scope generalised slightly beyond the single tiny instance: arbitrary n <= 12, arbitrary distinct target sets, any odd L and delta in (0,1); no measurement is included. Reason: The task requires an operation valid for varying instance parameters and measurement-free output.
