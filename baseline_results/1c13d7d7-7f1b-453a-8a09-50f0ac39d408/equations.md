# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Discrete-time coined quantum walk on a finite one-dimensional chain whose edges are randomly present or absent in each time step (dynamic percolation). The evolution of the averaged density operator is a random unitary map, and the goal is the long-time (asymptotic) behaviour of the walker, obtained via the attractor structure of the random unitary map.

Scope: Scoped to the smallest useful construction: a coined quantum walk on a path graph of N vertices with Hadamard coin, edges independently open with probability p in each step, reflecting (coin-flipping) shift on broken edges and at chain ends. Tiny explicit instance: N=4 (2 position qubits, 1 coin qubit), p=1/2, walker started at x=1 with coin |R>. Deliverables: the one-step unitaries U_K, the random unitary map Phi, the attractor equations, and the asymptotic-state formula, plus a sampling protocol to estimate Phi^t. Out of scope: the paper's literature review, the explicit attractor basis for the 1D chain (not derivable from the abstract alone), the paper's concrete step-by-step numerical example, and all two-dimensional integer-lattice / Grover-coin results.

## Symbols

- $N$: number of vertices of the chain (path graph); domain: positive integer; instance N=4
- $x$: walker position (vertex label); domain: \{0,\dots,N-1\}
- $c$: coin state, L (left, encoded 0) or R (right, encoded 1); domain: \{L,R\} \cong \{0,1\}
- $E$: edge set of the chain, E=\{(x,x+1): 0\le x\le N-2\}; domain: set of N-1 edges
- $K$: percolation configuration: subset of edges present in a given step; domain: K \subseteq E, 2^{N-1} possibilities
- $p$: probability that an edge is present in a given step; domain: [0,1]; instance p=1/2
- $\pi(K)$: probability of configuration K; domain: [0,1], \sum_K \pi(K)=1
- $C$: coin operator acting on the coin qubit; domain: 2\times 2 unitary; instance Hadamard
- $S_K$: configuration-dependent conditional shift; domain: 2N\times 2N permutation unitary
- $U_K$: one-step walk unitary for configuration K; domain: 2N\times 2N unitary
- $\Phi$: random unitary map (averaged one-step dynamics); domain: completely positive trace-preserving, unital map on 2N\times 2N density operators
- $\rho(t)$: averaged density operator after t steps; domain: 2N\times 2N positive, trace one
- $X_{\lambda,i}$: attractor of Phi with eigenvalue lambda; domain: 2N\times 2N operator, |\lambda|=1
- $t$: discrete time step; domain: non-negative integer

## eq_1: Hilbert space, basis ordering and percolation distribution

$$
\mathcal{H}=\mathbb{C}^{N}\otimes\mathbb{C}^{2},\quad |x,c\rangle=|x\rangle\otimes|c\rangle,\quad \pi(K)=p^{|K|}(1-p)^{|E|-|K|},\ K\subseteq E
$$

Position register (binary encoding of x, most significant) tensored with a coin qubit (L=0, R=1). Each edge is independently present with probability p in every step, giving the product distribution pi(K) over configurations.

Provenance: `abstract_inferred`. The abstract specifies random, per-step appearance/disappearance of connections; independent Bernoulli edges with parameter p is the standard dynamic-percolation model implied. Coined position-coin Hilbert space is the standard quantum-walk setting.

Abstract evidence: the connections appear and disappear randomly in each step during the time evolution

Equation assumptions:

- Edges are independent and identically distributed with probability p each step
- Coined (discrete-time) quantum walk with a two-dimensional coin

## eq_2: Configuration-dependent shift with reflection on broken edges

$$
S_K|x,R\rangle=\begin{cases}|x+1,R\rangle & (x,x+1)\in K\\ |x,L\rangle & \text{otherwise}\end{cases},\qquad S_K|x,L\rangle=\begin{cases}|x-1,L\rangle & (x-1,x)\in K\\ |x,R\rangle & \text{otherwise}\end{cases}
$$

If the edge in the direction of motion is present the walker moves; if the edge is absent (or the walker is at a chain end) it stays and its coin is flipped (reflection). S_K is a permutation of the basis, hence unitary.

Provenance: `assumption`. The abstract does not state how the walker behaves at a missing edge; the reflecting (coin-flip) rule is a common choice in percolation quantum-walk literature and keeps S_K unitary. Other rules (e.g. phase-free staying without coin flip) would change the attractor structure.

Equation assumptions:

- Reflecting boundary rule at broken edges and at chain ends
- Finite chain with no periodic wrap-around

## eq_3: One-step unitary and random unitary map

$$
U_K=S_K\,(I_N\otimes C),\qquad \Phi(\rho)=\sum_{K\subseteq E}\pi(K)\,U_K\,\rho\,U_K^{\dagger},\qquad \rho(t)=\Phi^{t}(\rho_0)
$$

Coin then shift for a fixed configuration; averaging over the per-step configuration gives a random unitary (unital) channel, iterated t times for the averaged state.

Provenance: `abstract_inferred`. The abstract identifies the averaged dynamics as a random unitary map; with per-step i.i.d. configurations the averaged state is exactly the t-fold iterate of the single-step convex mixture of unitaries.

Abstract evidence: applying the asymptotic methods concerning random unitary maps

Equation assumptions:

- Configurations are resampled independently each step (Markovian, memoryless)
- Coin acts before the shift

## eq_4: Attractor equations

