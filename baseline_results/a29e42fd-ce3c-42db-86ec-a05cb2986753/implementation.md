# Equation to Qiskit

Abstaining from circuit generation. The reconstructed specification describes a continuous-variable (single bosonic mode) squeezed-light phase-estimation scheme whose scientific content is classical stochastic estimation: an Ornstein-Uhlenbeck phase-noise model, a linearized homodyne record, a Kalman-Bucy filter, an RTS fixed-interval smoother, and a robust (min-max) smoother whose synthesis equations are the missing paper contribution. None of these equations defines a unitary qubit operation. A faithful qubit implementation would require (i) a truncated-Fock encoding with displacement and squeezing operators, which are non-standard dense unitaries on the encoded register (disallowed), and (ii) a classical filtering/smoothing pipeline that is not a quantum circuit at all. Fabricating a toy qubit circuit (e.g. a diagonal phase rotation on a Fock-encoded register) would not preserve the meaning of any specified equation, so no code is returned.

Source equation run: `32c26659-a914-41f8-86f1-e1f00269cfdf`

Generation: **unsupported**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- The abstract's scheme is taken at face value as single-mode squeezed-light homodyne phase estimation with classical Kalman/RTS/robust smoothing, as reconstructed in the preceding specification.
- Truncated-Fock encodings of displacement and squeezing on qubits were judged to violate the prohibition on opaque dense unitaries and to add content not present in the specification, so they were not attempted.

## Unresolved issues

- No qubit-native formulation of the scheme exists in the supplied material; a faithful implementation would require a continuous-variable (Gaussian-state) simulator plus classical filtering code, which is outside the build_circuit(instance) -> QuantumCircuit contract.
- The paper's actual robust fixed-interval smoother equations (guaranteed-cost/H-infinity Riccati structure, RTS vs two-filter form) remain unknown, so even the classical postprocessing could not be reconstructed exactly.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Classical stochastic differential equation (Ornstein-Uhlenbeck phase noise) describing the parameter process; it is not a unitary operation on qubits and the stochastic phase path would have to be sampled classically by the runner.
- `eq_2`: out_of_scope; no code location. Linearized homodyne measurement model on a continuous-variable mode with a squeezed probe; implementing it would require bosonic displacement/squeezing operators on a truncated Fock register (dense non-standard unitaries) and a measurement, both outside the allowed measurement-free, standard-gate qubit construction.
- `eq_3`: background; no code location. Definition of the norm-bounded uncertainty set on the damping rate; a purely classical design assumption with no circuit counterpart.
- `eq_4`: out_of_scope; no code location. Kalman-Bucy forward filter: classical postprocessing of the measurement record, not a quantum operation.
- `eq_5`: out_of_scope; no code location. RTS backward fixed-interval smoother: classical postprocessing, not a quantum operation.
- `eq_6`: out_of_scope; no code location. Robust worst-case smoothing criterion; the concrete robust-smoother synthesis is missing from the abstract and in any case is a classical optimization, not a circuit.
- `eq_7`: background; no code location. Mean-square-error figure of merit used to compare estimators; an evaluation metric for classical Monte Carlo, not an implementable operation.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5, eq_6, eq_7: Scope narrowed to zero: no Qiskit construction is produced for this specification. Reason: The specification is a continuous-variable metrology scheme with classical estimation; it contains no qubit-gate-model operation that can be implemented with standard gates without inventing content (bosonic encodings via dense unitaries) or misrepresenting classical filtering as a quantum circuit. The math stage itself flagged that a bosonic/Gaussian-state simulator rather than a qubit circuit would be needed.
