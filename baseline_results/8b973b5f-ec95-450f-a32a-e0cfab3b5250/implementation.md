# Equation to Qiskit

Qiskit module building a palindromic reversible circuit G=(g_1,...,g_m, T, g_m,...,g_1) over the involutive gate library {X, CX, multi-controlled X}. Two instance modes: 'transposition' automatically synthesizes the conjugating half for f=(a b) (a single transposition of basis states, t(f)=1) using a Toffoli with n-1 controls as the middle gate, reproducing eq_6 for n=3, a=0, b=7; 'explicit' takes a user-supplied half gate list and middle gate and assembles the palindrome. The returned circuit is measurement-free and unitary (a permutation of basis states) and is literally equal to its own reverse gate list.

Source equation run: `c1c957e7-9405-4028-93cd-d67c2bd08553`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- lines[0] = qubit 0 = specification line 1 (least significant bit x_1)
- lines[1] = qubit 1 = specification line 2 (bit x_2)
- lines[2] = qubit 2 = specification line 3 (most significant bit x_3)
- Basis state integer x = x_1 + 2 x_2 + 4 x_3; example swaps |000> (x=0) and |111> (x=7), fixing all other states
- Example gate sequence (applied left to right): X q0, X q1, CX q2->q0, CX q2->q1, CCX (q0,q1)->q2, CX q2->q1, CX q2->q0, X q1, X q0 (9 gates, equal to its reverse)

## Assumptions

- Gate library is restricted to X, CX, CCX and multi-controlled X with positive controls; all are involutive permutation gates, so the reverse circuit computes the inverse and palindromes realize self-inverse functions.
- The 'explicit' mode trusts the user to provide a meaningful half/middle; any such input yields a valid palindrome realizing some involution conjugate to the middle gate.
- Total qubit count n is capped at 12 and validated before register allocation; mcx with up to 11 controls is left to Qiskit's standard decomposition (no ancilla lines are added).
- No extra-line or quantum-gate constructions for non-realizable involutions are implemented.

## Unresolved issues

- The paper's precise realizability theorem (eq_5 is a derived candidate) is not available, so no criterion check is implemented and the general synthesis for t(f)=2^j, j>=1, is left to explicit user input.
- Constructions with one extra circuit line or with non-permutation quantum gates for non-realizable involutions are out of scope.

## Equation mapping

- `eq_1`: background; no code location. Identification of self-inverse functions with involutions of S_{2^n} and the integer encoding of basis states; used to interpret the instance keys a, b (basis-state integers) and the qubit layout, but no code computes cycle decompositions.
- `eq_2`: implemented; build_circuit: the three loops (half, middle, reversed(half)) emit a gate list equal to its own reverse over involutive gates; comment 'eq_2 / eq_3'. The emitted gate list satisfies g_i = g_{k+1-i}; all gates are from the involutive X/CX/CCX/MCX library so the circuit realizes a self-inverse function.
- `eq_3`: implemented; build_circuit (odd-length palindrome assembly) and _synthesize_transposition (construction of the conjugating half). The circuit realizes H^{-1} o T o H with H the product of the first half; the labeling correction (H vs C) is reported in specification_changes.
- `eq_4`: implemented; _apply_toffoli (dispatch X/CX/CCX/MCX by number of controls) and _synthesize_transposition (middle gate with n-1 controls, t=1). The middle Toffoli with n-1 positive controls is a single transposition of 2^n-1 and 2^n-1-2^p, i.e. t(T_{n-1}) = 2^{n-1-(n-1)} = 1, matching t(f)=1 of the target transposition.
- `eq_5`: background; no code location. The derived cycle-type criterion is not checked in code: transposition mode only handles t(f)=1 (always realizable), and explicit mode accepts any half/middle, whose realized function automatically has the cycle type of the middle gate. No general involution-to-palindrome synthesizer is implemented.
- `eq_6`: implemented; _synthesize_transposition with the example instance n=3, a=0, b=7; target p chosen as highest differing bit so the output equals the 9-gate list of eq_6. Produces X_1, X_2, CNOT_{3->1}, CNOT_{3->2}, T_{1,2->3}, CNOT_{3->2}, CNOT_{3->1}, X_2, X_1 in Qiskit indices q0,q1,q2.

## Specification changes

- eq_3: With C = g_m o ... o g_1 (g_1 applied first) the palindrome realizes C^{-1} o g_{m+1} o C, not C o g_{m+1} o C^{-1}; the code applies the first half first, then the middle gate, then the mirrored half. The two statements agree after renaming C <-> C^{-1} and the realized function is unchanged in the example. Reason: Composition-order bookkeeping; the specification's labeling of C was inverted relative to its definition.
- eq_5, eq_6: Scope narrowed: automatic synthesis is implemented only for single transpositions f=(a b) (t(f)=1, middle gate with n-1 controls). Involutions with t(f)=2^j, j>=1, are supported only through the 'explicit' mode where the user supplies the half gate list and middle gate; no realizability test of the eq_5 criterion is performed. Reason: A general conjugator-synthesis algorithm (finding and decomposing C for arbitrary cycle type) is not specified by the abstract and would exceed the compact-module scope.
- eq_6: Target line for the middle gate is fixed as the highest bit in which a and b differ, and the conjugating half is an X layer followed by CNOTs from the target into the other differing bits (X layer chosen so the images of a and b have all non-target bits equal to 1). Reason: Makes the construction deterministic for all n and all a != b while reproducing the exact gate order of eq_6 for the n=3 example.
- eq_1: Instance gate dicts and the states a, b use 0-based Qiskit qubit indices (qubit q = specification line q+1, little-endian). Reason: Alignment with Qiskit's physical qubit ordering; disclosed to avoid index-order confusion.
