# Equation to Qiskit

Qiskit implementation of the Grover-search baseline from eq_5 for triangle finding on a small graph (n<=13 vertices). It builds k iterations of the Grover operator, G = diffusion * oracle, on a register indexing the N=C(n,3) vertex triples. The oracle loads the three queried edge bits of each triple into 3 ancillas by index-controlled X gates, applies a CCZ (the AND of eq_4) and uncomputes. The diffusion is the inversion about the uniform state on the 2^m index space. The circuit has no state preparation, so the runner supplies the uniform superposition. This is NOT the paper's O~(n^{5/4}) algorithm, which is not reconstructed.

Source equation run: `e50bd805-cc0e-4061-b0a2-9499a03d8d87`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: 'triple' register, binary index t of the lexicographically ordered vertex triple (a<b<c), qubit 0 is LSB, m = max(1, ceil(log2 C(n,3)))
- qubit m: edge ancilla for edge (a,b) of the triple, input and output |0>
- qubit m+1: edge ancilla for edge (b,c), input and output |0>
- qubit m+2: edge ancilla for edge (a,c), input and output |0>
- Example n=4: m=2, triple qubits 0-1 (indices 0..3 = triples {0,1,2},{0,1,3},{0,2,3},{1,2,3}), edge ancillas 2,3,4; 5 qubits total
- Expected input: uniform superposition over the triple register (prepared by the runner), ancillas |0>

## Assumptions

- Undirected simple graph; duplicate edges are merged and edge orientation is ignored.
- Triples are enumerated lexicographically with a<b<c, and triple index t is the computational-basis value of the index register (qubit 0 LSB).
- The runner prepares the uniform superposition over the index register and leaves the ancillas in |0>.
- Vertex count n is limited to 3..13 so that the total qubits m+3 are at most 12.

## Unresolved issues

- The paper's actual combinatorial algorithm achieving O~(n^{5/4}) is not reconstructed.
- Optimal iteration counts depend on the number of marked triples, which the circuit does not compute.
- For N not a power of two, the diffusion over the padded index space only approximates uniform-over-N Grover search.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Claimed O~(n^{5/4}) query complexity of the paper's algorithm; an asymptotic statement, and the algorithm is not reconstructed.
- `eq_2`: out_of_scope; no code location. Previous O(n^{9/7}) upper bound, cited comparison only.
- `eq_3`: out_of_scope; no code location. Cited lower bound for the edge-weighted problem; no circuit content.
- `eq_4`: implemented; _oracle_edge_load plus the qc.ccz call in build_circuit. Edge bits x_ab, x_bc, x_ac of each triple are loaded into ancillas by index-controlled X gates (graph data from the instance edge list). The CCZ computes their AND as a phase, and the load is then uncomputed.
- `eq_5`: implemented; build_circuit loop (oracle, then _diffusion). Grover iterate: phase oracle O_T followed by diffusion about the uniform state, repeated 'iterations' times. The uniform-state preparation is left to the runner. The phase-kickback qubit is replaced by a direct CCZ.

## Specification changes

- eq_5: Dropped the |-> phase-kickback qubit and used a CCZ on the 3 edge ancillas for the phase flip, so the circuit has 3 ancillas instead of 4 non-index qubits. Reason: A CCZ is the standard equivalent of Toffoli plus a |-> target and needs one qubit less.
- eq_5: The diffusion reflects about the uniform state over all 2^m basis states of the index register. Indices >= C(n,3) are unmarked padding. The circuit takes the iteration count as an instance parameter, with no automatic optimal choice. Reason: When C(n,3) is not a power of two, a diffusion on exactly N states would need a state-preparation unitary, which the runner is supposed to supply. Only n=4 gives N=4 exactly.
- eq_4, eq_5: The graph edges are classical instance data compiled into index-controlled gates, not a black-box adjacency query oracle. Reason: Qiskit circuits cannot call a quantum query oracle. The edge loads emulate 3 queries per oracle call.
- eq_1, eq_2, eq_3: Scope narrowed to the Grover baseline circuit. The paper's O~(n^{5/4}) algorithm is not implemented and the complexity claims are not encoded. Reason: The abstract gives no algorithmic or circuit details.
