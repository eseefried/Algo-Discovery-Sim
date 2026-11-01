# Equation to Qiskit

Order-finding core of Shor's algorithm for N=15 with a base a coprime to 15 and t counting qubits (t<=8). It applies ideal controlled modular multiplications U_a^(2^k) built from cswap/cx, then a QFT whose controlled-phase angles are perturbed as theta_k + epsilon + delta_g. The sign convention matches QFTGate and eq_2. Hadamards and the work-register |1> preparation are left to the runner.

Source equation run: `c93174b2-7a82-4c75-a388-8694e17ead41`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..t-1: counting register 'cnt', little endian (qubit k is bit k of x and of y)
- Qubits t..t+3: work register 'wrk' for y mod 15, little endian (qubit t+i is bit i)
- Expected runner input: counting register in uniform superposition (Hadamards), work register |0001>
- Example: t=8 gives 12 qubits total (cnt 0..7, wrk 8..11)

## Assumptions

- The QFT sign convention follows eq_2 (e^{+2 pi i x y/Q}), identical to QFTGate; the circuit is the explicit H/cp/swap decomposition with the angles perturbed.
- Counting qubit k controls multiplication by a^(2^k) mod 15; for k>=2 this multiplier is 1, so no gates are emitted.
- Multiplication by 7, 11, 13 and 14 is implemented as a rotation (by 3, 2, 1 or 0 positions) followed by complement of all four work bits (since -y = 15-y mod 15), which is valid on y in 0..14.
- The runner is expected to set the work register to |0001>.

## Unresolved issues

- The paper's actual error model, affected gates and threshold formula are unknown, so the perturbation model is a proposal.
- Work states y=15 (outside the modular group) are not acted on meaningfully; the circuit is intended for inputs y in 0..14.
- The success-probability metric and threshold must be computed outside this module.

## Equation mapping

- `eq_1`: background; no code location. Order definition. Not computed in the circuit; it only motivates the choice of multipliers a^(2^k) mod 15, which the code computes via pow(a, 2**k, 15).
- `eq_2`: implemented; build_circuit loop with _cmult (modular exponentiation) followed by _perturbed_qft (QFT with e^{+2 pi i x y/Q} sign). Controlled modular multiplications take sum_x|x>|1> to sum_x|x>|a^x mod 15>. The QFT then gives the eq_2 state when the angle errors are zero. The Hadamards and work |1> are supplied by the runner.
- `eq_3`: implemented; _perturbed_qft and the deltas construction in build_circuit. Every controlled-phase angle is 2 pi/2^k + epsilon + delta_g. Systematic error is epsilon, random error is delta_g (explicit list or seeded Gaussian with std sigma), combined error uses both.
- `eq_4`: out_of_scope; no code location. Success probability is a figure of merit computed from measurement statistics, not an operation. The circuit contains no measurement.
- `eq_5`: out_of_scope; no code location. Classical gcd post-processing after continued fractions is not part of the unitary circuit.

## Specification changes

- eq_2: Scope narrowed to N=15, with a in {2,4,7,8,11,13,14}, t<=8. Modular exponentiation is built from cswap/cx permutation networks because a^(2^k) mod 15 is in {1,2,4,7,8,11,13,14}. Reason: A general modular-exponentiation circuit is not specified and the 12-qubit cap makes a small fixed-modulus construction necessary.
- eq_2: The operation excludes initial Hadamards on the counting register and the work register preparation |1>. Reason: The task forbids input-state preparation in the returned operation; the runner prepares inputs.
- eq_3: Errors apply only to controlled-phase gates of the QFT. Hadamards, swaps and the modular exponentiation are ideal. delta_j is indexed by controlled-phase gate in emission order (target j descending, control m descending). Random errors are either given explicitly or drawn from a seeded normal distribution. Reason: The abstract gives no parametrization; a deterministic, bound circuit requires fixed numeric angles.
- eq_4, eq_5: Measurement, success probability and classical post-processing are not implemented. Reason: The circuit must be measurement-free and purely unitary.
