# Equation to Qiskit

Qiskit module implementing the p-layer alternating-operator (QAOA) MaxCut unitary from the specification: optional Hadamard layer producing |+>^n from |0>^n, then for each layer l the cost unitary exp(-i*gamma_l*C) as one exact two-qubit phase gadget (CX, P(-gamma), CX) per edge, followed by the mixer exp(-i*beta_l*B) as RX(2*beta_l) on every qubit. The example instance is the specification's C_4 ring with p=1 and the recalled angles (gamma,beta)=(pi/4,pi/8). Angles are supplied by the instance; the classical angle optimization (eq_4) and the performance bounds (eq_5, eq_6) are not part of the circuit.

Source equation run: `a873f42d-8c81-4f4f-a751-0e84a13ea50e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0..3]: one qubit per vertex of the 4-cycle C_4; qubit j holds bit z_j (cut side of vertex j); qubit 0 is the least significant bit of |z_3 z_2 z_1 z_0>
- Expected runner input: |0000>; with prepare_plus=true the circuit's first layer of H gates produces |+>^4 before the single (p=1) cost/mixer layer
- Total qubits: 4 (module caps num_qubits at 12)

## Assumptions

- Qubit j corresponds to vertex j, little-endian ordering, Z_j|z> = (-1)^{z_j}|z>
- The algorithm is the standard QAOA structure with transverse-field mixer and one cost/mixer pair per layer, as fixed in the math stage
- Angles are real finite floats supplied by the caller; gammas[l] and betas[l] belong to layer l+1 (layer 1 first)
- Graphs must be simple (no self-loops, no duplicate edges) with at least one edge; edge weights are not supported
- Example angles (pi/4, pi/8) are taken from the recalled eq_5 and have not been verified numerically here

## Unresolved issues

- No simulation or verification was performed; the expected cut value 3 (ratio 3/4) for the C_4 example is a recalled claim, not a checked result
- The 0.6924 bound (eq_6) and its derivation are not reproduced or tested by this module
- Whether the runner wants the Hadamard layer inside the operation is resolved by the prepare_plus flag; if the runner supplies |+>^n directly, set prepare_plus to false

## Equation mapping

- `eq_1`: implemented; _apply_cost_unitary (CX, P(-gamma), CX per edge realises exp(-i gamma (1 - Z_j Z_k)/2) exactly). The MaxCut cost Hamiltonian enters the circuit only through its exponential; each edge term (1 - Z_j Z_k)/2 has eigenvalue 1 on cut edges and 0 otherwise, so exp(-i gamma * term) applies phase exp(-i gamma) exactly when z_j != z_k.
- `eq_2`: implemented; _apply_mixer_unitary (RX(2*beta) on each qubit). exp(-i beta sum_j X_j) factorises into single-qubit exp(-i beta X_j) = RX(2 beta).
- `eq_3`: implemented; build_circuit (optional H layer, then loop over zip(gammas, betas) applying cost then mixer). Layer l = 1 acts first; within each layer exp(-i gamma_l C) is applied before exp(-i beta_l B), matching the rightmost-acts-first operator product.
- `eq_4`: out_of_scope; no code location. Expectation evaluation and classical angle maximisation are classical preprocessing/postprocessing; the module takes the angles as instance parameters and does not compute expectations.
- `eq_5`: background; no code location. The recalled p=1 ring formula is only used to choose the example angles (pi/4, pi/8); it is not computed or asserted by the code and remains unverified here.
- `eq_6`: background; no code location. The 0.6924 worst-case ratio for 3-regular graphs is a performance statement from the abstract, not a circuit element.

## Specification changes

- eq_3: Scope generalised from the fixed C_4, p=1 instance to any simple graph on n <= 12 vertices with p >= 1 layers and caller-supplied angles; the C_4, p=1 case is retained as the example instance. Reason: The task requires the operation to work for varying valid instance parameters and to reject invalid ones.
- eq_3: The |+>^n preparation is realised as an explicit Hadamard layer controlled by the required boolean key prepare_plus; the runner supplies |0...0> as input and no measurement step from the specification is included. Reason: The deliverable is a measurement-free operation; the Hadamard layer is part of the algorithmic unitary rather than an input-state preparation by initialize/reset, so it is kept but made switchable.
- eq_1: The cost unitary is implemented edge by edge as CX-P(-gamma)-CX instead of RZZ plus a global phase; the global phase exp(-i gamma m/2) mentioned in the specification steps is therefore retained exactly rather than dropped. Reason: This gadget matches diag(1, e^{-i gamma}, e^{-i gamma}, 1) exactly with standard gates and avoids sign-convention mistakes with RZZ(theta) = exp(-i theta ZZ/2).
- eq_4, eq_5: Step 1 (classical angle optimisation) and step 5 (measurement and postprocessing) of the specification are not implemented in the module. Reason: They are classical or experimental stages outside the circuit operation.
