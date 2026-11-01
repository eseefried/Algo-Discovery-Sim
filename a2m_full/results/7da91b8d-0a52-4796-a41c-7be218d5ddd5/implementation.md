# Equation to Qiskit

Builds the n+1 qubit Hadamard-test operation for the influence of variable i. It applies CX(a->x_i), then a phase oracle U_f synthesized from a truth table, then CX(a->x_i), then H on the ancilla. The oracle uses X gates and one multi-controlled phase of pi per f(x)=1 input, with no dense unitary. Input preparation (H on the x qubits and the ancilla) and measurement are left to the runner. If the runner prepares |s>|+>, then P(ancilla=1)=Inf_i(f).

Source equation run: `dd21c7e9-1078-4219-b0d7-4834e54f2d7d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x_0 (least significant input bit)
- qubit 1: x_1
- qubit 2: x_2
- qubit 3: interference ancilla a (runner prepares |+>; read in the computational basis after the final H; P(1)=Inf_i)
- Input register is expected in |s>=H^{(x)n}|0^n> and the ancilla in |+>, both prepared by the runner
- Truth-table index x has bit j equal to x_j, stored on qubit j

## Assumptions

- f is indexed by the integer x=sum_j x_j 2^j, with x_j on qubit j.
- The phase oracle convention is U_f|x>=(-1)^{f(x)}|x>. The global phase is exactly preserved because mcp(pi) on the all-ones pattern gives -1.
- The runner prepares H on all input qubits and H on the ancilla (|s>|+>) before the circuit.
- The cap is n<=11, so total qubits n+1<=12.
- The example f is x0 AND x1 on 3 variables with target 0, so Inf_0=1/2.

## Unresolved issues

- The paper's BV-based approximation algorithm, junta-learning algorithms and comparison with Floess et al. are not reconstructed.
- The junta gap and threshold tau=2^{-k} are an assumption, and are not used in the circuit.
- Synthesizing the oracle from a truth table needs up to 2^n multi-controlled gates, which is acceptable only for small n.

## Equation mapping

- `eq_1`: background; no code location. Influence definition. It is the target quantity and is not coded. The circuit only provides the interferometric readout.
- `eq_2`: implemented; build_circuit: cx(anc,t), truth-table phase-oracle loop, cx(anc,t). The ancilla-controlled X_i conjugation around one unconditional U_f gives the branch state (|0>U_f|s> + |1>X_iU_fX_i|s>)/sqrt2 when the runner supplies |s>|+>.
- `eq_3`: background; no code location. Analytic identity for the overlap, derived from X_i|s>=|s>. It is not coded.
- `eq_4`: implemented; build_circuit: final qc.h(anc). The final Hadamard on the ancilla makes P(a=1)=(1-Re overlap)/2=Inf_i. Measurement itself is left to the runner.
- `eq_5`: out_of_scope; no code location. Hoeffding shot count and junta thresholding are classical postprocessing and sampling. The generated operation contains no measurement or sampling.

## Specification changes

- eq_2: The initial Hadamards on the input qubits and the ancilla (the |s>|+> preparation in step 1) are excluded from the returned circuit. Reason: The task requires an operation without input-state preparation. The runner must prepare |s>|+> for the stated probabilities to hold.
- eq_2: The opaque placeholder U_f is replaced by an explicit synthesis from a user-supplied truth table, using X gates and multi-controlled phase gates (mcp with angle pi). Reason: Opaque or dense unitaries are disallowed. This gives a concrete, bound, unitary oracle, so the scope is narrowed to oracles given as truth tables.
- eq_4: The measurement of the ancilla into a classical bit is removed. The circuit ends after the ancilla Hadamard. Reason: The returned circuit must be measurement-free.
- eq_5: Shot-count and junta-threshold postprocessing are not implemented. Reason: They are classical statistics outside a unitary circuit.
- eq_1, eq_2, eq_3, eq_4, eq_5: The construction is the Hadamard-test influence estimator, not the paper's Bernstein-Vazirani circuit. Reason: This follows the supplied specification. The BV-based algorithm is outside the specified scope.
