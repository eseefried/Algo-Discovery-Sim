# Equation to Qiskit

Level-one QAOA operation for Max E3LIN2: the phase-separation unitary exp(-i*gamma*C) with C = sum_k (1 + s_k Z_a Z_b Z_c)/2, followed by the transverse-field mixer exp(-i*beta*sum X_j). Each clause is a CNOT parity ladder, an RZ, and an uncompute. The |+>^n input is left to the runner, and gamma and beta are instance parameters.

Source equation run: `e5838a33-5242-4fba-bb7d-67ddac321f56`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit j (0..n-1) = boolean variable x_j in the computational basis; qubit 0 is the least significant bit; Z eigenvalue (-1)^{x_j}
- Single register 'q' of n qubits, no ancillas
- Input state (e.g. |+>^n) is prepared by the runner, not by this circuit

## Assumptions

- The Z-product clause encoding and standard transverse-field mixer are standard background, not taken from the abstract.
- Equations contain three distinct variables, indexed from 0 to n-1.
- Right-hand side bit b_k = 1 gives s_k = -1.
- n is restricted to 3 <= n <= 12, because an equation needs three distinct variables.
- The number of equations is capped at 200.
- If D is supplied, each variable's occurrence count is validated against it.

## Unresolved issues

- The abstract does not give the optimal (gamma,beta) as a function of D.
- The meaning of 'typical case' and the expectation-vs-high-probability criterion are undefined.
- The guarantee proofs and the classical comparison algorithm are not reconstructed.

## Equation mapping

- `eq_1`: implemented; build_circuit: clause loop (CX ladder onto qubit c, RZ(gamma*s_k), uncompute) plus the global_phase term. exp(-i*gamma*C) = prod_k exp(-i*gamma/2) exp(-i*gamma*s_k/2 Z_aZ_bZ_c), with s_k = (-1)^{b_k}. The ZZZ rotation is the parity ladder and an RZ, and the constant 1/2 per clause goes into the circuit global phase.
- `eq_2`: implemented; build_circuit: phase-separation loop followed by the RX(2*beta) mixer loop. Implements the operator exp(-i*beta*B) exp(-i*gamma*C) with B = sum X_j. The |+>^n preparation is excluded because the runner prepares inputs.
- `eq_3`: background; no code location. The expectation objective F(gamma,beta) is an evaluation quantity, not part of the operation. No expectation is computed or optimized in the circuit.
- `eq_4`: out_of_scope; no code location. The worst-case performance guarantee is a theorem about the algorithm and is not a circuit construction.
- `eq_5`: out_of_scope; no code location. The typical-case guarantee is a claim about performance. Its meaning is undefined in the abstract, and it requires specific angles that are not given.

## Specification changes

- eq_2: Scope narrowed to the unitary U(gamma,beta) = exp(-i*beta*B) exp(-i*gamma*C). The |+>^n preparation is not included in the circuit. Reason: The task requires an operation with no input-state preparation. Apply the circuit to |+>^n to get the QAOA state.
- eq_1, eq_2, eq_3: gamma and beta are required instance inputs, as are the equation list, n, and an optional D. No optimized or D-dependent angle values are supplied. Reason: The abstract does not give the angle schedule, so the angles cannot be hardcoded.
- eq_1: The constant offset in C is included as a circuit global phase of -gamma*m/2. Reason: This makes the circuit exactly equal exp(-i*gamma*C) rather than only equal up to a global phase.
- eq_4, eq_5: Performance guarantees are not implemented. They are classified out_of_scope. Reason: They are asymptotic claims about performance, not circuit constructions.
