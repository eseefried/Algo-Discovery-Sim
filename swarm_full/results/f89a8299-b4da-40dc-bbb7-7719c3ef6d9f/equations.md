# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize how many controlled unitaries are needed to decompose an arbitrary bipartite (d_A x d_B) or n-partite unitary, and bound CNOT or entanglement cost of bipartite permutation unitaries in terms of Schmidt rank, including a link to the log-rank conjecture via nonnegative rank.

Scope: Abstract-level statement of decomposition bounds only; no explicit circuits, constructions, or proofs are reconstructed. Equations capture only the stated counting bounds on controlled unitaries.

## Symbols

- $d_A$: Dimension of subsystem A (controlling system); domain: integer >= 2
- $d_B$: Dimension of subsystem B; domain: positive integer
- $d_j$: Dimension of j-th subsystem in n-partite space; domain: positive integers
- $N_{CU}$: Number of controlled unitaries in the decomposition; domain: nonnegative integer

## eq_1: Bipartite bound

$$
N_{CU}\le 4d_A-5
$$

Any unitary on d_A x d_B is a product of at most 4d_A-5 controlled unitaries.

Provenance: `abstract_inferred`. Stated in the abstract.

Abstract evidence: at most $4d_{A}-5$ controlled unitary operators

## eq_2: Power-of-two bound

$$
N_{CU}\le 2d_A-1\quad (d_A=2^k)
$$

Reduced count when d_A is a power of two.

Provenance: `abstract_inferred`. Stated in the abstract.

Abstract evidence: The number can be reduced to $2d_{A}-1$ when $d_{A}$ is a power of two

## eq_3: n-partite bound

$$
N_{CU}\le 2\prod_{j=1}^{n-1}(2d_j-2)-1
$$

Bound for n-partite unitaries, each gate controlled from n-1 systems.

Provenance: `abstract_inferred`. Stated in the abstract.

Abstract evidence: $[2\prod^{n-1}_{j=1}(2d_{j}-2)-1]$ controlled unitary gates

## Registers

- A: d_A (dimension) qubits; Control system of the controlled unitaries
- B: d_B (dimension) qubits; Target system acted on by the controlled unitaries

## Initial state

Arbitrary input state on A and B; the decomposition is operator-level and does not fix a state.

## Measurement

None prescribed: the result is an operator-level decomposition. Any verification would compare the product of controlled unitaries with the target U, for example via process fidelity or by checking action on a basis, but the abstract gives no measurement.

## Classical postprocessing

None given in the abstract. Classical computation would be needed to find the controlled-unitary factors, but the method is not stated.

## Algorithm steps

1. Take an arbitrary target unitary U on A⊗B. (no equation reference)
2. Write U as a product of at most 4d_A-5 controlled unitaries, controlled on A and acting on B (alternating control roles may be used; the exact construction is not given in the abstract). (eq_1)
3. If d_A is a power of two, the product length reduces to at most 2d_A-1. (eq_2)
4. For n parties, use at most the stated number of gates, each controlled from n-1 systems. (eq_3)

## Assumptions

- Bounds are treated as upper bounds on gate count, not constructions.
- Circuit plan is a schematic of the counting statement, not the paper's actual construction.
- Control system is A and target B in the bipartite plan.
- Measurement and postprocessing are not part of the abstract's results.

## Missing information

- Explicit decomposition construction
- Exact CNOT/entanglement cost bounds as functions of Schmidt rank
- Which system controls in each gate
- Order and control roles of individual controlled unitaries are unspecified
- Details of the permutation-unitary result and the nonnegative-rank link to the log-rank conjecture
