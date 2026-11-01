# Equation to Qiskit

build_circuit applies the N-segment piecewise-constant single-qubit propagator of eq_1 (fixed X gradient h0+delta_h, exchange J_k(1+eps) about Z) to one qubit. Each segment exp[-i tau (J Z + h X)/2] is built exactly as a rotation about the tilted axis (h,0,J) using ry(-phi) rz(theta) ry(phi). Pulse parameters and static errors come from the instance. The numerical optimizer, the cost and the fidelity sweeps are outside the circuit.

Source equation run: `0e1f7172-14d6-4e04-8e21-3d4114b0c310`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: single effective singlet-triplet qubit (little-endian index 0), computational basis |0>,|1>; no ancillas
- Gate axes: Z axis = exchange J, X axis = gradient h0 + delta_h

## Assumptions

- Quasi-static delta_h and epsilon are supplied by the runner as fixed numbers per instance.
- The factor 1/2 applies to both Z and X terms, so rotation angle = tau*sqrt(J^2+h^2).
- Segment order: index 0 of the J and tau lists is applied first, matching the product from k=N to 1.
- Optional J_max and tau_min bounds are enforced as validation only when given. tau must be nonnegative.
- The example parameters are generic illustrative values.

## Unresolved issues

- No optimized robust sequence is supplied, so first-order cancellation of delta_h and epsilon is not guaranteed by the example.
- The paper's Hamiltonian normalization, control bounds, voltage-to-J relation and non-quasi-static bath treatment are unspecified and not modeled.
- Target gate choice and the optimizer are not specified and are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop over segments (ry(-phi), rz(theta), ry(phi) with h=h0+delta_h, J*(1+epsilon)). The ordered product of segment exponentials is implemented exactly. Segment 1 is applied first, and each segment is a single tilted-axis rotation, so there is no Trotter error.
- `eq_2`: background; no code location. The first-order Magnus error vectors are used only in the offline parameter search. The circuit does not compute them, but it accepts delta_h and epsilon so the runner can probe the perturbed propagator.
- `eq_3`: out_of_scope; no code location. The cost function belongs to the classical optimizer, which is not part of the unitary operation.
- `eq_4`: background; no code location. The robust-gate conditions define what a good parameter set must satisfy. They are not computed in the circuit, which only applies the parameters it is given.
- `eq_5`: out_of_scope; no code location. Fidelity readout and the error sweep are done by the runner on the output unitary or state, not inside the circuit.

## Specification changes

- eq_1: Each segment is implemented as the exact rotation about axis (h,0,J) with angle tau*sqrt(h^2+J^2), via ry(-phi) rz(theta) ry(phi) with phi=atan2(h,J). This implements exp[-i tau (J Z + h X)/2] with the 1/2 convention on both terms. The step text suggested sequential rx/rz rotations, which would not be exact. Reason: The J Z and X terms do not commute within a segment, so sequential rotations would change the propagator. The tilted-axis form preserves eq_1 exactly.
- eq_1, eq_3, eq_4: Scope is narrowed to the circuit for supplied pulse parameters (J_k, tau_k, h0, delta_h, epsilon). No optimization is performed, and the example parameters are not claimed to be an optimized robust sequence. Reason: The optimizer is classical and offline, and no robust sequence values are available from the abstract.
- eq_3: The cost function is not implemented. Its stray factor '\cdot 1' is noted but not corrected because no code uses the equation. Reason: The equation is outside the circuit scope.
- eq_2: The bath operator is taken to be X (the gradient term of eq_1) for delta_h, and Z (weighted by J) for the multiplicative exchange error epsilon. This is background only and is not coded. Reason: This matches eq_1 and the assumption note on eq_2.
