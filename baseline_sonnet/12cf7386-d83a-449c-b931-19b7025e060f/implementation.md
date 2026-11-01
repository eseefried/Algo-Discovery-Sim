# Equation to Qiskit

Unitary block of the assumed controlled Grover iterate U = |0><0|_c (x) I + |1><1|_c (x) G, with G = -(I-2|s><s|)(I-2|w><w|), applied `steps` times on an n-qubit data register and one control qubit. Intermediate control measurements, Tulsi's construction, the alternative angular parameter, MI and CCM are not implemented, because the circuit must be measurement-free and unitary.

Source equation run: `0da901fc-85c1-41d3-8095-66f29ccf39a2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: data bit 0 (least significant bit of item index x)
- qubit 1: data bit 1 (item index x = b0 + 2*b1 for the n_data=2 example; general n_data uses qubits 0..n_data-1)
- qubit n_data (qubit 2 in the example): control qubit, |1> activates G, |0> acts as identity
- encoding: computational-basis integer encoding of item index, marked item w has bit i on qubit i

## Assumptions

- Single marked item w
- Control qubit is a plain control of G, with no other role from Tulsi's algorithm
- Control initial state |+> and data initial state |s> are prepared by the runner
- Total qubits n_data+1 <= 12, so n_data <= 11, and steps <= 1000
- Little-endian encoding of the item index on data qubits

## Unresolved issues

- Tulsi's exact modified operator and the control qubit's role
- The paper's alternative angular parameter
- Mutual Information and Cumulative Correlation Measure definitions
- The measurement-interleaved dynamics cannot be represented in a unitary circuit
- Order estimation and time lapses studied are unspecified

## Equation mapping

- `eq_1`: implemented; build_circuit loop body: controlled oracle and controlled diffusion. G = -(I-2|s><s|)(I-2|w><w|) is built from the X-conjugated multi-controlled Z oracle and the H/X-conjugated diffusion, each with the control added as an extra control. The overall minus sign is the controlled phase p(pi) on the control.
- `eq_2`: background; no code location. Closed-form success probability of the unmeasured Grover evolution. It is an analytic result for later comparison, not an operation.
- `eq_3`: implemented; build_circuit: every gate in the loop body carries the control qubit, plus the p(pi) on the control. U = |0><0|(x)I + |1><1|(x)G is realized for steps repetitions. Control and data initial states are prepared by the runner.
- `eq_4`: out_of_scope; no code location. A non-selective projective measurement of the control is a non-unitary channel, which is disallowed in a measurement-free unitary circuit.
- `eq_5`: out_of_scope; no code location. The total evolution interleaves the measurement channel of eq_4. Only the unitary block U^k is built, as `steps`, with no interleaved measurement.

## Specification changes

- eq_4, eq_5: Intermediate control measurement and the measured evolution are removed. The circuit is only the unitary block U^steps, with no dephasing between blocks. Reason: The operation must be measurement-free, unitary and non-dynamic.
- eq_3: The controlled -1 phase of G is implemented as a phase gate p(pi) on the control qubit. The oracle and diffusion are controlled by adding the control to the multi-controlled Z. Reason: This is the standard decomposition of a controlled G, and it keeps the relative phase between the control=0 and control=1 branches.
- eq_1, eq_2: Tulsi's modified operator and the paper's alternative angular parameter are not implemented. A generic controlled standard Grover iterate is used instead. Reason: The abstract does not give the exact construction, so it cannot be reconstructed.
- eq_3, eq_5: The time lapse k is not a parameter. Only the total number of steps is exposed. Reason: Without measurements, k has no effect on the circuit.
