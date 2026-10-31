# Equation to Qiskit

Bernstein-Vazirani operation H^n, then a phase oracle (-1)^{f(x)} built from a truth table, then H^n, on an n-qubit register. The oracle is ancilla-free: phase flips are applied directly with multi-controlled phase gates, which is equivalent to kickback from an ancilla in |->. Measuring qubit i afterwards would give Bernoulli(Inf_i) samples, but measurement, repetition and estimation are left to the runner.

Source equation run: `a8167d8e-8389-4850-a01c-a85e073b7f94`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit i (i=0..n-1) = input variable x_i, with qubit 0 the least significant bit; truth_table index x = sum_i x_i 2^i
- output bit y_i is read from qubit i after the circuit
- no ancilla qubit; total qubits = n <= 8 (within the 12-qubit cap)
- example: n=3 uses qubits 0,1,2, with f = x0 XOR (x1 AND x2)

## Assumptions

- Phase-oracle form of Bernstein-Vazirani
- Truth-table index x = sum_i x_i 2^i, with x_i on qubit i
- Runner prepares |0^n> and measures qubits afterwards
- Influence normalization is as in the specification (sum of fhat(s)^2 over s_i=1)

## Unresolved issues

- Influence normalization is not fixed by the abstract. The identity Pr[y_i=1]=Inf_i depends on the paper's definition, which may differ from the standard one by a factor.
- Sample complexity, error and confidence parameters, and the junta-learning algorithm are unspecified and not implemented.
- The truth-table oracle uses O(2^n) multi-controlled gates, which is inefficient for larger n.

## Equation mapping

- `eq_1`: background; no code location. Property of the measured output of the circuit (Pr[y_i=1]=Inf_i). The circuit does not compute it; the runner can check it by measuring qubit i.
- `eq_2`: implemented; build_circuit: H layer, truth-table phase oracle, H layer. The unitary H^n O_f H^n yields Pr[y=s]=fhat(s)^2 when applied to |0^n>. The runner prepares the input; the module only builds the operation.
- `eq_3`: background; no code location. Fourier expression for influence, used to link eq_1 and eq_2. It is a mathematical identity and needs no circuit.
- `eq_4`: out_of_scope; no code location. Empirical averaging over N repeated runs is classical post-processing involving measurement and sampling, which build_circuit must not contain.

## Specification changes

- eq_2: The ancilla in |-> and kickback were replaced by a direct ancilla-free phase oracle on the n-qubit register. Reason: The ancilla would have to be prepared in |1> and Hadamard-transformed (input-state preparation), which the operation must not include. The direct phase oracle implements the same (-1)^{f(x)} action.
- eq_2: The oracle is specified by an explicit truth table, and n is capped at 8. Reason: The abstract gives no oracle construction. A truth-table phase oracle works for any f, and its gate count grows as 2^n, so n is limited.
- eq_1, eq_3, eq_4: The scope is narrowed to the single-run BV unitary. Influence estimation, thresholding and junta learning are not implemented. Reason: They are classical post-processing or statistical claims, and the abstract does not detail the junta-learning algorithms.
