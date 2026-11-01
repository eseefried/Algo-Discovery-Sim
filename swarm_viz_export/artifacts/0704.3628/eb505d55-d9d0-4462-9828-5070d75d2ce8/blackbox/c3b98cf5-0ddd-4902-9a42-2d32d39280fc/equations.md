# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate the balanced depth-2 NAND formula f(x)=NAND(NAND(x1,x2),NAND(x3,x4)) for explicit classical x in {0,1}^4 with a discrete-time quantum walk on a tree plus tail, with x compiled into gates. The abstract's O(sqrt N) claim for balanced formulas is the motivating goal; the general-formula bound is out of scope.

Scope: Only the N=4 balanced instance. Explicit x is compiled into gates, so no black-box query complexity is certified. The circuit is a fixed unitary walk on a small graph with a tail; the decode is a root-overlap threshold that must be calibrated over all 16 inputs by simulation. If the calibration fails, the circuit is only a walk-dynamics demo. The paper's actual construction is unknown and not reconstructed.

## Symbols

- $x$: input bits; domain: {0,1}^4
- $f(x)$: formula value; domain: {0,1}
- $G$: walk graph: tail vertex t, root r, internal vertices a,b, leaves l1..l4; leaf li is connected to its parent only if x_i=1 (to be calibrated); domain: graph on 8 vertices
- $|v,d\rangle$: edge-directed basis state: vertex v, direction d among its incident edge slots; domain: vertex in 0..7, d in 0..2
- $S$: flip-flop shift swapping |u,e\rangle with |v,e\rangle across edge (u,v); domain: permutation unitary
- $C_v$: degree-aware Grover coin on the deg(v) used slots of vertex v, identity (a -1 phase for a degree-1 vertex) on unused slots; domain: unitary
- $T$: number of walk steps; domain: positive integer, chosen by calibration; O(sqrt N) is a heuristic
- $p$: return probability to the tail edge state; domain: [0,1]

## eq_1: Formula

$$
f(x)=\neg\big(\neg(x_1\wedge x_2)\wedge\neg(x_3\wedge x_4)\big)=(x_1\wedge x_2)\vee(x_3\wedge x_4)
$$

Balanced depth-2 formula, with NAND(a,b)=not(a and b). The NAND of two NANDs equals the OR of the ANDs.

Provenance: `standard_background`. Boolean identity; the instance is a chosen smallest case.

Equation assumptions:

- N=4

## eq_2: Walk step

$$
U_x=S_x\,C_x,\quad C_x=\bigoplus_v C_v(x)
$$

One step: the degree-aware coin at each vertex, then the flip-flop shift over edges present for x. Leaf edges present or absent depend on x, which is compiled into the gates.

Provenance: `assumption`. Standard coined-walk form adapted from the sketch. It corrects the previous flawed global 2-qubit Grover coin. This is not the paper's exact walk.

Equation assumptions:

- The x-dependent edge set is compiled classically
- Absent leaf edges are modeled as a reflecting boundary (the leaf slot acts as a self-loop)
- Unused slots are untouched

## eq_3: Initial state

$$
|\psi_0\rangle=|t,0\rangle
$$

The walker starts on the tail edge slot of the tail vertex that points toward the root, a valid used direction.

Provenance: `assumption`. Fixes the invalid-slot problem in the earlier build: the start must be a used slot.

Equation assumptions:

- Tail vertex t has one slot (0) toward the root

## eq_4: Evolution

$$
|\psi_T\rangle=U_x^{T}|\psi_0\rangle,\quad T=O(\sqrt N)
$$

State after T steps. T is calibrated, with O(sqrt N) steps as the heuristic.

Provenance: `abstract_inferred`. The abstract's sqrt(N) query bound suggests T=O(sqrt N) steps, each using one x-dependent operation.

Abstract evidence: O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- One x-dependent operation per step

## eq_5: Decode statistic

$$
p=|\langle t,0|\psi_T\rangle|^2,\quad \hat f=[p\ \text{on the side of }\theta\text{ matching the reflection regime}]
$$

Threshold on the return probability. By the sketch, reflection corresponds to f=1 and transmission to f=0, but the direction and threshold theta are to be validated over all 16 inputs. The sign convention is unverified.

Provenance: `assumption`. From the sketch, not from the abstract. The runner must verify that the threshold separates the 16 inputs, otherwise report a demo only.

Equation assumptions:

- Threshold theta found by simulation
- Energy near zero is not guaranteed by this finite construction

## Registers

- vertex: 3 qubits qubits; vertex index 0..7: 0 tail, 1 root, 2-3 internal, 4-7 leaves
- slot: 2 qubits qubits; edge slot at the vertex: 0 parent/tail direction, 1-2 child directions; slot 3 unused

## Initial state

|t,0> with vertex=0 and slot=0, prepared explicitly (this is the used tail slot). Qubit ordering is little-endian, slot low bits then vertex.

## Measurement

None inside the unitary. For decoding, measure or compute the probability of |t,0>. No output ancilla is built.

## Classical postprocessing

Threshold p at a calibrated theta to output f(x). If no theta separates all 16 inputs, disclose that the circuit is only a walk-dynamics demo.

## Algorithm steps

1. Prepare |t,0> explicitly, with the tail vertex's single slot pointing to the root. (eq_3)
2. Apply the degree-aware coin at every vertex and the flip-flop shift over the x-dependent edge set. Leaf slots with absent edges reflect. (eq_2)
3. Repeat for T steps, with T calibrated against all 16 inputs. (eq_4)
4. Offline, compute p and compare it to the threshold to decode f(x). This is outside the unitary. (eq_5, eq_1)

## Assumptions

- Scope is limited to depth-2 balanced N=4
- x is compiled into gates, so no black-box query claim
- The edge conventions, the reflecting leaf boundary and T are free choices that need calibration

## Missing information

- The paper's exact walk, weights and phase-estimation procedure
- A validated threshold and T
- The rebalancing procedure for arbitrary formulas
