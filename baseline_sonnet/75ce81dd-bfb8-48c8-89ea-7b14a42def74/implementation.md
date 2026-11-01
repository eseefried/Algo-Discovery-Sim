# Equation to Qiskit

Builds a first-order-accurate (Strang-split, second-order) Trotterized propagator U(T) for the two-spin Hamiltonian H = (mu_B B(t)/2)(g1 Z1 + g2 Z2) + (J/4) sigma1.sigma2, with B(t) piecewise constant over user-supplied segments (eq_1, eq_3). The Heisenberg exchange terms commute and are applied exactly via RXX, RYY and RZZ. The g-factor-dependent Zeeman terms are applied via RZ. No optimal control, no resonant drive and no fidelity evaluation are included.

Source equation run: `45c0ef5e-6db0-4cdb-af8a-44606c12fb59`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = q1 (electron 1 spin, register q1)
- qubit 1 = q2 (electron 2 spin, register q2)
- Encoding: computational basis |0> = sigma_z +1, |1> = sigma_z -1; Qiskit qubit 0 is least significant bit

## Assumptions

- hbar=1 and the angular-frequency units are consistent with J and mu_B*B
- Isotropic Heisenberg exchange replaces the paper's non-diagonal exchange
- Segments are applied in list order, first segment first
- g1 and g2 are positive and J may be any real value

## Unresolved issues

- The paper's actual non-diagonal exchange form is unknown
- Realistic values of J, g1, g2 and field amplitudes are unknown
- The optimal control parametrization and the target gate durations are not available
- The Trotter error is not quantified here

## Equation mapping

- `eq_1`: implemented; _zeeman and _exchange (called from build_circuit). The Zeeman term with g1, g2 is implemented by RZ rotations, and the isotropic Heisenberg exchange J/4 sigma1.sigma2 by RXX, RYY and RZZ with angle J*dt/2.
- `eq_2`: background; no code location. Resonance addressing motivates the g1 != g2 difference, but no rotating-frame drive or resonance tuning is implemented. B is just a static value per segment.
- `eq_3`: implemented; build_circuit segment/Trotter loop. The time-ordered exponential is approximated by a product over piecewise-constant segments, each with a symmetric (Strang) Trotter splitting of Zeeman and exchange parts.
- `eq_4`: out_of_scope; no code location. The fidelity objective is a classical optimization cost. This module returns only the operation and does no optimization or evaluation.

## Specification changes

- eq_3: The exact time-ordered exponential is replaced by a Strang-split Trotter product with a user-chosen number of steps per segment, so the unitary is approximate with error that shrinks as trotter_steps grows. Reason: The Zeeman difference term (g1-g2) does not commute with the exchange term, so no exact standard-gate decomposition is generally available.
- eq_1: B(t) is restricted to piecewise-constant segments supplied in the instance. mu_B is a user-supplied scale (default 1) and hbar=1. The circuit's global phase is not tracked. Reason: A gate-based circuit needs a discrete, bound parametrization. The abstract gives no numeric values or units.
- eq_1, eq_2: Scope is narrowed to isotropic exchange with static-field segments. There is no non-diagonal exchange, no exchange suppression by repeated single-spin rotations, no resonant drive, and no optimal-control search. Reason: These details are absent from the abstract, and the specification marks them as assumptions or missing information.
- eq_4: The fidelity cost is not implemented. Reason: It is a classical objective and not part of the circuit operation.
