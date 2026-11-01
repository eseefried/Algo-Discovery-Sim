# Equation to Qiskit

Implements only the discrete bit-flip query oracle O_x|i>|b> = |i>|b xor x_i> (eq_5) as a unitary Qiskit circuit for a classical bit string x supplied in the instance. For each i with x_i=1, an X gate on the target is controlled on the index register equal to i. The NAND-formula query algorithm and the complexity claims are not constructed, because the specification does not give the algorithm.

Source equation run: `785cc11f-70ee-4f50-a6c4-ae6e5e9f1962`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: index bit 0 (least significant bit of i)
- qubit 1: index bit 1 (for N=4 example; index uses ceil(log2 N) qubits, minimum 1)
- qubit n_index (qubit 2 in the example): target qubit b, receives x_i via XOR

## Assumptions

- The standard bit-flip oracle convention for discrete queries, as assumed in the specification.
- Index i is binary encoded with qubit 0 as the least significant bit.
- N is at most 2048 so that index plus target qubits stay within the 12-qubit cap.

## Unresolved issues

- The NAND formula evaluation algorithm itself is not implemented.
- The complexity claims eq_2 and eq_3 cannot be encoded as a circuit.
- The paper's exact oracle form may differ from the standard one assumed here.
- The circuit contains no state preparation, measurement, or formula decision rule.

## Equation mapping

- `eq_1`: background; no code location. NAND definition is background; the oracle circuit does not evaluate any NAND gates.
- `eq_2`: out_of_scope; no code location. O(sqrt(N)) query bound for balanced formulas is an asymptotic claim; the algorithm achieving it is not specified and not implemented.
- `eq_3`: out_of_scope; no code location. Query bound for arbitrary formulas is an asymptotic claim, based on a garbled abstract exponent; no algorithm is implemented.
- `eq_4`: out_of_scope; no code location. The toy N=4 formula is not evaluated by the circuit. The example instance only supplies the oracle's input bit string x and does not compute the formula.
- `eq_5`: implemented; build_circuit: loop over i with x_i=1 appending XGate().control(n_idx, ctrl_state=i). Implements O_x|i>|b>=|i>|b xor x_i> as a multi-controlled X per set bit, with index in binary (qubit 0 is the LSB).

## Specification changes

- eq_2, eq_3, eq_4: Scope narrowed from the NAND formula evaluation algorithm to just the query oracle O_x for a supplied classical string x. Reason: The specification lists the algorithm construction (walk/span program, phase schedule, registers) as missing, so the algorithm cannot be reconstructed faithfully.
- eq_5: The input string x is compiled into the circuit as a fixed set of controlled gates, rather than being accessed as a black box. Basis states of the index register with i >= N act as identity when N is not a power of two. Reason: A Qiskit circuit needs concrete gates, and the index register has dimension 2^k >= N.
