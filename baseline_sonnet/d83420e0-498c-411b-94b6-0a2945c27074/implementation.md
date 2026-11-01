# Equation to Qiskit

Builds the standard Grover/amplitude-amplification operator G^L, with G = -A S_0 A^dagger S_g, on n search qubits (n <= 12). A is the Hadamard layer, so the initial state is the uniform superposition. S_g is a multi-controlled phase flip on each marked basis state. The default example is n=2, one marked state, L=1, which is the eq_5 instance (lambda=1/4). The paper's fixed-point scheme is NOT implemented.

Source equation run: `ead4019f-04fe-40dd-b1c4-8bbcdc527c16`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: register 'search'; qubit k is bit k (little-endian) of the basis-state integer
- marked integers use the same little-endian convention
- no ancilla qubits; total qubits = n <= 12
- input state A|0> (or any state) is prepared by the runner; the circuit applies only G^L

## Assumptions

- A = H^n and the oracle marks an explicit list of distinct computational-basis states.
- Qubit k is bit k of each marked integer (little-endian).
- The oracle is applied directly as a phase flip, with no ancilla.
- L is capped at 256 and n at 12 for size safety.
- If all 2^n states are marked, the circuit is still built and G acts trivially up to phase.

## Unresolved issues

- The paper's fixed-point amplitude amplification with quadratic speedup is not implemented.
- Phase schedule, query count versus lambda_0 and delta, and the optimal lambda range remain unspecified.
- The generic oracle/ancilla layout from the specification is replaced by a direct phase-flip oracle.

## Equation mapping

- `eq_1`: background; no code location. Defines the decomposition and lambda. The circuit does not prepare |psi>; the runner supplies the input. With the Hadamard-layer A and k marked states, lambda = k/2^n.
- `eq_2`: implemented; build_circuit (loop body) and _flip_state. One iterate G = -A S_0 A^dagger S_g per loop pass. S_g and S_0 are multi-controlled phase flips built with X conjugation and mcp(pi). A = H^n. The -1 is added as global phase.
- `eq_3`: background; no code location. Analytic success probability sin^2((2L+1)theta) for the iterate. It is a property of the implemented circuit when the input is A|0>, not separate circuit code.
- `eq_4`: out_of_scope; no code location. The fixed-point failure-bound requirement over [lambda_0,1] needs the paper's unspecified phase schedule, which is not reconstructed. Standard Grover does not satisfy it.
- `eq_5`: implemented; example_instance_json with build_circuit. The example instance n=2, marked=[3], L=1 gives lambda=1/4 and one iteration. It is realised by parameters, not by dedicated code.

## Specification changes

- eq_2, eq_3: Implemented the standard Grover iterate with fixed pi phases, not the paper's fixed-point amplitude amplification. A is fixed to the Hadamard layer and the oracle to a phase flip on an explicit list of marked basis states. Reason: The paper's fixed-point phase schedule is not given in the specification, so it cannot be reconstructed. The concrete A and oracle make the operation well defined.
- eq_4: The fixed-point requirement and the query-count scaling are not implemented or enforced. Reason: Essential details (phase schedule, query count, range) are missing from the specification.
- eq_1: The initial state A|0> is not prepared inside the circuit. Reason: The task requires operations only, with inputs prepared by the runner. A appears only inside G.
