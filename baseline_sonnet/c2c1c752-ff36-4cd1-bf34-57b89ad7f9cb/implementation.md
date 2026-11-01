# Equation to Qiskit

Ancilla-free Bernstein-Vazirani operation H^n . O_f . H^n on n<=12 qubits. O_f is the diagonal phase oracle (-1)^{f(x)}, built from a truth table with one multi-controlled phase flip per minterm. Measuring the output register gives y with Pr[y=s]=fhat(s)^2, so Pr[y_i=1]=Inf_i(f). The example is f=AND on 2 bits.

Source equation run: `d8bffd3a-5116-4092-9140-a7a6ab18343b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x_1, least significant bit of the input and output string y (y_1)
- qubit 1: x_2 (y_2); in general qubit i-1 holds x_i and y_i for i=1..n
- No ancilla qubit; total qubits = n <= 12
- Truth-table index x = sum_i x_i 2^(i-1); the computational-basis input is prepared by the runner, expected |0^n>

## Assumptions

- f is given as a complete truth table of 0/1 values of length 2^n
- The runner prepares |0^n> and measures all qubits; the operation includes the leading and trailing Hadamard layers
- Multi-controlled phase gate (mcp) decomposition by Qiskit is acceptable
- Example f is AND on 2 bits, as assumed in the specification

## Unresolved issues

- The paper's own approximation algorithm, error bounds and junta-learning procedures are not implemented
- A truth-table oracle costs O(2^n) multi-controlled gates, which is acceptable only for the small sizes allowed here

## Equation mapping

- `eq_1`: implemented; build_circuit (H layer, oracle loop via _phase_flip_basis_state, H layer). The unitary H^n O_f H^n acting on |0^n> gives amplitudes fhat(s), so measuring yields Pr[y=s]=fhat(s)^2.
- `eq_2`: background; no code location. Influence definition. The circuit does not compute it; it is used to interpret the output distribution and to check it classically.
- `eq_3`: background; no code location. Marginal Pr[y_i=1]=Inf_i(f) is a property of the output distribution of the implemented circuit. Verification happens downstream, not in the circuit.
- `eq_4`: out_of_scope; no code location. Repeated sampling, averaging and the Hoeffding bound need measurement and classical postprocessing, which a measurement-free operation excludes.
- `eq_5`: background; no code location. Tiny AND instance. It is given as example_instance_json (truth_table [0,0,0,1]), and expected values come from the runner, not from this module.

## Specification changes

- eq_1: Used a direct ancilla-free phase oracle (-1)^{f(x)} built from multi-controlled phase flips on each minterm, instead of U_f with an ancilla in |->. Reason: Gives the same phase action on the input register without ancilla preparation, which the runner would otherwise have to do, and uses fewer qubits.
- eq_1, eq_3: Fixed the bit convention: variable x_i is on qubit i-1, and truth-table index bit i-1 equals x_i. Reason: The specification left the ordering assumed; Qiskit's little-endian convention forces an explicit choice.
- eq_4: Narrowed scope to the unitary operation only. Measurement, sampling, the estimator and the Hoeffding bound are excluded. Reason: The task requires a measurement-free unitary circuit.
- eq_1, eq_2, eq_3, eq_5: The function f is supplied as an explicit truth table, with n capped at 12. Reason: A generic Boolean function needs a concrete description for code generation, and the qubit cap bounds n.
