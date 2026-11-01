# Equation to Qiskit

Trotterized quantum phase estimation of U=exp(iAt) for a user-supplied weighted bipartite graph. The vertex register uses n qubits, with vertex v encoded as binary basis state |v>. Each edge term exp(i w tau (|a><b|+|b><a|)) is a CX-conjugated, multi-controlled RX gate that is also controlled on a phase qubit. The circuit applies H to the phase qubits, controlled U^(2^k) with first-order Trotterization, then QFTGate inverse on the phase register. The runner prepares the vertex input state. No measurement is included.

Source equation run: `9c0468a1-7050-4182-ada9-6bc519f6c2d0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: vertex register, little-endian binary label of graph vertex (qubit 0 is least significant)
- qubits n..n+m-1: phase register; phase qubit n+k controls U^(2^k), where U=exp(iAt)
- example: qubits 0,1 = vertex register (vertices 0..3, edges 0-1 and 0-2); qubits 2,3,4,5 = phase register
- phase register readout (by runner) is the integer j with eigenphase of U about j/2^m, after QFTGate(m).inverse() on the phase qubits

## Assumptions

- Vertices are labeled by integers in [0, 2^n); unused labels are isolated vertices.
- Weights are real, so A is real symmetric and Hermitian.
- Duplicate edges are allowed and their weights add to first order in the Trotter product.
- Time t and Trotter steps are chosen by the instance so that t*||A|| is small enough for the approximation to be meaningful.

## Unresolved issues

- No span-program-derived graph weights or gate-specific constructions are available from the abstract.
- Trotter error is not controlled or validated here; the spectral gap and the readout threshold are unspecified.
- The 0/1 convention for f(x) and the support condition for the zero eigenvector are unresolved.

## Equation mapping

- `eq_1`: background; no code location. The span-program/zero-eigenvector correspondence is a schematic statement. It is not a circuit. The code takes the graph G_P(x) as explicit edge data in the instance, so no span-program-to-graph construction is implemented.
- `eq_2`: implemented; build_circuit and _controlled_edge. Phase estimation of U=exp(iAt) with A the weighted adjacency operator. U^(2^k) is approximated by first-order Trotter products of per-edge exponentials, each controlled on phase qubit k. The circuit then applies the inverse QFT.

## Specification changes

- eq_2: exp(iAt) is approximated by a first-order Trotter product over edges (steps per power of two), not applied exactly. Reason: Only standard gates are allowed, with no dense unitaries or operator construction. Edge terms do not commute in general, so the result is approximate.
- eq_1, eq_2: Scope narrowed to an explicitly supplied weighted bipartite graph on at most 11 vertex qubits. Bipartiteness is validated. The gate-specific span programs, weights, and the input-dependent oracle for G_P(x) are not constructed. Reason: The abstract does not provide the weights or graph construction.
- eq_2: The circuit includes the phase-register Hadamards, the controlled evolutions, and the inverse QFT. It excludes preparation of the vertex input vertex, the zero-vs-nonzero threshold decision, repetition, and majority voting. Reason: The task asks for an operation only, without input preparation, measurement or classical postprocessing.
- eq_2: Sign and phase convention fixed to U|psi>=exp(2 pi i theta)|psi> with theta=j/2^m. The inverse QFT is applied to the phase qubits in their natural index order. Reason: This matches the QFTGate convention and resolves the order ambiguity.
