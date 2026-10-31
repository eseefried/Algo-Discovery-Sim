# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Determine whether a coined discrete-time quantum walk on a cycle-like graph achieves perfect state transfer (PST) between antipodal nodes, i.e. whether there is a step count t at which the walker, started at node 0, is found at node N/2 with probability exactly 1. The abstract studies this for modified versions of C4, C6, C8 and three coin operators, and reports generalised graph families with periodicity, PST or high-fidelity transfer.

Scope: Smallest useful construction chosen by assumption (no experiment_scope supplied): the unmodified cycle C4 (N=4) with a coined DTQW using the degree-2 Grover coin (which equals Pauli X) and a flip-flop shift, with initial state localised at node 0. In this instance antipodal PST 0 -> 2 occurs at t=2 and the walk is periodic with period 4; this serves as the baseline against which the paper's cycle modifications are compared. Outside scope: the specific modifications of C4/C6/C8 that preserve PST, the identity of the three coin operators used in the paper, the three generalised graph families, the continuous-time walk results, interpolation between structures, and the decoherence model.

## Symbols

- $N$: Number of nodes of the cycle C_N; antipodal node of 0 is N/2; domain: even positive integer; instance N=4
- $v$: Node (position) label on the cycle; domain: \mathbb{Z}_N = \{0,\dots,N-1\}
- $c$: Coin (direction) label: c=0 points to neighbour v+1, c=1 points to neighbour v-1 (mod N); domain: \{0,1\}
- $C$: Coin operator acting on the coin register at each node (assumed identical at every node for the regular instance); domain: 2\times 2 unitary matrix
- $S$: Flip-flop shift operator on the arc space; domain: unitary on \mathbb{C}^N\otimes\mathbb{C}^2
- $U$: One step of the discrete-time quantum walk; domain: unitary on \mathbb{C}^N\otimes\mathbb{C}^2
- $t$: Number of walk steps; domain: non-negative integer
- $|\psi_0\rangle$: Initial state, localised at node 0 with some coin state; domain: unit vector in \mathbb{C}^N\otimes\mathbb{C}^2
- $F(t)$: Transfer fidelity: probability of finding the walker at the antipodal node N/2 after t steps; domain: [0,1]

## eq_1: Walk Hilbert space and state

$$
|\psi\rangle=\sum_{v\in\mathbb{Z}_N}\sum_{c\in\{0,1\}} a_{v,c}\,|v\rangle\otimes|c\rangle,\qquad \sum_{v,c}|a_{v,c}|^2=1
$$

State of a coined DTQW on the cycle: position register tensored with a two-dimensional coin register (one coin state per neighbour of a degree-2 node).

Provenance: `standard_background`. Standard position-coin formulation of a coined discrete-time quantum walk on a 2-regular graph.

Equation assumptions:

- Position register ordered first (most significant), coin register second
- v encoded in binary with \lceil\log_2 N\rceil qubits

## eq_2: Grover coin (degree d) and its degree-2 form

$$
G_d=\frac{2}{d}J_d-I_d,\qquad G_2=\begin{pmatrix}0&1\\1&0\end{pmatrix}=X
$$

Grover diffusion coin on a degree-d node (J_d is the all-ones matrix); at degree 2 it reduces to Pauli X.

Provenance: `standard_background`. The Grover coin is the standard choice for DTQWs on general graphs; the abstract mentions 'three choices of coin operator' without naming them, so Grover is adopted as an assumption for the instance.

Equation assumptions:

- The Grover coin is one of the paper's three coins (not stated in the abstract)

## eq_3: Flip-flop shift on the cycle

$$
S\,|v\rangle|c\rangle=|v+(-1)^{c}\bmod N\rangle\,|c\oplus 1\rangle
$$

Moves the walker to the neighbour selected by the coin and flips the coin so that it points back along the traversed edge (arc reversal). Addition is modular on \mathbb{Z}_N.

Provenance: `standard_background`. Flip-flop shift is the standard graph-independent shift for DTQWs on arbitrary graphs; it is an assumption that the paper uses it rather than a moving shift.

Equation assumptions:

- Flip-flop (arc-reversing) shift rather than a moving shift

## eq_4: Walk operator and evolution

$$
U=S\,(I_N\otimes C),\qquad |\psi_t\rangle=U^{t}|\psi_0\rangle
$$

One DTQW step applies the coin at every node and then the shift; t steps give U^t.

Provenance: `standard_background`. Standard coined DTQW composition; node-independent coin assumed because the regular cycle instance has uniform degree.

Equation assumptions:

- Same coin C at every node (valid for the regular cycle; modified cycles may need node-dependent coins)

## eq_5: Antipodal transfer fidelity and PST condition

