# Equation to Qiskit

Qiskit module implementing the continuous-time quantum-walk search operator U = e^{-iH(gamma_2)t_2} e^{-iH(gamma_1)t_1} (eq_1, eq_2, eq_5) with H(gamma) = -gamma*A - |w><w| for two exactly-simulable graph families on N = 2^n vertices: the complete graph K_N (A = J - I, with e^{i gamma t J} compiled as Hadamards around a multi-controlled phase on |0...0>) and the n-dimensional hypercube (A = sum_k X_k, compiled as RX rotations). The non-commuting graph and oracle terms are combined with a second-order (Strang) product formula with a user-chosen number of Trotter steps per stage. The oracle e^{i t |w><w|} is an X-conjugated multi-controlled phase gate. Input-state preparation (eq_3) and measurement (eq_4) are left to the runner. The example instance is the assumed K_4 sanity instance of eq_7 (gamma = 1/4, w = 0, t = pi, single stage).

Source equation run: `b25f31b6-0470-4a3a-a7ff-d42b8f4434c9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- vertex[0] -> physical qubit 0: least significant bit of the vertex index v (N = 2^n vertices, n = num_qubits = 2 in the example)
- vertex[1] -> physical qubit 1: most significant bit of the vertex index for the example (K_4, N = 4)
- Vertex v in {0,...,N-1} is the computational basis state |v> with bit k of v on qubit k; marked vertex w = 0 is |00>
- No ancilla qubits are used; total qubits = num_qubits <= 12
- Expected runner input: uniform superposition H^{(x)n}|0...0> (eq_3); success outcome is the bitstring of w after measurement (eq_4), both outside this operation

## Assumptions

- Hamiltonian convention H(gamma) = -gamma A - |w><w| with hbar = 1 (adjacency form; Laplacian form differs only by a global phase on the regular graphs supported).
- Single marked vertex w given as an integer index in [0, N).
- Vertex index encoded in binary on the vertex register with qubit 0 as the least significant bit; N = 2^n so Hadamards prepare |s> exactly on the runner side.
- The complete-graph term uses J = N|s><s| with |s> = H^{(x)n}|0...0>, and the +gamma I part of -gamma(J - I) is tracked as a circuit global phase.
- Stage boundaries are sharp switches of gamma (piecewise-constant schedule); the same oracle term is used in every stage.
- Trotter step count is an instance parameter chosen by the user; the example uses 40 Strang steps for t = pi, gamma = 1/4 on K_4.
- The example instance (K_4, gamma = 1/4, w = 0, t = pi) is an agent-chosen sanity instance where the ideal continuous evolution gives success probability 1, not a graph from the paper.

## Unresolved issues

- The paper's two example graphs (low-connectivity/fast and high-connectivity/slow) and their adjacency structures are unknown, so they cannot be compiled; only K_N and hypercube families are supported.
- The optimal two-stage parameters (gamma_1, t_1, gamma_2, t_2) are not given by the abstract; the module accepts them as inputs but offers no defaults for the paper's algorithm.
- Product-formula error is not bounded automatically; users must choose trotter_steps large enough for the desired accuracy at the given gamma, t and N (the K_N term has spectral norm gamma*N, so large N or gamma needs more steps).
- Multi-controlled phase gates on up to 12 qubits are left for the transpiler to decompose; no ancilla-assisted decomposition is provided.

## Equation mapping

- `eq_1`: implemented; _apply_stage (second-order product-formula approximation of exp(-i H(gamma) t)). Each stage applies the Schrodinger propagator exp(-iH t) for a time-independent H, approximated by a Strang-split product formula with trotter_steps steps.
- `eq_2`: implemented; _apply_graph_term (exp(+i gamma dt A) for K_N or hypercube) and _apply_oracle_term (exp(+i dt |w><w|)). H(gamma) = -gamma A - |w><w| is split into the graph term and the oracle term; both are compiled exactly from standard gates (H, X, RX, multi-controlled phase, global phase for the -gamma I part of K_N).
- `eq_3`: background; no code location. The uniform superposition is the input state prepared by the runner; the returned circuit is the walk operator only and contains no state preparation.
- `eq_4`: out_of_scope; no code location. Success probability requires measurement/sampling, which the operation must not include; it is evaluated by the runner.
- `eq_5`: implemented; build_circuit stage loop over instance['stages']. Consecutive piecewise-constant stages with rates gamma_k and times t_k are applied in order; two entries realize the two-stage template with a sharp switch of the walking rate.
- `eq_6`: background; no code location. Asymptotic runtime criterion; it classifies results of experiments across N and is not an operation to compile.
- `eq_7`: implemented; example_instance_json and the 'complete' branch of _apply_graph_term. The assumed K_4 sanity instance (gamma = 1/4, w = 0, t = pi, single stage) is encoded as the example instance; the complete-graph adjacency J - I is compiled via H^{(x)n} mcp H^{(x)n} and a global phase.

## Specification changes

- eq_1, eq_2, eq_5: The propagator exp(-iH t) is approximated by a second-order Strang product formula splitting the graph term and the oracle term, with a user-specified number of steps per stage (error O(t * dt^2)), instead of an exact matrix exponential. Reason: Opaque dense unitaries are disallowed; the graph and oracle terms do not commute, but each is exactly compilable from standard gates, so a product formula is the natural gate-level implementation.
- eq_2, eq_7: Graph families restricted to the complete graph K_N and the n-dimensional hypercube Q_n with N = 2^n vertices; arbitrary edge lists are not supported. Reason: The abstract does not define the paper's two example graphs, and these two families have adjacency terms with exact standard-gate compilations (J = N|s><s| and sum_k X_k) without ancillas or operator construction.
- eq_3, eq_4: Initial-state preparation and computational-basis measurement are removed from the circuit; the module returns only the walk unitary. Reason: The task requires an operation without input-state preparation, measurement or sampling; the runner supplies |s> and measures.
- eq_5: The stage list may have any length >= 1 (one entry recovers the single-stage walk; two entries give the two-stage template of the abstract). Reason: Generalizing the number of stages costs nothing and lets the single-stage K_4 sanity instance and the two-stage template share one code path.
