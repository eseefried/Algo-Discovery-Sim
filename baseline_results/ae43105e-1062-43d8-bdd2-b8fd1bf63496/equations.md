# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Decompose an arbitrary bipartite unitary U acting on C^{d_A} ⊗ C^{d_B} into a product of a small number of controlled unitary operators (each controlled from one party and acting as a unitary on the other), with the abstract's bounds N ≤ 4d_A − 5 in general and N ≤ 2d_A − 1 when d_A is a power of two.

Scope: Scoped (as an assumption, since no experiment_scope was supplied) to the smallest case d_A = 2 (a power of two), for which the abstract's bound is 2·2 − 1 = 3 controlled unitaries, instantiated on the tiny instance d_A = d_B = 2 (a generic two-qubit unitary). The reconstruction uses the standard cosine–sine decomposition (CSD) to exhibit U as the product of a B-controlled unitary sandwiched between two A-controlled unitaries, which matches the abstract's count for d_A = 2; the paper's actual proof technique is unknown. Outside scope: the general-d_A recursion achieving 4d_A − 5 and 2d_A − 1, the three-controlled-unitary result for bipartite complex permutation unitaries and its link to classical reversible circuits, the n-partite bound, the decomposition into a 'simple type' of bipartite gate plus local unitaries, the CNOT/entanglement-cost bounds versus Schmidt rank, and the nonnegative-rank / log-rank-conjecture connection.

## Symbols

- $d_A, d_B$: Local dimensions of systems A and B (d_A ≥ 2); domain: integers ≥ 2
- $U$: Bipartite unitary to be decomposed; domain: U(d_A d_B) acting on C^{d_A} ⊗ C^{d_B}
- $|j\rangle_A, |k\rangle_B$: Computational basis states of A (j = 0..d_A−1) and B (k = 0..d_B−1); composite basis ordered |j⟩_A ⊗ |k⟩_B with A the most significant index, so the (j,k) basis vector has integer index j·d_B + k; domain: orthonormal bases of C^{d_A}, C^{d_B}
- $U_j, V_k$: Target unitaries of a controlled unitary: U_j acts on B when A is in |j⟩; V_k acts on A when B is in |k⟩; domain: U(d_B), U(d_A)
- $N$: Number of controlled-unitary factors in a decomposition of U; domain: positive integers
- $P_0,P_1,Q_0,Q_1$: d_B × d_B unitary blocks in the cosine–sine decomposition of U for d_A = 2; domain: U(d_B)
- $\theta_k$: CSD angles, k = 0..d_B−1, with C = diag(cos θ_k), S = diag(sin θ_k); domain: [0, π/2]
- $R_y(\phi)$: Real rotation on the qubit A: [[cos(φ/2), −sin(φ/2)],[sin(φ/2), cos(φ/2)]]; domain: SO(2) ⊂ U(2)
- $d_1,\dots,d_n$: Local dimensions in the n-partite statement; domain: integers ≥ 2

## eq_1: Controlled unitary operators (controlled from A or from B)

$$
C^{A}=\sum_{j=0}^{d_A-1}|j\rangle\langle j|_A\otimes U_j,\qquad C^{B}=\sum_{k=0}^{d_B-1}V_k\otimes|k\rangle\langle k|_B,\qquad U_j\in U(d_B),\;V_k\in U(d_A)
$$

A controlled unitary is block-diagonal in some orthonormal product basis of the controlling party; the controlling basis may be any local basis (local unitaries on the control side can be absorbed into neighboring factors).

Provenance: `standard_background`. Standard definition of a controlled unitary with control on one party of a bipartite system; the abstract names 'controlled unitary operators' without defining them.

Equation assumptions:

- The control basis is allowed to be an arbitrary orthonormal basis of the controlling system, not only the computational basis.

## eq_2: Main bipartite bounds on the number of controlled-unitary factors

$$
U=\prod_{i=1}^{N}C_i,\quad C_i\in\{C^{A}\text{-type},\,C^{B}\text{-type}\},\qquad N\le 4d_A-5\ \ (d_A\ge 2),\qquad N\le 2d_A-1\ \ (d_A=2^m)
$$

