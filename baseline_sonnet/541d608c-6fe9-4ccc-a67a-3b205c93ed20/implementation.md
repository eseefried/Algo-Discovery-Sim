# Equation to Qiskit

Implements build_circuit(instance) for a three-qubit CCZ, Toffoli or Fredkin (CSWAP) operation embedded in an n-qubit register (3..12). The conventional five conditional-two-qubit-gate CCZ decomposition (3 CP + 2 CNOT) is used, with a correction to the recalled eq_4. Toffoli is H-conjugated CCZ on the target, and Fredkin is CX(c,b) Toffoli(a,b->c) CX(c,b). The paper's global-gate circuits (3/4/7 global gates) are not reconstructed.

Source equation run: `cd8a0b55-306d-4c18-b384-666e484c973c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit i of the n-qubit register 'q' (index 0 = least significant bit); no ancillas
- 'qubits' = [a,b,c] selects physical indices; default [0,1,2]
- ccz: phase -1 on a=b=c=1 (symmetric)
- toffoli: a,b controls, c target
- fredkin: a control, b and c swapped
- example: 3 qubits, a=q0 control, b=q1, c=q2

## Assumptions

- Qubit tuple (a,b,c) maps to user-given Qiskit indices; there is no bit-order reversal in the gate definitions.
- CP(phi) is qiskit cp(phi, control, target) = diag(1,1,1,e^{i phi}).
- Fredkin is built via CX-Toffoli-CX, not a minimal-gate circuit.
- No public validation contract was supplied.

## Unresolved issues

- The paper's three-global-gate CCZ and four-global-gate Fredkin circuits are not reconstructed (missing Hamiltonians and sequences).
- The seven-global-gate conditional four-qubit phase gate is not implemented.
- The five nearest-neighbour constructions are not implemented.
- Gate counts in eq_5 are not verified by this module.

## Equation mapping

- `eq_1`: implemented; _ccz and build_circuit (gate='ccz'). CCZ applies (-1)^(abc) to basis states, realized by the CP/CX decomposition.
- `eq_2`: implemented; _toffoli. Toffoli is built as H on the target, CCZ, then H on the target.
- `eq_3`: implemented; build_circuit (gate='fredkin'). CSWAP is built as CX(c,b), Toffoli(a,b->c), CX(c,b), which gives |a, b xor a(b xor c), c xor a(b xor c)>.
- `eq_4`: implemented; _ccz. Conventional five-gate decomposition (3 CP + 2 CX), implemented with a correction: the CP_ab(pi/2) factor in the recalled form is removed.
- `eq_5`: out_of_scope; no code location. These are the abstract's global-gate counts. The global two-qubit gate sequences are not given, so they are not reconstructed.

## Specification changes

- eq_4: Removed the extra CP_ab(pi/2) factor. The implemented sequence is CP_bc(pi/2), CX_ab, CP_bc(-pi/2), CX_ab, CP_ac(pi/2). Reason: The accumulated phase is (pi/2)*c*(b - (a xor b) + a) = pi*abc, which is exactly CCZ. An additional CP_ab(pi/2) would add an unwanted phase (pi/2)*ab and break CCZ. This also gives the five conditional gates matching the abstract's conventional count.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to the conventional (non-global-gate) circuits for CCZ, Toffoli and Fredkin, embedded in an n-qubit register with selectable qubit indices. Reason: The abstract does not specify the global-gate, four-qubit phase gate or nearest-neighbour constructions.
