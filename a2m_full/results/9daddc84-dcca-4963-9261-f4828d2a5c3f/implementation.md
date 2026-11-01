# Equation to Qiskit

Implements, for q=2, one Bernstein-Vazirani step on the discrete derivative of a multilinear polynomial f of degree <=d on n qubits. The operation is H^n . (U_f . X_i U_f X_i) . H^n, where U_f is a phase oracle built from multi-controlled-Z gates, one per monomial with coefficient 1. On input |0^n> the output is |a> up to a global phase, with a_j = c_{ij} for j != i and a_i = 0. This is the derivative-learning step of the assumed recursion, not the full algorithm.

Source equation run: `e1e4f3ab-f269-4a09-8434-003513542c4e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data register x, one qubit per variable x_j (qubit j = variable j, qubit 0 least significant)
- no ancilla: the phase oracle is built directly, so no kickback ancilla is needed
- example: n=3, qubits 0,1,2 = x_0,x_1,x_2; derivative direction i=0

## Assumptions

- q=2, so the phase is (-1)^{f(x)}
- Coefficients are in F_2, so duplicate monomials in the instance cancel in pairs
- The oracle is supplied as the monomial list, with variable j mapped to qubit j
- Degree bound d satisfies 1<=d<=n, and each monomial has distinct variables and size <=d
- n is capped at 12 qubits
- Output is a BV result only when the derivative has degree <=1 (d<=2)

## Unresolved issues

- The paper's actual exact algorithm, its constants and the optimality argument are not reconstructed
- General q and the QFT over F_q are not implemented
- Handling of d>2, which needs a deeper recursion, is not implemented
- Reed-Muller decoding details are not implemented

## Equation mapping

- `eq_1`: implemented; _phase_oracle. The q=2 phase oracle (-1)^{f(x)} is built from Z, multi-controlled-phase(pi) and global-phase gates, one per monomial with coefficient 1. It is built directly, not from an XOR oracle with an ancilla.
- `eq_2`: implemented; build_circuit (Hadamard layers around the derivative oracle). H^n O H^n is applied with O the derivative oracle. On |0^n> this gives |a> up to phase, since the derivative has degree <=1 for d=2. For d>2 it is not a BV step.
- `eq_3`: implemented; build_circuit (oracle, X_i, oracle, X_i). The derivative phase oracle (-1)^{f(x+e_i)+f(x)} is U_f followed by X_i U_f X_i. This uses 2 oracle calls, and the constant term cancels.
- `eq_4`: background; no code location. Query-count recursion. Only one derivative step is built (2 oracle applications). The recursion over all i and the counting are not part of the circuit.
- `eq_5`: out_of_scope; no code location. Classical reassembly of coefficients from measured outcomes and the f(0) evaluation. It involves measurement and postprocessing, so it is not a unitary operation.

## Specification changes

- eq_1: The oracle is an explicit gate decomposition of f given by a monomial list in the instance, not an opaque black box or XOR oracle with a |-> ancilla. Reason: A bound, measurement-free unitary operation with no ancilla preparation is required, and the oracle must exist as a circuit for varying parameters.
- eq_2, eq_3, eq_4, eq_5: Scope narrowed to a single derivative direction i with one BV step. The full recursion, the loop over all i, measurement, classical reassembly and query counting are excluded. Reason: One explicitly scoped operation is required, with no measurement or dynamic control.
- eq_2, eq_3: The BV step acts on all n qubits, not on n-1 qubits with x_i fixed to 0. Since D_{e_i}f does not depend on x_i, the output on |0^n> has qubit i in |0>. Reason: This avoids a controlled-fix of x_i and keeps the same query structure.
- eq_2: The offset b of the derivative and the constant term c_empty appear only as global phases, which cancel for the derivative oracle. Reason: This follows the specification, which notes b is a global phase and needs a separate evaluation.
