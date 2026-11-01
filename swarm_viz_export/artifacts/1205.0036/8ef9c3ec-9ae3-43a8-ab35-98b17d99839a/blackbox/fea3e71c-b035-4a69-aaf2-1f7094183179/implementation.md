# Equation to Qiskit

Measurement-free unitary long-range CNOT between data qubits c (index 0) and t (last index) across a line of 2p ancillas. Local Bell pairs are fused by coherent entanglement swapping, then used to teleport a CNOT, with all measurement corrections deferred as controlled Paulis. Ancillas start in |0> and are returned to |0>, so the net operation is CNOT(c->t) on the data tensor identity on the ancillas.

Source equation run: `103006ae-32e2-47de-9581-caf0da1553e9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: logical control c (data)
- qubits 1..2p: path ancillas a_1..a_2p in line order; Bell pairs are (1,2),(3,4),...; qubit 1 is u (left end of the long-range pair) and qubit 2p is v (right end)
- qubit 2p+1: logical target t (data)
- example num_pairs=2: 6 qubits, c=0, ancillas 1-4, t=5
- all qubits in one register; Qiskit index 0 is the least significant bit

## Assumptions

- Ancillas start in |0>, supplied by the runner
- Data qubits are 0 and n-1 and may be in arbitrary states
- Deferred measurement principle: measurement outcomes are replaced by controlled Paulis, and the formerly measured qubits, left in uniform superposition, are restored to |0> by H
- Instance is a JSON object with a single integer key num_pairs in 1..5

## Unresolved issues

- The nearest-neighbor property and constant depth are not realized in the coherent version because the corrections are non-local and the swaps are sequential
- The general grid and routing constructions are not implemented

## Equation mapping

- `eq_1`: out_of_scope; no code location. Depth-equivalence claim for grid versus abstract circuits. It is not implemented by one small instance, and the sequential coherent swaps here have depth linear in num_pairs.
- `eq_2`: implemented; build_circuit: loop 'eq_2' (H on qubit 2i+1 then CX to 2i+2). Local Bell pairs |Phi+> = CNOT(H x I)|00> on adjacent ancilla pairs.
- `eq_3`: implemented; build_circuit: loop 'eq_3' (CX, H, coherent CX and CZ corrections). Entanglement swapping with the Bell measurement deferred. The Pauli byproducts become coherent controlled X and Z on the new right end of the merged pair.
- `eq_4`: implemented; build_circuit: block 'eq_4' (CX c->u, CX u->v, CX v->t, H v, CZ v->c, final H on ancillas). CNOT teleportation through the long-range Bell pair (u,v) with deferred measurement.

## Specification changes

- eq_3: The labelling X^{m1}Z^{m2} is replaced by the derived correction: X controlled on the Bell-measured qubit a3 (the CNOT target, outcome w) and Z controlled on the H-rotated qubit a2 (outcome z), both acting on the far end a4. Reason: Derived directly from sum_x (-1)^{zx}|x>|x xor w>. The correction is exact, with no residual branch-dependent phase.
- eq_4: The correction structure 'Z_t^{m2} X_c^{m1}' is replaced by: X on the relay qubit v controlled by u, then Z on c controlled by v after H. No correction is applied on t. Reason: Derived for the standard remote-CNOT protocol (CNOT c->u, measure u, copy c onto v, CNOT v->t, X-measure v, Z-correct c).
- eq_3, eq_4: Ancilla count is 2*num_pairs (even, 2 to 10) instead of 3. Measured ancillas are returned to |0> by a final layer of H. Reason: The Bell pairs must tile the path. The final H makes the circuit a clean operation: data CNOT times identity on the ancillas.
- eq_1, eq_3, eq_4: The swaps are applied sequentially. The coherent controlled corrections (CX u->v, CZ v->c, and the swap corrections) are non-local gates standing in for classical feed-forward, so the unitary is not strictly nearest-neighbor. Reason: A measurement-free unitary cannot express free classical control. Depth is O(num_pairs), not constant, so the constant-depth claim is not demonstrated.
- eq_1: Scope narrowed to a single long-range CNOT on a 1D line. No Z^k routing, congestion handling, fanout, Shor, or non-adaptive circuits. Reason: Only the core primitive was specified concretely.
