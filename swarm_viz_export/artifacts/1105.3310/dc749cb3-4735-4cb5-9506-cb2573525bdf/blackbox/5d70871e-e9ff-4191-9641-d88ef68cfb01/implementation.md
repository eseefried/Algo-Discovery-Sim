# Equation to Qiskit

Implements the Walsh-transform (Bernstein-Vazirani-style) circuit H^n O_g H^n on an n-qubit register. Here g is either the hard-coded F_2 multilinear polynomial f (direction 0) or its discrete derivative D_a f (direction a != 0). O_f is compiled from Z, CZ and multi-controlled-Z phase gates. The derivative oracle is built as O_f (X^a O_f X^a) using two oracle applications. This is a single parametrized operation. It does not implement the paper's O(n^(d-1)) exact algorithm, the full coefficient recovery, or any query counting.

Source equation run: `beb848e7-1959-48f9-933c-68eef079097e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = x1 (variable index 0, least significant bit of the Walsh index s and of direction mask a)
- qubit 1 = x2 (variable index 1)
- qubit 2 = x3 (variable index 2)
- No ancilla qubits. Input state is prepared by the runner (e.g. |000>) and the output is the Walsh-spectrum state sum_s F^(s)|s> of (-1)^g, where g = f if direction=0 and g = D_a f otherwise.

## Assumptions

- Coefficients are explicit classical parameters of the instance; the oracle is hard-coded for functional simulation, not a black box
- direction=0 means the plain Walsh transform of f; direction a != 0 means the Walsh transform of D_a f
- q=2 and the multilinear form (no repeated variables in a monomial)
- Input state is prepared by the runner, e.g. |0^n>
- The global phase from the constant monomial is tracked via circuit global_phase

## Unresolved issues

- The paper's exact O(n^(d-1))-query algorithm is not reconstructed
- Recovery of the linear and constant coefficients from phase-only outputs is not provided
- Query counting and optimality are out of scope
- No general q or d>n handling

## Equation mapping

- `eq_1`: implemented; _parse (monomial list with parity reduction, degree and multilinearity validation). The coefficients c_S in F_2 are given as the list of subsets S with c_S=1. Duplicates are XORed, and |S|<=d and distinct indices (x_i^2=x_i) are enforced.
- `eq_2`: implemented; _apply_phase_oracle. Diagonal phase oracle: empty S gives global phase pi, |S|=1 gives Z, |S|=2 gives CZ, |S|>=3 gives a multi-controlled phase of pi (CCZ for 3). The coefficients are compiled into gates, not queried from a black box.
- `eq_3`: implemented; build_circuit (H layer, oracle, H layer). H^n O_g H^n applied to the runner-provided input gives the Walsh transform. For input |0^n> the state is sum_s F^(s)|s>.
- `eq_4`: background; no code location. Degree reduction of discrete derivatives is the motivation for using D_a f. It is not computed in the code. The multilinear d=2 case has D_{e_i}f = c_i + sum_{j!=i} c_ij x_j.
- `eq_5`: implemented; build_circuit (branch for direction != 0). Derivative phase oracle O_f X^a O_f X^a, applied as O_f, then X^a, O_f, X^a on the set bits of the direction mask a.

## Specification changes

- eq_4: Corrected the description of the derivative for multilinear f: D_{e_i}f(x) = c_i + sum_{j!=i} c_ij x_j. The 'c_ii-type terms' mentioned in the specification do not exist for multilinear f. Reason: For x_i*m with m independent of x_i, (x_i+1)m + x_i m = m, so the x_i-dependence cancels and no square terms arise.
- eq_5, eq_3: Noted that in the derivative circuit the constant term c_0 cancels exactly, since the phase (-1)^{c_0} appears twice. The constant of D_a f (e.g. c_i) is itself a global sign of the derivative's Walsh state. Reason: Clarifies the specification's remark about the constant being only a global phase.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to one parametrized operation: H^n O_g H^n with g=f or g=D_a f. The full multi-run decoding, the linear/constant coefficient extraction and the paper's query-efficient exact algorithm are not built. n is generalized from 3 to any n<=12 with d<=n, and q is fixed at 2. Reason: The specification states that the paper's algorithm and coefficient recovery are missing. A single measurement-free unitary is required.
- eq_1: Qubit and variable indices are 0-based in code: qubit i corresponds to variable x_{i+1}. Reason: Matches the Qiskit convention that qubit 0 is the least significant bit.
