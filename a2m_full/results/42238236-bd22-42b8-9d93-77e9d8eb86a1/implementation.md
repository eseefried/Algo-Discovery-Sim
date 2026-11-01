# Equation to Qiskit

Coherent (measurement-free) quantum phase estimation of the 2-qubit reduced HeH+ Hamiltonian H = g0 I + g1 Z0 + g2 Z1 + g3 Z0Z1 + g4 X0X1 + g5 Y0Y1. The circuit has m ancilla qubits plus 2 system qubits. Each ancilla k controls an exactly compiled U^(2^k) = exp(-i (H - E_ref) t 2^k), built from the block structure of H after a CNOT parity basis change. The ancilla register then gets an inverse QFT, so its integer value approximates phi*2^m. The runner must prepare the system input state, for example the Hartree-Fock determinant. This replaces the specified iterative single-ancilla scheme, which needs mid-circuit measurement, reset and feedback.

Source equation run: `dfca3bfe-4823-4689-a41b-433cce8de8f1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: sys[0] = q0, the qubit of Z0, X0, Y0; least significant bit of the system label
- qubit 1: sys[1] = q1, the qubit of Z1, X1, Y1; Z1 = Zp*Z0 in the CX-transformed basis, with the parity p temporarily on this qubit
- qubits 2..(m+1): anc[k] = qubit 2+k, controls U^(2^k); k=0 is the least significant phase bit
- output: ancilla register holds integer y ~ phi*2^m (little-endian, anc[0] least significant) with 2*pi*phi = -(E-E_ref)t mod 2*pi
- input: the runner prepares the system state (e.g. X on a system qubit for the |01> or |10> Hartree-Fock determinant); the ancillas start in |0>

## Assumptions

- Little-endian convention: sys[0] is Z0/X0/Y0 and the least significant bit of the system label; sys[1] is Z1/X1/Y1.
- The ancilla k carries weight 2^k, so the output integer y has anc[0] as its least significant bit.
- The coefficients g0..g5 are real, supplied by the instance and not derived from HeH+ integrals; the example values are illustrative, not molecular data.
- t and e_ref are chosen by the caller so that (E-E_ref)t does not alias within one 2*pi window.
- The HeH+ identification and the inferred iterative-PEA reading come from the specification, not from the abstract.

## Unresolved issues

- The actual g_i(R) values, the qubit mapping and the t, E_ref and m used in the source experiment are not specified.
- The iterative-PEA feedback sign convention is not implemented, so the original measurement-based protocol is not reproduced.
- The coherent QPE output is a distribution over y, and its overlap with the ground state depends on the runner-prepared input state.
- The NV-center hardware-specific compilation and the 1e-14 Hartree uncertainty definition are out of scope.

## Equation mapping

- `eq_1`: implemented; build_circuit: the coefficients g0..g5 enter the blocks list, the qc.p and qc.crz scalar phases, and the Ry/Rz block rotations. All six Pauli terms are compiled exactly, using the CX-transformed form H' = g0 + g3 Zp + (g1+g2 Zp) Z + (g4-g5 Zp) X.
- `eq_2`: implemented; build_circuit: the CX basis change, the blocks list (a, b per parity p) and the controlled Ry/Rz/Ry sandwich. Implements the parity-block structure of H with corrected coefficients: the even block {|00>,|11>} couples with g4-g5 and the odd block {|01>,|10>} with g4+g5 (not 2(g4+g5)). Both blocks also carry Z terms. The even block is not decoupled unless g4=g5.
- `eq_3`: implemented; build_circuit: qc.p(tau*(e_ref-g0), c) and the per-ancilla loop with tau=t*2**k. The controlled unitary is U = exp(-i(H-E_ref)t), with the E_ref offset applied as a phase gate on the control ancilla. Controlled powers use tau = t*2^k, so the eigenphase is 2*pi*phi = -(E-E_ref)t.
- `eq_4`: out_of_scope; no code location. Iterative Kitaev feedback needs mid-circuit measurement, reset and classically conditioned phase feedback, which this unitary-only module cannot express. The coherent QPE with an inverse QFT replaces it.
- `eq_5`: out_of_scope; no code location. Energy readout E = E_ref - 2*pi*phi/t is classical post-processing of measured ancilla bits, and the circuit contains no measurement. The ancilla register of this circuit encodes y ~ phi*2^m.

## Specification changes

- eq_2: Corrected the block structure: X0X1 and Y0Y1 couple |00> and |11> with amplitude g4-g5, and couple |01> and |10> with amplitude g4+g5. The odd-block diagonal also has Z-type terms. The corrected H' = g0 + g3 Zp + (g1+g2 Zp)Z0' + (g4-g5 Zp)X0' is implemented for general g_i. Reason: The original text claimed XX+YY annihilates |00>,|11> and gave a factor of 2 on the odd block. Direct algebra (XX|00>=|11>, YY|00>=-|11>, XX|01>=YY|01>=|10>) shows this holds only when g4=g5.
- eq_4, eq_5: Replaced iterative single-ancilla PEA (measurement, reset, classical feedback, bit-by-bit readout) with a coherent m-ancilla PEA ending in QFTGate(m).inverse() on the ancilla register. Reason: The requested module must be a measurement-free, non-dynamic unitary with no reset, so mid-circuit measurement and feedback cannot be used.
- eq_1, eq_3, eq_5: Narrowed scope to the circuit for one parameter set (g, t, e_ref, m). Molecular integrals and the choice of R, t and E_ref are classical inputs, and the Hartree-Fock input state is prepared by the runner. The qubit count is capped at 12, so m <= 10, which cannot reach the ~45 bits needed for 1e-14 Hartree resolution. Reason: Capacity limits and the instruction to exclude state preparation and measurement.
