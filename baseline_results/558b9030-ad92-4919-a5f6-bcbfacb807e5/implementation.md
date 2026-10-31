# Equation to Qiskit

Implements one scoped construction from the specification: Grover search over a tiny quantum phone book. The circuit acts on an index register I (n qubits), two field work registers A (name) and B (number) of m qubits each, and a query register Q = (selector s, m-bit value q). Each Grover iteration applies the programmable phase oracle O_{s,q} = U_DB^dagger P_{s,q} U_DB (eq_1, eq_2), where U_DB is a table of multi-controlled NOTs loading name_i and num_i, and P_{s,q} flips the sign iff the field selected by s equals q (XOR with q, X, multi-controlled Z including the selector, uncompute), followed by the inversion about the uniform superposition on I (eq_3). An optional leading Hadamard layer on I creates |psi_0>; the iteration count k is an instance parameter (eq_4 is background used only to choose k). The distinguishability analysis for imprecise N (eq_5) is out of scope. Example: N=4 (n=2), m=2, 9 qubits, k=1; with unique names and numbers every basis-state query |s,q> yields M=1 and exact success for N=4.

Source equation run: `6b1142a8-dc5a-44a3-b58a-348a580be0cb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: idx (index register I, n=2); qubit 0 = bit 0 (LSB) of index i, qubit 1 = bit 1 (MSB)
- qubits 2-3: name (field register A, m=2); qubit 2+b holds bit b of name_i after U_DB; starts and ends in |0>
- qubits 4-5: num (field register B, m=2); qubit 4+b holds bit b of num_i after U_DB; starts and ends in |0>
- qubit 6: sel (selector s): |0> = search by name, |1> = search by number; prepared by runner, left unchanged
- qubits 7-8: qry (query value q, m=2); qubit 7+b holds bit b of q; prepared by runner, left unchanged
- total 9 qubits; example database: entry i has name i and number [3,0,2,1][i], so every query |s,q> has exactly M=1 match and one iteration succeeds with probability 1 for N=4 (e.g. all-zero input on sel,qry searches for name 0 -> index 0)

## Assumptions

- Phone-book entries are classical bit strings loaded by a fixed table of multi-controlled NOTs; the paper's actual encoding is unknown.
- The query (s,q) is a computational basis state on the sel/qry qubits provided by the runner; all-zero input corresponds to searching by name for name 0.
- The number of matches M for a given query is determined by the database; the example uses unique names and numbers so that M=1 for every query and k=1 is optimal for N=4.
- Multi-controlled gates (mcx, mcp) use no ancilla qubits; sizes are small enough (at most n or m+1 controls) for this to be acceptable.

## Unresolved issues

- The paper's concrete quantum phone-book model and mechanism of programmable queries are not available from the abstract; this is a minimal plausible construction.
- The imprecise-N distinguishability analysis (eq_5) and its numerical conclusions are not reconstructed or implemented.
- For general databases some queries may have M=0 or M>1 matches, for which the fixed iteration count k is not optimal; no handling of unknown M is included.

## Equation mapping

- `eq_1`: implemented; _apply_database (table of multi-controlled NOTs via _mcx_on_value; self-inverse so reused as U_DB^dagger). Loads name_i and num_i into registers A and B conditioned on the index register encoding i.
- `eq_2`: implemented; _apply_programmable_oracle and _apply_field_compare. O_{s,q} = U_DB^dagger P_{s,q} U_DB; P_{s,q} XORs the selected field with q, applies X, a multi-controlled Z including the selector qubit (X-conjugated for s=0), and uncomputes.
- `eq_3`: implemented; build_circuit (Hadamard layer and iteration loop) and _apply_diffusion. Uniform superposition H^{x n}|0> and the Grover iterate oracle followed by inversion about |psi_0> (global phase pi of the H X MCZ X H decomposition restored via global_phase).
- `eq_4`: background; no code location. Amplitude formula and k_opt are analysis results; the iteration count is supplied in the instance (k=1 for N=4, M=1). Not computed in the circuit.
- `eq_5`: out_of_scope; no code location. Unambiguous-discrimination overlap analysis for imprecise N is not a circuit operation and is excluded from the implemented construction.

## Specification changes

- eq_1, eq_2: Index, field and query bit strings are encoded LSB-first on Qiskit qubits (qubit j holds bit j) instead of the specification's MSB-first convention. Reason: Qiskit qubit index 0 is the least significant bit; the mapping is disclosed in the register layout.
- eq_2: The selector s and query value q are held in quantum register qubits (sel, qry) that the runner prepares in a computational basis state; the oracle is controlled by these qubits rather than being compiled classically. Reason: Implements programmability of the query as a single circuit valid for all basis-state queries; the circuit cannot prepare inputs itself.
- eq_3: The Hadamard layer creating |psi_0> is included in the circuit as the first algorithm step (controllable by apply_hadamard_layer); iterations k is an explicit instance parameter. Reason: The runner prepares inputs, so the circuit models Grover's algorithm applied to |0> on the index register with the query basis state supplied externally.
- eq_4, eq_5: Narrowed scope: the analysis equations are not implemented; eq_4 only informs the example's iteration count and eq_5 is excluded. Reason: They are analytical statements, not unitary operations; the second part of the paper cannot be turned into a circuit from the abstract.
