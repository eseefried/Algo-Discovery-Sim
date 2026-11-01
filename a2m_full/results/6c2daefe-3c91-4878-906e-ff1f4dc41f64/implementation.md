# Equation to Qiskit

One-qubit circuit for the five-segment control sequence Rz(a1) Rn(b1) Rz(a2) Rn(b2) Rz(a3) applied in time order. Rn(b)=Ry(theta)Rz(b)Ry(-theta) with n=(sin theta,0,cos theta). The angles, theta and an optional r are supplied by the instance. The classical time-optimal search, the cost evaluation and the angle bounds are not part of the circuit.

Source equation run: `e07bea4f-8cac-466d-a6c7-44d8fc5da383`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: the single data qubit; Qiskit index 0 is the least significant bit; no ancilla

## Assumptions

- theta lies in (0, pi/2], so the axes are non-parallel
- The five-segment ordering Rz, Rn, Rz, Rn, Rz is used
- Rotation angles use the Qiskit convention rz(a)=exp(-i a Z/2)
- Zero-angle segments are skipped

## Unresolved issues

- The paper's explicit angle bounds are unknown
- Which three angles are the free parameters, and the closed-form solution, are unknown
- The exact definition of r is unknown
- Shorter sequences than five segments are handled only by setting angles to zero
- The Ry sign convention should be verified by simulation

## Equation mapping

- `eq_1`: implemented; _append_rn. Rn(b)=Ry(theta)Rz(b)Ry(-theta) is built as ry(-theta), rz(b), ry(theta) in circuit order. Ry(theta) takes z to (sin theta,0,cos theta) under the standard convention.
- `eq_2`: implemented; build_circuit. The five alternating segments are appended in time order a1, b1, a2, b2, a3 for caller-supplied angles. The angles are not computed by the circuit.
- `eq_3`: out_of_scope; no code location. Total time is a classical cost used in the search. The circuit does not compute it; r is only validated as positive.
- `eq_4`: background; no code location. The fidelity check is performed by the external runner and is not part of the operation.
- `eq_5`: out_of_scope; no code location. The bounded classical search for time-optimal angles is not implemented. The paper's angle bounds are unavailable.

## Specification changes

- eq_2, eq_5: Scope narrowed to the circuit for a given set of five angles, with no search and no determination of the free angles. Reason: Which angles are free and the angle bounds are unresolved, and the operation must be a pure bound unitary circuit.
- eq_2: The segments are applied in time order a1 first, so the matrix product is Rz(a3)Rn(b2)Rz(a2)Rn(b1)Rz(a1), the reverse of the left-to-right form written in eq_2. Reason: The step description states time order and Qiskit applies gates in circuit order. The written product would correspond to reversing the angle lists.
- eq_3: r is only validated as positive and not used in the gates. The clockwise_only option enforces angles in [0,2pi). Reason: Rotation angles determine the unitary, and r only affects the time cost.
