# Equation to Qiskit

Unitary, measurement-free nonlocal CNOT (control logical qubit 0, target logical qubit 1) routed through a 1D chain of m Bell pairs. Bell pairs are prepared in parallel, and entanglement swapping at the m-1 junctions uses CNOT+H with the measurements deferred. The resulting Pauli corrections are applied coherently to the far end qubit. The Eisert-style CNOT teleportation is then done with deferred measurement, so the logical pair receives an ideal CNOT.

Source equation run: `620534b6-0127-40d3-b402-41ca6926116a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: logical control a (computational basis, little-endian)
- qubit 1: logical target b
- qubits 2..2m+1: path ancillas, link j = (qubit 2+2j, qubit 3+2j), j=0..m-1, all start in |0>
- qubit 2: end qubit e_a (left end of the chain)
- qubit 2m+1: end qubit e_b (right end of the chain)
- junction j (1..m-1) Bell-measured pair: q=1+2j, r=2+2j
- for m=3: 8 qubits total; ancillas 2..7 end in a state independent of the logical pair

## Assumptions

- Input state preparation on logical qubits 0 and 1 and all-zero path ancillas is provided by the runner.
- The ideal operation on the logical pair is CNOT with qubit 0 as control and qubit 1 as target. Path ancillas end in a state independent of the logical pair, but not necessarily |0>.
- Corrections that commute up to sign are accepted as a global phase difference.
- The instance contains only the integer m, the number of Bell links, with 1<=m<=5.

## Unresolved issues

- Constant-depth property and nearest-neighbour locality are not realised in this unitary deferred form.
- k>=2 grid routing, Pauli-frame absorption, constant-depth Shor and fanout constructions remain unimplemented.
- The paper's exact protocol is not specified, so the textbook entanglement swapping and gate teleportation are used.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop 'eq_1' applying H then CX on each link (2+2j, 3+2j). Each link is prepared as CNOT(H x I)|00> = |Phi+>.
- `eq_2`: implemented; build_circuit: junction loop 'eq_2' (cx(q,r), h(q), cx(r,eb), cz(q,eb)). Parallel Bell-basis measurements at the junctions use CNOT+H. The derived correction is X^c Z^s on the end qubit e_b, with the XOR of outcomes realised by repeated coherent controlled Paulis.
- `eq_3`: implemented; build_circuit: final five gates after the junction loop. CNOT(a->e_a), then X^u on e_b becomes CX(e_a,e_b), then CNOT(e_b->b), then H(e_b), then Z^v on a becomes CZ(e_b,a). This is the deferred-measurement form.
- `eq_4`: out_of_scope; no code location. The fanout lightcone depth bound is a counting argument about non-adaptive circuits and is not a circuit construction.
- `eq_5`: out_of_scope; no code location. The fanout action is not implemented. The scoped construction is the nonlocal CNOT, which is a single-target special case in spirit only.

## Specification changes

- eq_2, eq_3: Mid-circuit measurements and classical feed-forward are replaced by the deferred-measurement principle, with coherent controlled-X/Z gates from the would-be measured qubits. Reason: The required output is a measurement-free, non-dynamic unitary circuit.
- eq_2: The swap correction is derived as X^c on the far end from r's outcome and Z^s on the far end from q's outcome, with the CNOT(q->r), H(q) Bell measurement. The specification's x_j, z_j exponents are assigned accordingly. Corrections are applied to e_b only, not tracked in a frame. Reason: This was verified by hand algebra for a single swap. The specification left the exact assignment unspecified.
- eq_2: The constant-depth claim is not reproduced. The coherent XOR of corrections is a serial fan-in onto e_b, and the correction gates are long-range, so circuit depth grows O(m) and the gates are not nearest-neighbour. Reason: In the original, parity computation is done by the classical controller for free. Here it must be quantum gates.
- eq_1, eq_2, eq_3: Scope narrowed to a 1D chain with m<=5 links, 2+2m<=12 qubits, instead of kD grid routing with congestion resolution. Reason: Specification marks grid routing as outside the reconstruction scope, and the qubit cap is 12.
- eq_4, eq_5: Fanout and the lightcone bound are not implemented. Reason: Only one construction is scoped: the nonlocal CNOT.
