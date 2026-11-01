# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a 4-bit reversible function pi (a permutation of {0..15}), find a Toffoli network of NOT, CNOT, TOF3 and TOF4 gates realizing pi with minimum quantum cost QC, then build the measurement-free unitary U_pi from that network.

Scope: One tiny explicit 4-bit permutation pi is given as an input table. A classical offline Dijkstra over the Cayley graph of S_16 with the full NCT+TOF4 gate library (all control/target placements, costs 1/1/5/13) finds a min-QC network. The network is compiled to x, cx, ccx, mcx gates and checked against pi on all 16 basis states. The search is a stand-in for the paper's gate-count-optimal tool, whose internals are unknown. Out of scope: the paper's benchmarks, its actual tool, the 74% saving, and any optimality claim about the paper's circuits. The quantum circuit itself only implements the found permutation; the optimization is classical preprocessing, not quantum.

## Symbols

- $x$: 4-bit input integer x=sum_i x_i 2^i; qubit q_i holds x_i (little-endian); domain: {0,...,15}
- $\pi$: target permutation of basis states, given as an explicit table in the instance; domain: S_{16}
- $g$: library gate viewed as a permutation of {0..15}; domain: NOT (4), CNOT (12), TOF3 (12), TOF4 (4) placements on 4 wires; 32 gates total
- $qc(g)$: quantum cost of gate g (convention); domain: {1,5,13}
- $QC(C)$: total quantum cost of network C; domain: non-negative integers
- $d(\sigma)$: minimum QC found to reach permutation sigma from the identity; domain: non-negative integers or infinity
- $U_\pi$: permutation unitary on 4 qubits; domain: 16x16 unitary

## eq_1: Toffoli gate as Boolean map

$$
\mathrm{TOF3}(a,b,c)=(a,\,b,\,c\oplus ab),\quad \mathrm{TOF4}(a,b,c,d)=(a,b,c,\,d\oplus abc)
$$

Action of the Toffoli gates on basis bits: the target is flipped when all controls are 1. This defines each library gate as a permutation of {0..15}. The specialist's prediction Toff(A,B,C)=AB xor AC xor BC xor ABC is rejected because it is the majority-like expression and not the Toffoli map.

Provenance: `standard_background`. Standard definition of multiple-control Toffoli gates; the abstract names Toffoli networks only.

Equation assumptions:

- controls are distinct from the target

## eq_2: Permutation unitary

$$
U_\pi=\sum_{x=0}^{15}|\pi(x)\rangle\langle x|=G_k\cdots G_1,\quad \pi=g_k\circ\cdots\circ g_1
$$

Target unitary maps |x> to |pi(x)> in little-endian encoding and equals the product of gate unitaries of a realizing network.

Provenance: `assumption`. Chosen encoding of a reversible function as a unitary for the tiny instance.

Equation assumptions:

- little-endian encoding, qubit q_i = bit i

## eq_3: Quantum cost of a network

$$
QC(C)=\sum_{j=1}^{k}qc(G_j),\quad qc(\mathrm{NOT})=qc(\mathrm{CNOT})=1,\ qc(\mathrm{TOF3})=5,\ qc(\mathrm{TOF4})=13
$$

Additive cost model with commonly used values.

Provenance: `standard_background`. Conventional NCT cost table recalled from background; the abstract only mentions QC without values.

Equation assumptions:

- standard cost table; TOF4=13 is a convention

## eq_4: QC-minimal synthesis by Dijkstra

$$
d(\mathrm{id})=0,\quad d(g\circ\sigma)=\min\big(d(g\circ\sigma),\,d(\sigma)+qc(g)\big),\quad C^*=\arg\min_{C:\,\pi_C=\pi}QC(C)
$$

Dijkstra over permutations of {0..15} with edge weights qc(g), started from the identity and run until pi is settled. The first-settled path gives a provably QC-minimal network for the given library.

Provenance: `assumption`. The abstract states the goal of exact QC reduction using a gate-count-optimal tool; Dijkstra is a proposed stand-in, not the paper's method.

Equation assumptions:

- search replaces the paper's tool
- full S_16 is about 2.1e13 states, so the reachable search is feasible only for pi of small cost; pruning at the cost of pi is used

## eq_5: Saving percentage

$$
S=100\,\frac{QC_{old}-QC_{new}}{QC_{old}}
$$

Relative QC saving of the found network against a baseline network.

Provenance: `abstract_inferred`. Percentage saving is inferred from the abstract claim; the formula is the standard definition.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

Equation assumptions:

- QC_old is the baseline network cost

## Registers

- q: 4 qubits; data qubits q0..q3, little-endian; basis state |x> maps to |pi(x)>; no ancillas

## Initial state

Any computational basis state |x>, x in 0..15; for verification, all 16 basis states (the full unitary).

## Measurement

None in the circuit; output decoded by reading the computational-basis state as pi(x), little-endian.

## Classical postprocessing

Offline Dijkstra search for the min-QC network, verification against pi, and the saving percentage.

## Algorithm steps

1. Take the instance input pi as an explicit table over {0..15} and an optional baseline network, and define each library gate as a permutation. (eq_1, eq_2)
2. Assign costs and compute the baseline QC if a baseline is given. (eq_3)
3. Run classical Dijkstra from the identity over the gate library until pi is settled; recover the min-QC gate sequence by predecessor links. (eq_4)
4. Compile the sequence to x, cx, ccx, mcx (measurement-free, applied in order G_1..G_k). Check that U|x>=|pi(x)> for all 16 x, and compute S if a baseline exists. (eq_2, eq_5)

## Assumptions

- Tiny explicit pi chosen by the team, not from the abstract
- Standard NCT/TOF4 cost table
- Dijkstra search stands in for the paper's optimal-synthesis tool
- The circuit builder must include the search, taking pi as input, and must not accept a precomputed network as the only input

## Missing information

- Internals of the gate-count-optimal tool
- The paper's benchmark functions and circuits
- The exact cost model used in the paper