Existence statement: every U on the d_A × d_B system factors into at most 4d_A − 5 controlled unitaries, and at most 2d_A − 1 when d_A is a power of two. The constructive proof is not available from the abstract.

Provenance: `abstract_explicit`. Directly stated in the abstract; the type (A- or B-controlled) of each factor is not specified there.

Abstract evidence: any unitary operator on the $d_{A}\times d_{B}$ system ($d_{A}\geq 2$) can be decomposed into the product of at most $4d_{A}-5$ controlled unitary operators. The number can be reduced to $2d_{A}-1$ when $d_{A}$ is a power of two.

## eq_3: Cosine–sine decomposition of U for d_A = 2 (blocks ordered by the A index)

$$
U=\begin{pmatrix}P_0&0\\0&P_1\end{pmatrix}\begin{pmatrix}C&-S\\S&C\end{pmatrix}\begin{pmatrix}Q_0&0\\0&Q_1\end{pmatrix},\qquad C=\mathrm{diag}(\cos\theta_k),\ S=\mathrm{diag}(\sin\theta_k),\ C^2+S^2=I_{d_B}
$$

Exact equality: any U ∈ U(2d_B), partitioned into four d_B × d_B blocks according to the A index (A most significant), admits this decomposition with unitary P_0,P_1,Q_0,Q_1 and diagonal nonnegative C,S.

Provenance: `standard_background`. Standard cosine–sine decomposition for a unitary matrix partitioned into equal-size blocks; recalled from background, not from the paper.

Equation assumptions:

- Composite basis ordering |j⟩_A ⊗ |k⟩_B with A most significant, so the outer 2×2 block structure is indexed by A.

## eq_4: Identification of the CSD factors as controlled unitaries

$$
\begin{pmatrix}P_0&0\\0&P_1\end{pmatrix}=\sum_{j=0}^{1}|j\rangle\langle j|_A\otimes P_j,\qquad \begin{pmatrix}C&-S\\S&C\end{pmatrix}=\sum_{k=0}^{d_B-1}R_y(2\theta_k)\otimes|k\rangle\langle k|_B
$$

The outer factors are controlled from A with targets P_j (resp. Q_j) on B; the middle factor is controlled from B in its computational basis with target rotation R_y(2θ_k) on A.

Provenance: `standard_background`. Direct rewriting of the block matrices of eq_3 in tensor-product form using the stated basis ordering; the middle matrix has entries cos θ_k, ∓sin θ_k only between |0⟩_A|k⟩_B and |1⟩_A|k⟩_B.

Equation assumptions:

- Basis ordering as in eq_3.

## eq_5: Three-controlled-unitary decomposition for d_A = 2 (matches 2d_A − 1 = 3)

$$
U=C^{A}_{P}\,C^{B}_{\theta}\,C^{A}_{Q},\qquad C^{A}_{P}=\sum_j|j\rangle\langle j|_A\otimes P_j,\ C^{B}_{\theta}=\sum_k R_y(2\theta_k)\otimes|k\rangle\langle k|_B,\ C^{A}_{Q}=\sum_j|j\rangle\langle j|_A\otimes Q_j;\qquad N=3=2d_A-1
$$

Scoped instance of the abstract's power-of-two bound: for d_A = 2 the CSD yields exactly three controlled unitaries (A-controlled, B-controlled, A-controlled). Operators are applied right-to-left (C^A_Q first).

Provenance: `abstract_inferred`. Inferred: the abstract's bound evaluates to 3 at d_A = 2, and eq_3–eq_4 exhibit an explicit 3-factor decomposition achieving it; whether the paper's proof proceeds via CSD is unknown.

Abstract evidence: The number can be reduced to $2d_{A}-1$ when $d_{A}$ is a power of two.

Equation assumptions:

- The paper's construction for d_A = 2 is assumed to coincide in count (not necessarily in method) with the CSD-based construction.

## eq_6: n-partite bound (stated, outside reconstruction scope)

