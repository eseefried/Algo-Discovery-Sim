# Equation to Qiskit

Builds t Grover iterations over a small quantum phone book (N=2^k entries, constant name and number tables loaded by index-controlled X gates). Each iteration is: load tables, phase-flip the entries whose selected field (name or number) equals the query, unload tables, then diffuse the index register. The discrimination analysis (overlap and IDP success) is out of scope. The runner must supply H on the index register and |0> on the data registers.

Source equation run: `6425e81c-2db0-496a-be80-2626ee805242`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..k-1: index register (little-endian, qubit 0 least significant); expected input H^k|0>
- qubits k..k+name_bits-1: name register (little-endian), expected input |0>, returned to |0>
- qubits k+name_bits..k+name_bits+number_bits-1: number register (little-endian), expected input |0>, returned to |0>
- example (k=2, 2-bit names, 2-bit numbers): index=0,1; name=2,3; number=4,5 (6 qubits total)

## Assumptions

- The runner prepares H^k on the index register and |0> on the name and number registers.
- Tables are fixed classical constants supplied in the instance.
- The global phase of the diffusion (-1) is irrelevant.
- N = 2^k with k >= 1; the search field is either 'name' or 'number'.

## Unresolved issues

- The paper's programmable query mechanism and unknown-size parametrization are not reconstructed.
- The overlap and IDP analysis for N versus N' must be done outside this circuit.

## Equation mapping

- `eq_1`: implemented; _load (index-controlled X loading and unloading of the name and number tables). Implements the loading of classical entries. The uniform index superposition H^k is not applied, so the runner prepares it.
- `eq_2`: implemented; _oracle (X on zero query bits, multi-controlled Z on the data register, undo X). Phase-flips entries whose selected field equals the query. A direct multi-controlled Z replaces the |-> flag ancilla, which is equivalent.
- `eq_3`: implemented; build_circuit default iterations: t = round(pi/(4*theta) - 1/2), theta = asin(sqrt(M/N)). Used only when 'iterations' is omitted. The exact-angle form is used because round(pi/4*sqrt(N/M)) gives 2 for N=4, M=1 instead of the optimal 1.
- `eq_4`: background; no code location. Describes the 2D Grover geometry that the circuit realizes, so no separate code is needed.
- `eq_5`: out_of_scope; no code location. The overlap of states for sizes N and N' is a classical post-processing analysis and needs a cross-size identification that this single circuit does not do.
- `eq_6`: out_of_scope; no code location. The IDP success probability is a classical formula evaluated on overlaps and is not a circuit operation.

## Specification changes

- eq_1: The initial H on the index register is not in the circuit; it is expected from the runner as input preparation. Reason: The task requires an operation with no input-state preparation.
- eq_2: No flag qubit or |-> preparation. The oracle is a direct phase flip via multi-controlled Z on the data register, and both data registers are unloaded after each oracle call. Reason: Equivalent to the phase-kickback oracle while avoiding state preparation and an extra qubit.
- eq_3: The default iteration count is round(pi/(4 asin(sqrt(M/N))) - 1/2), with M counted from the table. An explicit 'iterations' value overrides it. Reason: Gives the correct optimal t for small N and is a standard refinement of the approximate formula.
- eq_5, eq_6: Scope narrowed to the Grover search circuit only. The discrimination analysis is not implemented. Reason: It is statevector post-processing across two different database sizes rather than a single unitary circuit.
- eq_1, eq_2: M is not restricted to 1: the oracle marks every entry that matches the query. Table sizes are capped at k<=4 and 4 bits per field, with total qubits <=12. Reason: The oracle handles multiple matches without extra work, and the caps keep the circuit within the 12-qubit limit.
