# Equation to Qiskit

Concrete, white-box implementation of the target unitary W_sigma = U_{sigma(n)} ... U_{sigma(1)} (eq_1). The instance supplies n explicit standard gates, each acting on one qubit of an m-qubit system register, together with a permutation sigma. The circuit applies the gates in sigma order. This is not the paper's switch-based or query-efficient construction, because the abstract does not specify those constructions.

Source equation run: `5111dacd-2da2-426e-b68c-6224a015ff27`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubits 0..m-1 form the 'system' register; qubit 0 is the least significant bit.
- Each gate spec's 'qubit' field is the index of the system qubit that U_i acts on.
- Example: m=2, qubit 0 and qubit 1 of the system register; no ancillas.

## Assumptions

- Each U_i is a single-qubit gate from a fixed standard set acting on one qubit of the system register.
- The number of gates n is at most 32 and the system size is at most 12 qubits.
- The circuit is purely unitary and contains no input preparation or measurement.

## Unresolved issues

- The paper's quantum-switch circuit with n log2(n)+Theta(n) switches is not reconstructed.
- The paper's query-model circuit with n^2-2n+4 calls is not reconstructed.
- Multi-qubit or arbitrary black-box unitaries are not supported.
- The lower-bound gate-family assumption and the link to permutation-as-substring remain unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit (loop applying gates[sigma[k]-1] for k=0..n-1). Gates are appended in the order U_{sigma(1)}, ..., U_{sigma(n)}, so U_{sigma(1)} acts first, as in W_sigma.
- `eq_2`: out_of_scope; no code location. Quantum-switch complexity claim. The switch model and its circuits are not defined in the abstract, so no switch construction is implemented.
- `eq_3`: out_of_scope; no code location. Query upper bound n^2-2n+4. The explicit circuit achieving it is not given. The implemented circuit uses each U_i exactly once because the gates are known.
- `eq_4`: out_of_scope; no code location. Query lower bound under an unspecified gate-family assumption. It is a proof-level statement with no circuit content.
- `eq_5`: background; example_instance_json. The toy instance n=3, sigma=(2,3,1) fixes the ordering convention (U_2, then U_3, then U_1). The example instance encodes it, but it is a parameter choice, not an operation.

## Specification changes

- eq_1: The black-box unitaries U_i are replaced by explicit standard single-qubit gates (h, x, y, z, s, sdg, t, tdg, rx, ry, rz, p) specified in the instance and applied directly. Each is applied exactly once. Reason: A Qiskit circuit needs concrete gates. Black-box queries or quantum switches cannot be built without the paper's undisclosed constructions.
- eq_2, eq_3, eq_4: The complexity bounds are not implemented. The circuit is the trivial direct composition and makes no attempt to realize or verify the switch or query counts. Reason: The abstract gives only asymptotic claims, not the circuits or proofs.
- eq_1, eq_5: Sigma is encoded as a 1-indexed list [sigma(1),...,sigma(n)]. Gates are 1-indexed in the mathematical text and 0-indexed in the list gates. Reason: This fixes the convention that U_{sigma(1)} is applied first.
