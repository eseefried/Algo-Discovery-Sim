# Equation to Qiskit

build_circuit returns a first-order Trotterized continuous-time quantum walk search evolution exp(-iHt) with H=-gamma*A - sum_{w in W}|w><w| on the simplex of M+1 cliques K_M (N=M(M+1) vertices, M in 2..6). It takes the marked set, gamma, t and the number of Trotter steps as parameters. Each adjacency edge is compiled as a multi-controlled RX two-level rotation, and each marked vertex gets a multi-controlled phase. No state preparation or measurement is included.

Source equation run: `edf08a75-3924-402d-b9fd-fecbb5ff876e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register 'v' with n=ceil(log2(M(M+1))) qubits (3 for M=2, 4 for M=3, 5 for M=4..5, 6 for M=6)
- Qiskit qubit 0 is the least significant bit of the vertex index
- Vertex index = clique*M + local_position, with clique in 0..M and local_position in 0..M-1
- Connector between clique i<j: vertex i*M+(j-1) in clique i joined to vertex j*M+i in clique j
- Basis states with index >= N are padding. They are left untouched by the A-term and receive no phase.
- Example (M=2): 3 qubits, N=6, cliques {0,1},{2,3},{4,5}, connector edges (0,3),(1,4),(2,5)

## Assumptions

- Adjacency-matrix Hamiltonian with oracle strength 1
- Evolution is exp(-iHt) with H=-gamma*A-P_W, so the phase signs are +i*gamma*A*t and +i*t on marked states
- The caller supplies marked vertex indices in the convention index = clique*M + local_position
- The runner prepares the initial state. If it uses H on all qubits when N is not a power of 2, the padding amplitude stays inert and the marked-set probability is scaled by N/2^n relative to a uniform state over the N vertices.
- The Trotter step count is given by the instance and should be large enough for the desired accuracy

## Unresolved issues

- The paper's exact connector structure and Laplacian-versus-adjacency convention are not confirmed
- The explicit critical jumping rates gamma* per marked-vertex configuration are not reconstructed
- The M+1 and 2(M+1) marked-vertex configurations are not provided as presets. They can only be entered manually through the marked list.
- Trotter error is not bounded or checked in the module
- For N not a power of 2, a clean start in the N-dimensional vertex subspace is left to the runner

## Equation mapping

- `eq_1`: implemented; build_circuit (A-term via _two_level, marked-vertex term via _phase_state). Implements exp(-iHt) with H=-gamma*A - sum_{w in W}|w><w|, so the evolution is exp(+i(gamma*A + P_W)t). The padding penalty term is dropped because padding states are exactly decoupled (see specification_changes).
- `eq_2`: implemented; _edges(M). Builds the edge list: complete graph K_M inside each of the M+1 cliques plus one connector edge per clique pair, with every vertex a connector as in the specification.
- `eq_3`: background; no code location. The uniform starting state |s> and the marked-set probability readout are prepared and performed by the runner. The circuit only supplies the evolution operator exp(-iHt).
- `eq_4`: out_of_scope; no code location. The critical rate gamma*(config,M) and the time t*~(pi/2)sqrt(N) are not reconstructed. gamma and t are free instance parameters that can be scanned externally.
- `eq_5`: implemented; build_circuit loop over steps; _two_level; _phase_state. First-order Trotter product of r steps, each with an A-factor exp(i*gamma*A*t/r) followed by a diagonal marked-vertex phase factor exp(i*t/r) on each marked basis state. The A-factor is compiled from standard gates (CX and multi-controlled RX), with no dense unitary.

## Specification changes

- eq_1, eq_5: The padding penalty E_pad is omitted. For N that is not a power of 2, padding basis states are left idle. Reason: A is compiled only from two-level rotations between valid vertex states. The padding subspace is therefore exactly decoupled from the vertex subspace, and a penalty phase would have no effect on vertex dynamics. It would only add gates.
- eq_5: The A-factor exp(i*gamma*A*t/r) is itself approximated by a sequential product of per-edge two-level rotations, rather than being exactly diagonalized. Reason: Edge terms do not commute, and an exact compilation would need an opaque dense unitary, which is disallowed. This adds a first-order Trotter error that shrinks as steps grows.
- eq_2: The connector assignment is fixed as vertex i*M+(j-1) in clique i joined to vertex j*M+i in clique j, for i<j. Reason: The specification left the local connector position open. This choice makes the vertex-to-connector map a bijection in every clique.
- eq_1, eq_3, eq_4: Scope narrowed to the evolution operator for an explicitly supplied marked set, with M limited to 2..6. Initial-state preparation, measurement, gamma scans and configuration comparison are left to the runner. Reason: The task requires an operation only, with no state preparation or measurement. The explicit gamma* formulas are not available.
