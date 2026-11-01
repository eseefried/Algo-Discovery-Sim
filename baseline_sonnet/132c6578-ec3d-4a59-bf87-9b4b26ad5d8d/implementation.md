# Equation to Qiskit

build_circuit(instance) returns the 3-qubit DJ phase-oracle unitary H^{⊗3} U_f H^{⊗3}, or U_f alone if include_hadamards is false. U_f is built from the algebraic normal form (ANF) of f as Z, CZ and CCZ gates, with a global phase of pi for a constant-1 term. The generic ANF construction is used, not the paper's 35-gate two-target protocol or the circuit QED implementation.

Source equation run: `222e4950-4ba4-4c6e-8e02-e1ccdc56b93f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = x_3 (least significant bit)
- qubit 1 = x_2
- qubit 2 = x_1 (most significant bit)
- basis index x = 4*x_1 + 2*x_2 + x_3
- Single register 'q' of 3 qubits; no ancillas

## Assumptions

- The phase convention is (-1)^{f(x)}.
- The standard DJ circuit H U_f H is used as a proxy for the refined algorithm.
- CCZ is used as the multi-qubit phase gate for cubic ANF terms.
- Only n=3 is supported.

## Unresolved issues

- The refined DJ algorithm definition and the set of 35 functions are unknown.
- The paper's two-target controlled-phase decomposition is not reproduced.
- The circuit QED qutrit/cavity implementation, pulses and fidelity results are out of scope and not modeled.

## Equation mapping

- `eq_1`: implemented; build_circuit: ANF gate loop (Z/CZ/CCZ/global phase). U_f|x> = (-1)^{f(x)}|x> is a diagonal phase oracle. It is realized as the product of the phase gates given by the ANF of f.
- `eq_2`: implemented; build_circuit: Hadamard layers before and after the oracle loop (include_hadamards). The unitary H^{⊗3} U_f H^{⊗3} is built. The runner prepares |000>. The amplitude formula is a property for later checking, not coded.
- `eq_3`: implemented; build_circuit: loop over `active` ANF terms. Each ANF term with coefficient c_S=1 becomes Z (|S|=1), CZ (|S|=2) or CCZ (|S|=3). An empty S adds a global phase of pi. Duplicate terms cancel under XOR.
- `eq_4`: implemented; example_instance_json. f = x1 XOR x2x3 is the example instance, with anf_terms [[1],[2,3]], giving Z on x1 and CZ on x2,x3.

## Specification changes

- eq_1, eq_3, eq_4: Variable x_1 is mapped to Qiskit qubit 2, x_2 to qubit 1 and x_3 to qubit 0. Reason: The spec defines x = 4x_1+2x_2+x_3 with q1 as the most significant bit, while Qiskit qubit 0 is the least significant bit.
- eq_3: Terms are given as an instance parameter (anf_terms) and the constant term is realized as a global phase. Reason: This makes the operation work for any Boolean function on 3 variables. The global phase is physically irrelevant but kept so the unitary matches (-1)^{f(x)} exactly.
- eq_2: The Hadamard layers are optional via include_hadamards, defaulting to true. The operation excludes input preparation and measurement. Reason: The task requires an operation without state preparation or measurement, and allows testing U_f alone.
- eq_1, eq_2, eq_3, eq_4: Scope is narrowed to the generic standard DJ phase-oracle construction on n=3. The paper's refined DJ algorithm, its 35 gates, the two-target controlled-phase gates and the qutrit/cavity dynamics are not implemented. Reason: The abstract and spec do not give these details.
