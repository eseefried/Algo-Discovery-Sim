# Equation to Qiskit

build_circuit(instance) synthesizes an n-qubit unitary U from a classically given 2^n x 2^m isometry V, using column-by-column reduction. For each column c, Givens rotations on index pairs (c,i), i>c, zero the entries below the pivot. A final phase on |c> makes the pivot equal to 1. The reduction gates S satisfy S V = [I;0]. The returned circuit is U = S^dagger, so U|x>_m|0>^(n-m) = V|x>. Each Givens step is a permutation-conjugated, multi-controlled Rz-Ry-Rz rotation. Gray-code multiplexors, CNOT optimization, and the CSD and qubit-by-qubit schemes are not implemented.

Source equation run: `8bebfa68-c0fd-40a2-8801-15f684a6b06e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0..q(m-1): input qubits (little-endian, q0 least significant bit of column index x)
- q(m)..q(n-1): qubits that the runner prepares in |0> (ancilla-like outputs)
- Basis index = sum_j q_j 2^j; column x of V is V|x>, with |x>_m on q0..q(m-1) and |0> on the rest
- Example n=2, m=1: q0 is the input qubit, q1 starts in |0>

## Assumptions

- The isometry is given as a dense classical matrix; the classical angle computation uses NumPy.
- The inputs occupy the low-order qubits and ancilla-like qubits are |0> (prepared by the runner).
- Multi-controlled gates from gate.control are acceptable standard gates and may be transpiled to CNOTs later.
- Rz-Ry-Rz in time order Rz(lam), Ry(theta), Rz(phi) realizes the SU(2) matrix [[p,q],[-conj q,conj p]].
- Tolerances of 1e-12 for skipping negligible rotations and 1e-8 for isometry validation are acceptable.

## Unresolved issues

- The circuit is not CNOT-optimal and does not reproduce the paper's gate counts or the factor-two-from-bound claim.
- The Knill/CSD and qubit-by-qubit decompositions, small-case numerical optimizations, and the Stinespring/POVM extension are not implemented.
- Large n with m close to n creates very many multi-controlled gates, so synthesis and transpilation can be slow near the 12-qubit cap.
- The code has not been simulated here; verification is left to the runner.

## Equation mapping

- `eq_1`: implemented; build_circuit: isometry validation (V^dagger V = I) and the final inverse of the reduction circuit. The returned unitary U satisfies U|x>|0..0> = V|x>, with the inputs on the low-order qubits and the other qubits in |0>. The phase is fixed per column. The runner supplies the inputs.
- `eq_2`: background; no code location. Parameter-counting lower bound on the CNOT count. It is not a gate-level construction and is not used in the code.
- `eq_3`: implemented; build_circuit loop with _givens and _phase_fix; the final red.inverse(). For each column c, G_c is built from two-level rotations on span{|c>,|i>} (i>c) and a phase on |c>. Both act only on indices >= c, so the fixed columns 0..c-1 are untouched. The returned circuit is the inverse of the product G_{2^m-1}...G_0.
- `eq_4`: background; no code location. Uniformly controlled rotations with Gray-code CNOT/rotation compilation are not implemented. Each rotation here is a single-pattern multi-controlled Rz/Ry (a special case of a multiplexor) built with gate.control(ctrl_state=...), with no Gray-code or Walsh-Hadamard compression.
- `eq_5`: out_of_scope; no code location. The 2^(m+n) leading CNOT scaling is not achieved by this implementation. It uses O(2^(m+n)) multi-controlled gates, each of which compiles to many CNOTs, so no CNOT-count claim is made.

## Specification changes

- eq_3, eq_4: Elementary steps of the column clearing are two-level (Givens) rotations on span{|c>,|i>}. Each is a CNOT-conjugated multi-controlled Rz-Ry-Rz rotation, not Gray-code uniformly controlled Ry/Rz cascades. Reason: The exact angle formulas and control ordering of the cascade were not specified. The Givens form is exact, easy to verify, and keeps earlier columns fixed.
- eq_3: Column phases are fixed by a multi-controlled phase gate on basis state |c>, replacing the 'diagonal phase' of the sketch. Reason: This gives an exact V rather than V up to column-dependent phases. The global phase of the circuit is still unspecified.
- eq_2, eq_5: CNOT-count optimization and the bound comparison are not implemented. Reason: The exact constants are unknown and the chosen construction is not CNOT-efficient.
- eq_1: The matrix V is supplied in the instance JSON as matrix_real and matrix_imag (2^n x 2^m), with the little-endian convention that the input qubits are q0..q(m-1). The code accepts any m and n with 0<=m<=n<=12 and rejects non-isometries (tolerance 1e-8) with ValueError. Reason: The instance parameters must define a concrete classical isometry.
