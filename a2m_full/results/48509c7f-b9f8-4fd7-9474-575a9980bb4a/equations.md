# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given an explicit N x N unitary U with N=2^n (n=2 or 3), find basis permutation matrices P,Q so that U' = (PQ) U (PQ)^T is cheaper to compile, then synthesize U = Q^T P^T U' P Q as an ancilla-free, measurement-free circuit from standard gates. The runner reads the unitary or statevector and compares it with U up to global phase.

Scope: One tiny instance (n=2 or 3, explicit classical U). Heuristic greedy-swap permutation search with a nonzero-entry count as the cost proxy. U' is compiled by a generic decomposition, and P and Q are compiled to X, CX and multi-controlled X gates. The circuit is applied to the all-zero input state, with the unitary or the statevector read out. Out of scope: the actual OptQC search, the Qcompiler internals, MPI parallelization, and any claim of gate-count savings.

## Symbols

- $U$: target unitary; domain: U(2^n)
- $U'$: permuted unitary that is cheaper to compile; domain: U(2^n)
- $P,Q$: permutation matrices on computational basis states; domain: {0,1} matrices with one 1 per row and column, size 2^n
- $n$: number of qubits; domain: positive integer, small
- $c(\cdot)$: heuristic cost proxy, the count of non-identity off-diagonal entries; domain: nonnegative integer
- $|\psi_0\rangle$: initial state of the n-qubit register; domain: C^{2^n}, unit vector
- $W$: assembled circuit operator; domain: U(2^n)

## eq_1: Permutation-conjugated factorization

$$
U = Q^{T}P^{T}U^{\prime}PQ
$$

U is expressed through a permutation similarity transform of U'.

Provenance: `abstract_explicit`. The abstract states this factorization directly.

Abstract evidence: U=Q^{T}P^{T}U^{\prime}PQ

Equation assumptions:

- P and Q are real permutation matrices, so their inverses are their transposes

## eq_2: Inverse relation for U'

$$
U^{\prime}=(PQ)\,U\,(PQ)^{T}
$$

U' follows from eq_1 because PQ is orthogonal.

Provenance: `abstract_inferred`. Left-multiplying eq_1 by PQ and right-multiplying by (PQ)^T gives this, since (PQ)^T(PQ)=I.

Abstract evidence: U=Q^{T}P^{T}U^{\prime}PQ

Equation assumptions:

- The same permutation acts on both sides

## eq_3: Search objective

$$
(P,Q)=\arg\min_{P,Q}\; c\big(PQ\,U\,(PQ)^{T}\big)+\mathrm{cost}(P)+\mathrm{cost}(Q)
$$

Heuristic minimization of a compiled-gate-count proxy.

Provenance: `assumption`. The abstract reports reduced gate counts but gives no explicit objective, so this form is proposed.

Equation assumptions:

- The cost proxy is the entry count plus the permutation circuit cost
- The search is heuristic, not exhaustive

## eq_4: Circuit operator and order

$$
W = Q^{T}P^{T}\,C_{U^{\prime}}\,P\,Q,\quad \text{applied in time as } Q,\;P,\;C_{U^{\prime}},\;P^{T},\;Q^{T}
$$

The rightmost operator acts first in time.

Provenance: `abstract_inferred`. Operator products act right to left, so Q is applied first.

Abstract evidence: U=Q^{T}P^{T}U^{\prime}PQ

Equation assumptions:

- C_{U'} is an exact compilation of U'

## eq_5: Initial state and output

$$
|\psi_0\rangle=|0\rangle^{\otimes n},\quad |\psi_{out}\rangle=W|\psi_0\rangle,\quad \min_{\phi}\|W-e^{i\phi}U\|_F<\epsilon
$$

The circuit starts in |0...0>. The output state equals U|0...0> up to a global phase, and the full unitary matches U up to a global phase.

Provenance: `assumption`. A statevector run needs a defined input, and all-zero is the default. The unitary comparison follows the task convention that global phase is unobservable.

Equation assumptions:

- Little-endian: basis index k=sum_j b_j 2^j, with qubit j holding b_j

## Registers

- q: n qubits; system qubits, little-endian index encoding, no ancillas

## Initial state

|0>^{\otimes n} (all qubits in |0>, basis index 0), with the circuit applying W so that the output is U|0...0> up to global phase

## Classical postprocessing

Classical permutation search and matrix decomposition only. After assembly, compare the unitary or statevector with U up to global phase.

## Algorithm steps

1. Take U as an explicit matrix, fix the little-endian basis encoding, and start from |0...0>. (eq_1, eq_5)
2. Heuristic greedy-swap search over basis permutations to minimize the cost proxy, yielding P, Q and U'. (eq_2, eq_3)
3. Compile U' with a generic decomposition (Givens or cosine-sine into uniformly controlled Ry/Rz plus CX), skipping identity and zero blocks. (eq_4)
4. Compile P and Q as X, CX and multi-controlled X gates, preferring bitwise permutations (qubit swaps and X flips). (eq_4)
5. Assemble the circuit in the order Q, P, U', P^T, Q^T and compare its unitary or output state with U up to global phase. (eq_4, eq_5)

## Assumptions

- Tiny instance (n=2 or 3) with explicit U
- Greedy swap search
- Entry count stands in for CNOT count
- No ancillas, no measurements, no black box
- Initial state |0...0> is assumed
- U' is compiled by a generic decomposition standing in for Qcompiler
- P=Q=I is a valid fallback

## Missing information

- The exact OptQC search algorithm and cost function
- The exact Qcompiler decomposition details
- The sense in which U' is 'equivalent to U up to a permutation' beyond the stated similarity form
- The meaning of 'each matrix component considered separately'
- Quantitative gate-count results
