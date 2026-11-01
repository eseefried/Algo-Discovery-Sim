# Equation to Qiskit

Qiskit unitary V = CNOT_A (H^{⊗m} ⊗ I) on n qubits. It maps computational basis |s>_sup|t>_tgt to the Bell-like state (1/sqrt(2^m)) sum_x (-1)^{s.x} |x>|Ax xor t>. Instance parameters are n, m and the binary (n-m) x m matrix A. The example is n=3, m=1, A=[[1],[1]]. The paper's two multi-qubit controlled-unitary gates are not implemented.

Source equation run: `aa9353dc-2854-46a3-8faa-c6255974db9e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = sup[0]: holds s_0 on input, then x_0 after H
- qubit 1 = tgt[0]: holds t_0 on input, then (Ax xor t)_0 = x_0 xor t_0
- qubit 2 = tgt[1]: holds t_1 on input, then (Ax xor t)_1 = x_0 xor t_1
- General layout: sup qubits 0..m-1, tgt qubits m..n-1, little-endian, bit j of s/x on qubit j, bit i of t on qubit m+i
- The runner prepares input |s>|t> as a computational basis state; the output is |psi_{s,t}>

## Assumptions

- The label register is the physical register itself; the runner prepares |s>|t>.
- Qubit ordering is little-endian, with sup on qubits 0..m-1 and tgt on m..n-1.
- A is given as a list of n-m rows, each with m entries in {0,1}, and arithmetic is mod 2.
- n <= 12 and n >= m+1.

## Unresolved issues

- The paper's multi-qubit controlled-unitary gates, the claim that prior algorithms are special cases, the entanglement and monogamy-score analyses and the qudit extension are not implemented.
- The earlier spec status 'partial' is not a valid status; this artifact is a complete implementation of the narrowed scope.

## Equation mapping

- `eq_1`: implemented; build_circuit: H loop on sup plus CNOT loop for A_ij=1. The circuit output on input |s>|t> is the state |psi_{s,t}>: the Hadamards give the (-1)^{s.x} signs and the CNOTs give |Ax xor t>.
- `eq_2`: background; no code location. Orthonormality follows from V being unitary (a product of H and CNOT gates) and from character orthogonality. It is not coded, and the software is expected to check it.
- `eq_3`: implemented; build_circuit: whole function (H^{⊗m} followed by CNOT_A). V = CNOT_A (H^{⊗m} ⊗ I) is implemented directly. The printed latex contains a placeholder Z^? and a state-preparation expression, and it was not used literally.
- `eq_4`: out_of_scope; no code location. The projector form of the multi-controlled X is not used. This construction uses only CNOT parity maps.

## Specification changes

- eq_3: The operation is implemented as H^{⊗m} on sup followed by CNOT_A, with no Z^s or X^t gates. The label is read from the input computational basis state. Reason: The printed latex for eq_3 contains a placeholder (Z^?) and mixes input encoding with the operator. The unitary form is unambiguous.
- eq_1, eq_2, eq_3: The earlier scope text restricting t1=0 is dropped. All 2^n inputs (s,t) are used, which gives the full basis. Reason: The count 2^m * 2^(n-m) = 2^n holds for all t, and the restriction was unnecessary.
- eq_1, eq_2, eq_3: Scope is narrowed to the CNOT-parity family of Bell-like bases. The paper's two multi-qubit controlled-unitary gates are not implemented. A is a user-supplied binary matrix, with no rank requirement enforced. Reason: The paper's controlled-unitary definitions are not available in the specification. Rank of A does not affect unitarity or orthonormality.
- eq_4: eq_4 is excluded from the circuit. Reason: The printed projector expression is ambiguous in its tensor ordering and was marked as rejected.
