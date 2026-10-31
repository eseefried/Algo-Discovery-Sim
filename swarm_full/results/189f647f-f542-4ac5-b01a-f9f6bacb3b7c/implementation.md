# Equation to Qiskit

Abstained: the abstract and specification do not give the overlap mapping, the MBQC resource state and measurement angles, the normalization relating the overlap to Z, or the approximation scale. A circuit built from them would be invented, not reconstructed, so no code is emitted.

Source equation run: `fec55541-d378-4269-a3b7-cb7e3d93671e`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- No public validation contract or requested instance was supplied, so none constrains the scope.
- The earlier generic MBQC outline is a plan only and not a faithful construction of the paper's algorithm.

## Unresolved issues

- Explicit overlap mapping from (J_ij, h_i) to a stabilizer-state overlap is not specified.
- MBQC resource state and measurement bases/angles are not specified.
- Normalization factor relating the overlap to Z is not specified.
- Formula for the approximation scale Delta is not specified.
- Real-parameter domain boundaries are not specified.
- Handling of complex couplings and fields in a unitary circuit is unresolved.

## Equation mapping

- `eq_1`: background; no code location. This is the classical definition of the Ising partition function. Without the paper's overlap mapping it does not determine a unitary operation, so it serves only as background.
- `eq_2`: out_of_scope; no code location. This is an additive-error criterion on classical post-processed estimates, with an undefined scale Delta. It involves sampling and estimation, which are excluded from a measurement-free unitary operation, and it is not a circuit operation.

## Specification changes

- eq_1, eq_2: Scope narrowed to nothing implementable. No circuit construction was selected and both equations are mapped to non-implemented dispositions. Reason: The specification marks the overlap mapping, MBQC circuit, resource state, measurement angles, normalization and approximation scale as missing. Any concrete circuit would rest on fabricated details.
