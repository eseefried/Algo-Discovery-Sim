# Equation to Qiskit

Two-qutrit ternary controlled-X (TCX) or controlled-Z (TCZ) operation on 4 qubits. Each qutrit is encoded as t=2*q1+q0, and the control is level 2, which on the valid subspace is the single qubit c1=1. TCX is a controlled-SWAP(t0,t1) followed by a b0 toggle conditioned on c1=1 and t1=0, which gives the cycle 0->1->2->0 and fixes 11. TCZ uses two controlled-phase gates, giving omega^t on the target. The instance selects the gate, which qutrit is the control, and an optional repetition count. The ternary SWAP (eq_5) is not implemented.

Source equation run: `945a7b2f-a8a8-45f7-b62d-c6c2539c9877`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = a0 (low bit of control qutrit a)
- qubit 1 = a1 (high bit of qutrit a)
- qubit 2 = b0 (low bit of qutrit b)
- qubit 3 = b1 (high bit of qutrit b)
- Encoding: trit t = 2*q1 + q0; |0>=00, |1>=01 (q1=0,q0=1), |2>=10 (q1=1,q0=0); 11 unused
- With control='b', b is the control and a is the target

## Assumptions

- Control level 2 and shift +1 mod 3, as in the specification
- Qubit 0 is the least significant bit; a=(0,1), b=(2,3)
- Correctness is only claimed on the 9 valid basis states, with 11 treated as a don't-care
- Input states are prepared by the runner
- Only standard gates (cswap, ccx, cp, x) are used, with no measurement

## Unresolved issues

- The paper's elementary one-qutrit gates from the Cartan decomposition, and its exact TCX/TCZ gate sequences, are not reproduced
- Ternary SWAP, Toffoli and Muthukrishnan-Stroud syntheses are not implemented
- Behavior on the unused 11 pair is a convention (11 fixed under TCX, phase 1 under TCZ), not taken from the source

## Equation mapping

- `eq_1`: implemented; build_circuit register layout (a=qubits 0,1; b=qubits 2,3) and the trit convention in the docstring. Encoding t=2*q1+q0 fixes which qubit is the control bit (c1) and which are the target pair (t0,t1). The runner prepares the input states.
- `eq_2`: implemented; _apply_tcx. Shift +1 mod 3 on the target trit, controlled on control level 2, which is implemented as c1=1.
- `eq_3`: implemented; _apply_tcz. Phase omega^t on the target when the control is 2. It is built from cp(2pi/3, c1, t0) and cp(4pi/3, c1, t1).
- `eq_4`: implemented; _apply_tcx. The sketch's open gate sequence is resolved. The shift is the product of two transpositions: swap trits 1<->2 first, then trits 0<->1. The first is a controlled-SWAP of (t0,t1). The second is X(t1), CCX(c1,t1,t0), X(t1). On the 4-state target pair this is the exact permutation 00->01->10->00 with 11 fixed.
- `eq_5`: out_of_scope; no code location. The ternary SWAP construction is not specified (gate count and arrangement unknown), so it is not implemented. The module builds a single TCX or TCZ operation.

## Specification changes

- eq_4: Gave a concrete exact gate sequence for the controlled shift: CSWAP(c1;t0,t1), then X(t1), CCX(c1,t1,t0), X(t1). It fixes the target state 11, and the original text said fix-ups were still needed. Reason: The sketch's tentative sequence (CCX then CX) was incomplete, so the sequence was re-derived as a product of two transpositions.
- eq_2, eq_3, eq_4: The control condition 'qutrit = 2' is implemented as the single qubit c1=1, which is exact only on the valid subspace. If the control pair is the unused state 11, the control also fires. Reason: The task states that 11 is never populated, and using one control qubit keeps the circuit compact.
- eq_3: Z_3 on the unused target state 11 is taken as phase omega^3 = 1. The qubit-level phase is exp(2 pi i t/3) with t=2*t1+t0. Reason: The behavior on 11 is unspecified, and this choice makes the controlled phases linear in the bits.
- eq_5: The ternary SWAP is not implemented. The scope is narrowed to TCX or TCZ with a selectable control qutrit and an optional integer repetition 'power' (0..8). Reason: The SWAP sequence is not determined by the abstract or the specification; 'gate', 'control' and 'power' are added to give the instance varying valid parameters.
