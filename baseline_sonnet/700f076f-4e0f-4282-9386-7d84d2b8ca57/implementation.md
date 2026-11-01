# Equation to Qiskit

Qiskit operation for the Grover iterate G=(2|s><s|-I)O_w applied k times on an n-qubit index register (N=2^n, single marked index w), with k=floor(pi/(4 asin(1/sqrt(guessed N)))) taken from a possibly wrong guessed database size. Uniform-superposition preparation is left to the runner. The default example uses N=4, w=3, guess 4, giving k=1.

Source equation run: `b51d67f7-96ac-40cf-891f-04390ae2f51e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: index register 'index'; computational basis |x>, x = sum_i b_i 2^i with qubit 0 least significant
- Example (n=2): q0 = LSB, q1 = MSB of the database index; marked w=3 is |11>
- No ancilla qubits; total qubits = n <= 12

## Assumptions

- Single marked item with index given directly as 'marked'.
- True database size is N=2^n; the guessed size only determines the iteration count.
- The runner prepares the uniform superposition (or any chosen input) before this operation.
- The global phase of the diffusion is corrected so that each iterate equals (2|s><s|-I)O_w exactly.

## Unresolved issues

- Paper-specific quantum database encoding and programmable query construction are unspecified.
- Unambiguous discrimination of Grover states for unknown N is not implemented.
- The floor rounding choice in eq_4 is an assumption, not taken from the paper.

## Equation mapping

- `eq_1`: implemented; _oracle. Phase oracle I-2|w><w| via X conjugation on zero bits of w and a multi-controlled Z.
- `eq_2`: implemented; _diffusion and build_circuit loop. Inversion about the mean 2|s><s|-I built from H, X, multi-controlled Z, with a global phase of pi to fix the sign; applied after the oracle each iteration. The initial |s> preparation is not included in the operation.
- `eq_3`: background; no code location. Analytic description of the rotation state after k iterations; not coded. It serves as the expected behaviour of the circuit.
- `eq_4`: implemented; _iterations. Iteration count computed from the guessed size guess_N with the floor formula.
- `eq_5`: background; no code location. Success probability is a measurement-level analytic quantity; the circuit contains no measurement and does not compute it.

## Specification changes

- eq_2: The operation is the Grover iterations G^k only; the Hadamard layer preparing |s> from |0...0> is not included. Reason: The operation must not prepare the input state; the runner supplies the input, e.g. the uniform superposition.
- eq_1, eq_2: Index bit ordering follows Qiskit little endian (qubit 0 least significant) instead of the spec's 'first qubit most significant'. Reason: Consistency with the required Qiskit convention; the phase oracle is a diagonal operation defined on the integer w.
- eq_2, eq_3: The scope is generalized from fixed N=4 to N=2^n with n up to 12, with N=4 as the example. Reason: Operation must work for varying valid parameters; the N=4 case is the n=2 instance.
- eq_4: A tolerance of 1e-12 is added before the floor, and guess_N is restricted to integers in 2..4096. Reason: Guards against floating-point error at exact integer values; bounds circuit depth. guess_N need not be a power of two since it only sets k.
- eq_1, eq_2, eq_3, eq_4, eq_5: The paper's quantum phone-book database, programmable name/number query, and unambiguous state discrimination analysis are not implemented; the query is reduced to a marked index. Reason: These details are not specified in the abstract or specification.
