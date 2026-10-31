# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given an n-qubit unitary U (2^n x 2^n), find permutation matrices P and Q such that compiling the factorized form U = Q^T P^T U' P Q (with U' = P Q U Q^T P^T, each factor compiled separately by the Qcompiler framework) yields a quantum circuit with fewer elementary gates than compiling U directly.

Scope: Single smallest useful construction: the permutation-conjugation identity, the resulting gate-count objective over permutation matrices, and the (background) cosine-sine decomposition used by Qcompiler to compile each factor. Tiny explicit instance (assumption): n = 2 qubits, 4 x 4 unitary, Q fixed to the identity, P ranging over all 24 permutations of the 4 basis states, objective evaluated by exhaustive enumeration. Outside scope: the actual OptQC search heuristic for P and Q, the MPI/multiprocessor parallelization, the specific elementary gate set and gate-counting rules of Qcompiler, and the paper's benchmark unitaries and numerical gate-count reductions.

## Symbols

- $n$: number of qubits; domain: positive integer (instance: n = 2)
- $N$: matrix dimension N = 2^n; domain: positive integer (instance: N = 4)
- $U$: target unitary operator to be compiled; domain: U \in \mathrm{U}(N), N x N complex unitary matrix
- $P, Q$: permutation matrices found by OptQC; domain: N x N 0/1 matrices with exactly one 1 per row and column; P, Q \in S_N embedded in O(N)
- $\pi, \sigma$: permutations of basis indices defining P and Q; domain: bijections \{0,\dots,N-1\}\to\{0,\dots,N-1\}
- $U'$: permutation-equivalent unitary actually compiled in place of U; domain: U' \in \mathrm{U}(N)
- $G(M)$: number of elementary gates in the Qcompiler circuit for matrix M; domain: non-negative integer
- $C(P,Q)$: total gate count of the factorized circuit; domain: non-negative integer
- $|i\rangle$: computational basis state with integer label i = \sum_{k=0}^{n-1} b_k 2^{n-1-k}, qubit 0 most significant; domain: i \in \{0,\dots,N-1\}

## eq_1: Permutation factorization of U

$$
U = Q^{T} P^{T} U' P Q
$$

The target unitary is written as a product of a permutation Q, a permutation P, the modified unitary U', and the transposed permutations; each factor is compiled separately and the circuits are concatenated.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: the number of gates in the quantum circuit of $U=Q^{T}P^{T}U^{\prime}PQ$ is significantly reduced

## eq_2: Definition of U' from U

$$
U' = P Q U Q^{T} P^{T}, \qquad P^{T}P = Q^{T}Q = I_N
$$

Exact equality: since permutation matrices are real orthogonal, inverting eq_1 gives U' as a simultaneous row/column permutation of U, i.e. U' is 'equivalent to U up to a permutation'.

Provenance: `abstract_inferred`. Follows exactly from eq_1 and orthogonality of permutation matrices.

Abstract evidence: where $U^{\prime}$ is equivalent to $U$ up to a permutation

## eq_3: Permutation matrix as basis relabeling

