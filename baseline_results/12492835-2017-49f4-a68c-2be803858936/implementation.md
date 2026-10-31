# Equation to Qiskit

Implements the scoped baseline construction (eq_4-eq_6): k Grover iterates G = D*U_f on a triple-index register for triangle finding in an n-vertex unweighted graph. U_f is realized by three compiled adjacency-matrix queries (eq_1) that load A[u,v], A[v,w], A[u,w] of the triple indexed by |t> into three edge-bit ancillas, a multi-controlled phase implementing (-1)^{A[u,v] AND A[v,w] AND A[u,w]} (eq_2), and uncomputation; D is the standard diffusion 2|psi0><psi0|-I (up to global phase). The runner prepares the uniform superposition on triple_index and |000> on edge_bits. This is explicitly the textbook O(n^{3/2}) baseline, NOT the paper's O~(n^{5/4}) algorithm, whose structure is not recoverable from the abstract.

Source equation run: `1805cbc7-4412-4877-b7fa-56fa9be8f21a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: triple_index (2 qubits, little-endian: qubit 0 = bit 0 of t, qubit 1 = bit 1 of t); t indexes lexicographic triples t0={0,1,2}, t1={0,1,3}, t2={0,2,3}, t3={1,2,3} (eq_6); runner should prepare H⊗H|00> here
- qubits 2-4: edge_bits (3 ancillas, start in |000>): qubit 2 = A[u,v], qubit 3 = A[v,w], qubit 4 = A[u,w] of the triple selected by t; returned to |000> after each oracle call
- total qubits for the example: 5 (general: ceil(log2 C(n,3)) + 3, capped at 12, i.e. n <= 12)

## Assumptions

- Instance is a simple undirected unweighted graph given by 'n' and an edge list; vertices are 0..n-1 and n >= 4 so that the triple register has at least 2 qubits.
- Qubit 0 is the least significant bit of the triple index; triples are numbered in lexicographic order of (u<v<w).
- Runner prepares the uniform superposition on triple_index and |000> on edge_bits before applying the returned operation; measuring triple_index afterwards and decoding t via the lexicographic table yields the candidate triangle.
- If 'iterations' is omitted, the number of triangles M is counted classically from the instance solely to set k per eq_5; this is a baseline convenience and not part of a genuine query algorithm.
- Qubit cap of 12 restricts n to at most 12 (m = ceil(log2 C(n,3)) <= 8, plus 3 edge bits).

## Unresolved issues

- The actual O~(n^{5/4}) combinatorial algorithm of the paper (vertex-subset decomposition, nested quantum walks/searches, parameters) cannot be reconstructed from the abstract and is not implemented.
- For graphs with no triangle, 'iterations' must be given explicitly; no amplitude-estimation or exponential-schedule logic for unknown M is included.
- Gate count grows as O(iterations * C(n,3) * m) multi-controlled gates; no circuit-depth optimization was attempted.

## Equation mapping

- `eq_1`: implemented; _load_edge_bit (called from _apply_oracle). Each call realizes one compiled query O_G: controlled on the triple index |t>, the target edge bit is XORed with A[p_j(t)], implemented as one multi-controlled X per triple whose j-th pair is an edge. The (u,v) pair is decoded from t by a fixed classical table rather than stored in a separate register.
- `eq_2`: implemented; _apply_oracle: qc.mcp(math.pi, [edge[0], edge[1]], edge[2]). The three loaded edge bits are ANDed into a phase (-1)^{A[u,v] AND A[v,w] AND A[u,w]} by a CCZ (mcp with angle pi), then the edge bits are uncomputed.
- `eq_3`: background; no code location. Asymptotic complexity claims of the paper and comparison bounds; not a circuit construction. The implemented baseline costs O(n^{3/2}) queries and does not achieve these bounds.
- `eq_4`: implemented; _apply_oracle (U_f), _apply_diffusion (2|psi0><psi0|-I), build_circuit loop (G = D*U_f). One Grover iterate per loop pass. The diffusion is implemented as H^m X^m CZ^{(m)} X^m H^m, which equals -(2|psi0><psi0|-I), a global phase. The uniform state |psi0> is over all 2^m register values (padding when C(n,3) is not a power of two).
- `eq_5`: implemented; build_circuit: 'iterations' handling and the k = floor((pi/4) sqrt(N'/M)) computation. The number of Grover iterates is either supplied in the instance or computed from eq_5 with N replaced by the padded size 2^m and M the classically counted number of triangles. The success-probability formula and the query-count statement are analysis, not circuit elements.
- `eq_6`: implemented; _triples (lexicographic triple table) and example_instance_json. The example instance is exactly the 4-vertex graph with edges {01,02,12,23}; the triple-index table follows the lexicographic order t0={0,1,2},...,t3={1,2,3} with t stored little-endian (qubit 0 = LSB), consistent with t = 2 t_1 + t_0.

## Specification changes

- eq_4, eq_2: The phase_ancilla register (prepared in |->) was removed; the phase kickback (-1)^f is implemented directly as a CCZ (mcp(pi)) on the three edge bits. Reason: Equivalent unitary action on the triple_index register, uses one fewer qubit, and avoids requiring the runner to prepare a |-> ancilla.
- eq_1: O_G is not built as a standalone oracle on separate |u>|v>|b> registers; instead the composition (decode t -> pair p_j(t)) followed by O_G is compiled into multi-controlled X gates controlled on the triple index. Reason: Storing u and v explicitly would require extra registers and a reversible triple-decoder, exceeding the 12-qubit budget for n >= 6; the compiled form has identical action on the computational basis of (triple_index, edge_bits).
- eq_4, eq_5: When N = C(n,3) is not a power of two, the search register has 2^m > N basis states and |psi0> is the uniform superposition over all 2^m values; index values t >= N are unmarked. The eq_5 iteration count uses N' = 2^m in place of N. Reason: A uniform superposition over exactly N non-power-of-two values would need state preparation, which is forbidden for this operation; padding preserves Grover semantics with a slightly smaller marked fraction. For the example (N = 4) there is no padding.
- eq_4: Diffusion operator is implemented up to a global phase of -1 (as I - 2|psi0><psi0| instead of 2|psi0><psi0| - I). Reason: Standard H-X-CZ-X-H realization; global phase is unobservable.
- eq_4, eq_6: The circuit contains only the Grover iterates: no Hadamard state preparation and no measurement. Reason: Required by the operation-only contract; the runner prepares H^{(x)m}|0> on triple_index and |000> on edge_bits.
- eq_3: Scope narrowed to the textbook Grover baseline (O(n^{3/2}) queries); the paper's O~(n^{5/4}) algorithm is not implemented. Reason: The abstract provides no construction details for the improved algorithm; this narrowing was already declared in the math specification.
