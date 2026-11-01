# Equation to Qiskit

Builds the Hadamard-test operation H(ctrl) - controlled-U_sigma - H(ctrl) on 3 qubits, with exactly one controlled query to a permutation sigma of {0,1,2,3}. U_sigma is built from multi-controlled X gates by cycle-to-transposition decomposition. Probe-state preparation, measurement and the parity decision are left to the runner or classical post-processing.

Source equation run: `b3511eb8-07be-4867-8ad5-06f1fe3b0069`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: ctrl (Hadamard-test control, least significant bit of the Qiskit index)
- qubit 1: sys bit b0 (least significant bit of ququart x)
- qubit 2: sys bit b1 (most significant bit of ququart x); x = 2*b1 + b0
- Input convention: runner prepares the probe |phi> on qubits 1,2 and ctrl in |0>; the operation applies H, controlled-U_sigma, H on ctrl; ctrl is to be measured by the runner

## Assumptions

- Instance is {"permutation": [sigma(0),sigma(1),sigma(2),sigma(3)]} with U|x>=|sigma(x)>
- Sys encoding x = 2*q2 + q1, control is qubit 0
- The initial H on the control is part of the operation, and ctrl is supplied in |0>
- The controlled oracle counts as one query; its internal gate decomposition is an implementation detail

## Unresolved issues

- No verified probe |phi> separating even and odd permutations by Re<phi|U|phi> is given
- The correspondence to the paper's photonic ququart protocol is not established
- The two-copy antisymmetric variant is not implemented

## Equation mapping

- `eq_1`: background; no code location. Parity as determinant of the permutation matrix is a standard fact motivating the task; the circuit does not compute it.
- `eq_2`: implemented; build_circuit (H on ctrl, controlled-U_sigma via _cswap, H on ctrl). The Hadamard-test structure with a single controlled-U_sigma query. P0 = (1+Re<phi|U|phi>)/2 holds for the runner-prepared probe |phi>.
- `eq_3`: background; no code location. Classical amplitude expansion of the overlap, used only for offline tabulation; no circuit element.
- `eq_4`: out_of_scope; no code location. Existence and search of a probe |phi> separating even and odd permutations is not resolved here and is not part of the operation.
- `eq_5`: out_of_scope; no code location. Classical decision rule on 2*P0-1 is post-processing performed outside the circuit.

## Specification changes

- eq_2, eq_3, eq_4: Probe-state preparation of |phi> (spec step 2) is omitted from the circuit; |phi> is expected to be prepared by the runner on qubits 1,2. Reason: The task requires an operation without input-state preparation, and no verified separating |phi> is available.
- eq_2: The black-box placeholder is replaced by an explicit controlled permutation built from multi-controlled X gates and CX conjugation, parametrized by the instance permutation. Reason: A concrete bound unitary circuit is required, and an opaque dense unitary is not allowed.
- eq_2, eq_5: Measurement of ctrl is not included in the circuit. Reason: The circuit must be measurement-free; the runner measures or computes P(0) from the final state.
- eq_4, eq_5: The parity-decision claim is narrowed: no claim is made that the single-probe separation exists or that parity is determined. Reason: The separation property is unverified in the specification.
