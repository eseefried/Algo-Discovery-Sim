# Equation to Qiskit

Non-adaptive generalized Kitaev phase-encoding operation on M<=12 unentangled probe qubits. Qubit k receives n_k separate applications of the phase gate P(phi), then optional feedback offset P(theta_k), then an X-basis readout Hadamard. The runner prepares |+>^M and performs measurement and Bayesian post-processing. Lossless; the circuit is bound, unitary and measurement-free.

Source equation run: `43cd7d75-9366-4347-ba77-5ae80013ff2e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = probe 0 (b_0), receives n[0] phase gates
- qubit 1 = probe 1 (b_1), receives n[1] phase gates
- qubit k = probe k (b_k), receives n[k] phase gates; k=0..M-1, M=len(n)<=12
- Runner should prepare each probe in |+> (H on |0>); no ancilla qubits; computational-basis little-endian, qubit 0 least significant bit

## Assumptions

- The phase gate is diag(1,e^{i phi}), implemented as qc.p(phi, k) directly with no controlled-U or eigenstate ancilla.
- Each repeated placement is an explicit separate gate, counted as one query.
- Caps of n_k<=64 and N<=128 are implementation limits, not from the source.
- The runner prepares |+>^M.

## Unresolved issues

- The abstract does not give the optimal n_k distributions, the exact estimator or the loss model, so no optimal strategy is encoded.
- Adaptive feedback schedules and entangled-strategy comparisons are not reconstructed.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop of qc.p(phi, qr[k]) repeated n[k] times. Acting on the runner-prepared |+> input, n_k applications of diag(1,e^{i phi}) give (|0>+e^{i n_k phi}|1>)/sqrt2.
- `eq_2`: implemented; build_circuit: validation of n and total = sum(n). The distribution n_k determines N=sum n_k, the number of placed gates; the code validates that each n_k is a positive integer and caps N.
- `eq_3`: implemented; build_circuit: optional qc.p(theta[k]) and readout qc.h(qr[k]). The offset and final Hadamard map the phase n_k phi+theta_k to the stated Z-basis outcome probabilities; the likelihood itself is a classical consequence, and sampling is left to the runner.
- `eq_4`: out_of_scope; no code location. Classical grid Bayesian estimator; it is post-processing of measurement outcomes and not a quantum operation.
- `eq_5`: out_of_scope; no code location. Circular error figure of merit is a classical average over outcomes and phases; no circuit is generated for it.

## Specification changes

- eq_1: |+> state preparation is not included in the circuit; the runner supplies the input state. Reason: The task requires an operation without input-state preparation.
- eq_3: Measurement is omitted; only the pre-measurement readout Hadamard (switchable via readout_hadamard) is applied. Reason: The circuit must be measurement-free; the Hadamard is a unitary basis change.
- eq_1, eq_2, eq_3: The scope is narrowed to the lossless, non-adaptive case with a fixed user-supplied n_k vector and a bound numerical phi. The theta offsets are static inputs, not feedback computed from earlier outcomes. Reason: Dynamic circuits are disallowed; loss, optimization of n_k and adaptivity are outside the specified instance.
- eq_4, eq_5: Classical estimation and error evaluation are excluded. Reason: They are not part of a unitary circuit operation.
