# Equation to Qiskit

Scoped to a depth-2 balanced NAND tree (N=4). It builds T steps of a coined discrete-time quantum walk on an 8-vertex heap-indexed tree (tail vertex 0, root 1, internal vertices 2-3, leaves 4-7), with x compiled into which leaf edges exist. One step is U = (I x Grover coin) * (x-dependent flip-flop shift), where the shift is built from transpositions of directed-edge basis states using CX and multi-controlled X gates. There is no measurement, no state preparation, and no readout. No query-complexity claim is made, and the general-formula bound is out of scope.

Source equation run: `8ac7c43b-5238-4f4d-a003-4559eaa3edaf`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0-q2: pos register, little-endian vertex heap index (0=tail, 1=root, 2,3=internal vertices, 4-7=leaves for x1..x4)
- q3-q4: coin register, little-endian direction (0=parent, 1=left child, 2=right child, 3=unused)
- Suggested root-edge input |r>: pos=0 (tail), coin=1, i.e. basis index 8; the runner prepares it
- Basis index = pos + 8*coin

## Assumptions

- Heap indexing gives the tree: tail 0, root 1, internal 2-3, leaves 4-7
- Leaf i is connected iff x_i=1
- The unused coin direction 3 is included in the Grover coin
- Basis-state transpositions use CX plus multi-controlled X gates
- Only 5 qubits are used

## Unresolved issues

- It is not established that this walk's root overlap decodes NAND(x) at any threshold or T
- The tail has length 1 and the Grover coin includes a dummy direction, which may distort the spectrum relative to the intended algorithm
- Phase estimation, the energy-near-zero analysis, and the threshold are not implemented
- Arbitrary formulas and rebalancing are out of scope

## Equation mapping

- `eq_1`: background; no code location. The classical NAND formula f(x) is not computed by the circuit. It only motivates the tree topology, and x enters through which leaf edges exist.
- `eq_2`: implemented; build_circuit: swap_states loop over edges (O_x) followed by the Grover coin gates (R_graph) inside the steps loop. One step is U = R_graph O_x. O_x is the x-dependent flip-flop shift with leaf edges present iff x_i=1, and R_graph is a Grover coin on the coin register. Both are concrete choices because the source does not specify them.
- `eq_3`: implemented; build_circuit: for _ in range(steps) loop. The unitary U^T is applied with T=steps. Initial state preparation is left to the runner. The default T=2=sqrt(N) is a placeholder and is not certified.
- `eq_4`: out_of_scope; no code location. The readout overlap p and the threshold decoding are post-processing and are not part of the unitary operation. The threshold is unspecified.

## Specification changes

- eq_2: R_graph is concretely taken as a Grover diffusion (I-2|s><s|) on a 2-qubit coin that includes an unused fourth direction. O_x is the x-dependent flip-flop shift on directed-edge states, not a phase or marking oracle. Reason: The abstract and spec do not give the walk graph, coin, or reflection, so a concrete well-defined unitary walk had to be chosen.
- eq_2, eq_3: Leaf edges are attached to their parent iff x_i=1. Absent edges act as fixed points of the shift (the walker is not moved). Reason: The spec leaves attachment of leaves and the tail unspecified. This is the simplest x-compiled choice, and its correctness for decoding f(x) is unverified.
- eq_3: The initial state is suggested as pos=tail (0) with coin direction 1 (the only physical tail edge), instead of coin |0>. Reason: The tail vertex has only one edge, to the root, so direction 1 is the root-edge state.
- eq_3, eq_4: No claim of O(sqrt N) query complexity. T is a user parameter (default 2, range 1..32) and x is compiled into gates rather than queried. Reason: The source gives no step-count derivation or phase estimation details.
- eq_1: Scope is narrowed to the balanced depth-2, N=4 formula only. Reason: The general-formula algorithm and the rebalancing procedure are not specified.
