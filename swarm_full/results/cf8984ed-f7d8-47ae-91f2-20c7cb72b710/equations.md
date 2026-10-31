# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Compile a given unitary U into a quantum circuit of elementary gates with fewer gates by searching for permutation matrices P and Q such that U = Q^T P^T U' P Q, where U' is equivalent to U up to a permutation, and each matrix component is implemented separately (OptQC extending Qcompiler, with MPI parallelization).

Scope: Abstract-level reconstruction of the permutation-based gate-count optimization objective only; the search algorithm, decomposition method, and MPI details are not specified in the abstract.

## Symbols

- $U$: Given target unitary matrix; domain: N x N unitary, N=2^n
- $U'$: Permutation-equivalent unitary to U; domain: N x N unitary
- $P, Q$: Permutation matrices found by the optimizer; domain: N x N permutation matrices

## eq_1: Permutation factorization

$$
U=Q^{T}P^{T}U^{\prime}PQ
$$

Target unitary expressed via permutations P, Q and equivalent unitary U' whose circuit has fewer gates.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: U=Q^{T}P^{T}U^{\prime}PQ

## eq_2: Gate count minimization

$$
\min_{P,Q}\; G(Q^{T})+G(P^{T})+G(U^{\prime})+G(P)+G(Q)
$$

Objective: minimize total elementary gate count G over permutations, with each factor compiled separately.

Provenance: `assumption`. Formalizes the abstract's goal of reducing gate count with components implemented separately; the exact cost function is not given.

Equation assumptions:

- Total gate count is the sum of per-component counts G(.)

## Registers

- q: n qubits (N=2^n), assumed qubits; System register on which U is implemented

## Initial state

Arbitrary n-qubit input state |psi>; the compiled circuit implements U as a unitary and is not tied to a specific input state.

## Measurement

None intrinsic to the compilation task; the abstract specifies no measurement. For verification, one could measure in the computational basis after applying the compiled circuit to test inputs, which is an assumption.

## Classical postprocessing

Classical optimization only: search over P and Q, compare gate counts of the resulting circuits, and select the minimum. Candidate evaluation is presumably distributed across processors via MPI (details unspecified).

## Algorithm steps

1. Classically search for permutation matrices P and Q to obtain U' = P Q U Q^T P^T (equivalent to U up to permutation) with lower expected gate cost. (eq_1, eq_2)
2. Compile each component (Q, P, U', P^T, Q^T) separately into elementary gates using the Qcompiler-style decomposition. (eq_2)
3. Concatenate component circuits in order of U=Q^T P^T U' P Q (acting right-to-left: Q, P, U', P^T, Q^T) on register q. (eq_1)

## Assumptions

- Gate-count cost is additive over components.
- Register size assumed n qubits with N=2^n; no ancillas.
- Circuit applied right-to-left on the same register.
- Measurement is not part of the abstract; the computational-basis check is an assumed verification option.

## Missing information

- Search algorithm for P and Q
- Elementary gate set and decomposition method
- MPI parallelization scheme
- Exact cost function and benchmark unitaries
