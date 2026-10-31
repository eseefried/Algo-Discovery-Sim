# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given an open quantum walk (OQW, a quantum Markov chain) on a finite graph with node set V and internal Hilbert space, specified by Kraus operators B_i^j (transition from node j to node i), construct a unitary quantum walk that generalizes Szegedy's quantization of classical Markov chains, and define the probability, time-averaged (mean) probability and asymptotic mean probability of finding the walk at a node.

Scope: One smallest useful construction: a Szegedy-type unitary quantization of a finite-graph OQW, built from the isometry whose columns are the Kraus operators of the OQW, a reflection about its range, and a swap of two node registers. Tiny explicit instance (an assumption, since no experiment_scope was supplied): 2 nodes, 2-dimensional internal space (one qubit), Kraus operators B_0^0=I/\sqrt2, B_1^0=X/\sqrt2, B_0^1=H/\sqrt2, B_1^1=I/\sqrt2, giving a 3-qubit circuit. Outside scope: OQWs on infinite lattices, the paper's exact definition/normalization of the unitary (e.g. one-step S R_A versus two-reflection R_B R_A), the paper's specific choice of which register defines the node, any closed-form or spectral theorem the paper derives for the asymptotic mean probability, and any proofs.

## Symbols

- $V$: finite set of graph nodes, labelled by integers 0..n-1; domain: finite set, |V| = n
- $\mathcal{H}$: internal (coin-like) Hilbert space of the open quantum walk; domain: complex Hilbert space of dimension d
- $B_i^j$: Kraus operator of the OQW for a transition from node j to node i; domain: d x d complex matrix, i,j in V
- $\rho_j$: unnormalized internal state block of the walker at node j; domain: positive semidefinite d x d matrix
- $A$: isometry embedding (internal state, node j) into (internal state, node j, node i) via Kraus operators; domain: linear map \mathcal{H}\otimes\mathbb{C}^n \to \mathcal{H}\otimes\mathbb{C}^n\otimes\mathbb{C}^n
- $R_A$: reflection about the range of A; domain: unitary, Hermitian operator on \mathcal{H}\otimes\mathbb{C}^n\otimes\mathbb{C}^n
- $S$: swap of the two node registers; domain: unitary on \mathcal{H}\otimes\mathbb{C}^n\otimes\mathbb{C}^n
- $U$: one step of the constructed unitary quantum walk; domain: unitary on \mathcal{H}\otimes\mathbb{C}^n\otimes\mathbb{C}^n
- $t, T$: discrete time step and averaging horizon; domain: non-negative integers
- $p_t(i)$: probability of finding the walk at node i after t steps; domain: [0,1]
- $\bar p_T(i)$: mean (Cesàro-averaged) probability at node i over T steps; domain: [0,1]
- $\Pi_\lambda$: orthogonal projector onto the eigenspace of U with eigenvalue \lambda; domain: projector on the walk Hilbert space
- $|\Psi_0\rangle$: initial state of the unitary walk; domain: unit vector in \mathcal{H}\otimes\mathbb{C}^n\otimes\mathbb{C}^n

## eq_1: Open quantum walk (quantum Markov chain) on a finite graph

$$
\mathcal{M}(\rho)=\sum_{i\in V}\Big(\sum_{j\in V} B_i^j\,\rho_j\,B_i^{j\dagger}\Big)\otimes|i\rangle\langle i|,\qquad \rho=\sum_{j}\rho_j\otimes|j\rangle\langle j|,\qquad \sum_{i\in V} B_i^{j\dagger}B_i^j=I_d\ \ \forall j\in V
$$

Definition of a discrete-time open quantum walk: a completely positive trace-preserving map on block-diagonal states over the nodes, with node-wise Kraus (trace-preservation) constraint.

Provenance: `standard_background`. Standard definition of open quantum walks (Attal–Petruccione–Sinayskiy framework) recalled from background; the abstract names the object but does not state the formula.

Equation assumptions:

- Finite graph; the lattice case (infinite V) is excluded from scope.

## eq_2: Kraus-operator isometry replacing Szegedy's square-root amplitudes

$$
A\big(|\xi\rangle\otimes|j\rangle\big)=\sum_{i\in V}\big(B_i^j|\xi\rangle\big)\otimes|j\rangle\otimes|i\rangle,\qquad A^\dagger A=I_{\mathcal{H}\otimes\mathbb{C}^n}
$$

