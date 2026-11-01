# Equation to Qiskit

Builds the two-qutrit ternary controlled-X (TCX: |c,t> -> |c,t+c mod 3>) or controlled-Z (TCZ: |c,t> -> w^(ct)|c,t>) gate on 4 qubits, with each qutrit encoded in 2 qubits (value = q_low + 2*q_high, and the unused value 3 is left fixed). Optional inverse. The Fourier-conjugation relation (eq_4) is not implemented.

Source equation run: `f60431d2-e0c0-404a-9d16-9f050a786c68`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control qutrit low bit (value = q0 + 2*q1)
- qubit 1: control qutrit high bit
- qubit 2: target qutrit low bit (value = q2 + 2*q3)
- qubit 3: target qutrit high bit
- qutrit value 3 (bits 11) is unused and left unchanged by the circuit

## Assumptions

- Control register is first (qubits 0,1) and target second (qubits 2,3).
- Little-endian qutrit encoding: value = low bit + 2*high bit.
- TCX applies X^c to the target and TCZ applies Z^c, as assumed in the specification.

## Unresolved issues

- The paper's exact TCX/TCZ definitions (for example, control on a single level) are unknown.
- The Fourier relation eq_4 is not realized in the circuit.
- Behavior on the unused encoded value 3 is identity by choice.

## Equation mapping

- `eq_1`: implemented; _shift (qutrit X); Z phases appear as omega^(c*t) in the TCZ branch of build_circuit. X is a 3-cycle on encoded values 0,1,2 built from SWAP and a negatively controlled CX. Z is used only through the controlled phases of TCZ.
- `eq_2`: implemented; build_circuit, TCX branch. The target is shifted by X for c=1 and by X^2 for c=2, using a 2-qubit controlled gate with ctrl_state selecting the control value.
- `eq_3`: implemented; build_circuit, TCZ branch. A multi-controlled phase gate with angle 2*pi*(c*t mod 3)/3 is applied for each basis pair (c,t) with c,t in {1,2}.
- `eq_4`: out_of_scope; no code location. The qutrit Fourier gate F has no compact exact standard-gate decomposition in the 2-qubit encoding without an opaque dense unitary, which is disallowed. The TCX/TCZ relation is therefore not built.

## Specification changes

- eq_1, eq_2, eq_3: Qutrits are encoded in 2 qubits each, with the unused value 3 mapped to itself (identity). The construction acts as the specified gate only on the 3x3 qutrit subspace. Reason: A qutrit does not fit in a qubit register, and the circuit must be a unitary on qubits.
- eq_4: The Fourier-conjugation relation between TCX and TCZ is not implemented. Reason: The Fourier gate cannot be built without an opaque dense unitary, and the scope is narrowed to a single TCX or TCZ gate.
- eq_2, eq_3: The instance selects TCX or TCZ with an optional inverse flag. The inverse is an added option that is not in the specification. Reason: It provides varying valid parameters while keeping the construction minimal.
