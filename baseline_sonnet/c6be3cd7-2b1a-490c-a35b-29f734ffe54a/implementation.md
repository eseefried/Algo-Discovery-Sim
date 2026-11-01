# Equation to Qiskit

Builds the miter circuit V^dagger U on n data qubits (step 1 / eq_3) from two user-supplied gate lists U and V. U is applied first, then the inverse of V. The circuit equals the identity exactly iff U=V, and equals a global phase times the identity iff U=e^{i theta}V. The identity or phase test itself, and state comparison, are left to the external runner.

Source equation run: `b395956e-aaff-462e-b085-8e29bfc205fb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] = qubit index 0 (least significant bit), data qubit on which U and V act
- q[1..n-1] = qubit indices 1..n-1, further data qubits; total qubits = n (max 12); no ancillas, no classical bits

## Assumptions

- The circuits U and V act on the same n qubits, with no ancillas, measurements or resets.
- U is applied first, then V^dagger, matching the operator product V^dagger U.
- Gate lists are supplied in the instance, since the abstract specifies no benchmark circuits.
- Global phase is not tracked by the circuit gates used here, so the miter equals the identity up to a phase only when U equals V up to a phase.

## Unresolved issues

- The specific equivalence notions beyond exact and global-phase equivalence are unknown.
- The paper's algorithms and data structures are unknown.
- The quantum communication and search benchmark circuits are unspecified.
- No reference result is available for validation.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Exact state equality is a comparison of output vectors performed by the runner. The operation prepares no states and measures nothing.
- `eq_2`: background; no code location. State equivalence up to global phase is a background criterion for comparing states. It is not constructed in the circuit.
- `eq_3`: implemented; build_circuit (miter V^dagger U via compose(uc) then compose(vc.inverse())) and _apply. The miter V^dagger U is built as a unitary circuit. It equals the identity iff U=V. The identity check is left to external verification.
- `eq_4`: background; no code location. The trace criterion |Tr(V^dagger U)|/d = 1 is a postprocessing test on the miter unitary. The same miter circuit serves both eq_3 and eq_4, but the trace evaluation is not implemented.

## Specification changes

- eq_3, eq_4: Scope narrowed to constructing the miter circuit V^dagger U from explicit gate lists in a fixed gate set (h,x,y,z,s,sdg,t,tdg,sx,rx,ry,rz,p,cx,cz,swap,cp). The equivalence decision is not implemented. Reason: The task requires an operation without measurement, simulation or operator construction, so the identity or global-phase test cannot be in the module.
- eq_1, eq_2: State-equivalence equations are not implemented. They concern comparing states, whereas the module is a pure operation with no input-state preparation. Reason: Inputs are prepared and compared by the runner.
- eq_1, eq_2, eq_3, eq_4: The paper's actual algorithms and scalability techniques for hundreds of qubits are not reconstructed. The qubit count is capped at 12 and gate lists at 200 ops each. Reason: The abstract gives no algorithmic details, and the task caps qubits at 12.
