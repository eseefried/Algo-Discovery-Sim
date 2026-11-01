# Equation to Qiskit

Trotterized continuous-time quantum walk search operator exp(-iHt) on the complete graph K_N with N=2^n and a single marked vertex w, where H=-gamma*A-|w><w|. For K_N, A=N|s><s|-I, so H splits into two exactly implementable phase-type exponentials. The circuit alternates exp(i*gamma*N*dt|s><s|) and exp(i*dt|w><w|) for r first-order Trotter steps, with global phase exp(-i*gamma*t). Input-state preparation and measurement are left to the runner. The paper's perturbation-theory diagrammatics are not implemented.

Source equation run: `10e49165-0953-4f8e-922c-5a4887ac9adf`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex register, computational-basis integer encoding of vertex x as |x>, qubit 0 is the least significant bit
- N = 2^n vertices; no ancilla qubits
- Marked vertex w is the integer 'marked' in the same encoding

## Assumptions

- Complete graph K_N with N a power of two
- Adjacency-matrix Hamiltonian with a single marked vertex
- gamma is supplied by the instance; gamma=1/N is the usual critical value for K_N
- The runner prepares the initial state, e.g. the uniform superposition

## Unresolved issues

- The paper's actual graph family and Hamiltonian form (adjacency vs Laplacian) are unknown
- The subspace whose dimension grows with N is not reconstructed
- The diagrammatic rules and perturbation order are unknown
- The Trotter step count is a free parameter chosen by the instance

## Equation mapping

- `eq_1`: implemented; build_circuit (complete-graph identity A=N|s><s|-I, split into _phase_on_uniform and _phase_on_basis_state). H=-gamma*A-|w><w| is implemented for the complete graph K_N with N=2^n, which is a choice of graph not given in the abstract. Adjacency form, single marked vertex.
- `eq_2`: implemented; build_circuit (Trotter loop and global_phase). The unitary exp(-iHt) is implemented as a first-order Trotter product. The initial uniform state |s> is prepared by the runner and is not part of the circuit.
- `eq_3`: background; no code location. The H0/V split is graph-specific and not given in the abstract. The circuit evolves under the full H, so no split is used.
- `eq_4`: background; no code location. Generic second-order effective Hamiltonian. It is an analysis tool, not a circuit operation, and is not implemented.
- `eq_5`: out_of_scope; no code location. The paper's weighted self-loop graph reduction and its diagrammatic rules are not specified, and the subspace growing with N is not reconstructed.

## Specification changes

- eq_1, eq_2: Narrowed to the complete graph K_N with N=2^n, one marked vertex, and an adjustable gamma, instead of the paper's unspecified graph family. Reason: A concrete graph is required to build a circuit. K_N admits an exact decomposition of H into two phase-type operators.
- eq_2: The exact exponential is replaced by an r-step first-order Trotter product. The error is O(t^2/r) because |s><s| and |w><w| do not commute. Reason: The two terms are each cheap to exponentiate exactly, but exp(-iHt) as a whole would otherwise need a dense unitary.
- eq_3, eq_4, eq_5: The perturbation-theory and weighted-graph content is not built into the circuit. Reason: The abstract does not specify the necessary details. The circuit applies the full evolution rather than an effective-Hamiltonian evolution.