$$
U_K\,X\,U_K^{\dagger}=\lambda\,X\quad \forall K\text{ with }\pi(K)>0,\qquad |\lambda|=1\ \Longleftrightarrow\ U_K X=\lambda X U_K
$$

Operators X in the peripheral spectrum of Phi (eigenvalue of unit modulus) are exactly those satisfying the simultaneous intertwining relations for all unitaries in the mixture; these span the asymptotic (attractor) space.

Provenance: `standard_background`. Known result for random unitary maps (Novotny-Alber-Jex type attractor theory): unital channel, peripheral eigenvectors are common eigenoperators of all Kraus unitaries. Recalled as background, not extracted from the paper.

Equation assumptions:

- 0<p<1 so that all configurations have positive probability; if p=1 only K=E contributes

## eq_5: Asymptotic (long-time) averaged state

$$
\rho(t)\ \xrightarrow{t\to\infty}\ \rho_{\mathrm{as}}(t)=\sum_{|\lambda|=1}\lambda^{t}\sum_{i}\mathrm{Tr}\!\left(X_{\lambda,i}^{\dagger}\rho_0\right)X_{\lambda,i},\qquad \mathrm{Tr}(X_{\lambda,i}^{\dagger}X_{\lambda',j})=\delta_{\lambda\lambda'}\delta_{ij}
$$

After the contributions of eigenvalues with |lambda|<1 have decayed, the averaged state is the projection of rho_0 onto the attractor space, with possibly non-stationary (oscillating) terms from lambda not equal to 1. The limit is an asymptotic approximation for finite t, exact only as t tends to infinity.

Provenance: `standard_background`. Standard asymptotic formula for random unitary maps given a Hilbert-Schmidt-orthonormal attractor basis; this is the 'asymptotic method' the abstract refers to but the explicit attractors for the 1D chain are a paper result not available here.

Equation assumptions:

- Attractors can be chosen Hilbert-Schmidt orthonormal (Phi is unital so the peripheral part is diagonalizable)

## eq_6: Tiny explicit instance

$$
N=4,\quad C=H=\tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad p=\tfrac12,\quad \rho_0=|1,R\rangle\langle 1,R|,\quad \pi(K)=\tfrac18\ \forall K\subseteq\{(0,1),(1,2),(2,3)\}
$$

Three-qubit instance: 2 position qubits encoding x in {0,1,2,3}, 1 coin qubit; 8 equiprobable edge configurations; walker starts at vertex 1 pointing right.

Provenance: `assumption`. No experiment scope was supplied; this is the smallest qubit-encodable chain with internal edges, chosen to make all 2^{N-1}=8 configurations explicit. The abstract says 'one dimensional chains' but does not give N, p, the coin, or initial state.

Equation assumptions:

- Hadamard coin for the 1D walk
- Uniform percolation probability p=1/2
- Localized initial state

## Registers

- pos: 2 qubits (log2 N for N=4) qubits; binary encoding of the walker position x in {0,1,2,3}; placed first (most significant) in |x,c>
- coin: 1 qubit qubits; coin/direction state, |0>=L, |1>=R; placed last

## Initial state

|psi_0> = |x=1> |c=R> = |01>_pos |1>_coin, i.e. rho_0 = |1,R><1,R| as in eq_6.

## Measurement

Measure the position register (and optionally the coin qubit) in the computational basis at the final step; repeat over many shots and many independently sampled configuration sequences to estimate P_t(x)=<x|Tr_coin rho(t)|x>.

## Classical postprocessing

Average measured position histograms over configuration samples to estimate the diagonal of Phi^t(rho_0); compare with the long-time prediction from eq_5 obtained by classically solving eq_4 for the attractor space of the 2N x 2N unitaries U_K. Note that eq_5 is an asymptotic statement; finite-t estimates differ by decaying transient terms.

## Algorithm steps

1. Prepare the position and coin registers in the localized initial state of eq_6. (eq_1, eq_6)
2. For each time step s=1..t: classically sample a configuration K_s from pi(K) (each edge kept with probability p). (eq_1)
3. Apply the coin operator C to the coin qubit. (eq_3, eq_6)
4. Apply the configuration-dependent conditional shift S_{K_s} (move along present edges, coin-flip reflection at absent edges and chain ends), completing U_{K_s}. (eq_2, eq_3)
5. Repeat coin+shift for t steps; averaging the resulting states over many independent configuration sequences realizes rho(t)=Phi^t(rho_0). (eq_3)
6. Classically (not on the circuit): solve the attractor equations for the 8 unitaries U_K and project rho_0 to obtain the predicted asymptotic state for comparison with large-t sampled statistics. (eq_4, eq_5)

## Assumptions

- Dynamic percolation modelled as i.i.d. Bernoulli(p) edges resampled every step
- Coined discrete-time quantum walk with coin applied before the shift
- Reflecting (coin-flip) rule at broken edges and chain boundaries
- Hadamard coin for the one-dimensional chain
- Instance parameters N=4, p=1/2, initial state |1,R> are chosen by the reconstruction, not taken from the abstract
- Attractor theory for random unitary maps is recalled as background and is not verified here

## Missing information

- The paper's actual rule for the walker at a missing edge (reflection vs. other unitary choices)
- The specific coin operator(s) used for the 1D chain and the chain length / boundary conditions in the paper
- The explicit attractor basis and resulting asymptotic states for the 1D chain (the paper's main result)
- Details of the paper's concrete step-by-step numerical example
- All two-dimensional integer-lattice results with the Grover coin
- Whether the paper treats open (finite chain) or periodic (cycle) boundary conditions
