# Equation to Qiskit

Builds the conjugation structure U = Q^T P^T U' P Q from eq_1 as an n-qubit unitary circuit. P and Q are basis-state permutations given as ordered lists of transpositions, each implemented with CX networks and a multi-controlled X. U' is narrowed to a diagonal unitary with user-supplied phases, implemented with X-conjugated multi-controlled phase gates. Circuit order is Q, P, U', P^T, Q^T. The classical search for P and Q (eq_2) is not implemented.

Source equation run: `cf8984ed-f7d8-47ae-91f2-20c7cb72b710`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form register q; qubit 0 is the least significant bit of the computational-basis index.
- Basis state |x> has x = sum_j b_j 2^j with b_j the state of qubit j.
- No ancilla qubits; total qubits = n <= 6.

## Assumptions

- Permutation matrices act as P|x> = |p(x)>, with P a product of transpositions applied in listed order; P^T is the reverse order.
- Gate sets use standard gates only (X, CX, MCX, P, MCP) without optimization.
- Qubit index 0 is the least significant bit.
- n is capped at 6 to keep the 2^n multi-controlled-phase gate count small.

## Unresolved issues

- Gate-count optimization and the choice of P and Q are not implemented.
- General (non-diagonal) U' compilation as in Qcompiler is not implemented.
- MPI parallelization is not represented.

## Equation mapping

- `eq_1`: implemented; build_circuit (with _apply_perm and _diagonal): applies Q, P, U', P^T, Q^T in that order. The conjugation U = Q^T P^T U' P Q is built with P and Q as ordered products of basis-state transpositions. Transposes are the reversed transposition sequences. U' is narrowed to a diagonal unitary.
- `eq_2`: out_of_scope; no code location. This is a classical optimization objective (gate-count minimization over P and Q). It is not a quantum operation, and the search and MPI details are unspecified, so the circuit takes P and Q as inputs.

## Specification changes

- eq_1: U' is restricted to a diagonal unitary with user-supplied phases. P and Q are restricted to products of basis-state transpositions supplied in the instance. The target U is defined by the factorization and is not given as an input matrix. Reason: A general dense U' cannot be implemented without an opaque dense unitary or an unspecified Qcompiler decomposition, and the abstract does not give the decomposition.
- eq_2: The gate-count minimization search is not implemented. P and Q are inputs rather than outputs of an optimizer. Reason: The search algorithm and cost function are not specified, and the search is classical rather than a circuit operation.