$$
P_{ij} = \delta_{i,\pi(j)}, \qquad P\,|j\rangle = |\pi(j)\rangle, \qquad (P^{T} U' P)_{ij} = U'_{\pi(i)\pi(j)}
$$

Standard definition of a permutation matrix and its action on computational basis states; conjugation by P relabels the basis indices of U'.

Provenance: `standard_background`. Standard linear-algebra definition recalled from background knowledge.

Equation assumptions:

- Basis label i uses binary encoding with qubit 0 as most significant bit.

## eq_4: Gate-count objective minimized by OptQC

$$
C(P,Q) = G(Q) + G(P) + G(U') + G(P^{T}) + G(Q^{T}), \qquad (P^{*},Q^{*}) = \arg\min_{P,Q \in S_N} C(P,Q), \qquad C(P^{*},Q^{*}) < G(U)
$$

Total number of elementary gates when each matrix component in eq_1 is compiled separately; OptQC seeks P, Q reducing this total below the direct compilation cost G(U). The optimizer actually used (exhaustive, heuristic, or stochastic) is not stated in the abstract.

Provenance: `abstract_inferred`. The abstract says the gate count of the factorized circuit is reduced and each component is compiled separately, so the natural objective is the additive gate count over components; the minimization form is an inference.

Abstract evidence: the quantum circuit implementation of each matrix component is considered separately

Equation assumptions:

- Gate count is additive over concatenated sub-circuits.
- G(.) is defined by the Qcompiler gate set and counting rules, which are not given in the abstract.

## eq_5: Cosine-sine decomposition used by Qcompiler for a unitary factor

$$
U' = \begin{pmatrix} A_1 & 0 \\ 0 & A_2 \end{pmatrix} \begin{pmatrix} C & -S \\ S & C \end{pmatrix} \begin{pmatrix} B_1 & 0 \\ 0 & B_2 \end{pmatrix}, \qquad C = \mathrm{diag}(\cos\theta_k),\; S = \mathrm{diag}(\sin\theta_k),\; C^2 + S^2 = I_{N/2}
$$

Recursive cosine-sine decomposition of a 2^n x 2^n unitary into block-diagonal unitaries (uniformly controlled gates on n-1 qubits) and a uniformly controlled rotation; A_1, A_2, B_1, B_2 are recursively decomposed down to single-qubit gates. This is the known compilation scheme of Qcompiler to which OptQC adds permutation optimization.

Provenance: `standard_background`. Background knowledge of the cosine-sine-decomposition-based compilation approach; the abstract only names the Qcompiler framework.

Equation assumptions:

- Qcompiler compiles via recursive cosine-sine decomposition; the exact gate-level reduction rules are not given in the abstract.

## eq_6: Tiny instance: exhaustive search with Q = I

$$
n = 2,\; N = 4,\; Q = I_4,\; P^{*} = \arg\min_{\pi \in S_4} \left[ G(P_\pi) + G(P_\pi U P_\pi^{T}) + G(P_\pi^{T}) \right]
$$

Proposed smallest explicit instance: fix Q to the identity and enumerate all 24 permutations of the 4 basis states of a 2-qubit unitary, compiling each candidate U' with eq_5 and selecting the minimum total gate count.

Provenance: `assumption`. A finite, checkable instance of the objective in eq_4; chosen because no experiment_scope was supplied.

Equation assumptions:

- Q = I_4 so only P is optimized.
- Exhaustive enumeration replaces whatever search heuristic OptQC uses.

## Registers

- data: n (instance: 2) qubits; Register on which U acts; basis state |i> with i encoded in binary, qubit 0 most significant.

## Initial state

Arbitrary input state |\psi\rangle on the n-qubit data register; the construction is a unitary synthesis, not a state-preparation algorithm.

## Classical postprocessing

Compare the total gate count C(P*,Q*) of the factorized circuit with the direct Qcompiler gate count G(U); report the reduction. Optionally verify numerically that the assembled circuit matrix equals U exactly (up to floating-point error).

## Algorithm steps

1. Choose a permutation Q (instance: Q = I); compile Q into a circuit of gate count G(Q). (eq_3, eq_6)
2. For each candidate permutation P in the search set, form U' = P Q U Q^T P^T. (eq_2, eq_3)
3. Compile U', P, P^T, Q^T separately with the Qcompiler (cosine-sine decomposition) framework and evaluate the total gate count C(P,Q). (eq_5, eq_4)
4. Select (P*, Q*) minimizing C(P,Q) (instance: exhaustive over S_4 with Q = I); accept if C(P*,Q*) < G(U). (eq_4, eq_6)
5. Assemble the final circuit acting in time order Q, then P, then U', then P^T, then Q^T, which implements U exactly. (eq_1)

## Assumptions

- No experiment_scope supplied; a 2-qubit, Q = I, exhaustive-search instance was chosen as the smallest useful construction.
- Qcompiler compiles unitaries via recursive cosine-sine decomposition into single-qubit and CNOT-type elementary gates.
- Gate counts are additive over concatenated sub-circuits and the permutation circuits P, Q are counted with the same gate model.
- Basis index encoding: qubit 0 is the most significant bit.

## Missing information

- The actual OptQC search algorithm for P and Q (e.g. heuristic or stochastic optimization) and any restriction on the form of Q (e.g. qubit permutations) is not stated in the abstract.
- The elementary gate set and gate-counting rules of Qcompiler, including how permutation matrices P and Q are compiled.
- The MPI parallelization scheme and how the search is distributed across processors.
- The benchmark unitary operators and the reported numerical gate-count reductions.
