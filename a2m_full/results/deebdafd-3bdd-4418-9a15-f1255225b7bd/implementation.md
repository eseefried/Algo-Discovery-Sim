# Equation to Qiskit

Hybrid qutrit+qubits QFT over Z_N with N=3*2^m (m=2 gives the specified Z_12 case on 4 physical qubits). The qutrit sits on qubits (0,1) with level l=q0+2*q1 and level 3 left fixed. F_3 is compiled exactly into standard gates: a controlled-H on levels 1,2, selective phases, and a controlled-Ry on levels 0,1. The circuit then applies qutrit-to-qubit controlled phases, a qubit QFT without swaps, and an optional inverse.

Source equation run: `c1fc37e7-41f7-4713-8ca8-e7a88691bc0e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: qutrit bit q0 (level l = q0 + 2*q1; holds x_1 at input, y_1 at output)
- qubit 1: qutrit bit q1 (level 3 = q0=q1=1 is unused and left fixed)
- qubit 2: qubit digit 2 (x_2 at input, y_2 at output)
- qubit 3: qubit digit 3 (x_3 at input, y_3 at output); for num_qubits=m the qubit digits are on qubits 2..m+1
- Input integer x = 2^m*x_1 + 2^(m-1)*x_2 + ... + x_{m+1}; output y = y_1 + 3*(y_2 + 2*y_3 + ...); Qiskit basis index = x_1 + 4*x_2 + 8*x_3 + ...

## Assumptions

- Qutrit levels 0,1,2 are encoded as q1q0 = 00, 01, 10 (l = q0 + 2*q1), and level 3 is unused
- Qutrit is the most significant input digit
- The runner prepares inputs only on the valid 12-dimensional subspace (qutrit level not 3)
- Output labelling is the digit-reversed order y = y_1 + 3*y_2 + 6*y_3
- Qiskit basis index is x_1 + 4*x_2 + 8*x_3, so digits must be converted

## Unresolved issues

- The runner's expected output ordering is unknown. If standard output order is needed, a digit permutation would have to be added.
- The decomposition of F_3 was derived analytically and not verified here. Software verification will check it.
- The behaviour on the unused level 3 is unspecified and not verified.

## Equation mapping

- `eq_1`: implemented; build_circuit (whole circuit realizes the Z_N DFT on the valid subspace). The target transform is realized by the composition of F_3, the qutrit-qubit phases, and the qubit QFT without swaps, giving the digit-reversed output labelling.
- `eq_2`: implemented; build_circuit step ordering: _f3, then qutrit-to-qubit phase loop, then the qubit H/CP loop. The mixed-radix phase factorization fixes the gate order. The qutrit digit is processed first and each qubit digit afterwards, with controlled phases from later input digits.
- `eq_3`: implemented; _f3 and the qc.h calls in build_circuit. F_3 is compiled exactly as H on levels 1,2, phases -1 and i on levels 1 and 2, Ry on levels 0,1, then H on levels 1,2. Level 3 is untouched. The qubit Hadamard is qc.h.
- `eq_4`: implemented; build_circuit: loop 'for k in range(1, m + 1)'. Phase exp(2 pi i l x_k/(3*2^k)) is built from cp(ang, q0, target) and cp(2*ang, q1, target). For m=2 the angles are 2pi/6 and 2pi/12, with the q1 angles doubled.
- `eq_5`: implemented; build_circuit: inner loop 'for j in range(i + 1, m + 1)'. Qubit-qubit controlled phases cp(2pi/2^(j-i+1)) are applied. For the two qubits of the specified case this is CP(pi/2).

## Specification changes

- eq_1, eq_2, eq_4, eq_5: Generalized the single instance (3,2,2) to (3,2,...,2) with a parameter num_qubits=m. The qutrit-to-qubit angles are 2pi/(3*2^k) and the qubit-qubit angles are 2pi/2^(j-i+1). The default example m=2 is the specified Z_12 case. An optional 'inverse' flag returns the inverse circuit. Reason: Gives a family of valid instance parameters with the same meaning. The m=2 case is exactly the specified construction.
- eq_3: Gave an explicit exact decomposition of F_3 into standard gates: controlled-H on levels 1,2 (CX-conjugated), phases -1 and i, controlled-Ry(2*atan(sqrt2)) on levels 0,1, then controlled-H on levels 1,2 again. The paper's NMR selective-rotation pulses are not reproduced. Reason: The specification left the compilation to the builder. This decomposition was derived by two-level reduction of the F_3 matrix and acts as identity on level 3.
- eq_1: The output is in digit-reversed order, y = y_1 + 3*y_2 + 6*y_3 for m=2, with no final permutation to standard order. Reason: This follows the specification's stated convention. The unitary is exact only on the valid subspace where the qutrit level is not 3.
- eq_4: The phase on the unused qutrit level 3 is whatever the CP gates give (l=3). Level 3 is not mapped to a defined output. Reason: The spec states the action on level 3 is irrelevant and only the valid subspace is checked.
