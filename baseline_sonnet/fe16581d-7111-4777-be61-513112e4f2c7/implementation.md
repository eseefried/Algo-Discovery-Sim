# Equation to Qiskit

Implements only the standard bit-flip query oracle O_f|x>|b> = |x>|b XOR f(x)> (eq_5) for an explicit truth table of f on n bits (1 <= n <= 11). Each input x with f(x)=1 gets a multi-controlled X onto the answer qubit, with X gates conjugating the zero-valued bits of x. The monotonicity tester itself is not reconstructed, because the abstract does not specify it.

Source equation run: `e6847447-152f-41f7-bae6-f09628080acd`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x_0 (least significant bit of query point x)
- qubit 1..n-1: x_1..x_{n-1} (for the example n=2, qubit 1 is x_1, the most significant bit)
- qubit n: b, answer qubit (index 2 in the example), receives b XOR f(x)
- computational basis: |x>|b> with x = sum_i x_i 2^i; truth_table[x] = f(x)

## Assumptions

- Little-endian encoding: bit i of the integer x is on qubit i.
- The answer qubit is the single qubit with index n, after the n input qubits.
- truth_table[x] = f(x) with entries 0 or 1 (booleans accepted).
- Multi-controlled X is built with qc.mcx without ancillas and left for the transpiler to decompose.

## Unresolved issues

- The actual monotonicity-testing algorithm is not specified in the abstract and is not implemented.
- The polylog factors hidden by the tilde in the query bound are unspecified.
- The circuit contains no tester, so eq_3 and eq_4 cannot be checked against this module.

## Equation mapping

- `eq_1`: background; no code location. Definition of monotonicity. It defines the property being tested and is not part of the oracle circuit. The oracle accepts any truth table, monotone or not.
- `eq_2`: background; no code location. Definition of epsilon-farness via normalized Hamming distance. It is not needed to build the oracle.
- `eq_3`: out_of_scope; no code location. The accept/reject guarantee belongs to the full tester, which the abstract does not specify and which is not reconstructed.
- `eq_4`: out_of_scope; no code location. The query complexity bound concerns the unspecified algorithm. The circuit contains a single oracle application and no tester.
- `eq_5`: implemented; build_circuit: loop over x with f(x)=1 applying X-conjugated multi-controlled X onto qubit n. Implements O_f|x>|b> = |x>|b xor f(x)> from an explicit truth table, as a product of multi-controlled X gates. The control pattern for each x is selected by conjugating its zero bits with X.

## Specification changes

- eq_5: The label 'Phase query oracle' conflicts with the formula, which is a bit-flip (standard XOR) oracle. The circuit implements the formula as written. A phase oracle could be obtained with b in |->. Reason: The formula is unambiguous, so it takes precedence over the label.
- eq_3, eq_4: Scope narrowed to the oracle construction only. No tester, quantum search, or amplitude amplification is implemented. Reason: The abstract gives no algorithmic details, so any tester would be fabricated.
- eq_5: The function f is supplied as an explicit truth table, with n limited to 1..11. Reason: A circuit needs a concrete f, and the 12-qubit cap leaves n+1 <= 12.
