# Equation to Qiskit

Builds the 3-qubit f-controlled phase oracle U_f|x> = (-1)^f(x)|x> for a supplied truth table f satisfying the DJ promise (constant or balanced). The oracle is decomposed using only single-qubit Z, two-qubit CZ and the three-qubit CCZ gate. The decomposition uses the algebraic normal form (Moebius transform) of f. No state preparation, Hadamards, or measurement is included. The circuit-QED qutrit/cavity implementation is out of scope.

Source equation run: `471baa2c-3380-4476-999b-85ae32e139f8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = x0 (least significant bit of x)
- qubit 1 = x1
- qubit 2 = x2 (most significant bit of x)
- truth_table index x = x0 + 2*x1 + 4*x2
- no ancilla, no cavity mode, no classical bits

## Assumptions

- Phase-oracle convention: U_f|x> = (-1)^f(x)|x>.
- Qiskit little-endian ordering: qubit i is bit i of x.
- CCZ stands in for the paper's multi-qubit phase primitives, which are not specified.
- Global phase from f(0)=1 is kept via the circuit global_phase.
- The set of 35 gates is assumed (not stated) to relate to balanced functions modulo complement, 70/2 = 35. This is not used in the code.

## Unresolved issues

- Explicit decomposition of the paper's 35 gates into two-target controlled-phase gates is unknown.
- The refined DJ algorithm definition and its function set are unknown.
- The cavity-transmon qutrit encoding, pulses and numerical fidelity results are out of scope.
- Input state preparation and final Hadamards are left to the runner.

## Equation mapping

- `eq_1`: implemented; build_circuit (with helper _anf): diagonal phase oracle from ANF monomials mapped to Z/CZ/CCZ and global phase. Each ANF monomial of f becomes a Z, CZ or CCZ gate, and a constant term becomes a global phase of pi. The product of these gates gives the phase (-1)^f(x) on |x>.
- `eq_2`: background; no code location. The count of 35 gates is a property of the full paper's gate family, which the abstract does not define. This module builds one oracle per call from a supplied truth table. It does not enumerate the 35 gates.
- `eq_3`: implemented; build_circuit: promise check on s = 8 - 2*sum(f). Truth tables whose sum of (-1)^f(x) is not in {8, -8, 0} are rejected with ValueError.

## Specification changes

- eq_1, eq_2: Scope narrowed to a single abstract 3-qubit phase oracle U_f built from Z, CZ and CCZ. The paper's two-target-qubit controlled-phase gates and the circuit-QED cavity/qutrit realization are not implemented. No enumeration of the 35 gates is done. Reason: The abstract does not give the gate decomposition, the Hamiltonian, or the definition of the refined DJ function set, so those details cannot be reconstructed.
- eq_3: The standard DJ promise is enforced as input validation. Refined DJ may use a different function family. Reason: The refined-DJ definition is not given in the abstract.