$$
U\in U(d_1\cdots d_n):\quad U=\prod_{i=1}^{N}G_i,\qquad N\le 2\prod_{j=1}^{n-1}(2d_j-2)-1,\quad G_i\ \text{controlled from } n-1 \text{ systems}
$$

Existence bound for multipartite unitaries; each gate G_i is a unitary on one system controlled jointly by the other n − 1 systems. No construction is available from the abstract.

Provenance: `abstract_explicit`. Directly stated in the abstract; recorded for completeness, not reconstructed.

Abstract evidence: any $n$-partite unitary on the space $\mathbb{C}^{d_{1}}\otimes\cdots\otimes\mathbb{C}^{d_{n}}$ is the product of at most $[2\prod^{n-1}_{j=1}(2d_{j}-2)-1]$ controlled unitary gates, each of which is controlled from $n-1$ systems

## Registers

- A: 1 qubit (d_A = 2 in the scoped instance; log2 d_A qubits in general when d_A is a power of two) qubits; First party; controls the outer two factors and is the target of the middle B-controlled rotation
- B: 1 qubit (d_B = 2 in the tiny instance; a d_B-level system or ⌈log2 d_B⌉ qubits in general) qubits; Second party; target of the A-controlled unitaries P_j, Q_j and control of the middle factor

## Initial state

Arbitrary |ψ⟩ ∈ C^{d_A} ⊗ C^{d_B} (the decomposition is an operator identity, independent of the input state); for a test, e.g. |0⟩_A ⊗ |0⟩_B with d_A = d_B = 2.

## Classical postprocessing

None required for the decomposition itself; verification of the scoped instance consists of classically checking the operator identity U = C^A_P C^B_θ C^A_Q (eq_5) to numerical precision and counting the factors.

## Algorithm steps

1. Classical preprocessing: given U ∈ U(2d_B) in the basis |j⟩_A ⊗ |k⟩_B (A most significant), partition into d_B × d_B blocks and compute the cosine–sine decomposition to obtain P_0, P_1, Q_0, Q_1 and angles θ_k. (eq_3)
2. Apply the A-controlled unitary C^A_Q = Σ_j |j⟩⟨j|_A ⊗ Q_j (target B). (eq_1, eq_4, eq_5)
3. Apply the B-controlled unitary C^B_θ = Σ_k R_y(2θ_k) ⊗ |k⟩⟨k|_B (target A). For d_B = 2 this is two controlled-R_y rotations on A, one for each value of B. (eq_4, eq_5)
4. Apply the A-controlled unitary C^A_P = Σ_j |j⟩⟨j|_A ⊗ P_j (target B). The product equals U exactly, using N = 3 = 2d_A − 1 controlled unitaries. (eq_1, eq_4, eq_5, eq_2)

## Assumptions

- No experiment_scope was provided; the scope was chosen as the smallest case d_A = 2 (a power of two) with the tiny instance d_A = d_B = 2.
- The explicit 3-factor construction is the standard cosine–sine decomposition; the paper's own proof method is unknown and may differ.
- Controlled unitaries may be controlled in an arbitrary local orthonormal basis; in the CSD-based instance all controls happen to be in the computational basis.
- Composite basis ordering |j⟩_A ⊗ |k⟩_B with A as the most significant index, so a basis vector has integer index j·d_B + k.

## Missing information

- The paper's general recursive construction achieving 4d_A − 5 controlled unitaries for arbitrary d_A ≥ 2, and the improved 2d_A − 1 construction for d_A a power of two beyond d_A = 2.
- Whether factors in the paper's decompositions alternate between A-control and B-control, and any constraints on the target unitaries.
- The definition of 'bipartite complex permutation operator' and the three-controlled-unitary construction for it, plus the analogy to classical reversible circuits.
- The definition of the 'simple type of bipartite gates' and the associated decomposition with local unitaries.
- The protocol, ancilla size, and the explicit dimension-independent CNOT/entanglement-cost bounds as functions of Schmidt rank.
- The precise statement linking these costs to nonnegative rank and the log-rank conjecture.
