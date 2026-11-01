# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Decompose a general bipartite unitary on C^{d_A} ⊗ C^{d_B} into a product of controlled unitaries (controlled from A, targeting B), with the gate-count bounds stated in the abstract. Only the counting bounds are explicit; the construction itself is not in the abstract.

Scope: Scope: the bipartite controlled-unitary decomposition form and its stated gate-count bounds, plus the tiny instance d_A=2, d_B=2. Outside scope: the explicit decomposition construction, the complex permutation result with three controlled unitaries, the n-partite bound proof, the local-unitary plus simple-gate decomposition, the CNOT/entanglement cost bounds via Schmidt rank, and the log-rank / nonnegative rank connection.

## Symbols

- $d_A$: dimension of the control system A; domain: integer >= 2
- $d_B$: dimension of the target system B; domain: integer >= 1
- $U$: target bipartite unitary; domain: U(d_A d_B)
- $CU_k$: k-th controlled unitary, block diagonal in a fixed A basis; domain: U(d_A d_B)
- $V_{k,i}$: unitary on B applied when A is in basis state i in the k-th gate; domain: U(d_B)
- $N$: number of controlled unitaries in the decomposition; domain: positive integer

## eq_1: Controlled unitary form

$$
CU_k=\sum_{i=0}^{d_A-1}|i\rangle\langle i|_A\otimes V_{k,i}
$$

General form of a controlled unitary with control A and target B, in a fixed computational basis of A.

Provenance: `standard_background`. Standard definition of a controlled unitary; the abstract does not give its explicit form.

Equation assumptions:

- The control basis is the computational basis of A.
- Controlled unitaries are controlled from A onto B.

## eq_2: Decomposition form

$$
U=\prod_{k=1}^{N}CU_k
$$

Any bipartite unitary is a product of N controlled unitaries.

Provenance: `abstract_inferred`. Inferred from the claim of a product of controlled unitaries. The control direction may alternate between A and B in the actual method; this is not stated.

Abstract evidence: any unitary operator on the $d_{A}\times d_{B}$ system ($d_{A}\geq 2$) can be decomposed into the product of at most $4d_{A}-5$ controlled unitary operators

Equation assumptions:

- Which system controls each factor is not specified in the abstract.

## eq_3: General bound

$$
N\le 4d_A-5
$$

Upper bound on the number of controlled unitaries for general d_A.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: at most $4d_{A}-5$ controlled unitary operators

## eq_4: Power-of-two bound

$$
N\le 2d_A-1\quad\text{if } d_A=2^m
$$

Reduced bound when d_A is a power of two.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: The number can be reduced to $2d_{A}-1$ when $d_{A}$ is a power of two

Equation assumptions:

- The bound is read as an upper bound, consistent with the preceding 'at most'.

## eq_5: n-partite bound

$$
N\le 2\prod_{j=1}^{n-1}(2d_j-2)-1
$$

Bound for n-partite unitaries, each gate controlled from n-1 systems.

Provenance: `abstract_explicit`. Stated in the abstract; listed for context only and outside the construction scope.

Abstract evidence: $[2\prod^{n-1}_{j=1}(2d_{j}-2)-1]$ controlled unitary gates

## Registers

- A: d_A (tiny instance: 2, one qubit) qubits; control system
- B: d_B (tiny instance: 2, one qubit) qubits; target system

## Algorithm steps

1. Fix the computational bases of A and B and the target unitary U on C^{d_A} ⊗ C^{d_B}. (no equation reference)
2. Write the decomposition as a product of N controlled unitaries of the form in eq_1, with N within the bounds of eq_3 or eq_4. For d_A=2 the bound is N<=3 (=2d_A-1). (eq_1, eq_2, eq_3, eq_4)
3. The explicit choice of the V_{k,i} and the control direction of each factor is not derivable from the abstract and must come from the paper. (no equation reference)

## Assumptions

- Tiny instance d_A=d_B=2 chosen by me as the smallest useful case.
- Controlled unitaries are taken to be block diagonal in a computational basis of the control system.
- The decomposition is treated as an exact operator identity.

## Missing information

- Explicit construction of the controlled unitaries V_{k,i} for a given U
- Which system controls each factor and the ordering of factors
- Details of the complex permutation, local-unitary and CNOT/entanglement cost results
- Definitions of the Schmidt-rank cost bounds and the nonnegative rank link
