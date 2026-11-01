# Equation to Qiskit

Builds an n-line reversible circuit from an explicit gate list over self-inverse gates (X, CX, CCX), and accepts it only if the gate sequence is palindromic (C = C^R, eq_2). The resulting circuit is therefore its own reverse and implements an involution. The paper's characterization theorem, extra-line construction and quantum-gate construction are not implemented.

Source equation run: `dc0172a9-6667-4629-bf34-7b9d311656ec`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: register x, data lines; basis index = sum_i x_i 2^i, qubit 0 is least significant bit
- no ancilla lines are used (n=2 in the example: qubits 0,1)

## Assumptions

- Gate library is {X, CX, CCX}, each self-inverse
- Equality in eq_2 is of gate sequences, not just of realized functions
- Qubit i holds bit i of x (little-endian, matching Qiskit)
- The extra-line and quantum-gate constructions are out of scope

## Unresolved issues

- Exact criterion for which involutions admit palindromic circuits is not given
- Extra-line palindromic construction is not implemented
- Quantum-gate palindromic construction is not implemented
- The paper's gate library is unknown

## Equation mapping

- `eq_1`: background; no code location. Defines involutions f∘f=id; the circuit's realized function is one when the circuit is palindromic, but no code checks or constructs permutations.
- `eq_2`: implemented; build_circuit: palindrome check `norm != norm[::-1]` raising ValueError, with gates canonicalized by _normalize_gate. Gate-sequence equality C=C^R is enforced on the input gate list; only palindromic sequences are emitted as circuits.
- `eq_3`: background; no code location. Reverse circuit equals inverse for self-inverse gates; this holds by the choice of X, CX, CCX gates and is not separately coded.
- `eq_4`: background; no code location. Consequence (palindromic implies involution) of eq_2 and eq_3; it is a property of the output circuit, not an operation, and the converse is not reconstructed.

## Specification changes

- eq_2: Scope narrowed to a validator-plus-builder: user supplies the gate list and the module verifies it is palindromic, rather than synthesizing a palindromic circuit for a given involution. Reason: The abstract gives no synthesis criterion or algorithm for which involutions are palindromically realizable.
- eq_1, eq_3, eq_4: Treated as background; no permutation-level analysis is implemented. Reason: The missing characterization theorem and the requirement for a unitary circuit operation without simulation or dense operators.
- eq_2: Gate library fixed to X, CX, CCX; Toffoli controls are treated as unordered when testing equality. Reason: The paper's gate library is not specified; these are standard self-inverse reversible gates.
