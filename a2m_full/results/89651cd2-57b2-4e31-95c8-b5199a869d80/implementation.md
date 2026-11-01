# Equation to Qiskit

Grover iterations G^k for triangle finding on a small graph (3<=n<=8, at most 12 qubits). The graph comes from the instance's edge list, and the adjacency oracle O_G is compiled into multi-controlled X gates onto 3 edge ancillas. The phase oracle computes the three edge bits, applies a CCZ on them, then uncomputes, so the ancillas return to |0>. Diffusion is applied on the 3 vertex registers. The runner must prepare the uniform superposition on u,v,w and leave the ancillas in |0>. The circuit is measurement-free and unitary.

Source equation run: `18cb6506-c7aa-472a-ae70-dbce4bc50ddb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: register u (first vertex, little-endian)
- qubits m..2m-1: register v (second vertex, little-endian)
- qubits 2m..3m-1: register w (third vertex, little-endian)
- qubits 3m..3m+2: edge ancillas e0=A[u][v], e1=A[v][w], e2=A[u][w]; they start and end in |0>
- m = max(1, ceil(log2 n)); the example n=4 has m=2, so u=0,1, v=2,3, w=4,5, e=6,7,8 (9 qubits)
- The runner prepares the uniform superposition on u,v,w (qubits 0..3m-1) and |0> on the ancillas

## Assumptions

- The graph is undirected, and duplicate edges are merged.
- The input state is the uniform superposition over u,v,w with the edge ancillas in |0>.
- If iterations is absent, the number of triangles is counted classically from the instance to choose k, and a graph with no triangle is then rejected.
- Ordered triples are searched, so M = 6 times the number of triangles.

## Unresolved issues

- The paper's O~(n^{5/4}) algorithm (sampling, edge classification, neighborhood search) is not reconstructed.
- The skeleton does not realise a real query-complexity advantage, since the oracle is compiled from the known graph.
- The measurement and classical verification steps of the specification are not part of the returned operation.

## Equation mapping

- `eq_1`: implemented; _edge_query. The oracle is compiled from the instance edge list into multi-controlled X gates. Each ordered adjacent pair (a,b) flips the target when the registers hold |a>|b>.
- `eq_2`: implemented; _phase_oracle (CCZ on the AND of the three edge ancillas). The AND of the three edge bits is realised by the CCZ. Distinctness and range checks come for free: the diagonal of A is zero and out-of-range indices have no edges, so no flag ancilla is needed.
- `eq_3`: implemented; _phase_oracle. Compute the three edge bits, apply CCZ, then uncompute the edge bits. CCZ acting on the edge bits directly replaces the kickback ancilla in |->, which has the same phase effect with one qubit fewer.
- `eq_4`: implemented; _diffusion and the loop in build_circuit. The Grover diffusion H X MCZ X H on the 3m vertex qubits, composed with the oracle, repeated k times. It equals 2|s><s|-I up to a global phase of -1. The initial Hadamards that prepare |s> are left to the runner.
- `eq_5`: implemented; build_circuit (default iterations). If iterations is not given, k = round(pi/(4 theta) - 1/2), with sin(theta) = sqrt(M/N). M = 6 times the classically counted triangles, and N = 2^(3m). The success-probability formula itself is background.

## Specification changes

- eq_3: The kickback ancilla in |-> is replaced by CCZ on the three edge ancillas, and the optional validity flag ancilla is dropped. Reason: This saves qubits to stay within the 12-qubit cap. Validity checks are implied by the zero diagonal and the absence of edges at indices >= n.
- eq_1: O_G is compiled from the instance's explicit edge list as multi-controlled X gates, not an opaque query. This costs no real queries and measures no query complexity. Reason: The runner needs a concrete unitary, and opaque or dense unitaries are disallowed.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to the outer Grover skeleton with 3<=n<=8, reduced from the specified 4..6. Because of the 12-qubit cap, 3m+3 <= 12 is the real limit, and n=7 and 8 also fit. The paper's O~(n^{5/4}) combinatorial algorithm is not implemented. Reason: The abstract gives no details of the combinatorial algorithm. The 12-qubit cap rules out the specified 3m+5 qubits for m=3.
- eq_4: The circuit excludes the initial Hadamards on u,v,w and the kickback preparation, as well as all measurements and classical verification. Reason: The task requires an operation only. The runner prepares the inputs.