$$
F(t)=\sum_{c\in\{0,1\}}\left|\langle N/2|\langle c|\,U^{t}\,|\psi_0\rangle\right|^2,\qquad \text{PST}\iff \exists\,t\ge1:\ F(t)=1
$$

Probability of finding the walker at the antipodal node after t steps (summed over coin states); perfect state transfer means this probability equals 1 exactly for some t.

Provenance: `abstract_inferred`. The abstract states PST between antipodal nodes is studied; the vertex-occupation-probability definition of transfer fidelity is the usual one for DTQWs, but the paper's precise fidelity definition (e.g. whether coin state must also be transferred) is not given.

Abstract evidence: perfect state transfer between antipodal nodes of discrete time quantum walks

Equation assumptions:

- Fidelity defined by position occupation probability, tracing out the coin

## eq_6: Instance result: PST and periodicity on C4 with coin X

$$
U|v\rangle|c\rangle=|v-(-1)^{c}\bmod 4\rangle|c\rangle,\qquad U^{2}|0\rangle|c\rangle=|2\rangle|c\rangle,\qquad U^{4}=I
$$

With C=X and the flip-flop shift on C4 the walker moves persistently in one direction, reaching the antipodal node 2 exactly at t=2 (F(2)=1 for any initial coin state) and returning at t=4 (period 4). Equalities are exact.

Provenance: `assumption`. Direct composition of eq_2, eq_3, eq_4 for N=4: X maps c to c\oplus1, then S moves to v+(-1)^{c\oplus1}=v-(-1)^{c} and flips the coin back to c. This is a baseline instance chosen by the reconstruction, not a result reported in the abstract.

Equation assumptions:

- N=4, C=X, flip-flop shift, initial state localised at node 0

## Registers

- position: 2 qubits; Encodes node v\in\{0,1,2,3\} of C4 in binary (v = 2 v_1 + v_0); most significant register in |v\rangle|c\rangle ordering
- coin: 1 qubits; Encodes direction c\in\{0,1\} (c=0: toward v+1, c=1: toward v-1 mod 4)

## Initial state

|\psi_0\rangle=|0\rangle_{\text{pos}}\otimes|0\rangle_{\text{coin}} (walker at node 0, coin pointing toward node 1); by eq_6 any coin state at node 0 gives the same antipodal transfer in this instance.

## Measurement

Measure both position qubits in the computational basis; the coin qubit may be measured and discarded. The outcome v=2 (binary 10) corresponds to the antipodal node; its frequency estimates F(t).

## Classical postprocessing

Estimate F(t) as the fraction of shots with position outcome 2. For the C4/X instance the exact prediction is F(2)=1 and F(4)=0 with return to node 0; deviations beyond shot noise indicate circuit error. PST is declared when F(t)=1 within statistical tolerance.

## Algorithm steps

1. Prepare the position register in |0\rangle and the coin register in |0\rangle. (eq_1)
2. Apply the coin operator C = X to the coin register (degree-2 Grover coin). (eq_2, eq_4)
3. Apply the flip-flop shift: controlled on coin c=0 increment the position mod 4, controlled on c=1 decrement mod 4, then apply X to the coin register. (eq_3, eq_4)
4. Repeat the coin and shift steps to reach the desired step count; for the C4 instance use t=2 (expected PST) and optionally t=4 (expected return to the initial state). (eq_4, eq_6)
5. Measure the position register and estimate the antipodal occupation probability F(t). (eq_5)

## Assumptions

- No experiment_scope was supplied; the unmodified C4 with Grover (=X) coin and flip-flop shift was chosen as the smallest useful instance
- The three coin operators in the paper are not named in the abstract; Grover was assumed for the instance
- The flip-flop shift convention and position-first register ordering are reconstruction choices
- Transfer fidelity is taken as antipodal-node occupation probability with the coin traced out
- The paper's cycle modifications (added edges, self-loops, pendant vertices, weights, etc.) are unknown and were not reconstructed; the modified graphs would generally require node-dependent coin dimensions and a general arc-space formulation

## Missing information

- Which specific modifications of C4, C6, C8 were investigated and which few preserve PST
- Identity of the three coin operators (e.g. Grover, Fourier/DFT, Hadamard are plausible but unstated)
- Definition of the three generalised graph families and their node counts
- Precise fidelity/PST definition used (coin-state transfer vs vertex occupation)
- Continuous-time walk Hamiltonian (adjacency vs Laplacian) and transfer times for the families
- Initial conditions (coin states) under which PST or high-fidelity transfer occurs on the modified graphs
- Interpolation scheme between structures and the decoherence model used in robustness tests
- Any quantitative fidelity values or transfer times reported in the paper
