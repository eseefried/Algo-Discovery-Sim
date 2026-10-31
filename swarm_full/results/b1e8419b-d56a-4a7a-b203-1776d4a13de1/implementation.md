# Equation to Qiskit

Scope-narrowed construction: k iterations of a Grover-type search iteration on an n-qubit search register (N=2^n), with both phase inversions replaced by a phase e^{i(pi+beta)} that carries a systematic error beta. It is the Grover baseline with phase errors, NOT the paper's optimized quantum random-walk search, whose operators the abstract does not give. Inputs such as the uniform superposition are prepared by the runner, and no measurement is included.

Source equation run: `3d82378d-f8f9-40eb-ad55-08171c3d268d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: search register 'search', little-endian (qubit 0 is the least significant bit of the database index; marked item bit i is on qubit i)
- No coin or ancilla qubits; total qubits = n_qubits <= 12
- Runner is expected to prepare the uniform superposition on the search register before the operation

## Assumptions

- Search register has n qubits and N=2^n; one marked item given as an integer.
- Phase inversions are generalized to exp(i(pi+beta)) for both the oracle and the inversion about the uniform state.
- The initial uniform superposition is prepared externally by the runner.
- Iterations capped at 200 and n_qubits capped at 12.

## Unresolved issues

- The optimized quantum random-walk search operators, coin register and optimal iteration formula are not specified in the abstract.
- The paper's exact phase error model may differ from the assumed one.
- Robustness comparison against the optimized algorithm cannot be made, because only the Grover baseline is built.

## Equation mapping

- `eq_1`: background; no code location. The abstract gives no explicit formula for P_k(N,k,beta). The circuit only provides a dependence on N, k and beta through its parameters, and the success rate is obtained later by simulation. No closed form is coded.
- `eq_2`: implemented; build_circuit: the loop over iterations (oracle and diffusion phase inversions); beta=0 reproduces the ideal Grover iteration whose success probability is sin^2((2k+1)theta). Implements the ideal Grover iteration baseline underlying eq_2 for N=2^n. With beta=0 the oracle and diffusion operators match the ideal ones up to a global phase. The probability formula is not coded.

## Specification changes

- eq_1, eq_2: Scope narrowed to the Grover-type baseline iteration with phase errors. The optimized quantum random-walk search operator is not implemented. Reason: The abstract and the specification do not give the optimized random-walk operators, so they cannot be reconstructed without fabricating them.
- eq_1: The phase error model is assumed: both phase inversions use phase pi+beta instead of pi, with the same beta in each. This is the standard modeling choice but is not taken from the paper. Reason: The abstract only mentions systematic phase inversion errors without a definition.
- eq_2: Database size is restricted to N=2^n with a single marked item. Only the operation is built, with no state preparation or measurement. Reason: The register is an n-qubit register, and the runner prepares inputs.
