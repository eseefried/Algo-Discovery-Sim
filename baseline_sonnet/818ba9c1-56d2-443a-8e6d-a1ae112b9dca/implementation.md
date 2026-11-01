# Equation to Qiskit

Single-qubit operation implementing the amplitude-error gate U(epsilon)=RX(pi(1+epsilon)) applied m times in sequence, with no state preparation or measurement. Input validation is done before the circuit is allocated.

Source equation run: `68e47f24-7f98-47a1-913f-90a1ffe21b26`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: single data qubit q (least significant bit; computational basis |0>,|1>); no ancilla, no classical bits

## Assumptions

- The amplitude-error model on an X rotation is my own parametrization, not taken from the abstract.
- Repetitions are emitted as m separate RX gates rather than one RX(m*theta), so the repeated-gate structure is preserved.
- The runner prepares the input state, e.g. |0>, and performs any measurement.

## Unresolved issues

- The robust Higgins-type phase estimation procedure, its depth schedule and its error bounds are not specified in the abstract and are not implemented.
- The off-resonance error model, the universal gate-set sequences and the SPAM-robustness mechanism are not implemented.
- No public validation contract was supplied.

## Equation mapping

- `eq_1`: implemented; build_circuit: theta = pi*(1+eps); qc.rx(theta, 0). RX(theta) equals exp(-i theta X/2) exactly, so one gate application is U(epsilon).
- `eq_2`: implemented; build_circuit: for loop applying qc.rx(theta, 0) m times. The gate is repeated m times with identical coherent error, giving U(epsilon)^m.
- `eq_3`: background; no code location. Outcome probability cos^2(m pi(1+epsilon)/2) is a property of the circuit's output when measured from |0>. Measurement and input preparation are excluded from the operation.
- `eq_4`: out_of_scope; no code location. Empirical shot statistics and binomial variance are sampling and post-processing, not part of the unitary operation.
- `eq_5`: out_of_scope; no code location. The Heisenberg-scaling target is an estimation-precision claim for the full protocol, which needs multiple depths and classical post-processing. It is not a circuit.

## Specification changes

- eq_3, eq_4, eq_5: Scope narrowed to the coherent operation U(epsilon)^m only. Measurement, shot sampling, estimator and depth-combination logic are not implemented. Reason: The task requires an operation without measurement or sampling, and the abstract does not give the robust phase-estimation rule.
- eq_1, eq_2: Added validation limits: |epsilon| <= 1 and 1 <= m <= 1024. Each m is a separate instance, not a depth schedule. Reason: Bounds the circuit size and keeps epsilon in the small-error regime. A single depth per circuit is the simplest scope.
