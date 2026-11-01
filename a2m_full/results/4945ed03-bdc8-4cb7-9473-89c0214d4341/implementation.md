# Equation to Qiskit

Narrowed construction: compiles a product of 1-/2-level matrices E_(j,l) on n<=2 data qubits. Each factor is built as P^dagger C(W) P with a CX Gray-code permutation, X-conjugations for control and target polarity, and a user-supplied single-qubit word W over {h,s,sdg,t,tdg,x,z,w}. The classical Giles-Selinger column reduction over Z[omega] is not implemented. The controlled W gates are standard Qiskit gates (ch, cs, csdg, cp), not exact Clifford+T circuits.

Source equation run: `6fd198b0-0f04-4722-9ad8-653ccca740e9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = q0 (least significant bit of basis index)
- qubit 1 = q1 (basis index = 2*q1 + q0)
- no ancilla qubit is used (total qubits = n <= 2)

## Assumptions

- Word gates are listed in time order, so W = G_last ... G_first.
- Little-endian basis index: index = 2*q1 + q0.
- Identity is applied outside the two selected basis states.
- For n=2 and a pair differing in both bits, CX(0->1) makes the indices adjacent (they differ only in bit 0 afterwards).

## Unresolved issues

- Column reduction over Z[omega] to derive factors from a given U is not implemented.
- Controlled gates are not exact Clifford+T and no ancilla construction is provided.
- The O(k) bound and the factor-count bounds are not addressed.

## Equation mapping

- `eq_1`: background; no code location. Ring form of entries is context; the code takes the single-qubit words directly and does no ring arithmetic.
- `eq_2`: implemented; build_circuit: loop over factors, applying _two_level in time order. Realizes the product E_m...E_1 from a supplied list of 1-/2-level factors. The classical column reduction that finds the factors for a given U is not implemented.
- `eq_3`: out_of_scope; no code location. The O(k) gate-count bound is an asymptotic claim and is not constructed or checked.
- `eq_4`: out_of_scope; no code location. The sde-reduction case analysis was not specified in the abstract and is not implemented.
- `eq_5`: implemented; _two_level and _apply_word. Implements E_(j,l)=P^dag C(W) P with a CX Gray-code permutation P for index pairs differing in both bits, X conjugations for control and target polarity, and a controlled single-qubit word W.

## Specification changes

- eq_2, eq_4: Scope narrowed to compiling user-supplied two-level factors. The Z[omega] column reduction that derives the factors from U is not implemented. Reason: The reduction rules (residue case analysis) are not given in the abstract and cannot be fixed from the specification.
- eq_5: Controlled W is built from standard Qiskit gates (ch, cs, csdg, cp(+-pi/4), cx, cz), not exact Clifford+T. The 'w' symbol is a global phase for n=1 and a controlled phase p(pi/4) on the control for n=2. Reason: Exact controlled-W Clifford+T circuits (possibly with an ancilla) are unspecified. Standard controlled gates preserve the operator meaning.
- eq_3: No ancilla is used and no gate-count bound is enforced. Reason: The ancilla scheme and the constants are unspecified.
- eq_5: In the pair (j,l), index 0 of W corresponds to |j> and index 1 to |l>. For n=1 only the pair as given is used, with W on qubit 0. Reason: The orientation convention was not specified.
