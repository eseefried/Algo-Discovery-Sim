# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a 4-bit reversible function pi (permutation of {0..15}), find a Toffoli network (NOT, CNOT, TOF3, TOF4) realizing pi with minimum quantum cost QC, and build the corresponding measurement-free unitary U_pi.

Scope: One tiny explicit 4-bit permutation, classical offline Dijkstra search over the Cayley graph of the NCT-plus-TOF4 gate library, then compilation of the resulting network to x, cx, ccx, mcx gates. The paper's actual gate-count-optimal tool, its benchmarks and the 74% saving are out of scope.

## Symbols

- $x$: 4-bit input integer, x=sum_i x_i 2^i, qubit q_i holds x_i (little-endian); domain: {0,...,15}
- $\pi$: target permutation of basis states; domain: S_{16}
- $g$: library gate viewed as a permutation of {0..15}; domain: set of NOT, CNOT, TOF3, TOF4 on 4 wires with all control/target choices
- $qc(g)$: standard quantum cost of gate g; domain: {1,5,13}
- $QC(C)$: total quantum cost of network C; domain: positive integers
- $U_\pi$: permutation unitary on 4 qubits; domain: 16x16 unitary

## eq_1: Permutation unitary

$$
U_\pi=\sum_{x=0}^{15}|\pi(x)\rangle\langle x|
$$

Target unitary mapping each basis state to its image under pi, little-endian encoding.

Provenance: `assumption`. Standard encoding of a reversible function as a unitary; chosen for the tiny instance, not stated in the abstract.

Equation assumptions:

- little-endian encoding

## eq_2: Network composition

$$
U_\pi=G_k\cdots G_1,\quad \pi=g_k\circ\cdots\circ g_1
$$

A Toffoli network realizes pi as a product of gate permutations.

Provenance: `standard_background`. Background on reversible circuits composed of Toffoli-class gates.

## eq_3: Quantum cost of a network

$$
QC(C)=\sum_{j=1}^{k}qc(G_j),\quad qc(\mathrm{NOT})=qc(\mathrm{CNOT})=1,\ qc(\mathrm{TOF3})=5,\ qc(\mathrm{TOF4})=13
$$

Additive cost model with the commonly used standard costs.

Provenance: `standard_background`. Common NCT quantum cost values recalled from background; the abstract only mentions quantum cost (QC).

Equation assumptions:

- standard cost table

## eq_4: QC-minimal synthesis

$$
C^*=\arg\min_{C:\,U_C=U_\pi}QC(C),\quad d(\sigma g)=\min\big(d(\sigma g),d(\sigma)+qc(g)\big)
$$

Dijkstra on the Cayley graph of S_16 with edge weight qc(g), starting from the identity, until pi is reached.

Provenance: `assumption`. The abstract states the goal of reducing QC with an exact gate-count tool; the Dijkstra search is a proposed stand-in for the tool, whose internals are unknown.

Equation assumptions:

- the search replaces the paper's tool

## eq_5: Saving percentage

$$
S=100\,\frac{QC_{old}-QC_{new}}{QC_{old}}
$$

Relative quantum cost saving versus a baseline circuit.

Provenance: `abstract_inferred`. The percentage saving is inferred from the abstract's claim; the exact formula is the standard definition.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

## Registers

- q: 4 qubits; data qubits q0..q3, little-endian; computational basis state |x> maps to |pi(x)>

## Initial state

Any computational basis state |x>, x in 0..15, or the full basis for unitary verification; no ancillas.

## Measurement

None in the circuit; the output is decoded by reading the computational basis state as pi(x) (little-endian).

## Classical postprocessing

Offline classical search for the min-QC network and calculation of the saving percentage.

## Algorithm steps

1. Fix a small instance pi, for example a 4-bit permutation given explicitly, and a baseline GC-optimal network. (eq_1, eq_2)
2. Assign standard quantum costs to the gates and compute the baseline QC. (eq_3)
3. Run Dijkstra over permutations with the gate library to find the min-QC network for pi. (eq_4)
4. Compile the chosen network to x, cx, ccx, mcx gates, measurement-free, and check U|x>=|pi(x)> for all 16 x. Compute the saving. (eq_1, eq_5)

## Assumptions

- Tiny explicit instance chosen by the team, not from the abstract
- Standard NCT/TOF4 quantum cost table
- Dijkstra search stands in for the paper's optimal-synthesis tool

## Missing information

- Internals of the gate-count-optimal tool
- The paper's benchmark functions and circuits
- The exact cost model used in the paper
