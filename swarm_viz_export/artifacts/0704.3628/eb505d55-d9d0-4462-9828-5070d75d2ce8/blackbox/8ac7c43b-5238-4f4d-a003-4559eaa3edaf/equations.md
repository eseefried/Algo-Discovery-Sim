# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate a balanced binary NAND formula (depth 2, N=4 leaves, explicit classical input x) via a discrete-time quantum walk whose phase is compiled from x. The scoped instance is the balanced depth-2 tree only, NAND(NAND(x1,x2),NAND(x3,x4)).

Scope: Build a fixed unitary U=R_graph*O_x on a small tree-graph walk space for the balanced depth-2 instance, with x compiled into gates. The O(sqrt N) scaling is not certified, and no black-box query complexity is claimed. The general-formula bound N^{1/2+O(1/sqrt(log N))} is out of scope. The decoding threshold, the walk and reflection details, and the exact attachment of the tail are not derived from the abstract.

## Symbols

- $N$: number of leaves; domain: positive integer, N=4 for the instance
- $x$: input bit string; domain: {0,1}^4
- $f(x)$: NAND formula value; domain: {0,1}
- $O_x$: unitary compiled from known x that marks leaf edges; domain: unitary on the walk space
- $R_graph$: fixed reflection or diffusion on each vertex star; domain: unitary on the walk space
- $U$: one walk step; domain: unitary on the walk space
- $T$: number of walk steps; domain: positive integer, T=O(sqrt N)
- $|r\rangle$: initial root-edge (tail) state; domain: basis state of the position register

## eq_1: Formula for the instance

$$
f(x)=\neg\big(\neg(x_1\wedge x_2)\wedge\neg(x_3\wedge x_4)\big)
$$

Depth-2 balanced NAND tree on 4 leaves, written with NAND(a,b)=not(a and b).

Provenance: `standard_background`. The abstract names balanced binary NAND formulas; the depth-2 case is a chosen smallest instance.

Equation assumptions:

- Instance choice N=4

## eq_2: Walk step

$$
U=R_{\mathrm{graph}}\,O_x
$$

One discrete walk step: the x-dependent oracle followed by a fixed reflection.

Provenance: `assumption`. Taken from the method sketch. This is a proposed construction, not stated in the abstract.

Equation assumptions:

- x is compiled classically into gates
- the exact form of R_graph is not specified

## eq_3: Evolved state

$$
|\psi_T\rangle=U^{T}|r\rangle,\quad T=O(\sqrt N)
$$

State after T steps from the root-edge initial state.

Provenance: `abstract_inferred`. The abstract's O(sqrt N) query claim suggests T=O(sqrt N) walk steps, each using one query-like O_x.

Abstract evidence: O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- one O_x per step

## eq_4: Readout statistic

$$
p=|\langle r|\psi_T\rangle|^2
$$

Overlap with the initial state, compared to a threshold. By the sketch, a value near 1 (reflection) corresponds to f=1 and a value near 0 (transmission) to f=0.

Provenance: `assumption`. Taken from the method sketch. The threshold and the walk details are unverified.

Equation assumptions:

- energy near zero
- threshold to be calibrated by simulation

## Registers

- pos: ceil(log2 V) qubits, V=vertex or edge count (about 8 for the tree plus tail) qubits; position over tree vertices, leaf edges, and the root tail
- coin: 2 qubits (assumed) qubits; edge or direction register within a vertex star

## Initial state

|r> on pos, the root-edge/tail vertex, with coin in |0>

## Measurement

Measure (or classically compute, in simulation) the probability of the root-edge state; no measurement is included in the unitary itself.

## Classical postprocessing

Threshold p to output f(x). The threshold value is not specified.

## Algorithm steps

1. Prepare the root-edge state |r>. (eq_3)
2. Apply O_x, compiled from the known x, to attach leaf edges with x_i=1 and detach those with x_i=0. (eq_2)
3. Apply the fixed star reflection R_graph. Repeat for T steps. (eq_2, eq_3)
4. Compute the root overlap p and compare with a threshold to decode f(x). (eq_4, eq_1)

## Assumptions

- Scope is limited to depth-2 balanced N=4
- x is compiled into gates, so no black-box query complexity is claimed
- the encoding of vertices into pos and coin is a free choice

## Missing information

- Exact walk graph, weights and coin operators
- The correct reflection operators and phase-estimation details
- Threshold and T for the instance
- Rebalancing procedure for arbitrary formulas