Isometry from (internal, current node) to (internal, current node, next node); the isometry property follows exactly from the Kraus constraint in eq_1. For a classical chain with d=1 and B_i^j=\sqrt{P_{ij}} this reduces to Szegedy's state |\psi_j\rangle.

Provenance: `abstract_inferred`. Inferred: Szegedy's construction builds an isometry from \sqrt{P_{ij}}; the natural generalization to an OQW replaces the scalar amplitudes by the Kraus operators B_i^j, with isometry guaranteed by trace preservation. The paper's exact construction is not available, so this is a reconstruction, not a sourced formula.

Abstract evidence: This approach generalizes to the domain of open quantum walks (or quantum Markov chains) the framework introduced by Szegedy for quantizing Markov chains.

Equation assumptions:

- Register ordering internal ⊗ node1 ⊗ node2 and the role of the registers are the reconstructor's convention.

## eq_3: Unitary quantum walk step (Szegedy-type)

$$
R_A=2AA^\dagger-I,\qquad S\big(|\xi\rangle\otimes|j\rangle\otimes|i\rangle\big)=|\xi\rangle\otimes|i\rangle\otimes|j\rangle,\qquad U=S\,R_A,\qquad W=U^2=(S R_A S)\,R_A
$$

The walk unitary is a reflection about the range of A followed by a swap of the node registers; two such steps give the two-reflection Szegedy form W=R_B R_A with R_B=S R_A S.

Provenance: `abstract_inferred`. Inferred from the stated Szegedy generalization: Szegedy's walk is a product of reflections about the ranges of two isometries related by the swap. Whether the paper uses U or W (or another normalization) as its unit time step is unknown.

Abstract evidence: convert to a unitary quantum walk any open quantum walk which is defined on lattices as well as on finite graphs

Equation assumptions:

- Choice of U=S R_A as the elementary step (W=U^2 is the equivalent two-reflection form).

## eq_4: Probability of finding the walk at a node

$$
p_t(i)=\big\|\big(I_d\otimes I_n\otimes\langle i|\big)\,U^t\,|\Psi_0\rangle\big\|^2,\qquad \sum_{i\in V}p_t(i)=1
$$

Probability that a computational-basis measurement of the second node register after t steps returns node i, with the internal and first node registers traced out.

Provenance: `abstract_inferred`. The abstract states such a probability is defined; the specific register measured (second node register here) is the reconstructor's convention consistent with eq_2, where the last register holds the destination node.

Abstract evidence: we define the probability and the mean probability of finding the walk at a node

Equation assumptions:

- Node position is read from the second (destination) node register; the paper might use the first register or a symmetrized definition.

## eq_5: Mean probability and asymptotic mean probability

$$
\bar p_T(i)=\frac{1}{T}\sum_{t=0}^{T-1}p_t(i),\qquad \bar p_\infty(i)=\lim_{T\to\infty}\bar p_T(i)=\sum_{\lambda\in\mathrm{spec}(U)}\big\|\big(I_d\otimes I_n\otimes\langle i|\big)\Pi_\lambda|\Psi_0\rangle\big\|^2
$$

Cesàro time average of p_t(i) and its limit. In finite dimension, the limit exists exactly and equals the sum over distinct eigenvalues of U of the squared norm of the node-i component of the eigenprojected initial state (cross terms between distinct eigenvalues average to zero).

Provenance: `standard_background`. The Cesàro-mean/eigenprojector formula is a standard result for finite-dimensional unitaries; the abstract says an asymptotic mean probability is derived but gives no formula, so the paper's specific expression (e.g. in terms of OQW data) is not reproduced here.

Equation assumptions:

- Finite-dimensional walk space; the Cesàro mean is the intended averaging (the abstract does not specify the averaging convention).

## eq_6: Tiny explicit instance: 2 nodes, qubit internal space

$$
B_0^0=\tfrac{1}{\sqrt2}I,\ B_1^0=\tfrac{1}{\sqrt2}X,\ B_0^1=\tfrac{1}{\sqrt2}H,\ B_1^1=\tfrac{1}{\sqrt2}I;\qquad |\Psi_0\rangle=A(|0\rangle\otimes|0\rangle)=\tfrac{1}{\sqrt2}\big(|0\rangle|0\rangle|0\rangle+|1\rangle|0\rangle|1\rangle\big)
$$

