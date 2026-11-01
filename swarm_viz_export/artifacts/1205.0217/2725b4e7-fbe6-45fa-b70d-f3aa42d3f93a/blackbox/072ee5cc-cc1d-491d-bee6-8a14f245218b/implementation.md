# Equation to Qiskit

Single-qubit circuit for the ideal piecewise-constant singlet-triplet evolution U = prod exp(-i H_k tau_k) with H_k = (J_k/2) Z + (h/2) X. Each segment is compiled exactly as a rotation about the axis (h,0,J)/sqrt(J^2+h^2) using Ry(beta) Rz(theta) Ry(-beta). Segments are appended in time order. The pulses are user-supplied placeholders and are not claimed to cancel errors.

Source equation run: `17e2d022-b9b1-45a6-b5d5-711f63d82316`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: singlet-triplet logical qubit; |0> and |1> are the sigma_z eigenstates (Qiskit little-endian, single qubit)

## Assumptions

- Energies and times are in consistent units with hbar=1.
- sigma_z maps to Z and sigma_x to X.
- The first segment is applied first in time.
- The example pulses are placeholders, not an error-cancelling sequence.

## Unresolved issues

- Explicit dynamically corrected pulse sequences are not given in the abstract.
- The control-noise coupling J'(J) is undefined.
- Noise spectra and fidelity values are unknown.
- Non-Markovian bath effects and the universal gate set are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: per-segment omega=hypot(J,h), beta=atan2(h,J) define H_k=(J_k/2)Z+(h/2)X. Each segment Hamiltonian is realized through its axis and angle; sigma_z is Qiskit Z and sigma_x is Qiskit X.
- `eq_2`: implemented; build_circuit: loop over segments appending ry(-beta), rz(theta), ry(beta) in time order. Exact exponential of each segment, with the ordered product giving later segments on the left in matrix form.
- `eq_3`: out_of_scope; no code location. The first-order error vectors E_h and E_J are classical diagnostics for pulse design and are not part of the circuit. The J'(J) coupling is also undefined in the specification.

## Specification changes

- eq_1, eq_2: Scope narrowed to the ideal noiseless unitary for user-supplied pulses; no pulse search is performed and no pulse values are hardcoded in the module. Reason: The abstract gives no explicit sequences or search constraints. The example pulses are placeholders and are not claimed to cancel errors.
- eq_3: Error-vector cancellation is not implemented or checked in the circuit. Reason: This is classical post-processing, and J'(J) is not defined.
- eq_1: Added input validation: h>0, J_max>0, 0<=J_k<=J_max, tau_k>=0, and at most 64 segments. Reason: These bounds enforce the physical constraints and keep the circuit size bounded.
