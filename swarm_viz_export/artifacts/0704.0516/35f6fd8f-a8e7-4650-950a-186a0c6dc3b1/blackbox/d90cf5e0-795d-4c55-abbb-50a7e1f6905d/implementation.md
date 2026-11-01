# Equation to Qiskit

Order-finding operation for Shor's algorithm with N=15 and a in {2,4,8}. It applies H on t counting qubits and controlled modular multiplications U^(2^k) on a 4-qubit work register, implemented as controlled cyclic bit rotations. It then applies an inverse QFT with explicit controlled-phase gates and swaps. The phase angles are perturbed under an ideal, systematic, random or combined error model. Random offsets are seeded and drawn uniformly with zero mean and variance sigma^2. There is no state preparation, measurement, or threshold analysis.

Source equation run: `97935d82-71ad-4c35-a585-40537ddb7c48`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..t-1: counting register 'count', little-endian (qubit k is bit k of x); example t=4 uses qubits 0-3
- qubits t..t+3: work register 'work', little-endian bits of y mod 15; runner should prepare y=1 (qubit t = |1>, others |0>); example uses qubits 4-7
- count register ends holding the phase-estimation outcome x in the computational basis (QFTGate-compatible ordering with swaps)

## Assumptions

- The runner prepares the work register in y=1 (qubit index t set to |1>) and counting qubits in |0>.
- The initial Hadamards on the counting register are part of the operation, as specified in step 1.
- Error models are the assumed definitions from the specification, not the paper's.
- Random offsets are uniform in [-sqrt(3) sigma, sqrt(3) sigma] with a fixed seed so the circuit is deterministic and bound.
- The x register is little-endian and matches QFTGate conventions.

## Unresolved issues

- The paper's exact error definitions, distributions and analytic threshold as a function of N are unknown and not reconstructed.
- Only the order-finding unitary for N=15 with a in {2,4,8} is covered; a in {7,11,13} are not implemented.
- Seed averaging and sigma_c extraction must be done by the runner over multiple instances.

## Equation mapping

- `eq_1`: implemented; _controlled_rotate_left and the controlled-exponentiation loop in build_circuit. Controlled U^(2^k) with U^(2^k) = multiplication by a^(2^k) mod 15, implemented as a controlled left bit rotation using cswap chains, for a in {2,4,8}.
- `eq_2`: background; no code location. Ideal output distribution is the expected result of the ideal circuit and is not coded; the ideal case (error_model='ideal') is meant to reproduce it.
- `eq_3`: implemented; build_circuit: angle ang = -(mag*(1+e)+d+off) with e, d from epsilon, delta for model 'systematic' or 'combined'. The same relative error epsilon and absolute error delta are applied to every controlled-phase gate of the inverse QFT.
- `eq_4`: implemented; build_circuit: rng.uniform offset 'off' per cp gate for model 'random' or 'combined'. Independent seeded zero-mean uniform offsets with variance sigma^2 per controlled-phase gate; the combined model adds the fixed errors.
- `eq_5`: out_of_scope; no code location. Success probability and the threshold sigma_c are computed from measurement statistics and seed averaging outside the unitary.
- `eq_6`: implemented; build_circuit: inverse QFT section (swaps, then cp ladder and H). Inverse QFT built from H, controlled phases of magnitude pi/2^m and bit-reversal swaps, with the perturbed angles per eq_3/eq_4.

## Specification changes

- eq_1: Base a is restricted to {2,4,8} and N to 15; the controlled multiplications are implemented as bit rotations instead of general modular arithmetic. Reason: For a in {7,11,13} the multiplication needs a bitwise complement which would map y=0 and y=15 differently from the specified action (y>=15 fixed, 0 fixed), so they are excluded to preserve the spec.
- eq_6: The bit-reversal swaps are placed before the controlled-phase and H ladder (as the exact inverse of the forward QFT with swaps at the end), not after. Reason: This is the order that makes the ideal circuit equal QFTGate(t).inverse() in Qiskit little-endian order; the spec's wording 'then bit-reversal swaps' would give a different ordering.
- eq_3, eq_4: Perturbation is applied to the magnitude of the angle: angle = -(theta_m(1+epsilon)+delta+delta_j). Random model uses only delta_j; systematic uses epsilon and delta; combined uses all. The distribution is uniform with variance sigma^2 from a numpy seeded generator. Reason: The spec leaves definitions and distributions open; these are explicit assumed choices. The abstract does not define the paper's error models.
- eq_2, eq_5: Success probability, ideal distribution and the sigma_c threshold are not implemented in the circuit. Reason: They are measurement-level analysis, which the operation must not contain.
- eq_1, eq_2: The optional small Rz rotations after the controlled multiplications are not included; t is variable up to 8 (default 4) rather than fixed at 4. Reason: Only the three phase-gate error models are specified numerically; total qubits t+4 must be <= 12.
