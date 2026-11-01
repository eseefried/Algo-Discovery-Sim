# Equation to Qiskit

Single MAJ3 gate. A fixed 2-dimensional read-once span program (target t=(1,0); v1=(1,1), v2=(1,-1), v3=(0,1)) is turned into a weighted bipartite graph whose root is the target-column vertex. Edges for inputs with x_i=0 are omitted. The adjacency matrix A is padded to 8 vertices on 3 qubits. U=exp(iAs) is implemented as a first-order Trotter product of two-level hopping rotations, which are controlled multi-controlled RX gates conjugated by CX gates. Standard phase estimation applies controlled powers of that same Trotter unitary, then an inverse QFT on the phase register. The circuit has no state preparation or measurement. A phase reading near 0 for root input |100> signals a zero eigenvector with root overlap.

Source equation run: `55847133-1d02-4b7b-a93f-e6c1b64588d3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: vertex index bit 0 (LSB)
- qubit 1: vertex index bit 1
- qubit 2: side bit (0 = left/row vertices j=0..3, 1 = right/column vertices 0..3); vertex label = 4*side + index
- Left vertices: rows of the span-program space (indices 0,1 used, 2,3 padding)
- Right vertices: index 0 = target column t (ROOT, basis state |side=1,idx=0> = integer 4 on qubits 0-2), indices 1,2,3 = inputs x1,x2,x3 (disconnected if x_i=0)
- qubits 3..3+m-1: phase-estimation register, qubit 3 is the least significant bit and controls U^1; qubit 3+k controls U^(2^k)
- Intended input: vertex register in root |100> (qubit 2 = 1), phase register |0...0>; prepared by the runner

## Assumptions

- Vertex labeling: label = 4*side + idx, root = target column on the right side at idx 0 (integer 4 on the vertex register).
- Phase-estimation convention: U=exp(iAs) has eigenphase lambda*s, read as phi=lambda*s/(2*pi) mod 1, so zero eigenvalue gives outcome 0 and negative eigenvalues wrap near 2^m.
- Trotter error means the eigenvalue-zero bin is only approximately preserved: exact zero eigenvectors of A are generally not exact eigenvectors of the Trotter unitary.
- The runner prepares the root input state and interprets the readout.
- The default weights and time keep the nonzero eigenvalue scale distinguishable from zero only for sufficiently many phase qubits.

## Unresolved issues

- The paper's actual MAJ3 span program, graph weights and scaling are not reproduced.
- No gap or precision analysis was done. For small phase_qubits, nonzero eigenvalues may alias into the zero bin.
- Trotter error is uncontrolled in the circuit and is not tuned to the gap.
- The root-overlap threshold and repetition rule are left to external post-processing.
- In the specification_changes entry for eq_4, the reason text contains a malformed inequality fragment ('||B||<=sqrt(6)<pi/1.2...'). The intended statement is that ||A|| is at most about sqrt(6)=2.45 (a Frobenius norm bound), so time<=1.2 gives time*||A||<pi.

## Equation mapping

- `eq_1`: background; no code location. MAJ3 definition is the target function. It is not coded directly but is the property the chosen span program in _COLS is designed to satisfy.
- `eq_2`: implemented; _COLS and _edges. The concrete span program (t=(1,0), v1=(1,1), v2=(1,-1), v3=(0,1)) is encoded as biadjacency columns, and only vectors with x_i=1 are included. Any two vectors span R^2, so they span t. No single vector is parallel to t.
- `eq_3`: implemented; _edges and build_circuit. The graph has the target column as root and the input columns gated by x. A zero eigenvector with root overlap exists iff c*t+sum a_i v_i=0 with c!=0. The circuit applies spectral estimation to this graph, but the zero-eigenvector criterion itself is checked externally.
- `eq_4`: implemented; _apply_edge and the controlled-power loop in build_circuit. A=[[0,B],[B^T,0]] is a sum of edge hopping terms w(|a><b|+|b><a|). Each term is exponentiated exactly by a CX-conjugated multi-controlled RX. exp(iAs) is approximated by a first-order Trotter product, and controlled powers are powers of that same Trotter unitary.
- `eq_5`: background; no code location. The zero-phase probability is a property of the output distribution of the phase register, read by the runner or analysis. The circuit supplies the phase estimation (Hadamards, controlled powers, inverse QFT) but does not compute p_0.

## Specification changes

- eq_2, eq_3: A specific MAJ3 span program (2-dimensional, read-once) and bipartite graph with the target column as root vertex were fixed. All edge weights are +-1. Reason: The abstract gives no span program or graph weights. A concrete choice was needed to produce a circuit.
- eq_4: exp(iAs) is realized by first-order Trotterization with trotter_steps steps per unit U, not exactly. The 6 real vertices are padded to 8 on 3 qubits, with unused padding vertices isolated. The time s is the instance parameter 'time', restricted to (0,1.2]. Reason: The edge terms do not commute, and opaque dense unitaries and operator construction are disallowed. ||B||<=sqrt(6)<pi/1.2... the bound time*||A||<pi is enforced via time<=1.2.
- eq_3, eq_5: Scope narrowed to a single depth-1 MAJ3 gate with explicit classical x compiled into gates. There is no recursive formula composition, no optimality claim and no query-complexity claim. Phase-register readout and thresholding are left to the runner. Reason: Consistent with the specified reconstruction scope and the measurement-free operation requirement.
- eq_4, eq_5: phase_qubits is capped at 6 and trotter_steps at 4. Reason: Bound circuit size, since controlled powers cost 2^k*trotter_steps repetitions, and keep the total at or below 12 qubits (max 9 used).
