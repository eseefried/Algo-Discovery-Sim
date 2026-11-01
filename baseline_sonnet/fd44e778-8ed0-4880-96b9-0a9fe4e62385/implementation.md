# Equation to Qiskit

Hybrid-qudit QFT on one qutrit (encoded in 2 qubits) plus n qubits (n=2 gives dimension N=12). It uses the Cooley-Tukey split N=3*2^n: a generalized (3-dimensional) Hadamard on the qutrit, generalized controlled-phase twiddles omega_N^(x_l*y') between the qubits and the qutrit, then a qubit QFT (QFTGate) on the qubit digits. The qutrit DFT is built from standard controlled gates by an exact two-level decomposition, with no dense unitary. Output digits are in the Cooley-Tukey order y = y_q + 3*y_r, where y_q is the qutrit digit and y_r is the qubit-register value, with no final reordering permutation.

Source equation run: `d9b138af-793f-4b08-a9e4-2e2c68de785d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: qutrit 'lo' bit
- qubit 1: qutrit 'hi' bit
- qutrit encoding: level 0=|hi=0,lo=0>, level 1=|hi=0,lo=1>, level 2=|hi=1,lo=1>; |hi=1,lo=0> is unused and left invariant
- qubit 2: qubit digit x_0 (least significant bit of x_l)
- qubit 2+k: qubit digit x_k, k=0..n_qubits-1 (n=2 example: qubits 2,3)
- input integer x = 2^n * x_qutrit + x_l, x_l = sum_k 2^k x_k
- output: qutrit register holds y mod 3; qubit register holds floor(y/3), in little-endian binary

## Assumptions

- The qutrit occupies the most significant input digit, and the DFT sign convention is exp(+2 pi i kl/d).
- The input state must lie in the valid qutrit subspace (levels 0,1,2). The unused state |hi=1,lo=0> is not acted on by any gate except where it is merely a control, and stays invariant.
- QFTGate(n) on the qubit digits uses little-endian order with qubit 2 as the least significant bit.

## Unresolved issues

- The paper's actual gate decomposition, phase schedule, and output ordering are unknown.
- No reordering permutation is applied, so the output digits are in Cooley-Tukey order rather than the natural mixed-radix order.
- Correctness is not verified here; software will do that.

## Equation mapping

- `eq_1`: implemented; build_circuit (whole circuit). The full circuit realizes F_N with N=3*2^n via Cooley-Tukey factorization N=3*2^n. The output digit order is permuted (y mod 3 in the qutrit, y//3 in the qubits) and no final reordering is applied.
- `eq_2`: implemented; _qutrit_dft (d=3); QFTGate (qubit digits, d=2 Hadamards inside the qubit QFT). H_3 with matrix entries omega_3^(kl)/sqrt3 is built from controlled-H, controlled-phase, CZ and CRY gates by an exact two-level decomposition. The qubit Hadamards are inside QFTGate.
- `eq_3`: implemented; register layout; build_circuit. Input is a mixed-radix integer with the qutrit as the most significant digit: x = 2^n x_q + x_l (for n=2, x=4x_0+2x_1+x_2). The qutrit is embedded in two qubits with a non-binary level encoding chosen so that every two-level rotation is a singly controlled gate.
- `eq_4`: implemented; _twiddle. The generalized controlled phase has the derived form omega_N^(x_l*y') with N=3*2^n. For each qubit k it applies angle 2 pi 2^k/N times y'=lo+lo*hi, using cp(qubit,lo) and mcp(qubit,lo; hi). The denominators are derived from the factorization, not guessed.
- `eq_5`: implemented; build_circuit ordering: _qutrit_dft, _twiddle, QFTGate. The decomposition is H_3 on the qutrit, then the controlled-phase twiddles, then the qubit QFT. The QFTGate includes its own bit-reversal swaps.

## Specification changes

- eq_5, eq_1: The schematic 'SWAP/reorder . prod(H prod CP)' is replaced by the concrete Cooley-Tukey order (qutrit H_3, twiddle phases, qubit QFT) with no final digit-reordering permutation. The circuit equals F_N only up to the output relabeling y = y_q + 3*y_r. Reason: The abstract's decomposition is not specified. The direct digit-by-digit radix-(3,2,2) factorization does not exist with the qutrit as most significant output digit, because the phase x*y/12 does not factor over digits. The Cooley-Tukey form is exact.
- eq_3: The qutrit is embedded in two qubits with levels 0,1,2 mapped to |00>,|01>,|11> (hi,lo), and generalized to n qubit digits (n up to 10) with a total qubit cap of 12. An optional 'inverse' flag is added. Reason: A qubit-based circuit needs an encoding of d=3. This one makes the two-level rotations controlled single-qubit gates.
- eq_4: The generic phase 2 pi k_a k_b/m is specialized to angles 2 pi 2^k y'/N. Reason: These angles are required by the factorization.
- eq_1, eq_2, eq_3, eq_4, eq_5: Narrowed scope: the NMR selective-rotation pulses, the four-qubit qutrit emulation of the paper, and the experimental results are not implemented. Reason: The abstract gives no details.
