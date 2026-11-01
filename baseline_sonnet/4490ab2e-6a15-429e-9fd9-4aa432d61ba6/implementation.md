# Equation to Qiskit

Hadamard-test unitary on a rows x cols open-boundary square lattice (default example 2x2). The ancilla controls U = V^dagger . CZ_layer . H^n, where H^n followed by the CZ layer builds the graph state from |0...0> and V^dagger un-prepares a user-parameterised product state. The ancilla has H, then controlled-U, then an optional S^dagger, then H. Starting from |0>_anc|0..0>_data, Pr[ancilla=0] = (1 + Re or Im of <alpha|G>)/2. This is a narrowed placeholder: the product-state angles are free parameters and are not derived from J and h.

Source equation run: `7b8e2e63-28cb-4f3b-aaee-a248c3a34927`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data qubits, one per lattice site, index = row*cols + col (qubit 0 least significant); for the 2x2 example qubits 0,1,2,3
- qubit n (4 in the example): Hadamard-test ancilla
- Input convention: all qubits start in |0>, prepared by the runner
- Output: Pr[ancilla=0] = (1 + Re<alpha|G>)/2, or (1 + Im<alpha|G>)/2 when imaginary_part is true, with |G> = prod CZ H^n |0^n> and |alpha> = tensor_i P(phi_i)Ry(theta_i)|0>

## Assumptions

- The instance supplies rows, cols, theta, phi, and an optional imaginary_part flag.
- Lattice has open boundaries, with a horizontal and a vertical edge for each neighbouring pair.
- |alpha_i> = P(phi_i)Ry(theta_i)|0>, an arbitrary normalized single-qubit state parameterisation.
- Qubits start in |0>; the runner prepares inputs and performs measurements.
- Controlled gates (ch, ccz, cp, cry) are chosen to have no relative-global-phase errors, so the ancilla-controlled phases are exact.

## Unresolved issues

- The J,h-to-product-state map and the proportionality constant c are not implemented.
- The paper's MBQC measurement pattern, algorithmic domain, and approximation scale are not reconstructed.
- BQP-completeness, the real-parameter extension, and the comparison with constant-depth algorithms are out of scope.
- Equation eq_1 is only background; the circuit does not verify that its amplitude equals a partition function.

## Equation mapping

- `eq_1`: background; no code location. Ising partition function definition. It is the target quantity, but the code does not evaluate it or encode J and h.
- `eq_2`: implemented; build_circuit: controlled-H layer (ch) and ccz on lattice edges. The graph state is prepared as CZ edges applied after H on each qubit, here controlled on the ancilla. H on |0> equals |+>, so the input state prep is part of the unitary U.
- `eq_3`: implemented; build_circuit: cp(-phi) and cry(-theta) loop. Implements only the overlap structure. The ancilla-controlled V^dagger un-prepares a product state |alpha>, so the test amplitude is <alpha|G>. The angles are free instance parameters. The map from J and h to |alpha_i>, and the constant c, are not reconstructed.
- `eq_4`: implemented; build_circuit: initial h(a), optional sdg(a), final h(a). Hadamard test. Without S^dagger, Pr[0] = (1+Re<alpha|G>)/2. With S^dagger before the final H, Pr[0] = (1+Im<alpha|G>)/2. The test measurement itself is left to the runner.

## Specification changes

- eq_3: Product-state angles theta_i and phi_i are free input parameters instead of functions of J_ij and h_i. The constant c is omitted. Reason: The abstract and spec do not give the J,h-to-|alpha_i> mapping or c. Fabricating them would be unsupported.
- eq_2, eq_3: The graph state is built directly on the open-boundary rows x cols lattice. The paper's overlap mapping may use a different or decorated graph. Reason: The spec states that the lattice used for the graph state may differ and gives no details.
- eq_4: The Hadamard test replaces the paper's MBQC procedure. The overlap is <0|U|0> with U = V^dagger CZ H^n, and the ancilla is the only measured qubit (measurement left to the runner). Reason: The MBQC pattern is not given in the abstract. The spec labels the Hadamard test as a placeholder.
- eq_1: Scope is narrowed to a generic overlap-estimation operation. No partition function value is computed. Reason: The algorithmic domain and approximation scale are unspecified.
