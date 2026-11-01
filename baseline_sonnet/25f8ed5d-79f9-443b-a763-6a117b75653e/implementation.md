# Equation to Qiskit

Builds the first-order two-term Trotter circuit (e^{-iAt/n} e^{-iBt/n})^n for a transverse-field Ising chain, with A = J*sum Z_i Z_{i+1} and B = h*sum X_i. Only the ideal unitary Trotter product of eq_1 is implemented. The imperfect-gate error model and the n* optimisation are not circuit operations, so they are left as background or out of scope.

Source equation run: `08210274-37ab-4448-a570-e27cd1c4887b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit i (0..num_qubits-1) = spin site i of register 'sys'; qubit 0 is the least significant computational-basis bit
- No ancilla qubits; total qubits = num_qubits <= 12

## Assumptions

- Ideal gates: RZZ(2*J*t/n) implements exp(-i J (t/n) Z Z) and RX(2*h*t/n) implements exp(-i h (t/n) X)
- Within one step all A terms are applied first (they commute), then all B terms
- Periodic boundary conditions require at least 3 qubits to avoid doubling a bond
- t must be positive

## Unresolved issues

- The paper's actual gate-error model, statistical distance and exact n* formula are not given in the abstract and are not reproduced
- The paper's Hamiltonian and system size are unknown

## Equation mapping

- `eq_1`: implemented; build_circuit: loop over n steps applying RZZ gates (e^{-iAt/n}) then RX gates (e^{-iBt/n}). The finite-n product (e^{-iAt/n} e^{-iBt/n})^n is built for a concrete Ising A and B. The limit n->infinity is not taken; n is an instance parameter.
- `eq_2`: background; no code location. The first-order Trotter error bound c_T t^2/n motivates the construction but is not a circuit operation.
- `eq_3`: out_of_scope; no code location. The toy gate-error accumulation model describes noise, but the required output is a measurement-free ideal unitary circuit with no noise channels.
- `eq_4`: out_of_scope; no code location. The total-error trade-off depends on the assumed noise model of eq_3 and is a classical analysis, not part of the circuit.
- `eq_5`: out_of_scope; no code location. The toy-model optimum n* is classical post-processing. The caller chooses n, and no optimisation is done in the circuit.

## Specification changes

- eq_1: Specialised the abstract two-term splitting to a transverse-field Ising chain with A = J sum Z_i Z_{i+1} (open or periodic) and B = h sum X_i. Reason: The specification left the Hamiltonian, system size and register unspecified, and a concrete circuit needs them.
- eq_1: The circuit has a finite, user-chosen Trotter number n (1..500) instead of the limit n->infinity. Reason: A circuit can only contain finitely many steps.
- eq_3, eq_4, eq_5: Narrowed scope to the ideal (noise-free) Trotter circuit; the gate-error model, total-error trade-off and n* optimisation are not implemented. Reason: The error model is only a toy assumption, and the artifact must be a bound, measurement-free unitary circuit with no noise channels or classical post-processing.
