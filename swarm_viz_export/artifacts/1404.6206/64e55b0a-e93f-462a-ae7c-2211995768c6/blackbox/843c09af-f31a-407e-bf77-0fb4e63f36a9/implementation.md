# Equation to Qiskit

Builds the Bell-like-basis unitary W = (controlled-X layer)(H on m control qubits). Qubits 0..m-1 are controls and m..n-1 are targets. Variant 'xor' uses a CNOT fan-out from every control to every target, so f(c) is the parity of c. Variant 'and' uses a multi-controlled X from all controls to each target, so f(c) is the AND of c. The default instance is n=3, m=2. Columns of W are the states |B_x>. The circuit has no input loading and no measurement.

Source equation run: `bdfab35f-9c9a-46b1-bbe7-86dcd74e9e34`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = c1 (control, Hadamard, least significant bit of x)
- qubit 1 = c2 (control, Hadamard)
- qubits m..n-1 = targets t (for the example n=3, m=2: qubit 2 = t)
- Input basis index x = a1 + 2*a2 + 4*y for the example, with qubit 0 as the least significant bit; basis states are prepared externally by the runner

## Assumptions

- Qubit order is c1=qubit 0, c2=qubit 1, targets after the controls.
- Only X-type controlled operations are used.
- The variant key takes 'xor' or 'and', and defaults are n=3, m=2, variant='xor' when keys are absent.
- No default values are used in function signatures.

## Unresolved issues

- The paper's two specific multiple-qubit controlled-unitary gates are not reconstructed.
- The claim that earlier entangled-basis algorithms are special cases is not addressed.
- The number of terms in each basis state (2^m) holds only up to the structure of the chosen f, and software must check orthonormality.

## Equation mapping

- `eq_1`: implemented; build_circuit (whole circuit; column x of the unitary is |B_x>). Applying H to control state |a> gives the (-1)^{a.c} signs. The controlled-X layer then maps |c>|y> to |c>|f(c) xor y>. The circuit produces this state from input |a>|y>.
- `eq_2`: implemented; build_circuit: H loop followed by the controlled-X loop. H on the controls, then the controlled-X layer, in that order.
- `eq_3`: background; no code location. Orthonormality follows from W being unitary. It is a property to be checked by software, not an operation to build.
- `eq_4`: implemented; build_circuit: variant branch ('xor' vs 'and'). f_A is the CNOT fan-out ('xor') and f_B is the multi-controlled X ('and'). Both are generalized to m controls and n-m targets.
- `eq_5`: implemented; build_circuit: qc.mcx(list(c), tq) in the 'and' branch. Standard multi-controlled X, used to flip the target only if all controls are 1. For m=1 it reduces to cx.

## Specification changes

- eq_2: The optional input loading with X gates (parameter x) is not implemented. The circuit is only the unitary W. Reason: The task requires an operation, not an experiment, and inputs are prepared by the runner.
- eq_2, eq_4: Generalized from n=3, m=2 to n up to 12 and 1<=m<n. When n-m>1, the 'xor' variant puts the parity of all controls on every target. The 'and' variant puts the AND of all controls on every target. Reason: The spec leaves f undefined for several targets. This is the simplest consistent extension, and it equals the specified circuit for n=3, m=2.
- eq_1, eq_2, eq_4, eq_5: The construction is a generic H plus controlled-X family, not the paper's two specific controlled-unitary gates. Qudit, entanglement and monogamy analyses are excluded. Reason: The abstract does not give the paper's gates, and the spec marks them as assumptions.
