# Equation to Qiskit

build_circuit(instance) returns R iterations of the Grover operator G = (reflection about uniform state on the index register) · O. O is a compute/mark/uncompute oracle: an address-controlled-X QRAM load of a classical database, a phase-kickback comparison against target w onto a flag qubit, then a second load to clean the data register. Input preparation (H on index, |-> on flag, data in |0>) is left to the runner.

Source equation run: `c33fe7cb-839b-4360-a849-da04e4d1f040`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: index register (address, little-endian, qubit k = bit k of address)
- qubits n..n+m-1: data register (QRAM output word, little-endian; returned to |0> after each oracle)
- qubit n+m: flag qubit (expected input |->); example n=2,m=2: index=0,1; data=2,3; flag=4

## Assumptions

- The runner prepares the index register in the uniform superposition (or other desired state), the data register in |0>, and the flag in |->.
- Database and target are classical build-time data in the instance.
- Qubit order is little-endian; the address bit k is index qubit k and data bit j is data qubit j.
- Gate-level QRAM design is an assumed address-controlled-X realization, not taken from the paper.

## Unresolved issues

- The paper's exact QRAM design and any gate-count optimizations are unknown from the abstract.
- Handling of unknown M is not addressed; M is computed classically from the database at build time.

## Equation mapping

- `eq_1`: implemented; _load. Address-controlled X gates onto data bits where D[i] has a 1, using X conjugation on index qubits for zero address bits and mcx.
- `eq_2`: implemented; _mark. X on data bits where w is 0, mcx from the data register to the flag, then undo the X gates.
- `eq_3`: implemented; _oracle. Compute (load), mark, uncompute (load).
- `eq_4`: implemented; _diffusion and the loop in build_circuit. Reflection about the uniform state via H X C^{n-1}Z X H on the index register, composed with the oracle each iteration. The |s> preparation is not included because the runner prepares inputs.
- `eq_5`: implemented; build_circuit (iteration count R computation). Default R = floor(pi/4 sqrt(N/M)), with M counted from the database; the success probability formula is analysis only and not implemented.

## Specification changes

- eq_4: Initial H^n on the index register and flag preparation in |-> are excluded from the circuit; only the Grover iterations are built. Reason: The task requires an operation without input-state preparation; the runner prepares the inputs.
- eq_4: The multi-controlled-Z diffusion gives I-2|s><s|, the negative of 2|s><s|-I, so a global phase of pi is added per iteration. Reason: To make the circuit match G exactly rather than only up to a global sign.
- eq_1, eq_2, eq_3, eq_4, eq_5: Generalized from fixed n=2,m=2,M=1 to varying n, m, database, target. M is counted from the database, multiple matches are allowed with 1<=M<N, and iterations may be overridden. Reason: The operation must work for varying valid instance parameters. M=N is rejected because the oracle would be a global phase.
- eq_1, eq_2, eq_4: Multi-controlled gates use qc.mcx without a dedicated ancilla qubit. Reason: This keeps the layout to n+m+1 qubits, within the 12-qubit cap.