Concrete OQW on the 2-node complete graph with self-loops satisfying the Kraus constraint for each j (each pair consists of two unitaries scaled by 1/\sqrt2). The initial state is the isometric embedding of internal |0\rangle at node 0. Total circuit size: 3 qubits (internal, node1, node2).

Provenance: `assumption`. No experiment_scope was supplied; this is the smallest nontrivial instance chosen by the reconstructor to make the construction concrete. The abstract does not provide any example.

Equation assumptions:

- X, H denote the Pauli-X and Hadamard gates; node labels 0,1 are encoded as computational basis states of one qubit.

## Registers

- internal: 1 qubit (d=2 in the instance; \lceil\log_2 d\rceil in general) qubits; internal (coin-like) degree of freedom of the open quantum walk on which the Kraus operators act
- node1: 1 qubit (n=2 in the instance; \lceil\log_2 n\rceil in general) qubits; first node register (current/source node j); node label j encoded as computational basis state |j\rangle
- node2: 1 qubit (n=2 in the instance; \lceil\log_2 n\rceil in general) qubits; second node register (destination node i); measured to obtain p_t(i); tensor order internal ⊗ node1 ⊗ node2

## Initial state

|\Psi_0\rangle = A(|\xi_0\rangle\otimes|j_0\rangle) with internal state |\xi_0\rangle=|0\rangle and starting node j_0=0; for the instance |\Psi_0\rangle=(|000\rangle+|101\rangle)/\sqrt2 in order internal, node1, node2 (eq_6). Prepared from |000\rangle by the controlled Stinespring dilation U_A with U_A(|\xi\rangle|j\rangle|0\rangle)=A(|\xi\rangle|j\rangle).

## Measurement

Computational-basis measurement of the node2 register after t applications of U; outcome i occurs with probability p_t(i) (eq_4). Internal and node1 registers are discarded.

## Classical postprocessing

Estimate p_t(i) from outcome frequencies for each t, form the Cesàro mean \bar p_T(i)=\frac1T\sum_{t<T}p_t(i), and compare with the spectral prediction \bar p_\infty(i) computed by exact diagonalization of the 8x8 unitary U in the instance (eq_5).

## Algorithm steps

1. Prepare |\Psi_0\rangle by applying the dilation unitary U_A (controlled on node1, apply the Stinespring dilation of the Kraus family {B_i^j}_i to internal ⊗ node2) to |\xi_0\rangle|j_0\rangle|0\rangle. (eq_2, eq_6)
2. Apply the reflection R_A = U_A (I ⊗ I ⊗ (2|0\rangle\langle0| - I)) U_A^\dagger, i.e. uncompute U_A, reflect about |0\rangle on node2, recompute U_A. (eq_3)
3. Apply the swap S of registers node1 and node2. Together with the previous step this is one walk step U = S R_A; repeat steps 2-3 t times to obtain U^t|\Psi_0\rangle. (eq_3)
4. Measure node2 in the computational basis to estimate p_t(i); repeat for t=0,...,T-1 to form the mean probability. (eq_4, eq_5)

## Assumptions

- No experiment_scope supplied: the 2-node, qubit-internal-space instance in eq_6 and the 3-qubit circuit are the reconstructor's choice.
- The unitary walk is reconstructed as the Szegedy-type construction U = S R_A built from the Kraus isometry A; the paper's actual construction may differ in normalization, register layout or the use of W=R_B R_A as the unit step.
- Node position is defined by the second node register; the paper's definition may use a different register or combination.
- Mean probability is taken to be the Cesàro time average; the asymptotic formula given is the generic finite-dimensional spectral expression, not the paper's derived result.
- Only finite graphs are treated; lattice (infinite) OQWs are out of scope.

## Missing information

- Exact definition of the unitary walk in the paper (operator form, Hilbert space, register conventions, one- versus two-reflection step).
- The paper's precise definitions of the probability and mean probability of finding the walk at a node (which register(s) are measured, averaging convention).
- The paper's derived expression for the asymptotic mean probability in terms of the OQW data and its relation to OQW stationary states or spectral properties.
- Treatment of OQWs on lattices (infinite node sets) and any conditions (e.g. irreducibility, homogeneity) imposed on the Kraus operators.
- Any worked examples, numerical results or comparisons to classical Szegedy walks.
