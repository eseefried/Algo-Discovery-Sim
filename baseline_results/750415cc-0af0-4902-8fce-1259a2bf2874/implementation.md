# Equation to Qiskit

Implements the ternary SWAP gate synthesis of eq_6 (three TCX gates plus one one-qutrit negation F_3^2) on qubit-encoded qutrits. Each qutrit is encoded in two qubits (value j = q_low + 2*q_high, |11> unused but mapped to itself so every gate is a permutation and the circuit is unitary). X_3 and X_3^2 (eq_1) are built as products of two transpositions realised by X-conjugated CX/CCX gates; TCX^k (eq_2) is realised as C_{c_low}(X_3^k) C_{c_high}(X_3^{2k}); the negation is a qubit SWAP inside the qutrit. Instance parameters: num_pairs (1-3 independent qutrit pairs swapped in parallel, 4 qubits each, max 12) and variant ('A' = eq_6 as written, 'B' = the mirror synthesis TCX^{-1}, TCX, TCX^{-1} with negation on the second qutrit).

Source equation run: `2b020afc-0567-40d7-a727-e607d61924f2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Total qubits for the example: 4 (num_pairs=1); qubit 0 is the least significant bit of the Qiskit computational basis.
- Qutrit q_1 (specification's first qutrit, control of TCX_{1->2}, left ket in |a>|b>): qubits 0 (low bit) and 1 (high bit); value a = q0 + 2*q1 with a in {0,1,2}; |q1 q0> = |11> is an unused (invalid) code word mapped to itself.
- Qutrit q_2 (specification's second qutrit, right ket in |a>|b>): qubits 2 (low bit) and 3 (high bit); value b = q2 + 2*q3.
- Example input |a>|b> = |1>|2> corresponds to qubits (q3 q2 q1 q0) = (1 0 0 1), i.e. basis index 9; expected output |2>|1> is (q3 q2 q1 q0) = (0 1 1 0), basis index 6.
- For num_pairs = k, pair p (0-based) uses qubits 4p,4p+1 (qutrit 1) and 4p+2,4p+3 (qutrit 2); pairs are swapped independently and in parallel.

## Assumptions

- TCX follows the generalized SUM convention |a>|b> -> |a>|b+a mod 3> (eq_2); the paper's actual TCX definition may differ (e.g. control condition on a specific state), which would change the synthesis circuit.
- Input states prepared by the runner are expected to lie in the valid code space (each qutrit in {|00>,|01>,|10>}); behaviour on |11> code words is the identity extension and carries no physical meaning.
- The negation gate F_3^2 is treated as an available one-qutrit gate, consistent with the abstract's assumption of arbitrary one-qutrit gates.
- Qubit index 0 is the least significant bit; within each qutrit the lower-indexed qubit is the low bit of the ternary value.

## Unresolved issues

- The paper's exact TCX/TCZ definitions and its actual ternary SWAP circuit are not recoverable from the abstract; the implemented decomposition is a valid one under the stated convention but may not be the paper's.
- No synthesis of the one-qutrit Fourier gate F_3 (needed for eq_4 or a TCZ-based variant) is provided.

## Equation mapping

- `eq_1`: implemented; _controlled_shift (with _transposition_01 / _transposition_02): X_3 and X_3^2 as 3-cycles on the encoded qutrit; Z_3 and the commutation relation are not needed for the SWAP synthesis. The qutrit cyclic shift X_3 is realised as the permutation (0 2)(0 1) on the two-qubit code space using X-conjugated CX/CCX gates; its square is the reversed product. The code word |11> is left fixed so the extension to 4 dimensions is a permutation (unitary).
- `eq_2`: implemented; _tcx. TCX^power (power 1 = TCX, power 2 = TCX^{-1}) is implemented as C_{c_low}(X_3^power) C_{c_high}(X_3^{2 power mod 3}), which applies X_3^{power*a} to the target for control value a = c_low + 2 c_high in {0,1,2}.
- `eq_3`: background; no code location. The TCZ definition is context only; the chosen construction (ternary SWAP, eq_6) uses TCX gates exclusively.
- `eq_4`: out_of_scope; no code location. Replacing TCX by F_3-conjugated TCZ would require synthesising the one-qutrit Fourier gate F_3 inside the two-qubit code space from standard gates, which is not done here; eq_4 is a relation between gates, not part of the implemented operation.
- `eq_5`: background; no code location. The Cartan KAK structure of a general one-qutrit gate is structural background; the only one-qutrit gate used (F_3^2 negation) is implemented directly as a qubit SWAP.
- `eq_6`: implemented; build_circuit (variant 'A' branch) together with _negation. The circuit applies, in time order, TCX_{1->2}, TCX_{2->1}^{-1}, TCX_{1->2}, then F_3^2 on qutrit 1, exactly the right-to-left product of eq_6, mapping |a>|b> -> |b>|a> on valid code words.

## Specification changes

- eq_1, eq_2, eq_6: Qutrits are encoded in two qubits each (j = q_low + 2 q_high), and every qutrit operation is extended to the unused code word |11> as the identity (for X_3, X_3^2, F_3^2) and as X_3^{3k} = I for an invalid control value 3, so all gates are permutations of the 4-qubit basis. Reason: Qiskit provides only qubits; a unitary extension to the full 2^n-dimensional space is required and the identity extension keeps the construction a pure permutation circuit built from X, CX, CCX and SWAP.
- eq_2, eq_6: TCX_{2->1}^{-1} is implemented directly as a single controlled X_3^2 (power=2) rather than as two sequential TCX gates. Reason: TCX^{-1} = TCX^2 (eq_2) and the controlled 3-cycle X_3^2 is just the reversed transposition product, so this is exactly equal and shorter.
- eq_6: An optional mirror variant 'B' is offered: SWAP_3 = (I x F_3^2) TCX_{1->2}^{-1} TCX_{2->1} TCX_{1->2}^{-1}; variant 'A' is eq_6 as written and is the example instance. Reason: Provides a second valid instance parameter family while preserving the meaning (|a>|b> -> |b>|a>): |a,b> -> |a,b-a> -> |b,b-a> -> |b,-a> -> |b,a>.
- eq_3, eq_4: The TCZ-based realisation of the elementary gate (TCZ conjugated by F_3) is not implemented; only the TCX path is used. Reason: Scope narrowed to the single smallest construction (ternary SWAP from TCX); synthesising F_3 on the encoded qutrit from standard gates is outside this scope.
