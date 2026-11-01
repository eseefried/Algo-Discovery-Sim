# Equation to Qiskit

Builds the Grover amplitude-amplification operator around a one-sided monotonicity edge checker for a small Boolean function f on n in {2,3} bits. The checker is U_check: Hadamards on x and edge-direction i, then f is queried at x with bit i forced to 0 and to 1 through XOR-oracle ancillas, flag F is set to f(lo) AND NOT f(hi), and the queries are uncomputed. The circuit then applies k iterations of Q = -U S_0 U^dagger S_flag. No input preparation or measurement is included.

Source equation run: `596f02ef-5389-4931-96d1-1e3e127f0f11`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: X register (input x, qubit j = bit j, little-endian); n=3 -> qubits 0,1,2
- Qubits n..n+m-1: I register (edge direction i, m=ceil(log2 n), little-endian); n=3 -> qubits 3,4
- Qubits n+m..2n+m-1: Y work register (copy of x with bit i forced to 0/1, returned to |0>); n=3 -> qubits 5,6,7
- Qubits 2n+m, 2n+m+1: A ancillas holding f(lo), f(hi), returned to |0>; n=3 -> qubits 8,9
- Qubit 2n+m+2: F flag holding v(x,i); n=3 -> qubit 10
- Truth table index y = sum_j y_j 2^j; the circuit takes no prepared inputs and the runner supplies |0...0> with U_check applied as the first operation

## Assumptions

- The circuit applies U_check to the all-zero input as its first operation, so the runner should supply |0...0>.
- truth_table has 2^n entries in {0,1} indexed by sum_j y_j 2^j.
- Qubits are little-endian and bit j of x is X qubit j.
- S_0 reflects about |0...0> over all qubits, which is valid because the Y and A work registers are returned to |0> by U_check.
- The mcx gates are decomposed by Qiskit without extra ancillas, so there are no extra qubits beyond the stated layout.

## Unresolved issues

- The actual algorithm of the paper (the n^{1/4} eps^{-1/2} polylog tester, path/line tester, and handling of unknown eps) is not reconstructed.
- Only a tiny edge-tester amplification model is implemented, with n limited to 2 or 3.
- The query count is not asymptotically meaningful at this size.

## Equation mapping

- `eq_1`: implemented; _checker (calls _force, _oracle, then mcx on [a0,a1] -> F with ctrl_state=1). The flag is computed as f(x^{i->0}) AND NOT f(x^{i->1}), using the XOR oracle at both forced endpoints. The ancillas are then uncomputed.
- `eq_2`: implemented; _checker and the initial qc.compose(u) in build_circuit. H on X and I, then the flag computation with all junk uncomputed. For n=3 the I register has an unused value 3, for which no forcing occurs so f(lo)=f(hi) and v=0 automatically. This matches the spec's convention that padded indices are non-violating.
- `eq_3`: implemented; build_circuit loop: z(F), U^dagger, reflection about |0..0>, U, global phase pi. Each iteration applies Q = -U S_0 U^dagger S_flag. The iteration count k is supplied in the instance; the sin^2((2k+1)theta) formula is not evaluated in the code.
- `eq_4`: background; no code location. The edge-density lower bound p >= eps/sqrt(n) comes from external analyses, and the complexity bound is not encoded in the circuit. k is simply an input.
- `eq_5`: out_of_scope; no code location. Measurement, classical recheck of the returned edge, and the decision rule are post-processing and are excluded from the operation.

## Specification changes

- eq_2: Restricted to n in {2,3}. The total qubit count is 2n+ceil(log2 n)+3, which must be <= 12, so n=4 (13 qubits) is rejected with ValueError. Reason: The 12-qubit cap combined with the work-register design.
- eq_1, eq_2: Work registers are a Y register of n qubits plus 2 ancillas A. The endpoints are processed sequentially, reusing Y, instead of the 'about 2 to 4' work qubits in the spec. The oracle f is realised as a truth-table XOR oracle (one multi-controlled X per f=1 input), supplied via instance['truth_table']. Reason: A concrete standard-gate implementation of the placeholder oracle is needed, and the specified work qubits cannot hold a forced copy of x.
- eq_2, eq_3: For n=3 the success probability is p = (#violated (x,i) pairs)/(4*2^n), i.e. rescaled by n/4 from the spec's n*2^n normalisation. For n=2 the index is uniform with no padding. Reason: The I register spans 2^m values, so padded index values dilute the amplitude. These padded values are non-violating.
- eq_3, eq_4: k is a user-given instance parameter (0..16) rather than derived from eps or p. Reason: The abstract gives no concrete rule, and the circuit is an operation with fixed gate count.
- eq_5: Measurement and classical verification are removed from the circuit. Reason: The task requires a measurement-free unitary operation.
- eq_3: Global phase of pi per Grover iteration is added to represent the leading minus sign in Q. Reason: This reproduces Q = -U S_0 U^dagger S_flag exactly. It is physically irrelevant.
