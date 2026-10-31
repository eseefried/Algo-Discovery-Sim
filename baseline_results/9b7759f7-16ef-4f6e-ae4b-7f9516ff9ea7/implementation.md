# Equation to Qiskit

Qiskit module implementing the scoped construction: Shor order finding for N=15 (control register t<=8 qubits, 4-qubit work register) with an explicitly decomposed inverse QFT whose controlled-phase angles are perturbed by a systematic fractional over-rotation epsilon (eq_3) and one seeded realization of i.i.d. Gaussian phase noise of strength sigma (eq_4). Controlled modular multiplications by a^(2^j) mod 15 are built from controlled-SWAP bit rotations and CNOT complements. The circuit is a measurement-free unitary; success-probability evaluation (eq_5) and threshold extraction (eq_6) are left to the runner.

Source equation run: `0c9041c1-b9d2-4e89-98d5-bcf77914a030`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0-7: control register c (t=8), qubit 0 = least significant bit of exponent x / measured outcome y
- Qubits 8-11: work register w (4 qubits), qubit 8 = least significant bit of a^x mod 15
- Expected input: control |00000000>, work |0001> (integer 1), unless prepare_work_one=true in which case an X on qubit 8 is included

## Assumptions

- Hadamards and the controlled modular-multiplication gates are ideal; only the inverse-QFT controlled-phase gates are perturbed.
- Systematic error is a uniform fractional over-rotation (1+epsilon) applied to every controlled-phase angle.
- Random error is i.i.d. Gaussian with zero mean and standard deviation sigma, drawn per gate in a fixed deterministic gate order from numpy default_rng(seed).
- The runner prepares the control register in |0...0> and the work register in |0001> (integer 1), unless prepare_work_one is true.
- t is allowed to vary from 1 to 8 (12-qubit cap); the canonical instance uses t = 8 = 2n.

## Unresolved issues

- The paper's actual error model (which gates are perturbed, distributions, 'combined' category) is unknown; the chosen model is a minimal concrete stand-in.
- The success-probability metric and threshold definition (eq_5, eq_6) are inferred and must be evaluated externally by measuring the control register and applying continued fractions.
- Whether the paper also perturbs the modular-exponentiation network is unknown; such errors are not modeled.

## Equation mapping

- `eq_1`: implemented; build_circuit (Hadamard loop and controlled-U^(2^j) loop) and _controlled_mult_mod15. Hadamards on the control register followed by controlled multiplications by a^(2^j) mod 15, realized as controlled cyclic bit rotations (cswap) and controlled complements (cx).
- `eq_2`: implemented; _imperfect_inverse_qft (with epsilon=0, sigma=0 it is the exact inverse QFT). Explicit H and controlled-phase decomposition of the inverse QFT, with bit-reversal swaps first, matching QFTGate(t).inverse() on qubit 0 = LSB.
- `eq_3`: implemented; _imperfect_inverse_qft: factor (1.0 + epsilon) multiplying theta. Every controlled phase angle is scaled by the same fixed factor (1+epsilon).
- `eq_4`: implemented; _imperfect_inverse_qft: delta drawn from rng.normal(0, sigma) per gate. One seeded realization of i.i.d. Gaussian phase noise is added to each gate angle; ensemble averaging over seeds is left to the runner.
- `eq_5`: out_of_scope; no code location. Success probability requires measurement, continued-fraction post-processing and averaging over error samples, which are experiment-level tasks not part of the unitary operation.
- `eq_6`: out_of_scope; no code location. Threshold extraction is a classical sweep over sigma using eq_5 results; not part of the circuit.

## Specification changes

- eq_1: N restricted to 15 and a restricted to {2,4,7,8,11,13,14}; the controlled multiplication uses the permutation 'cyclic bit shift then complement', which equals multiplication mod 15 on the units 1..14 but maps |0> and |15> non-arithmetically. Reason: A general modular-exponentiation network does not fit within 12 qubits; for N=15 every unit is +/-2^s so the shift/complement construction is exact on the states actually reached from work input |1>.
- eq_2, eq_3, eq_4: Perturbations are applied to the inverse-QFT angles theta = -pi/2^(j-k) (negative sign, controlled-phase form) rather than the forward-QFT angles 2pi/2^k written in eq_2; the systematic factor multiplies the signed angle and the inverse decomposition order (swaps first, then ascending qubits) is fixed to match QFTGate(t).inverse() with qubit 0 as LSB. Reason: The algorithm applies the inverse QFT; the symbolic R_k form in eq_2 was for the forward transform and did not fix the physical qubit order.
- eq_4: The circuit contains a single deterministic realization of the random errors selected by the integer seed; averaging over the error ensemble must be done by building circuits with different seeds. Reason: A QuantumCircuit must be a fixed bound unitary; the ensemble expectation is not a single operation.
- eq_1: The work-register |1> input is expected from the runner; an optional prepare_work_one flag (default false) adds a single X on the work LSB. Reason: Instruction forbids input-state preparation inside the operation; the flag is an opt-in convenience and is disclosed.
- eq_5, eq_6: Not implemented in the module. Reason: They are measurement/classical post-processing quantities evaluated by the runner, not unitary operations.
