# Equation to Qiskit

Qiskit module implementing the basis-change operation of cyclic-MUB tomography: build_circuit(instance) returns the unitary (U^dagger)^k (or U^k) on an n-qubit data register, where U is the cyclic MUB generator. For n=1 the explicit order-3 generator U_1 = S H of eq_4 is built in (bases Z -> Y -> X). For n>1 (or on request for n=1) the Hadamard/controlled-phase template of eq_3, U = H^{(x)n} D with D a user-supplied CZ edge set and S vertex set, is implemented; the module cannot certify that a user-supplied pattern is cyclic or unbiased, since the paper's explicit multi-qubit patterns are not available. No state preparation, measurement, or classical inversion (eq_6) is included.

Source equation run: `58a8c4fe-a83e-423c-a419-2fe9a3078fb8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- data[0] (qubit 0): the single data qubit holding the unknown state; for n>1, data[i] is bit i (little-endian, qubit 0 least significant) of the computational-basis label j
- Example: n=1, k=1, inverse=true -> circuit is U_1^dagger = H S^dagger (S^dagger applied first, then H), rotating the Y-eigenbasis B_1 = {|+i>,|-i>} onto the computational basis

## Assumptions

- n=1 built-in instance uses U_1 = S H as in eq_4; it is a choice of this reconstruction, not the paper's multi-qubit generator.
- 'inverse' defaults to true so the returned operation is the measurement rotation (U^dagger)^k of eq_5; inverse=false returns U^k (basis generation direction of eq_2).
- k is allowed in 0..d inclusive (d+1 values, matching the d+1 bases; k=d returns a circuit equal to the identity up to global phase for a genuine cyclic generator, k=0 returns an empty circuit).
- Little-endian qubit ordering: data[0] is the least significant bit of the basis label j.
- For large n and k the circuit contains k*(n+|E|+|V|) gates (up to roughly 4096 repetitions for n=12); no additional depth cap is imposed beyond the 12-qubit limit.

## Unresolved issues

- Explicit cyclic generators for n=2,3,4 (edge sets, S placements, number of alternating layers) are unknown; a user-supplied eq_3 pattern is not guaranteed to be cyclic or unbiased.
- The paper's entanglement-structure classification of MUB sets and the corresponding circuits are not implemented.
- Global phase exp(i*phi) of U^{d+1} is not tracked; for the eq_4 instance it is exp(i*pi/4) per the specification.

## Equation mapping

- `eq_1`: background; no code location. Unbiasedness condition is a property of the generated bases, not an operation; it is satisfied by the built-in eq_4 generator but not checked in code (no operator construction allowed).
- `eq_2`: implemented; build_circuit: loop 'for _ in range(k): qc.compose(gen, ...)' with comment 'eq_2 / eq_5'. The circuit is the k-th power U^k (inverse=false) of the cyclic generator, realising the k-th basis B_k = {U^k|j>}.
- `eq_3`: implemented; _generator_eq3 and _validate_pattern. Hadamard/controlled-phase template U = H^{(x)n} D with D = prod CZ_ab prod S_c for a user-supplied edge set and S-vertex set; the specific pattern that makes U cyclic of order d+1 is not available from the abstract and is therefore not fixed by the code.
- `eq_4`: implemented; _generator_eq4 (gen.h(0); gen.s(0)). Single-qubit order-3 generator U_1 = S H, Hadamard applied first then S; default when n=1 and no pattern is given.
- `eq_5`: implemented; build_circuit: 'if inverse: gen = gen.inverse()' and the repetition loop. With inverse=true (default) the circuit is (U^dagger)^k, the basis-change operation that maps a measurement in B_k to a computational-basis measurement; the measurement itself and probability estimation are left to the runner.
- `eq_6`: out_of_scope; no code location. Linear-inversion reconstruction of rho from the probabilities is classical post-processing, not part of the quantum operation.

## Specification changes

- eq_3, eq_4: The two equations use opposite operator orderings: eq_4 writes U_1 = S H (H acts first, then S) while eq_3 writes U = H^{(x)n} D (D acts first, then Hadamards). The code implements each as written; the n=1 default follows eq_4, the template follows eq_3. For n=1 the template with s_qubits=[0] therefore yields H S (not S H), which is unitarily equivalent (conjugate by H) and also of order 3 modulo phase. Reason: Faithfulness to each stated equation; ordering discrepancy disclosed rather than silently harmonised.
- eq_3: The multi-qubit generator is not fixed: the user must supply 'cz_edges' and 's_qubits'. The module validates indices only and does not certify that the resulting U has order d+1 or produces mutually unbiased bases. Reason: The abstract does not specify the explicit two-, three-, four-qubit generators; inventing one would be fabrication, and operator-level verification is disallowed in the module.
- eq_5, eq_6: Scope narrowed to the unitary basis-change operation (U^dagger)^k; state preparation, computational-basis measurement, shot statistics, and the inversion formula are excluded. Reason: Task requires a measurement-free unitary operation; the runner handles inputs and measurement.
