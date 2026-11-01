# Equation to Qiskit

Single-qubit circuit for an alternating two-axis SU(2) rotation sequence U = R_{jN}(theta_N)...R_{j1}(theta_1). Axis 1 is z. Axis 2 lies in the x-z plane at angle alpha from z, so n2 = (sin alpha, 0, cos alpha). R_1 is rz(theta). R_2 is ry(-alpha), rz(theta), ry(alpha) in time order. Segment 1 acts first. The time cost, the time-optimal search and the angle bounds are not part of the circuit.

Source equation run: `402deb7e-10fd-4649-a8ab-fc011b3abf6d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: the single data qubit on which the SU(2) sequence acts; Qiskit little-endian, only one qubit
- Axis 1 = Bloch z axis; axis 2 = (sin alpha, 0, cos alpha), in the x-z plane
- Segments are applied in list order (segment 1 first)

## Assumptions

- Each rotation is exp(-i theta n.sigma/2) with Pauli sigma, applied to one qubit.
- Segments are given in time order.
- The global phase is zero, because the standard rz, ry gates are used.
- No target unitary is supplied. The caller provides the angles.

## Unresolved issues

- The explicit angle bounds and the three-angle parametrization of optimal sequences are not in the abstract.
- The clockwise-only scaling laws are not implemented.
- No time-optimal angles are computed. The example angles are arbitrary.

## Equation mapping

- `eq_1`: implemented; build_circuit: axis==1 branch (qc.rz) and axis==2 branch (ry(-alpha), rz, ry(alpha)). R_j(theta)=exp(-i theta n_j.sigma/2). n1=z and n2=(sin alpha,0,cos alpha) give n1.n2=cos alpha. R_2 is built by conjugating Rz with Ry(alpha).
- `eq_2`: implemented; build_circuit: loop over segments with the alternating-axis check. Gates are appended in time order, so the operator is R_{jN}...R_{j1}. Consecutive segments on the same axis raise ValueError.
- `eq_3`: background; no code location. The time cost depends on the speeds Omega_j, which a unitary circuit does not use. The circuit takes angles directly. The only trace of the cost model is the clockwise-only check theta>=0.
- `eq_4`: out_of_scope; no code location. The time-optimal synthesis is a classical numerical optimization, not a circuit.
- `eq_5`: background; no code location. N<=5 is a property of optimal sequences, not a constraint on arbitrary sequences. The builder does not enforce it. Segments are only limited to 50.

## Specification changes

- eq_1: Fixed the axes to n1=z and n2=(sin alpha,0,cos alpha) in the x-z plane. Reason: The abstract does not fix the axes. Only the angle between them matters, up to a global frame rotation.
- eq_3, eq_4, eq_5: Narrowed scope to applying a given sequence. There is no speed ratio, time cost, optimization, or enforced N<=5 bound. Reason: The abstract gives no explicit angle bounds, parametrization, or search procedure, and a circuit implements the operation, not the optimization.
- eq_2: Segment lists must alternate axes, and angles are real. With allow_counterclockwise=false, angles must be nonnegative, with no reduction mod 2pi. Reason: This is a simple validation of the clockwise-only variant.
