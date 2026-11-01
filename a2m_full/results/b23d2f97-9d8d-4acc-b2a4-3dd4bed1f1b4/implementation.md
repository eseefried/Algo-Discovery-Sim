# Equation to Qiskit

Qiskit realization of a 4-wire reversible cascade (eq_1) from an explicit gate list drawn from NOT, CNOT, Toffoli, Peres and Fredkin. It also computes the additive quantum cost (eq_2) and can check an optional cost bound and an optional target permutation by classical permutation composition. Exact minimum-QC synthesis (meet-in-the-middle) is not implemented.

Source equation run: `9acec301-3745-4806-9cac-b40b5a7dc489`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] = wire a, least significant bit of x
- q[1] = wire b
- q[2] = wire c
- q[3] = wire d, most significant bit; x = a + 2b + 4c + 8d
- No ancilla qubits; 4 qubits total
- Gate qubit lists: not [t]; cnot [control, target]; toffoli [c1, c2, target]; peres [a, b, c] = ccx(a,b,c) then cx(a,b); fredkin [control, t1, t2]

## Assumptions

- Gate g_1 is applied first, and the gate list order is the circuit order.
- Qubit 0 is the least significant bit of x, i.e. wire a.
- Exactly 4 wires and no ancillas.
- Standard NCV costs NOT/CNOT=1, Toffoli=5, Peres=4, Fredkin=7.
- Peres(a,b,c) = Toffoli(a,b;c) followed by CNOT(a;b).

## Unresolved issues

- Exact minimum-QC synthesis is not implemented; the network must be supplied.
- Benchmark functions and their previous QC values are unspecified.
- The meet-in-the-middle cost-straddling split is unresolved.
- Costs for larger controlled gates are unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit (gate loop appending x/cx/ccx/cswap in order, g_1 first) and _step (classical permutation check against optional target). The cascade of gates is built in order as a Qiskit circuit; the optional target permutation is verified by classical composition of gate permutations.
- `eq_2`: implemented; _spec and the cost accumulation (total) in build_circuit. QC is the sum of per-gate costs NOT/CNOT=1, Toffoli=5, Peres=4, Fredkin=7; it is used for the optional max_cost check. Qiskit uses ccx etc. directly, not NCV decompositions.
- `eq_3`: out_of_scope; no code location. Exact minimization over all networks is a classical search problem; the module realizes a supplied network and does not search.
- `eq_4`: out_of_scope; no code location. The meet-in-the-middle hash-table search is not implemented because the full 16! permutation space is too large to enumerate here and the cost-straddling details are unresolved.
- `eq_5`: out_of_scope; no code location. The percent saving is classical postprocessing relative to benchmark values and is not part of the quantum operation.

## Specification changes

- eq_3, eq_4: Scope narrowed from exact minimum-QC synthesis plus realization to realization of a user-supplied gate cascade, with optional cost bound and target-permutation consistency checks. Reason: The exact search has unresolved details such as symmetry reduction and cost straddling, and is infeasible within a compact module. The task requires a circuit operation, not a synthesis tool.
- eq_2: Peres is realized as ccx(a,b,c) followed by cx(a,b), with cost 4 counted nominally. Fredkin is realized with cswap, with cost 7 counted nominally. Reason: Qiskit uses standard gates directly. The NCV decomposition is used for costing only, as the specification states.
- eq_5: The saving computation is excluded from the circuit module. Reason: It is classical postprocessing and requires benchmark data that is not supplied.
