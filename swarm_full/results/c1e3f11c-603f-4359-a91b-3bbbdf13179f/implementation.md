# Equation to Qiskit

Implements the one-query Bernstein-Vazirani operation for a completely specified linear Boolean function f(x)=a.x mod 2 on n input qubits: H^{(x)n}, then a phase oracle built from Z gates on the qubits where a_i=1, then H^{(x)n}. When the runner supplies |0^n>, the output is |a>. The two-query affine algorithm and the incompletely defined function classes are not implemented.

Source equation run: `cbc1befa-6df4-45ad-a07e-42318ac5579b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: register x, input register; qubit i is bit i of the computational-basis index (qubit 0 least significant)
- Coefficient a[i] acts on qubit i; for input |0^n> the output basis state has bit i equal to a[i], so its integer index is sum a[i]*2^i
- No ancilla; the phase oracle is implemented directly with Z gates

## Assumptions

- The hidden string a is given explicitly in the instance, and a[i] is the coefficient of qubit i.
- The runner prepares |0^n> and performs any measurement.
- The oracle is a phase oracle, applied as Z gates on the support of a.

## Unresolved issues

- The two-query affine algorithm, its decision rule, and the recovery of b are not specified or implemented.
- The incompletely defined linear and affine function classes and the 2/3 success-probability analysis are not specified or implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop applying qc.z on qubits with a[i]==1 (phase oracle). f(x)=a.x mod 2 is realized as the phase oracle (-1)^{a.x}, a product of Z gates on the support of a.
- `eq_2`: out_of_scope; no code location. The affine function with constant b and the two-query affinity test are not implemented because the second-query construction is unspecified in the abstract. A constant b would only add a global phase in the one-query circuit.
- `eq_3`: implemented; build_circuit: the H layers before and after the oracle loop. The Hadamard-oracle-Hadamard sequence implements the BV mechanism that sends the uniform superposition with phases (-1)^{a.x} to |a>. The initial state preparation is left to the runner.

## Specification changes

- eq_2: Scope narrowed to the one-query linear BV construction only. The two-query affine algorithm is not implemented. Reason: The abstract does not give the second-query construction or the decision rule, so any implementation would be fabricated.
- eq_1, eq_3: A phase oracle built directly from Z gates is used. There is no ancilla in |->, and the circuit does not include input preparation or measurement. Reason: The task requires an operation without state preparation or measurement. The phase-oracle form is the one that eq_3 assumes.
- eq_3: The incompletely defined function classes and the 2/3 bounded-error analysis are not implemented. The circuit covers only completely specified linear f. Reason: These classes and the success-probability analysis are listed as missing information in the specification.
