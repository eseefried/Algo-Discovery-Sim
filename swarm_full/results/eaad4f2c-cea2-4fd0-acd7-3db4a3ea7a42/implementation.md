# Equation to Qiskit

Implements the XOR oracle O_f|x>|b>=|x>|b xor f(x)> for a classical f on n<=8 bits, either OR or a user truth table. f is expanded exactly in its Fourier (parity) basis, f(x)=sum_S fhat(S) Z_S. O_f is then H_b * prod_S exp(i*pi/2*fhat(S)*Z_S) * exp(-i*pi/2*fhat(S)*Z_S*Z_b) * H_b, built from H, CNOT and Rz gates with one ancilla per nonzero parity term. Ancillas are returned to |0>. The MBQC equivalence and the constant-depth claim are not implemented.

Source equation run: `78a434eb-5079-49de-8c75-82bc974e0f62`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: input register x, x_i on qubit i (qubit 0 is the least significant bit of x)
- qubit n: target qubit b, receives b XOR f(x)
- qubits n+1..n+m: parity ancillas, one per nonzero nonempty Fourier subset S in increasing bitmask order; must be input as |0> and are returned to |0>
- example n=3, OR: x=q0,q1,q2; b=q3; ancillas q4..q10 for S=1..7 (11 qubits total)

## Assumptions

- XOR (bit-flip) oracle form.
- Ancillas are prepared in |0> by the runner.
- x_i is stored on qubit i, so truth_table index x has bit i equal to x_i.
- Fourier coefficients with magnitude <=1e-12 are treated as zero.
- Instance format: {'n': int, 'function': 'or' | 'truth_table', 'truth_table': optional list of 2^n bits}.

## Unresolved issues

- The paper's actual constant-depth construction and MBQC equivalence are not reconstructed.
- Depth of this circuit is not constant because CNOT fan-out is sequential.
- Ancilla count is exponential in n for dense functions such as OR, which limits n to 3 for OR.

## Equation mapping

- `eq_1`: implemented; build_circuit: whole construction (H on b, parity-ancilla phase gadgets, H on b). The XOR oracle is realised as H_b * exp(i pi/2 f(x)) * exp(-i pi/2 f(x) Z_b) * H_b, with f expanded exactly as sum_S fhat(S) Z_S.
- `eq_2`: implemented; build_circuit: qc.rz calls on ancillas and on b. Arbitrary Z rotations Rz(theta)=exp(-i theta Z/2) with angles +-pi*fhat(S) are the only non-Clifford gates used.
- `eq_3`: implemented; build_circuit: function=='or' branch (table=[0]+[1]*(2^n-1)). The disjunction oracle is obtained exactly by setting the truth table of f to OR.

## Specification changes

- eq_1, eq_3: Narrowed to an explicit finite-n circuit-model construction with n<=8 inputs and total qubits <=12. Dense Fourier expansion with one ancilla per nonzero parity term; for OR this means 2^n-1 ancillas, so n<=3 in practice. Reason: The abstract gives no explicit constant-depth construction, so a concrete exact phase-polynomial realisation was chosen, subject to the 12-qubit cap.
- eq_1, eq_2, eq_3: The MBQC pattern, measurement angles, byproduct corrections, and the constant-depth/unbounded fan-out claim are not implemented. Parity fan-in uses sequential CNOTs, so circuit depth grows with n. Reason: These details are not in the specification, and the operation must be a unitary measurement-free circuit.
- eq_1: The oracle is exact only up to a global phase exp(i pi/2 fhat(empty set)), which is dropped, and only on the subspace where the ancillas are in |0>. Reason: A global phase is physically irrelevant, and ancillas are uncomputed to |0>.
