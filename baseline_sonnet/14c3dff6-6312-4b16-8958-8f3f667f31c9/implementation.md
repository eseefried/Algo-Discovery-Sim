# Equation to Qiskit

Builds a Trotterized (symmetric second-order) approximation of the continuous-time quantum-walk search unitary exp(-iHT) with H = -gamma*L - |w><w| on the complete graph K_N, N = 2^n (n <= 12 qubits). For K_N, L = N*I - N|s><s|, so H = -gamma*N*I + gamma*N|s><s| - |w><w|. The circuit uses H/X layers with multi-controlled phase gates for the |s><s| and |w><w| phase kicks, plus a global phase for the identity term. It contains no state preparation or measurement.

Source equation run: `c72baa13-3c28-440b-9122-5ebf999257af`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form the 'vertex' register; qubit i is bit i (2^i weight) of the vertex label v, so the computational basis state |v> is the integer v in Qiskit little-endian order.
- Example: n_qubits=2 gives K_4 with vertices 0..3 on qubits 0 (LSB) and 1 (MSB); marked vertex w=0.
- No ancilla qubits.

## Assumptions

- hbar = 1, with a time-independent single-stage Hamiltonian.
- N = 2^n, with n between 1 and 12.
- Marked vertex w is an integer label in [0, N-1].
- Global phase exp(i*gamma*N*T) is included for exactness of the Hamiltonian's identity part.

## Unresolved issues

- The paper's low-connectivity fast-search graph, high-connectivity slow-search graph and two-stage walk are not defined and not implemented.
- Optimal T and gamma for any non-complete graph are unknown.
- The Trotter step count needed for a target accuracy is not determined here.

## Equation mapping

- `eq_1`: implemented; build_circuit (Trotter loop and global_phase). The unitary exp(-iHT) is approximated by a symmetric second-order Trotter product with trotter_steps slices.
- `eq_2`: implemented; build_circuit, _marked_phase, _uniform_phase. For K_N, H = -gamma*N*I + gamma*N|s><s| - |w><w|. The identity term becomes the global phase, the |s><s| term is _uniform_phase with angle -gamma*N*dt, and the oracle term is _marked_phase with angle +dt/2 on each side.
- `eq_3`: background; no code location. Initial state |s> is prepared by the runner; the operation contains no input-state preparation. The |s> projector appears only inside the evolution.
- `eq_4`: background; no code location. The success probability comes from measurement, which the circuit does not contain; it is computed by the runner.
- `eq_5`: out_of_scope; no code location. Asymptotic scaling claim for d-dimensional lattices; not a circuit construction.

## Specification changes

- eq_1, eq_2: Exact evolution replaced by a symmetric (Strang) Trotter product of the oracle phase and the |s><s| phase; the result is approximate, with error decreasing as trotter_steps grows. Reason: Standard gates cannot express the exact non-commuting exponential without an opaque dense unitary or operator construction.
- eq_2: Scope narrowed to the complete graph K_N with N = 2^n and Laplacian L = N*I - J. The paper's two example graphs and its two-stage algorithm are not implemented. Reason: The specification does not define the paper's graphs or the gamma schedule. The spec's ceil(log2 N) register size is also restricted to exact powers of two so no padding vertices are needed.
- eq_2: gamma defaults to 1/N when omitted, and time and trotter_steps are explicit instance parameters. Reason: The specification gives no optimal gamma or T; 1/N is the known critical value for the complete graph.
- eq_3, eq_4: The vertex register encoding is stated as Qiskit little-endian, not 'most significant bit first'. Vertex v maps to the basis state with integer value v. Reason: The task requires qubit index 0 to be the least significant bit.
