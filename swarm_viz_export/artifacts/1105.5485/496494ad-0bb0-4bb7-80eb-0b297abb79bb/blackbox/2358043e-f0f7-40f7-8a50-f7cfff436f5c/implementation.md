# Equation to Qiskit

Builds a 4-qubit circuit for two qutrits, each encoded in 2 qubits (level j is the binary integer j, level 3 untouched). The 'gate' field selects CZ3 (diagonal phases omega^(ab)), CX3 (controlled shift |a,b> -> |a,b+a mod 3>) or SWAP3. SWAP3 is three controlled shifts plus a one-qutrit negation that corrects the trace error in eq_5. The Fourier gate F is not synthesized, so CX3 is built directly as a controlled cyclic permutation using only X, CX and multi-controlled X and phase gates.

Source equation run: `ca44b316-4539-459e-a251-cb85bf6fadf3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: qutrit A low bit (level j = q0 + 2*q1)
- qubit 1: qutrit A high bit
- qubit 2: qutrit B low bit (level j = q2 + 2*q3)
- qubit 3: qutrit B high bit
- Level 3 (binary 11) of each qutrit is left unchanged by all gates; valid inputs are the 9 states |a,b> with a,b in {0,1,2}

## Assumptions

- Qutrit level j is encoded as the binary integer j with the lower qubit index as the least significant bit.
- The gates act as the identity on level 3 of each qutrit.
- The inputs prepared by the runner lie in the 9-dimensional qutrit subspace.
- The 'swap3' gate ignores the 'inverse' flag because it is self-inverse.

## Unresolved issues

- The Fourier gate F and the Cartan-derived one-qutrit gates are not implemented.
- The sign convention of F X F^dagger is not resolved because F is unused.
- Toffoli, Muthukrishnan-Stroud and qudit generalizations are not covered.
- The circuit has not been simulated or verified; verification is left to the software stage.

## Equation mapping

- `eq_1`: background; _shift (X action only). Definitions of F, X and Z. Only the shift X appears, as the permutation inside _shift. F and Z are not built as gates.
- `eq_2`: out_of_scope; no code location. The F conjugation identity is not used because F is not synthesized. By hand, X F = F Z^{-1} for the F defined in eq_1, so the sign in the sketch is likely Z^{-1}; this is not verified.
- `eq_3`: implemented; _cz3. Diagonal phases omega^(ab) on |a,b> for a,b in {0,1,2}, each applied as a multi-controlled phase gate, with identity on level 3.
- `eq_4`: implemented; _cx3 and _shift. CX3 |a,b> -> |a,b+a mod 3> is implemented as a controlled cyclic permutation of the target levels using X, CX and multi-controlled X gates. This differs from the (I x F^dagger) CZ3 (I x F) route.
- `eq_5`: implemented; build_circuit (gate == 'swap3' branch). Sequence CX3(a->b), CX3^{-1}(b->a), CX3(a->b) followed by the negation |j> -> |-j> on qutrit A, implemented by swapping qubits 0 and 1, gives the exact swap |a,b> -> |b,a>.

## Specification changes

- eq_4, eq_2: CX3 is built directly as a controlled cyclic permutation instead of F-conjugation of CZ3 on the target. Reason: A qutrit Fourier gate embedded in two qubits needs a dense unitary or a nontrivial exact decomposition, and opaque dense unitaries are disallowed. The F/F^dagger ordering and sign question is therefore not exercised.
- eq_5: A final one-qutrit negation (swap of levels 1 and 2 on qutrit A) is appended to the three controlled shifts. Reason: Tracing (a,b) -> (a,a+b) -> (-b,a+b) -> (-b,a) shows the three shifts alone give (-b,a), not (b,a).
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to three selectable two-qutrit gates (CZ3, CX3, SWAP3) on 4 qubits. An optional inverse flag is added for CZ3 and CX3, and CX3 may be controlled from either qutrit. Reason: Implements one explicitly scoped construction with parameters that can vary.
