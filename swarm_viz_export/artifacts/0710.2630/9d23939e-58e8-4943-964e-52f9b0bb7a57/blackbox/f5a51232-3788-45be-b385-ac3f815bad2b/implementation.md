# Equation to Qiskit

Builds a measurement-free phase-estimation circuit for one depth-1 MAJ3 gate on a classical input x. A span program with t=(1,0), v1=(0,1), v2=(1,1), v3=(1,-1) gives a 6-vertex weighted bipartite graph with a root, 2 span-row vertices and 3 input vertices. Edges to unavailable inputs (x_i=0) are omitted. exp(iAs) is implemented with a symmetric Trotter product of exact two-level edge rotations. Each rotation is built from CX, controlled RX and the phase control, with no dense unitary. The phase register uses controlled powers of U and an inverse QFTGate. Outcome 0 on the phase register is meant to signal a root-supported zero eigenvector. The runner must prepare the vertex register in |000>, the root, which has index 0.

Source equation run: `55af29b3-1b1a-42a6-8a3b-5283c718d43d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-2: vertex register, little-endian index; 0=root, 1=span row 0 (target coordinate), 2=span row 1, 3=input vertex 1, 4=input vertex 2, 5=input vertex 3; indices 6 and 7 are unused
- qubits 3..3+m-1: phase estimation register, little-endian, qubit 3 is the least significant and controls U^1
- expected input: vertex register in |000> (root), phase register in |0...0> prepared by the runner
- phase-register outcome 0 indicates a zero eigenvalue with root overlap

## Assumptions

- Vertex indices: root 0, rows 1-2, inputs 3-5, stored little-endian on qubits 0-2.
- s is a user-chosen evolution time with |s|<=1.5, so that s*||A|| stays below pi.
- Phase estimation maps eigenvalue lambda to phase lambda*s/(2*pi) mod 1, read in the phase register with outcome 0 meaning lambda near 0.
- Precision (phase_qubits), s and trotter_steps must be chosen so that the smallest nonzero |eigenvalue| is resolved; this is not checked here.
- The leakage from nonzero eigenvalues and the Trotter error are not analyzed.

## Unresolved issues

- The gap of the graph for each x is not analyzed, so the separation of p_0 between accepting and rejecting inputs is unverified.
- The Trotter error is not bounded and may shift the zero-eigenvalue peak.
- The threshold for decoding p_0 is not specified.
- The paper's own span-program-to-graph construction (e.g. weight scalings) is not reproduced.
- Recursive formula evaluation and optimality are out of scope.

## Equation mapping

- `eq_1`: background; no code location. The MAJ3 truth table is the target function. It is realized only through the span program and is not coded separately.
- `eq_2`: implemented; build_circuit: vecs tuple and the loop selecting edges for inputs with x[i]==1. Concrete valid span program: t=(1,0), v1=(0,1), v2=(1,1), v3=(1,-1). These are pairwise independent and none is parallel to t, so t is in the span of the available vectors iff at least 2 inputs are 1. Only vectors of inputs with x_i=1 contribute edges.
- `eq_3`: implemented; build_circuit: edges list (root-row0 edge weight 1, row-input edges with weights v_i[j]). Graph construction. Root vertex joins row 0 and rows join available inputs with weights v_i[j]. A kernel vector with nonzero root amplitude r then has input amplitudes c satisfying sum c_i v_i = -r t, which exists iff t is in the span. The correspondence is implemented as the graph and is tested by phase estimation, not checked in the code.
- `eq_4`: implemented; _edge and the Trotter loops in build_circuit. U=exp(iAs) is applied as a symmetric (Strang) Trotter product of exact per-edge two-level rotations, controlled on phase qubit k and repeated 2^k times. This is approximate, not an exact exponential.
- `eq_5`: background; no code location. The zero-bin probability formula is an analysis statement about the outputs. It is evaluated externally and not built into the circuit.

## Specification changes

- eq_2: Replaced the invalid assumed span program (v1=(1,1), v2=(1,-1), v3=(0,1)) with a verified MAJ3 program: t=(1,0), v1=(0,1), v2=(1,1), v3=(1,-1). Reason: The earlier vectors were flagged in the specification as not valid for MAJ3. The new set is checked by the pairwise-independence argument over all 8 inputs.
- eq_3: Fixed the graph: a root vertex joined to the first span-coordinate row with weight 1, and rows joined to input vertices with weights equal to the vector components (zero entries dropped). Inputs with x_i=0 become isolated vertices. Reason: The abstract gives no graph; this choice makes root support of a zero eigenvector equivalent to span-program acceptance.
- eq_4: Replaced the exact dense matrix exponential of A with a symmetric Trotter product of exact edge rotations, with a trotter_steps parameter. Reason: Opaque dense unitaries and operator construction are not allowed. Each edge term is exactly a controlled RX after CX basis changes, but non-commuting edges make the product approximate.
- eq_3, eq_5: Root-state preparation is removed from the circuit and left to the runner, which supplies |000> on the vertex register. Hadamards on the phase register are kept inside the operation. Thresholding of p_0 is not implemented. Reason: The circuit is an operation, not an experiment. The runner prepares inputs and decoding is classical.
- eq_4, eq_5: Narrowed to a single depth-1 MAJ3 gate with explicit classical x compiled into the gate structure. There is no recursion, no query model and no optimality claim. Reason: Matches the experiment scope given in the specification.
