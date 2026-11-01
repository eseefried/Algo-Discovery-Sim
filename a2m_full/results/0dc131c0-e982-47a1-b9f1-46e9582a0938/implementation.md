# Equation to Qiskit

Builds T repetitions of a discrete-time quantum-walk step on a balanced binary tree with 2^depth leaves (default depth 2, N=4 leaves) plus a path tail attached at the root. Each step applies one leaf phase oracle O_x, a per-vertex Grover coin, and a flip-flop edge shift. Only the unitary walk U^T is built. Tail plane-wave preparation, measurement, threshold and majority vote are left to the runner. The leaf rule is my own design, and the circuit is not claimed to compute NAND.

Source equation run: `da8a1ce9-e4d3-4f62-840a-fa67688424a7`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Example (depth=2, tail_length=4: 7 tree vertices + 4 tail = 11 vertices, nv=4):
- qubits 0-3: vertex register, little-endian (qubit 0 = LSB of vertex index)
- vertex index: tree nodes in heap order, root=0, children of v are 2v+1 and 2v+2, leaf i = 2^depth-1+i (3..6 here), tail vertex j = (2^(depth+1)-1)+j (7..10), j=0 adjacent to root
- qubits 4-5: coin register, little-endian slot index; slot 0 = parent (tail vertices: away from tree), slot 1 = left child (tail vertices: toward tree), slot 2 = right child, slot 3 unused
- qubit 6: anc, query/flag ancilla, must be |0> on input and is returned to |0>
- General: nv = max(2, ceil(log2(total vertices))), total qubits = nv+3 <= 12

## Assumptions

- Coin vector is uniform over the real edges at each vertex
- Tail is a path of tail_length vertices attached to the root, with a reflecting end
- Anc is |0> on input and is restored to |0> by every flag compute/uncompute
- The slot-3 coin state is never populated when the input has coin slots in 0..2 on valid vertices

## Unresolved issues

- The cited algorithm's true leaf rule, coin weights and readout are unknown, so no claim is made that this walk separates f=0 from f=1
- Good values of tail_length, steps and wave number k, and the threshold, are untuned
- Tail plane-wave initial state must be prepared by the runner, and amplitudes on invalid (vertex, slot) basis states are not handled
- Oracle is built from the explicit string x, not a hidden black box

## Equation mapping

- `eq_1`: background; no code location. NAND recursion defines the target function f(x). The circuit does not evaluate it classically, and nothing in the circuit is claimed to compute it.
- `eq_2`: implemented; _step: oracle block (leaf flag on anc, then Z on anc). The phase oracle (-1)^{x_i} on leaf vertex i is realized once per walk step as an x-dependent pattern-controlled phase on the vertex register, using anc as a leaf flag. It acts as identity on non-leaf vertices.
- `eq_3`: implemented; _step: coin blocks and flip-flop shift (_swap_states, _edges). One walk step is shift after coin after oracle. The coin is the Grover reflection 2|phi><phi|-I with uniform phi: a 3-slot coin on degree-3 vertices, a slot swap on degree-2 tail vertices, and identity on degree-1 vertices. The shift is a flip-flop permutation built from basis-state swaps on edge arcs.
- `eq_4`: out_of_scope; no code location. Initial-state preparation is done by the runner, so the tail plane-wave state is not prepared in this operation.
- `eq_5`: implemented; build_circuit: loop of `steps` calls to _step. U^T is implemented with T = instance['steps'] and tail length L = instance['tail_length']. The readout p_refl, threshold theta and majority vote are classical and not part of the circuit.

## Specification changes

- eq_2, eq_3: Leaf rule fixed as a pure phase reflection: the leaf coin is the identity and the oracle gives phase (-1)^{x_i}. The oracle is built as x-dependent phase gates from the bit string in the instance. Reason: The abstract and spec do not give the leaf rule. This is a design choice that makes the oracle a known-string phase circuit, not a true black box. It is not claimed to implement the cited algorithm.
- eq_3: The shift is specified explicitly as flip-flop over arcs (v, slot) with slots 0=parent, 1=left, 2=right. Degree-2 tail vertices use slots 0 (away from tree) and 1 (toward tree). The coin on 2 qubits has one unused slot. Reason: The spec leaves the shift and coin encoding unspecified. A concrete unitary permutation with standard gates is needed.
- eq_4: Tail plane-wave state preparation excluded from the circuit. Reason: The task requires an operation with inputs prepared by the runner. k is therefore not a circuit parameter.
- eq_5: Scope narrowed to the unitary U^T. Readout, threshold theta and majority voting are omitted. T and L are free instance parameters (steps <= 40, tail_length <= 32) rather than c*sqrt(N). Reason: Measurements and classical postprocessing are forbidden in the circuit. The constants are unresolved.
- eq_1, eq_2, eq_3, eq_4, eq_5: Instance family limited to balanced trees of depth 1..3 (N = 2, 4 or 8 leaves). The arbitrary-formula algorithm (rebalancing, weighted edges, phase estimation) is excluded. Reason: The spec's declared scope is the balanced binary tree, and the 12-qubit cap applies.
