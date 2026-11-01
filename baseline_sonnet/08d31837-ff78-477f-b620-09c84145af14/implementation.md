# Equation to Qiskit

Builds the Bell-basis encoding unitary (H on each control qubit, then CNOT onto its partner target), which maps computational inputs |a>|b> to Bell-like states with 2^m equal-magnitude terms. The default m=1 is the specified 2-qubit instance. Values of m up to 6 give a tensor product of m Bell pairs, which is a simple extension. The paper's two multi-qubit controlled-unitary gates are not reconstructed because the abstract does not define them.

Source equation run: `12af79bc-738e-4218-a4aa-6960f6c653b0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit 0 = specification qubit 1 (control, receives H); input bit a
- Qiskit qubit 1 = specification qubit 2 (CNOT target); input bit b
- For general m: qubits 0..m-1 are controls with input bits a_i, qubits m..2m-1 are targets with input bits b_i, and pair i is (i, m+i)
- Little-endian: qubit 0 is the least significant bit of the computational-basis index

## Assumptions

- The Bell construction is a stand-in and not the paper's controlled-unitary algorithm.
- Input basis states |a>|b> are prepared by the runner, not by the circuit.
- m=1 on 2 qubits is the primary instance.

## Unresolved issues

- The definitions and working principles of the paper's two multi-qubit controlled-unitary gates are unknown.
- The general-m sign and term-selection patterns for genuinely multi-term entangled bases are not reconstructed.
- The entanglement and monogamy-score analysis and the qudit extension are out of scope.

## Equation mapping

- `eq_1`: background; no code location. This is the equal-amplitude form of the output states. The circuit produces it (2^m terms with signs ±1/sqrt(2^m)), but no gate corresponds directly to it. It is a property to check after generation.
- `eq_2`: background; no code location. Orthonormality is a property of the basis. It holds because the circuit is a unitary applied to the orthonormal computational inputs. No code is needed for it.
- `eq_3`: implemented; build_circuit: loop with qc.h(i); qc.cx(i, m+i). H on the control qubit followed by CNOT to the target gives the Bell state for input |a>|b>. This is exact for m=1 and applied per pair for m>1.
- `eq_4`: background; no code location. The generic multi-controlled unitary C^kU is not used. The only controlled gate is a single-control CNOT, which is the k=1 case with U=X. The paper's two specific gates are unspecified.

## Specification changes

- eq_3: Added an optional parameter m (1..6) that tensors m Bell-pair encoders on 2m qubits. The default m=1 is exactly the specified instance. Reason: The task asks for varying valid instance parameters. The output still has 2^m terms with amplitudes ±1/sqrt(2^m). It is a product of Bell pairs, not the paper's general multi-term constructions.
- eq_3: Mapped specification qubit 1 (control) to Qiskit qubit 0 and specification qubit 2 (target) to Qiskit qubit 1, with the ket written |q1 q2> in the specification but little-endian in Qiskit. Reason: This follows Qiskit's convention that qubit 0 is the least significant bit.
- eq_4: The paper's two multi-qubit controlled-unitary gates are not implemented. Reason: The abstract does not define them, so scope is narrowed to the standard H and CNOT stand-in.
