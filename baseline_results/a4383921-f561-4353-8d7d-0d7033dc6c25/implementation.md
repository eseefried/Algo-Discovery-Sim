# Equation to Qiskit

Implements the two-axis control-sequence compiler of the specification: a concatenation of alternating Bloch-sphere rotations about axis n_1 = z and axis n_2 = (sin gamma, 0, cos gamma) (eq_1, eq_2, eq_3) is compiled into a single-qubit Qiskit circuit, with the total control time T = sum |theta_k|/omega_{i_k} recorded in circuit metadata. Admissibility of the sequence (alternating axes, allowed rotation senses, angle ranges, optional N<=5 bound of eq_5) is validated. The time-optimal search itself (eq_4, eq_6) is classical optimization outside the circuit operation and is not performed; the example instance is the feasible ZXZ Hadamard sequence of eq_7.

Source equation run: `af71248c-6d19-4e53-ad19-740cf2c2f3ce`

Generation: **generated**; validation: **failed**.

Generated source was not executed: ValueError: Module constants must be literals or small numeric expressions.

Paper fidelity has not been independently verified.

## Register layout

- q[0] (Qiskit qubit index 0): the single qubit whose SU(2) evolution is synthesized; axis 1 = z (rz), axis 2 = (sin gamma, 0, cos gamma) realized as ry(-gamma) rz(theta) ry(gamma)
- Example: three segments Rz(pi/2), Rx(pi/2), Rz(pi/2) applied in that time order, equal to Hadamard up to global phase, total time T = 3pi/2 (stored in circuit metadata)

## Assumptions

- Controls are bang-bang at fixed per-axis speed so segment duration is |theta|/omega.
- Global phase is irrelevant; the example ZXZ sequence equals Hadamard only up to global phase.
- Bidirectional case angles in (-2pi, 2pi); clockwise-only case angles in (0, 2pi).
- Optimality of the example N=3 sequence is not asserted; it is a feasible candidate (upper bound T = 3pi/2).

## Unresolved issues

- The paper's explicit three-angle parametrization and angle bounds are unknown, so no restriction of the angle search space beyond the basic box is encoded.
- Clockwise-only length scaling laws are not available; in that mode no length bound is enforced.
- Finding T* requires an external classical optimizer that calls build_circuit on candidate sequences and compares them to the target.

## Equation mapping

- `eq_1`: implemented; _axis_rotation (rz for n_1 = z; ry(-gamma) rz(theta) ry(gamma) for n_2). R_n(theta) = exp(-i theta/2 n.sigma) matches Qiskit rz for the z axis; the tilted axis is obtained by conjugating rz with ry(gamma).
- `eq_2`: implemented; build_circuit: validation of gamma in (0,pi), positive omega, bidirectional flag and angle-range checks. Control set geometry (two non-parallel axes at angle gamma), per-axis speeds, and the allowed rotation senses are encoded as instance parameters and admissibility checks.
- `eq_3`: implemented; build_circuit: segment parsing loop (alternation check) and the time-ordered append loop computing total_time. Alternating segments are appended with the first listed segment applied first (rightmost operator factor); T = sum |theta_k|/omega_{i_k} is computed and stored in qc.metadata.
- `eq_4`: out_of_scope; no code location. The minimization over sequences is a classical optimization problem, not a unitary circuit operation; the module compiles a given candidate sequence only.
- `eq_5`: implemented; build_circuit: enforce_length_bound check (N <= 5 when bidirectional). Only the five-concatenation necessary condition is implemented as an optional admissibility check; the finite search over N<=5 structures itself is classical and not performed.
- `eq_6`: out_of_scope; no code location. The explicit three-angle parametrization is unknown from the abstract, so no reduction of the angle list is imposed; arbitrary admissible angle lists are accepted.
- `eq_7`: implemented; example_instance_json (gamma = pi/2, omega = [1,1], segments ZXZ with pi/2 each). The tiny instance is the module's example: orthogonal axes, equal unit speeds, feasible N=3 Hadamard sequence with T = 3pi/2.

## Specification changes

- eq_4, eq_5, eq_6: Scope narrowed from time-optimal synthesis to compilation of a user-supplied admissible control sequence; no optimization or search is performed in build_circuit. Reason: The circuit stage must return a unitary operation without classical numerical search or operator construction; the optimizer is a classical outer loop outside the module.
- eq_2: Axis n_1 fixed to z and n_2 fixed to (sin gamma, 0, cos gamma) in the xz-plane (azimuth 0). Reason: Any pair of axes at angle gamma is related to this pair by a global SU(2) frame change (rotation about n_1), so this is without loss of generality for the control model.
- eq_1: Rotation-sense convention fixed to R_n(theta) = exp(-i theta/2 n.sigma), i.e. Qiskit's rz/ry sign convention. Reason: The specification left the sign convention as a choice; Qiskit's native gate convention is adopted.
- eq_3: Zero-angle segments are rejected, and an empty segment list is accepted as the identity (T = 0); the total time T is reported via qc.metadata rather than returned. Reason: Zero-length segments contradict the alternating-merged-segment model; build_circuit must return only a QuantumCircuit.
