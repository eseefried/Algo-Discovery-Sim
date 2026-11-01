# Equation to Qiskit

Single-qubit unitary for the piecewise-constant control Hamiltonian H=1/2[u_x X+(u_z+beta) Z] with a fixed quasi-static dephasing offset beta (default 0). Each segment is the exact rotation exp(-i dt/2 (u_x X+(u_z+beta) Z)), built as Ry(phi) Rz(angle) Ry(-phi). The example is a CORPSE-like pi rotation about X. No numerical search or cancellation analysis is implemented.

Source equation run: `643cf37c-6c2a-4e34-b6cc-f820fa8fcdef`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: effective singlet-triplet logical qubit (computational basis; Qiskit index 0 is the least significant bit)

## Assumptions

- Control amplitudes are in angular-frequency units so that a segment rotates by angle dt*|(ux,uz+beta)|.
- The Hamiltonian is H=1/2[ux X+(uz+beta) Z] with no hbar factor.
- Segments are applied in list order.
- beta is a single quasi-static value shared by all segments and defaults to 0.
- The example is a CORPSE-like sequence of rotations 420, 300 and 60 degrees with alternating sign of ux. It is only an illustrative instance, not a result from the paper.

## Unresolved issues

- The actual singlet-triplet Hamiltonian and control constraints are not available.
- The non-Markovian noise models and the paper's perturbative formalism are not reconstructed.
- The paper's explicit pulse sequences are not reproduced.
- Control-noise terms are not modeled beyond the single beta offset.

## Equation mapping

- `eq_1`: implemented; build_circuit: per-segment rotation about axis (ux,0,uz+beta) with angle dt*sqrt(ux^2+(uz+beta)^2). Exact propagator of the piecewise-constant noisy Hamiltonian with a fixed quasi-static beta. Setting beta=0 gives the ideal U_0(T).
- `eq_2`: background; no code location. First-order Magnus/toggling-frame approximation used to analyse errors. The circuit applies the exact product of segment rotations, so this approximation is not used.
- `eq_3`: out_of_scope; no code location. Cancellation condition is a classical analysis of the control sequence and is not checked in the circuit builder.
- `eq_4`: background; no code location. Target-gate constraint is a property the chosen controls should satisfy. The builder does not enforce it. The example sequence is chosen to give an X pi rotation up to global phase at beta=0.
- `eq_5`: out_of_scope; no code location. Numerical optimization of the cost function is classical search and is not part of the circuit operation. Its output (controls) is supplied as instance data.

## Specification changes

- eq_1: Narrowed to implementing the propagator of piecewise-constant controls with an optional fixed quasi-static beta, taking [ux,uz,dt] segments as input. Pulse shapes, bounds and the singlet-triplet Hamiltonian are not included. Reason: The specification gives only a generic assumed model, and the paper's actual Hamiltonian and constraints are missing.
- eq_2, eq_3, eq_5: Error-cancellation analysis and numerical search are excluded from the circuit. Reason: They are classical computations that do not belong in a measurement-free unitary operation.
- eq_4: The target gate is not enforced or validated. Reason: The builder returns the operation for any valid controls; the controls are supplied by the caller.
