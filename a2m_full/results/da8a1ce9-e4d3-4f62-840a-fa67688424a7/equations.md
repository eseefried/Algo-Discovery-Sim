# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate a balanced binary NAND formula on N=4 leaves (depth-2 tree, value NAND(NAND(x0,x1),NAND(x2,x3))) with a discrete-query quantum walk, using one phase-oracle query per walk step and majority vote on the readout.

Scope: One tiny instance: a 4-leaf balanced NAND tree with an attached tail, a discrete-time walk with oracle-dependent leaf behaviour, a scattering-style readout, and a majority vote. Outside scope: the arbitrary-formula algorithm (rebalancing, weighted trees, phase estimation, N^{1/2+O(1/sqrt(log N))} cost) and any proof of the stated complexities.

## Symbols

- $N$: number of formula leaves; domain: positive integer, 4 here
- $x_i$: input bit at leaf i; domain: {0,1}, i in 0..N-1
- $O_x$: black-box phase oracle on the leaf register, placed once per walk step; domain: unitary, |i> -> (-1)^{x_i}|i>
- $U$: one walk step (oracle, coin/diffusion, shift); domain: unitary on vertex, coin and ancilla registers
- $T$: number of walk steps; domain: integer, about c*sqrt(N)
- $L$: tail length; domain: integer, about c'*sqrt(N)
- $k$: wave number of the incoming plane wave; domain: real, near 0 or about pi/4 (tuned numerically)
- $f(x)$: NAND formula value; domain: {0,1}

## eq_1: NAND recursion

$$
f(x)=\mathrm{NAND}(f_L(x),f_R(x)),\quad \mathrm{NAND}(a,b)=1-ab
$$

Recursive value of the balanced formula; for N=4 f=NAND(NAND(x0,x1),NAND(x2,x3)).

Provenance: `standard_background`. Definition of a binary NAND formula; the abstract only names it.

Equation assumptions:

- Balanced binary tree with N=4 leaves

## eq_2: Leaf phase oracle

$$
O_x|i\rangle=(-1)^{x_i}|i\rangle
$$

The black box acts on the leaf index and marks leaves by phase. A placeholder is placed once per step.

Provenance: `assumption`. Taken from the sketch's phase-oracle model; the abstract only says 'discrete query'.

Equation assumptions:

- Oracle acts as identity on non-leaf vertices (controlled on a leaf flag)

## eq_3: Walk step

$$
U=S\,C_x,\quad C_x=\bigoplus_v \big(2|\phi_v\rangle\langle\phi_v|-I\big)\cdot O_x\text{ on leaves}
$$

Shift S along tree edges composed with a per-vertex Grover/Szegedy-type reflection, with leaf behaviour set by one oracle call.

Provenance: `assumption`. Sketch-based construction. The exact coin weights and leaf rule of the cited discrete-query walk are not given in the abstract.

Equation assumptions:

- Coin vector phi_v is uniform over the edges at v for the unweighted tree

## eq_4: Tail plane-wave initial state

$$
|\psi_0\rangle=\frac{1}{\sqrt{L+1}}\sum_{j=-L}^{0}e^{-ikj}|j\rangle|\text{coin}_{\rightarrow}\rangle
$$

Incoming wave on the tail attached at the root, moving toward the tree.

Provenance: `assumption`. From the sketch; the amplitude profile and k are tuned numerically.

Equation assumptions:

- Tail vertices j=-L..0 are joined to the root

## eq_5: Query count and readout

$$
|\psi_T\rangle=U^{T}|\psi_0\rangle,\quad T=\Theta(\sqrt N),\quad p_{\mathrm{refl}}=\sum_{j\le 0}\|\Pi_j\psi_T\|^2,\quad \hat f=\mathbb 1[p_{\mathrm{refl}}<\theta]
$$

T queries are used in total. A large reflected probability is read as f=0 and a small one as f=1. The threshold theta is set from simulation.

Provenance: `abstract_inferred`. The abstract's O(sqrt N) query claim implies T=Theta(sqrt N) steps with one query each. The readout rule is from the sketch.

Abstract evidence: We present an O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- Tail on the incoming side is the 'reflected side'
- theta is tuned numerically

## Registers

- vertex: about ceil(log2(2N+L+O(1))) qubits qubits; tree node or tail position
- coin: 2 qubits qubits; direction: parent, left child, right child
- anc: 1 qubit qubits; query ancilla and leaf flag for the oracle phase

## Initial state

Tail plane-wave state of eq_4 on the vertex register, with coin set to the toward-root direction and the ancilla in |0>. Preparing it needs standard-gate rotations, not initialize.

## Measurement

Measure the vertex register only. In Qiskit, bit i holds vertex-index bit i (little-endian). Classify the outcome as tail (reflected side) or tree side by index range.

## Classical postprocessing

Estimate p_refl, compare with the tuned threshold theta, and take the majority vote over a constant number of repetitions.

## Algorithm steps

1. Prepare the tail plane-wave state with standard gates. (eq_4)
2. Repeat T times: apply the oracle placeholder once, then the coin reflection, then the edge shift. (eq_2, eq_3, eq_5)
3. Measure the vertex register, flag the tail side as reflected, and estimate p_refl over repeated runs. (eq_5)
4. Take the majority of a constant number of runs as the value of the formula, and compare with eq_1 on the test instance. (eq_1, eq_5)

## Assumptions

- The N=4 instance is chosen by me because no scope was given
- Walk details such as coin weights, leaf rule, k, L and T are my assumptions, tuned numerically
- The arbitrary-formula algorithm is out of scope

## Missing information

- Exact discrete-time walk operator and leaf rule of the cited algorithm
- Precise tail length, k, T and threshold
- Rebalancing and weighted-edge construction for arbitrary formulas
- Whether the true method reads out by reflection probability or by phase estimation
