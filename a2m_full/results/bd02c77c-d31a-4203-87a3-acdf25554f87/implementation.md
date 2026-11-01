# Equation to Qiskit

Builds a measurement-free phase-estimation circuit for a Szegedy-style walk U=R_B R_A on a small weighted bipartite graph. The graph is given by the instance, with edges kept or removed by a classical input string x. This is a narrowed, illustrative construction, not the paper's span-program-to-graph construction. The optional convention W=-U^2 maps adjacency eigenvalue 0 to phase 0.

Source equation run: `079b5b0d-dac1-49e4-ad1a-d211cbc6b4d9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..na-1: left-vertex index a, little-endian (register 'left')
- qubit na..na+nb-1: right-vertex index b, little-endian (register 'right'); the edge state is |a>|b>
- qubit na+nb..na+nb+m-1: phase-estimation register, qubit j controls W^(2^j); after the inverse QFT the integer value k approximates 2^m*phase/(2*pi)
- Example (na=1,nb=1,m=3): q0=a, q1=b, q2..q4=phase; total 5 qubits

## Assumptions

- Edge weights are nonnegative and every left and right vertex keeps at least one positive-weight edge after x is applied. Otherwise ValueError is raised.
- The runner prepares the input state on the left and right registers, for example an edge state corresponding to |r>.
- Per-gate Ry-tree state loading with nonnegative real amplitudes is sufficient.
- Total qubits na+nb+m<=12, with na,nb in [1,3] and m in [1,6].

## Unresolved issues

- The paper's span-program-to-graph weights, composition, and balance rules are not implemented, so the example graph is not a verified AND or NAND formula evaluator.
- The coherent oracle with query-register uncomputation is not implemented.
- The Szegedy edge-space walk is not the same Hilbert space as the paper's vertex walk. The correspondence to the zero eigenspace of the adjacency matrix holds only up to the discriminant normalisation.
- The required phase-estimation precision and acceptance thresholds are unspecified.

## Equation mapping

- `eq_1`: background; _effective_weights (classical x only). The coherent oracle O_x is not implemented. The input bits x are classical instance data that keep or remove edges when the circuit is built. No query register or ancilla is used.
- `eq_2`: background; no code location. The zero-eigenvector criterion and the 1/sqrt(W) gap are the motivation. The circuit does not construct the paper's span-program graph and does not check the criterion.
- `eq_3`: implemented; _walk, _reflector, _prep. U=R_B R_A is implemented as a Szegedy-type walk on the edge space of a weighted bipartite graph. R_A is multiplexed over the left index a and reflects about |phi_a>=sum_b sqrt(w_ab/sum_b w_ab)|b>. R_B is multiplexed over b and reflects about |chi_b>. Both reflections are built from Ry trees and controlled phase flips. Each reflection carries a global sign of -1, and the two signs cancel in U.
- `eq_4`: implemented; build_circuit (convention='zero_eigenvalue'). In the plain Szegedy walk, cos(theta) equals a singular value of the discriminant. The optional convention uses W=-U^2, whose phase is pi+2*theta mod 2pi. Eigenvalue 0 (theta=pi/2) therefore gives phase 0 for both e^{+i theta} and e^{-i theta}. The trivial singular value 1 maps to phase pi.
- `eq_5`: implemented; build_circuit (Hadamards, controlled W^(2^j), QFTGate inverse). Standard phase estimation on W with m phase qubits. Measurement, the all-zero acceptance rule, the choice of epsilon, and majority voting are left to the runner and are not in the circuit.

## Specification changes

- eq_1: The coherent oracle is replaced by classical x that selects which edges are present when the circuit is built. Reason: The spec gives no oracle-based reflection construction. Building the circuit from classical x keeps it a bound unitary operation.
- eq_2, eq_3: Graph weights are supplied by the instance instead of derived from a span program. The graph is at most 8x8 (na,nb<=3). It is not claimed to be the paper's AND or NAND span-program graph. The walk is the Szegedy edge-space form with row and column normalised weights. Reason: The exact weight construction is listed as missing information.
- eq_4: Added the optional convention W=-U^2 so that adjacency eigenvalue 0 maps to phase 0. The 'plain' convention estimates the phase of U itself. Reason: A plain walk puts eigenvalue 0 at phase pi/2. The spec left the convention unresolved.
- eq_5: Narrowed to the phase-estimation unitary only. There is no measurement, acceptance threshold, or repetition, and m is user-chosen with m<=6. Reason: The task requires a measurement-free operation, and the spec gives no constants.
