# Equation to Qiskit

Qiskit module implementing the continuous-time quantum-walk search evolution operator exp(-iHt), H = -gamma*A - |w><w| with A = J - I, on the complete graph K_N with N = 2^n vertices (n <= 12 qubits). Using A = N|s><s| - I the operator is exp(-i*gamma*t) * exp(i t (gamma*N |s><s| + |w><w|)); the two non-commuting rank-one projector phases are realised exactly with (X-conjugated) multi-controlled phase gates (the uniform-superposition projector via Hadamard conjugation) and combined with a symmetric second-order Trotter product with a user-chosen number of steps. Defaults follow the degenerate-perturbation-theory estimate gamma_c = 1/N, t_* = pi*sqrt(N)/2. No state preparation or measurement is included.

Source equation run: `dd058376-512e-4c22-8a62-717ce9e7dded`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'vertex' with n = num_qubits qubits (example: 2 qubits, N = 4 vertices of K_4).
- Qubit i (Qiskit index i, little-endian) holds bit i of the vertex index v = sum_i 2^i v_i; qubit 0 is the least significant bit.
- Example: marked vertex w = 3 = |11>; the uniform superposition |s> = H^{x2}|00> is the intended input state (prepared by the runner, not by the module).
- Total qubits = num_qubits <= 12; no ancillas (mcp is used directly).

## Assumptions

- Adjacency-matrix form of the walk Hamiltonian; for the regular complete graph the Laplacian form differs only by a constant shift (global phase).
- Single marked vertex w given as an integer in [0, 2^n - 1].
- Little-endian vertex encoding: qubit i holds bit i of the vertex index.
- Default parameters follow the asymptotic degenerate-perturbation-theory estimates gamma_c = 1/N and t_* = pi*sqrt(N)/2; at small N (e.g. N = 4) the peak success probability is not exactly 1 and the optimal time differs slightly from pi.
- Multi-controlled phase gates (qc.mcp) without ancillas are acceptable as standard library gates for up to 12 qubits.

## Unresolved issues

- The paper's diagrammatic weighted-graph-with-self-loops method and its specific graph with growing invariant subspace dimension are not reconstructed; only the standard complete-graph search is implemented.
- Trotter error at the default 16 steps is small for the K_4 example (t = pi, gamma*N = 1) but larger instances/times may require more steps; the runner should choose trotter_steps accordingly.
- Whether the paper uses the adjacency or Laplacian walk is unknown; irrelevant for regular graphs but would matter for the paper's actual example graph.

## Equation mapping

- `eq_1`: implemented; build_circuit docstring and body (half_walk_angle / oracle_angle); module docstring derivation A = N|s><s| - I. The search Hamiltonian H = -gamma*A - |w><w| for the complete graph is exponentiated: the walk term becomes exp(i gamma N d |s><s|) (via _uniform_projector_phase), the oracle term exp(i d |w><w|) (via _projector_phase) and the constant shift gamma*I a global phase.
- `eq_2`: out_of_scope; no code location. Initial uniform superposition is input-state preparation, which the runner performs; the module only uses the identity |s> = H^{x n}|0> inside _uniform_projector_phase to implement the walk term.
- `eq_3`: implemented; build_circuit loop: symmetric Trotter product of _uniform_projector_phase (H^(0) = -gamma*A) and _projector_phase (V = -|w><w|). The perturbative split into walk term and oracle term is exactly the split used for the second-order Trotter product; the two exponentials are each realised exactly and alternated.
- `eq_4`: background; no code location. The degenerate-perturbation-theory gap/runtime estimate is an analytical prediction, not an operation; it only motivates the default evolution time through eq_5.
- `eq_5`: implemented; _parse_instance (defaults gamma = 1/N, time = pi*sqrt(N)/2) and build_circuit (A = J - I via A = N|s><s| - I). The complete-graph instance (adjacency J - I, critical gamma_c = 1/N, runtime pi*sqrt(N)/2) is the construction implemented; the example instance is K_4 with gamma = 1/4, t = pi.
- `eq_6`: out_of_scope; no code location. Success probability requires measurement/sampling of the output state, which is excluded from the returned operation and left to the runner.

## Specification changes

- eq_1, eq_3: exp(-iHt) is approximated by a symmetric second-order Trotter product with 'trotter_steps' (default 16) steps rather than exact exponentiation; each factor (walk projector phase and oracle projector phase) is exact. Reason: The walk and oracle terms do not commute, and opaque dense unitaries are disallowed; Trotterization with standard gates (H, X, mcp, p) is the compliant realisation. Error is O(t^3/r^2) and controllable via trotter_steps.
- eq_5: Vertex count restricted to N = 2^n (n = 1..12) so the complete graph fills the whole computational basis; graphs other than the complete graph are rejected with ValueError. Reason: Only the complete-graph instance is specified; a power-of-two vertex count avoids padding states and keeps A = N|s><s| - I exact on the register.
- eq_1: The constant term +gamma*I arising from A = J - I is carried as qc.global_phase = -gamma*t (mod 2 pi) instead of as gates. Reason: A multiple of the identity contributes only a global phase; recording it keeps the circuit equal to exp(-iHt) as an operator rather than merely up to phase.
- eq_2, eq_6: Initial-state preparation and the final measurement are removed from the circuit. Reason: The module must return an operation only; the runner prepares inputs and performs measurement/sampling.
