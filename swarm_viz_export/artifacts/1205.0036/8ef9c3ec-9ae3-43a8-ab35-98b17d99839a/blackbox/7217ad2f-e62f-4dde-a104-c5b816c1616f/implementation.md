# Equation to Qiskit

Qiskit build_circuit for the 2x2 nearest-neighbor, ancilla-free, measurement-free fanout from eq_3. Qubit 0 is the control c and qubits 1..3 are the targets t1, t2, t3. The gate order is CX(c,t1), CX(t1,t3), CX(c,t1), CX(t1,t3), CX(c,t1), CX(c,t2). Only the grid edges c-t1, t1-t3 and c-t2 are used. An optional x_mask selects which targets receive X, giving a controlled product of X or I gates, and the default mask [1,1,1] is the full fanout.

Source equation run: `406c97c4-1257-4529-ad3e-3c33d892b581`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control c at grid site (0,0)
- qubit 1: target t1 at grid site (0,1)
- qubit 2: target t2 at grid site (1,0)
- qubit 3: target t3 at grid site (1,1), diagonal to c, reached only via t1
- Grid-adjacent edges used: c-t1 (0,1), t1-t3 (1,3), c-t2 (0,2)
- Encoding: computational basis, Qiskit little-endian (qubit 0 least significant); no ancillas

## Assumptions

- Row-major site labelling with c at qubit 0 and t1, t2, t3 at qubits 1, 2, 3
- Operators in eq_3 act right to left, so the rightmost factor is applied first
- The x_mask variants are an added parametrization, and the default is the full fanout

## Unresolved issues

- The adaptive classical-controller simulation, constant-depth Shor, the lower-bound proof and the large-n circuits are not implemented
- eq_5 scaling is not reflected in a single fixed-size instance

## Equation mapping

- `eq_1`: implemented; build_circuit (default x_mask [1,1,1]). The circuit is the fanout truth table: x is XORed onto each of the three targets.
- `eq_2`: implemented; build_circuit via x_mask. Implemented only for U_i in {I, X}: x_mask selects which targets get X, and the all-X case is eq_1. General single-qubit U_i is not implemented.
- `eq_3`: implemented; build_circuit: the cx sequence for t3, then cx(c,t1), then cx(c,t2). The gate order follows the right-to-left reading of the operator product. A hand trace of the bit values gives t3 -> y3^x, t1 -> y1^x, t2 -> y2^x.
- `eq_4`: background; no code location. This is the hand-verification trace of eq_3. It is documented in the build_circuit comments and not coded separately.
- `eq_5`: out_of_scope; no code location. Asymptotic depth scaling Theta(k n^(1/k)) cannot be shown by a fixed 4-qubit instance.

## Specification changes

- eq_2: Restricted the controlled-product operation to U_i in {I, X} through an optional x_mask. General U_i is not implemented. Reason: Controlled-U on the diagonal site t3 needs a path-based construction that the specification does not give, and the X case is verifiable.
- eq_1, eq_3: Scope narrowed to the 2x2 grid (k=2, 3 targets). The instance keys k and side must equal 2 if supplied, and other values raise ValueError. Reason: The specification only fixes the 2x2 construction. The paper's large-n constructions and the adaptive simulation are not specified.
- eq_3: No equation correction was needed: the stated gate order was checked and confirmed to give the fanout. In the mask variants, steps are omitted when the corresponding target is unselected. Reason: The trace in eq_4 confirms eq_3 and shows t1 is restored to y1 after the four-gate path copy.
