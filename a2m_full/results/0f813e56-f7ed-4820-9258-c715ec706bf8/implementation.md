# Equation to Qiskit

Implements one scoped construction: the Hadamard-test circuit (eq_3) for comparing two small gate-list unitaries U and V on n data qubits. It uses one ancilla. The circuit applies H on the ancilla, then controlled-U, then controlled-V^dagger (V's gate list reversed with each gate inverted), then either H (X readout, Re<0|V^dagger U|0>) or Sdg then H (Y readout, Im). Inputs, measurement, sampling and the thresholding decision are left to the runner. The swap test, the Bell-pair test and the classification rule are not implemented.

Source equation run: `83d79914-df8e-4bf9-a709-ce05d0b540a1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data register (data_A), little-endian, expected to hold |0^n> or another runner-prepared input
- qubit n: ancilla (anc), expected |0> on input
- data_B is not used (swap and Bell tests out of scope)
- Total qubits = n+1, capped at 12 so n<=11
- Readout: ancilla P0-P1 gives Re<0|V^dagger U|0> for readout X and Im for readout Y

## Assumptions

- Gate lists use the supported names h, x, y, z, s, sdg, t, tdg, cx, cz, swap, rx, ry, rz, p and gphase.
- Each gate is controlled via the standard Gate.control(1) with the ancilla as control.
- The runner prepares the data register in |0^n> and the ancilla in |0>.
- The example circuit has n=1, U=H and V=H Z Z e^{0.7i}, so it is equal to U up to a global phase.
- At most 200 gates per list.

## Unresolved issues

- The paper's actual equivalence-checking algorithms (stabilizer, decision-diagram, tableau) and its benchmark circuits are not reconstructed.
- Exact versus up-to-phase classification (eq_5) must be done outside the circuit by the runner.
- The Hadamard test here is input-specific to |0^n>. Full-unitary phase equality needs the Bell register, which is not implemented.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Swap test is not built. Only the Hadamard test is implemented in this artifact.
- `eq_2`: background; build_circuit / _apply: V^dagger is built by reversing V's gate list and inverting each gate. The compute-uncompute measurement is not implemented. Its V^dagger U construction is reused inside the controlled-W of the Hadamard test.
- `eq_3`: implemented; build_circuit: H on anc, controlled U, controlled V^dagger, then H (X) or Sdg then H (Y). The Hadamard-test circuit. After the circuit, the ancilla P0-P1 equals Re (X) or Im (Y) of <0^n|V^dagger U|0^n> when the data input is |0^n>. The readout itself is done by the runner.
- `eq_4`: out_of_scope; no code location. The Bell-pair Choi test is not built, because it needs input-state preparation of Bell pairs. The circuit here is the Hadamard test on the data register only.
- `eq_5`: out_of_scope; no code location. Threshold classification is classical post-processing and is not part of the unitary circuit.

## Specification changes

- eq_3: Scope narrowed to the Hadamard test alone, on the data input supplied by the runner (nominally |0^n>). The first H on the ancilla is included as part of the test circuit. Compute-uncompute, swap and Bell variants are omitted. Reason: The task asks for ONE construction, and the circuit must be an operation with no measurement and no input-state preparation.
- eq_3: Added a 'gphase' pseudo-gate to the gate-list format. Its controlled version is a phase gate p(angle) on the ancilla, and the inverse negates the angle. Reason: Lets V = e^{i phi} H be expressed, so global-phase differences become observable as relative ancilla phase, as eq_3 intends.
- eq_3: Controlled-W is implemented as controlled-U followed by controlled-V^dagger, with V^dagger from the reversed, inverted gate list. Sign check: Sdg then H on (|0>+w|1>)/sqrt2 gives P0-P1 = Im w. Reason: Matches the stated convention that the Y readout uses S^dagger before the final H.
