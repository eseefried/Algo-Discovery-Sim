# Equation to Qiskit

Position-only coinless 1D walk on a cycle of N=2^n sites. One step is U = H_1 H_0, where H_a is the reflection 2*sum|alpha_k^a><alpha_k^a| - I over adjacent site pairs. For size-2 polygons H_0 reduces exactly to X on qubit 0, and H_1 is the same swap on the one-site-shifted pairs, built as Inc X0 Inc^dagger with an increment mod N from multi-controlled X gates. The circuit applies U for t steps and contains no state preparation or measurement.

Source equation run: `60be2e42-515f-45c2-849d-02c164c794e7`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register 'pos', little-endian, site x = sum_i q_i*2^i, N = 2^n sites on a cycle
- no coin qubit and no ancilla qubits
- input state (e.g. localized |x=0>) is prepared by the runner

## Assumptions

- Qiskit qubit 0 is the least significant bit of the site index x.
- H_1 pairs sites (2k+1, 2k+2 mod N).
- Steps are applied as H_0 first, then H_1.
- The initial state, measurement and mixing-time analysis are handled by the runner.

## Unresolved issues

- With size-2 polygons and the plain reflection, H_a is a permutation (swap). U is then a deterministic permutation, so a localized state does not spread into a superposition. The more general operator family from the paper, which would give nontrivial quantum spreading, is not specified and was not invented.
- The coined-walk equivalence mapping and the mixing-time and limiting-distribution results are not reconstructed.
- The upper bound of 256 steps is an arbitrary cap on circuit size.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop applying _h0 then _h1 each step. One step U = H_1 H_0 is implemented by applying H_0 first and H_1 second, repeated per step.
- `eq_2`: implemented; _h0 and _h1. For size-2 polygons, 2|alpha><alpha| - I on each pair equals the swap (X) of the pair. H_0 is X on qubit 0. H_1 is the same pairing shifted by one site, built as Inc X0 Dec with periodic wrap (even N = 2^n).
- `eq_3`: implemented; build_circuit: the loop over t steps. The circuit implements the operator U^t. Applying it to the runner-prepared |psi_0> gives |psi_t>. The probabilities p_t(x) come from measurement outside the module.

## Specification changes

- eq_2: Register size restricted to N = 2^n sites with periodic boundary conditions, n between 2 and 12. The infinite line is not implemented. Reason: A finite qubit register is needed, and a power-of-two cycle was the assumed layout.
- eq_1, eq_2: Scope narrowed to the assumed size-2-polygon tessellation operator. The coined equivalence, the specific operator family and the cycle mixing analysis are not implemented. Reason: The abstract gives no formulas for those parts, and the specification lists them as missing information.
