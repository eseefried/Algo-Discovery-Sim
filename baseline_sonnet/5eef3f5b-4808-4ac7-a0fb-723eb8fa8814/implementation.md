# Equation to Qiskit

Builds a single-qubit unitary circuit from a user-supplied finite word over the Pauli+V generators {X,Y,Z,V1,V2,V3 and inverses}, using V_k=(I+2i*sigma_k)/sqrt5 realised exactly as Rx/Ry/Rz rotations by -/+2*atan(2). The deterministic search, target rotation Rz(theta) and epsilon-error check are out of scope. The circuit only applies the given word.

Source equation run: `fbc0255c-4795-4725-bdfe-d75f0467e2e1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: single data qubit, standard computational basis, qubit 0 is the least significant bit (only one qubit used)

## Assumptions

- The V gates are (I+2i*sigma_k)/sqrt5 for k=X,Y,Z, which is the usual Pauli+V convention recalled from the literature and not given in the abstract.
- The circuit-form generator list in eq_5 is assumed.
- Word order: the first list element is applied first, matching U = g_k...g_1.
- The example word is arbitrary and illustrative.

## Unresolved issues

- The deterministic-search algorithm and its depth and optimality guarantees are not implemented because the source is unspecified.
- The exact V convention from the source paper is unverified.
- The operator-norm approximation to Rz(theta) at precision epsilon is not checked or produced by this module.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Target Rz(theta) is the approximation goal. The implemented operation applies a given word and does not construct or compare against the target.
- `eq_2`: out_of_scope; no code location. Flagged placeholder that the specification itself says to discard. It is not a valid V definition and is not used.
- `eq_3`: implemented; build_circuit: V gate branch (theta = -/+2*atan(2) with rx/ry/rz). V_k = (I+2i*sigma_k)/sqrt5 is implemented exactly as a rotation about axis k. The labelling is corrected as described in specification_changes.
- `eq_4`: out_of_scope; no code location. The operator-norm error criterion is an evaluation condition, not a circuit operation. It is not implemented in the generated module.
- `eq_5`: implemented; build_circuit: loop over word appending gates in order. The finite product U = g_k...g_1 over the Pauli+V generators is built by appending g_1 first. Length is capped at 1000 and labels are validated.

## Specification changes

- eq_3: The matrix (1/sqrt5)[[1,2],[-2,1]] listed as V_3 equals (I+2iY)/sqrt5. It is labelled V2 here, and V3 is taken as (I+2iZ)/sqrt5 = diag(1+2i, 1-2i)/sqrt5. V1=(I+2iX)/sqrt5 is unchanged. Reason: The labels in the specification were inconsistent with the stated 'analogues for other axes'. A uniform axis-based convention is used.
- eq_1, eq_2, eq_4: The scope is narrowed to applying a user-supplied word over the gate set. The deterministic search for an approximating word, target construction and epsilon check are not implemented. Reason: The abstract and specification do not give the search algorithm or the geometric construction. The V convention and error criterion are only assumed.
- eq_2: The equation is discarded. Reason: The specification marks it as a superseded placeholder.
