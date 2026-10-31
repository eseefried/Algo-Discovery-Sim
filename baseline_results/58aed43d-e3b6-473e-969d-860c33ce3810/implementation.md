# Equation to Qiskit

Implements the proposed non-adaptive nearest-neighbour CNOT fanout (eq_5) on a rows x cols 2D grid: a control qubit at grid site (0,0) is broadcast along row 0 by a sequential chain of CNOTs, then down every column by parallel layers of CNOTs. Every CNOT acts on L1-adjacent grid sites (eq_2, checked at construction time), size is n-1 and depth is (cols-1)+(rows-1), i.e. Theta(sqrt n) for square grids. On clean targets (|0>) the circuit realises the fanout of eq_1 (GHZ-type copy of the control).

Source equation run: `a161f9db-f5c3-46b2-8db9-c947a9be4bb0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'grid' with rows*cols = 9 qubits for the example; grid site (r,c) maps to qubit index i = r*cols + c (qubit 0 is the least significant bit).
- Qubit 0 = site (0,0): control qubit holding |x>.
- Qubits 1,2 = sites (0,1),(0,2): row-0 targets, filled by the sequential row broadcast (layers 1-2).
- Qubits 3,4,5 = sites (1,0),(1,1),(1,2): filled by column layer 1 (layer 3).
- Qubits 6,7,8 = sites (2,0),(2,1),(2,2): filled by column layer 2 (layer 4).
- All targets are assumed to be prepared in |0> by the runner; output on |x>|0>^8 is |x>^9.

## Assumptions

- k = 2 (2D grid); grid site (r,c) is mapped to qubit index r*cols + c with the control at qubit 0 (site (0,0)).
- Target qubits are prepared in |0> by the runner; the control may be any single-qubit state (e.g. (|0>+|1>)/sqrt2 yields an n-qubit GHZ state).
- Depth is counted as layers of disjoint nearest-neighbour CNOTs; Qiskit's qc.depth() will report (rows-1)+(cols-1) for this circuit since the column layers are disjoint.
- The construction is the specification's own proposal consistent with the stated Theta(sqrt n) bounds, not the paper's actual circuit.

## Unresolved issues

- The paper's actual non-adaptive fanout/controlled-operation circuits and their exact constants are unknown; only a construction matching the asymptotic bounds is implemented.
- Handling of arbitrary (non-zero) target inputs for a true general fanout in nearest-neighbour depth O(sqrt n) is not implemented.
- No software verification was performed here; equivalence to F_n on clean targets is asserted from the CNOT-tree argument only.

## Equation mapping

- `eq_1`: implemented; build_circuit docstring and module docstring: the circuit realises F_n on clean targets |x>|0...0> -> |x>^{n}. The CNOT tree copies the control value onto every target when targets start in |0>; for arbitrary target inputs the Boolean map differs from eq_1 (reported in specification_changes).
- `eq_2`: implemented; _nn_cx (raises ValueError if the requested CNOT is not between L1-adjacent sites) and _site_index (linear layout i = r*cols + c). Every two-qubit gate is checked to act on grid sites at L1 distance 1; the layout maps grid coordinates to physical qubit indices.
- `eq_3`: background; no code location. Asymptotic Theta bounds from the abstract; the implemented circuit has depth (rows-1)+(cols-1) = 2(sqrt n - 1) for square grids and size n-1, consistent with these bounds, but no asymptotic statement is encoded in code.
- `eq_4`: background; no code location. Light-cone lower bound used to argue optimality; it constrains depth but is not an operation to implement.
- `eq_5`: implemented; build_circuit: the two loops commented 'eq_5, first factor' (row broadcast) and 'eq_5, second factor' (parallel column broadcast). Row-then-column CNOT fanout with control at (0,0); time ordering follows the right-to-left product (row chain first, then column layers).
- `eq_6`: out_of_scope; no code location. Adaptive-model depth equivalence requires measurements and classically controlled gates, which are excluded from this unitary, non-adaptive construction.

## Specification changes

- eq_5: Generalised the m x m square grid to a rows x cols rectangular grid with 2 <= rows*cols <= 12 (so the square 3 x 3 example of the specification is one valid instance); depth becomes (cols-1)+(rows-1), size rows*cols-1. Reason: The 12-qubit cap would otherwise allow only m in {2,3}; rectangular grids give more valid instances while preserving the same row-then-column nearest-neighbour construction.
- eq_1, eq_5: The circuit equals the fanout F_n of eq_1 only on inputs whose target qubits are |0> (clean-ancilla / GHZ-type copy); for arbitrary target inputs y_i it implements a different Boolean map (each target receives the XOR of its tree-parent's current value). Reason: Inherited from the specification's eq_5 assumptions; the general-input fanout conversion was declared outside scope.
- eq_6: Narrowed scope to the non-adaptive, unitary nearest-neighbour fanout; the adaptive constant-depth constructions are not implemented. Reason: Adaptive circuits need mid-circuit measurement and classical feed-forward, which are disallowed for this operation-only artifact and not described in the abstract.
