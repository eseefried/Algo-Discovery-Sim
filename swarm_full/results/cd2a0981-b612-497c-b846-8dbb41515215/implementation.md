# Equation to Qiskit

Trotterized continuous-time quantum-walk search on the n-dimensional hypercube (N=2^n vertices), approximating exp(-iHt) for H = -gamma*L - |w><w|, with L = sum_j (I - X_j). Each step applies RX mixing for the Laplacian term and a phase e^{i dt} on the marked basis state. Scope is narrowed to the hypercube, a fixed single-stage rate, and a Trotter approximation.

Source equation run: `8dcc871b-217b-46d1-a505-0b033698c32f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex register of the n-dimensional hypercube; qubit k holds bit k of the vertex label (little-endian, qubit 0 least significant); vertex x = sum_k x_k 2^k
- Hypercube edges connect labels that differ in exactly one bit
- Marked vertex w is given as an integer label in [0, 2^n); no ancilla qubits
- Input state (e.g. uniform superposition) is prepared by the runner, not by the circuit

## Assumptions

- Marked vertex w is a computational-basis state with little-endian bit order.
- gamma > 0 and time >= 0 are real; steps is at most 2000 and n is at most 12.
- The runner prepares the initial state, e.g. the uniform superposition.
- Global phase gamma*n*t is included for fidelity to exp(-iHt).

## Unresolved issues

- The paper's actual graphs (low-connectivity fast-search and high-connectivity slow-search) are not reconstructed.
- The two-stage walk and its walking-rate schedule are not implemented.
- The Trotter error depends on the steps and order parameters; the right choice of gamma, t, and steps is not specified by the abstract.

## Equation mapping

- `eq_1`: implemented; build_circuit (Trotter loop over steps, using _mix and _mark_phase). exp(-iHt) is approximated by a first- or second-order product formula; the circuit is the operation only, with no state preparation.
- `eq_2`: implemented; _mix (the -gamma*L term, with the global phase set in build_circuit) and _mark_phase (the -|w><w| term). H = -gamma*L - |w><w| with L = sum_j (I - X_j) for the hypercube. exp(i*gamma*dt*L) becomes RX(2*gamma*dt) on each qubit plus a global phase. exp(i*dt*|w><w|) becomes a multi-controlled phase on |w>.
- `eq_3`: out_of_scope; no code location. The O(sqrt(N)) runtime claim for cubic lattices with d>=5 is an asymptotic statement. The circuit is on hypercubes and does not implement or encode that claim.

## Specification changes

- eq_2: Graph chosen as the n-dimensional hypercube (L = sum_j (I - X_j)) instead of an unspecified graph. Reason: The abstract does not define the graphs. The hypercube is a standard highly connected search graph with an efficient gate decomposition, so the Laplacian term needs no dense unitary.
- eq_1, eq_2: Exact evolution replaced by a Trotter product formula (order 1 or 2) with a user-chosen number of steps. Reason: The Laplacian and oracle terms do not commute, so exact evolution has no simple gate decomposition.
- eq_1, eq_2: Only a single-stage walk with fixed gamma is implemented. The two-stage walk with an adjusted rate is not implemented. Reason: The abstract gives no stage details, gamma schedule, or graph for the two-stage algorithm.
- eq_3: Runtime claim not implemented. Reason: Asymptotic claim about cubic lattices with d>=5, not a circuit construction.
