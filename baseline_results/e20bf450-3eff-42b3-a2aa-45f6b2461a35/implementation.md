# Equation to Qiskit

Level-one (p=1) QAOA unitary U(gamma,beta) = exp(-i beta B) exp(-i gamma C) for an explicit bounded-occurrence Max E3LIN2 instance (eq_2, eq_3), with C = sum_e (1 + d_e Z_a Z_b Z_c)/2 realized exactly (including the global phase from the constant m/2) via CX-ladder + Rz(gamma*d_e) three-body rotations and the mixer via Rx(2 beta) on every qubit. The circuit is an operation acting on a runner-prepared input (nominally |+>^n); an optional flag can prepend the H layer. Example: the n=4, m=2, D=2 instance of eq_6. The paper's performance bounds (eq_4, eq_5) are not reconstructed.

Source equation run: `7d7abeec-f8bf-4040-bc6b-874df61f60d5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] (Qiskit qubit 0, least significant bit) = variable x_1, |0> <-> x_1 = 0
- q[1] = variable x_2
- q[2] = variable x_3
- q[3] (most significant bit) = variable x_4
- Measured bitstrings (if the runner measures) read x_4 x_3 x_2 x_1 left to right; the spec's 'qubit 1 leftmost' convention is reversed relative to Qiskit's little-endian printing, but each qubit still holds exactly one variable.

## Assumptions

- Variables in equations are 1-indexed in the instance JSON and must be distinct within an equation (E3LIN2).
- Rz(theta) = exp(-i theta Z/2) and Rx(theta) = exp(-i theta X/2) (Qiskit conventions), so Rz(gamma*d_e) on the parity qubit gives exp(-i (gamma/2) d_e ZZZ) and Rx(2 beta) gives exp(-i beta X).
- Duplicate equations on the same variable triple are allowed and simply contribute additively, as in eq_2.
- The optional D key enforces the bounded-occurrence constraint; if absent, no occurrence bound is checked.
- The example angles gamma=pi/4, beta=pi/8 are arbitrary placeholders, not the paper's angles.

## Unresolved issues

- The (gamma, beta) values used in the paper's proofs are unknown; the example angles are not optimized.
- The 'typical case' ensemble and the constants in eq_4/eq_5 cannot be validated with the n=4, D=2 example, which is far outside the asymptotic regime.

## Equation mapping

- `eq_1`: background; _parse_equations (d = 1 - 2*r implements d_e = (-1)^{r_e}); classical evaluation of C(x) is postprocessing outside the circuit. The classical objective is not a circuit operation; only its sign convention d_e=(-1)^{r_e} is used to parametrize the ZZZ rotations. Evaluating C(x) on samples is the runner's classical postprocessing.
- `eq_2`: implemented; _apply_cost_unitary. exp(-i gamma C) with C = sum_e (1 + d_e Z_a Z_b Z_c)/2 is realized exactly: CX ladder onto qubit c, Rz(gamma*d_e) = exp(-i gamma d_e Z/2) giving exp(-i(gamma/2) d_e ZZZ), uncompute; the constant m/2 is kept as global_phase -= gamma*m/2.
- `eq_3`: implemented; build_circuit, _apply_cost_unitary, _apply_mixer_unitary (optional H layer under prepare_plus_state). The p=1 QAOA unitary exp(-i beta B) exp(-i gamma C) is built; exp(-i beta X_j) is Rx(2 beta). The |+>^n preparation is excluded by default because the module returns an operation and the runner prepares inputs; it can be enabled with prepare_plus_state=true.
- `eq_4`: out_of_scope; no code location. The worst-case guarantee 1/2 + 1/(101 D^{1/2} ln D) is a theorem about the expectation F_1 at angles not available from the abstract; the circuit can be used to estimate F_1 but the bound itself is not reconstructed.
- `eq_5`: out_of_scope; no code location. The typical-case value 1/2 + 1/(2 sqrt(3e) D^{1/2}) depends on an undefined instance ensemble and an analytic argument not available here.
- `eq_6`: implemented; example_instance_json (n=4, equations [[1,2,3,0],[2,3,4,1]], D=2). The tiny instance x1+x2+x3=0 (d_1=+1), x2+x3+x4=1 (d_2=-1) is encoded as the example instance; _apply_cost_unitary produces C = 1 + Z1Z2Z3/2 - Z2Z3Z4/2 in the exponent.

## Specification changes

- eq_3: The initial H^{\otimes n} layer preparing |+>^n is omitted by default; the returned circuit is the unitary exp(-i beta B) exp(-i gamma C) only. An optional instance flag prepare_plus_state=true re-inserts the Hadamard layer. Reason: The implementation contract requires an operation without input-state preparation; the runner supplies the input state.
- eq_2, eq_6: Variable x_j is mapped to Qiskit qubit index j-1, so x_1 is the least significant bit of Qiskit bitstrings (printed rightmost) rather than the leftmost tensor factor as in the specification. Reason: Qiskit's little-endian convention; the spec's 'qubit 1 leftmost' phrasing was resolved to a consistent per-variable layout. Since each equation is a symmetric function of its three variables, no cost term changes meaning.
- eq_2: The constant m/2 in C, described in the spec as a droppable global phase, is retained as an exact global_phase shift of -gamma*m/2. Reason: Makes the circuit unitary equal to exp(-i gamma C) exactly rather than up to phase, at zero gate cost.
- eq_4, eq_5: Scope narrowed to the circuit construction for a given (gamma, beta); the performance bounds and angle selection are not implemented. Reason: The angles and proof techniques are not available from the abstract, and classical optimization/grid search is outside a measurement-free operation.
