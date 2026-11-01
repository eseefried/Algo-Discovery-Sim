# Equation to Qiskit

build_circuit(instance) takes a small explicit unitary U on n=1..4 qubits and returns W = Q^T P^T C_U' P Q as an ancilla-free, measurement-free circuit. Q is an XOR-mask basis permutation (X gates). P is a product of basis transpositions found by a greedy search that minimizes a nonzero-off-diagonal-count proxy plus a permutation cost. U' = (PQ)U(PQ)^T is compiled exactly by a two-level (Givens) decomposition into Gray-code-style CX conjugations, multi-controlled U gates and multi-controlled phases. The permutations are compiled to X, CX and multi-controlled X gates. No input state is prepared and nothing is measured.

Source equation run: `48509c7f-b9f8-4fd7-9474-575a9980bb4a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0..n-1]: system qubits, little-endian (qubit j holds bit j of basis index k = sum_j b_j 2^j)
- Example n=2: q[0] = least significant bit, q[1] = most significant bit
- No ancilla qubits; no classical bits

## Assumptions

- The instance supplies U explicitly and it is unitary to within 1e-8.
- Little-endian basis index convention: qubit j holds bit j of the basis index.
- Qiskit controlled-UGate and mcp implement the intended controlled operations, including the separately applied controlled global phase of each 2x2 block.
- The cost proxy counts off-diagonal entries with magnitude above 1e-9, and the Givens elimination skips entries below 1e-12.
- P = Q = I is possible (no swaps and a zero mask) when the greedy search finds no improvement.

## Unresolved issues

- The exact OptQC search algorithm and cost function remain unknown, so the permutations found may differ from the paper's.
- The Qcompiler decomposition is replaced by a generic Givens decomposition whose gate count is not optimized.
- The precise meaning of 'equivalent up to a permutation' and 'components considered separately' beyond the similarity form is not modeled.
- Cost grows quickly with n, so only n<=4 is allowed, and no numerical verification has been performed at generation time.

## Equation mapping

- `eq_1`: implemented; build_circuit (assembly Q^T P^T C_U' P Q). The circuit is the factorization U = Q^T P^T U' P Q, with Q, P and U' obtained from _search and compiled exactly.
- `eq_2`: implemented; _search (the returned matrix up = U'). U' = (PQ) U (PQ)^T is computed by successive basis-permutation conjugations: first the Q XOR mask, then the P transpositions.
- `eq_3`: implemented; _cost and _search. A greedy heuristic, not an exact argmin: the entry-count proxy plus a permutation cost (popcount of the XOR mask, 1 per transposition). Q is searched over XOR masks and P over transpositions.
- `eq_4`: implemented; build_circuit (gate ordering) and _decompose/_emit/_diag (C_U'). Time order is Q, P (T_1..T_s), C_U', P^T (T_s..T_1), Q^T. C_U' is an exact two-level decomposition: the diagonal first, then G_m^dag ... G_1^dag.
- `eq_5`: background; no code location. The |0...0> input is prepared by the runner, and the global-phase comparison with U is a validation criterion. The circuit itself is a bare operation with no state preparation. The little-endian convention is used in all index arithmetic.

## Specification changes

- eq_3: Q is restricted to XOR-mask permutations k -> k XOR m (cost popcount(m)). P is a sequence of basis transpositions found greedily, each costing 1, and a swap is accepted only if the entry count drops by at least 2. The search is not an exact minimization. Reason: The abstract gives no explicit search or cost. A cheap, well-defined heuristic stands in for OptQC.
- eq_4, eq_1: U' is compiled by a two-level Givens decomposition with multi-controlled U/phase gates instead of the Qcompiler decomposition. Reason: The Qcompiler internals are unspecified and the circuit must use only standard gates, with no opaque dense unitary.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to n in 1..4 qubits with an explicit unitary supplied as instance fields n, unitary_real and optional unitary_imag. No gate-count savings are claimed. MPI parallelism and the 'each matrix component separately' idea are not implemented. Reason: The dense classical processing grows as 4^n and the specification only requires tiny instances.
- eq_5: The initial state |0...0> is not prepared and no measurement is performed. Reason: The task requires an operation only. The runner prepares inputs and compares the unitary or statevector with U up to global phase.
