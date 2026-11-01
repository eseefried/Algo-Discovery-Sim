# Equation to Qiskit

Builds the single-qubit circuit for the Clifford-cyclotomic decomposition form U = C_k Rz(pi/n) C_{k-1} ... Rz(pi/n) C_0. The instance gives n (positive even) and a list of k+1 Clifford words over the letters H, S, D (S-dagger), X, Y, Z. The circuit applies C_0 first, then Rz(pi/n), then C_1, and so on, ending with C_k. It does not run the synthesis algorithm itself.

Source equation run: `4184bb08-b5fa-4f68-ba3b-2249162eba58`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 (q[0]): the single data qubit acted on by U; Qiskit little-endian, no other qubits

## Assumptions

- The instance supplies the Clifford words explicitly as strings.
- Rz(pi/n) acts on qubit 0.
- n is capped at 1e6 and the number of Cliffords at 101, with word length at most 64, for sanity.
- For n=4, Rz(pi/4) equals the T gate up to a global phase.

## Unresolved issues

- The general-n exact synthesis algorithm and its minimality guarantee are not reconstructed.
- It is not checked whether a given decomposition is T-count (rotation-count) optimal.
- The exact phase normalization from the original Clifford+T result is not enforced.

## Equation mapping

- `eq_1`: background; no code location. The ring Z[e^{i pi/n},1/2] describes the entries of synthesizable unitaries. It is not computed or checked, because the circuit is built from a supplied gate decomposition.
- `eq_2`: implemented; build_circuit: Clifford words via _apply_clifford_word and qc.rz(math.pi / n, 0). The gate set is realized with Clifford letters (H, S, Sdg, X, Y, Z) and the z-rotation Rz(pi/n) for even n.
- `eq_3`: implemented; build_circuit: loop interleaving Clifford words and Rz(pi/n). Implements the interleaved product with k = len(cliffords) - 1 rotations. The k Cliffords' minimality is the caller's responsibility; the circuit only composes the supplied words.
- `eq_4`: out_of_scope; no code location. The n=4 characterization (exactly synthesizable = unitaries over R_4) is a theorem about the set of synthesizable unitaries. It is not an operation and is not checked.
- `eq_5`: background; no code location. Unitarity holds automatically because the circuit is made only of unitary gates. No ring-entry unitarity test is implemented.

## Specification changes

- eq_3: Fixed the ordering convention: time order is C_0, Rz, C_1, Rz, ..., C_k, giving the operator C_k Rz C_{k-1} ... Rz C_0. Reason: The spec said 'up to ordering', so a concrete convention was needed. Each Clifford word is applied left to right in circuit time.
- eq_2, eq_3, eq_4, eq_1, eq_5: Scope narrowed to composing a user-supplied decomposition into a circuit. The exact synthesis algorithm, its reduction step, and the minimality of the rotation count are not implemented. Ring membership and the unitarity of ring entries are not verified. Reason: The abstract gives no synthesis reduction rule or phase conventions, so the algorithm cannot be reconstructed. The equations that describe the decomposition form can be realized.
- eq_2: Clifford words are generated from H, S, Sdg, X, Y, Z, so Cliffords are realized only up to the global phase of the gates. Qiskit's rz carries the exact phase of diag(e^{-i pi/2n}, e^{i pi/2n}). Reason: The spec leaves global phase conventions unspecified.
