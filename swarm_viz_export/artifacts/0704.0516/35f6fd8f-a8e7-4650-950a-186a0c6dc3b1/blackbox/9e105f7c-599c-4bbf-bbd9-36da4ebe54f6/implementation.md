# Equation to Qiskit

Order-finding operation for N=15 with a in {2,4,8} and t counting qubits (default t=4). It applies H on the counting register, then controlled multiplications by a^(2^k) mod 15 built as controlled-SWAP bit rotations, then an inverse QFT on the counting register. The inverse-QFT controlled-phase angles can be perturbed by systematic, random or combined error models with explicit numeric parameters. With no errors it uses QFTGate(t).inverse(). No measurement or classical post-processing.

Source equation run: `1678a4f2-e41b-4c79-9eb0-c7c7098b0728`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- count register: qubits 0..t-1 (default 0-3), little-endian x=sum x_k 2^k
- work register: qubits t..t+3 (default 4-7), little-endian y mod 15; runner must prepare y=1 (work[0]=|1>) unless include_work_init is true
- total qubits = t + 4 <= 12

## Assumptions

- Error models are my own definitions because the paper's definitions are not available.
- Gaussian offsets with a seeded numpy RNG are used when sigma>0 and no explicit random_offsets are given.
- Error perturbations apply only to inverse-QFT controlled-phase gates, not to the modular multiplication gates or H gates.
- Gates are numbered in construction order (j ascending, k ascending) for random_offsets.
- The runner prepares work register |0001>, or include_work_init is set to true.

## Unresolved issues

- The paper's exact error definitions, distributions and analytic threshold are unknown.
- Bases 7, 11 and 13 are not supported.
- Success probability and threshold sigma_c are not computed.

## Equation mapping

- `eq_1`: implemented; build_circuit: controlled-SWAP rotation loop over k (and optional qc.x(work[0])). Controlled U^(2^k) with U multiplication by a mod 15, compiled as controlled left rotations of the 4 work bits by log2(a^(2^k) mod 15). It is exact for a in {2,4,8}; the all-ones state 15 is fixed.
- `eq_2`: background; no code location. Ideal output distribution is the expected result of the H layer, controlled multiplications and inverse QFT. It is not coded separately.
- `eq_3`: implemented; build_circuit: eps_u/dl_u terms in the angle 'mag' (models systematic and combined). The same relative error epsilon and absolute error delta are applied to the magnitude of every inverse-QFT controlled-phase angle.
- `eq_4`: implemented; build_circuit: offs list (random_offsets or seeded normal draws) added to 'mag'. Per-gate offsets delta_j are either explicit or Gaussian with width sigma from a seeded RNG, and are added alone (random) or with epsilon/delta (combined).
- `eq_5`: out_of_scope; no code location. Success probability and threshold sigma_c need simulation and averaging over seeds, which are outside the unitary.
- `eq_6`: implemented; build_circuit: inverse QFT section (QFTGate(t).inverse() or explicit swaps + CP(-pi/2^m) + H). Ideal inverse QFT in Qiskit little-endian convention with bit-reversal swaps. Errors enter through the CP angles, so the explicit decomposition is used whenever any error is nonzero.

## Specification changes

- eq_1: Supported bases narrowed to a in {2,4,8} with N=15. The spec also listed 7, 11 and 13. Reason: Those bases need complement-plus-rotation maps whose 0 and 15 handling would break the stated rule that y>=15 is fixed. The demonstrated instance is a=2.
- eq_1: The X on work[0] preparing y=1 is optional via include_work_init and is off by default. Reason: The task says the operation must not include input-state preparation and that the runner prepares inputs. The flag restores the spec's included X.
- eq_6: Inverse QFT index order resolved for the little-endian convention: swaps first, then for j ascending and k<j ascending, CP(-pi/2^(j-k)) with control k and target j, then H(j). Reason: This is the exact inverse of Qiskit's QFT convention. The spec only gave a qualitative description of the gate decomposition.
- eq_3, eq_4: Perturbations are applied to the angle magnitude pi/2^m, and the gate applies the negated perturbed angle. Systematic uses (epsilon, delta), random uses only delta_j, and combined uses all three. Reason: The spec did not define the sign convention or how epsilon and delta combine. Explicit parameters were chosen.
- eq_5: P_succ and sigma_c are not built into the circuit. Reason: They are classical analysis of simulated output.
