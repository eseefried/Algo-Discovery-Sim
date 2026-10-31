# Equation to Qiskit

Qiskit operation U(t) ~ exp(-i H_w t) for the continuous-time quantum walk search Hamiltonian on an n x n periodic honeycomb (graphene) lattice with one marked site whose three bonds are modified by epsilon and which optionally carries an on-site potential mu. Sites are binary-encoded on ceil(log2(2n^2)) qubits; each of the 3n^2 bond terms is applied exactly as a two-level X rotation between two computational basis states (CX-chain conjugated multi-controlled RX) and the on-site term as a multi-controlled phase, combined in a first- or second-order Trotter product. The Dirac-point initial state and the measurement of P_w(t) are left to the runner.

Source equation run: `e4be69ff-78d6-4b3e-89a0-c23bcf093578`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- site[0..4] (qubits 0-4): 5-qubit binary site register for N = 2 n^2 = 18 sites; qubit j holds bit j of idx(m1,m2,sigma) = 2(3 m1 + m2) + sigma (qubit 0 = sublattice bit sigma, A=0/B=1; qubits 1-4 = cell index 3 m1 + m2), little-endian
- basis states 18..31 are unused and left strictly decoupled (no gate couples them to states < 18)
- marked site w = idx(0,0,A) = 0 = |00000>; its neighbours are idx(0,0,B)=1, idx(2,0,B)=13, idx(0,2,B)=5

## Assumptions

- Periodic boundary conditions, uniform hopping gamma > 0 and zero background on-site energy.
- Two-level bond term exp(-i c dt (|k><l|+|l><k|)) is realised as RX(2 c dt) on the differing qubit after a CX chain aligns k and l to differ in exactly one bit; the chain is self-inverse because all CXs share the same control.
- On-site term exp(-i mu dt |w><w|) realised as a multi-controlled phase gate with angle -mu dt selecting basis state w; it is skipped when mu == 0.
- Qubit count is ceil(log2(2 n^2)) (5 for n = 3); n up to 45 would fit under 12 qubits but circuit depth grows as 3 n^2 multi-controlled rotations per Trotter step.

## Unresolved issues

- The paper's exact family of marking perturbations and strengths, its starting state, and its scaling results are unknown; only the generic (epsilon, mu) local perturbation is implemented.
- Trotter error is not controlled analytically here; the runner should choose trotter_steps large enough for the desired t.
- The multi-controlled RX/phase gates are left to the transpiler for decomposition; no gate-count optimisation (e.g. Gray-code ordering of bonds) is performed.

## Equation mapping

- `eq_1`: implemented; _bond_list (coefficient -gamma on every A-B bond, neighbour offsets (0,0),(1,0),(0,1) mod n). Unperturbed honeycomb tight-binding Hamiltonian; each bond is exponentiated exactly in _apply_two_level_x.
- `eq_2`: background; no code location. Bloch spectrum and Dirac points motivate the constraint n % 3 == 0 enforced in build_circuit but are not themselves implemented.
- `eq_3`: implemented; _bond_list (epsilon added to bonds touching w) and _apply_onsite_phase (mu |w><w| term). Marked Hamiltonian with bond modification epsilon and on-site potential mu localised at the marked site.
- `eq_4`: out_of_scope; no code location. Initial Dirac-point state is prepared by the runner; the module returns only the evolution operator.
- `eq_5`: implemented; build_circuit main loop (Trotter product over bond and on-site exponentials). exp(-i H_w t) is implemented as a first- or second-order Trotter product; P_w(t) estimation and t_opt search are measurement/post-processing steps left to the runner.
- `eq_6`: implemented; _site_index and the register construction in build_circuit. Binary site encoding idx = 2(n m1 + m2) + sigma on ceil(log2 N) qubits; unused basis states are never acted upon by two-level couplings.

## Specification changes

- eq_5: Exact exp(-i H_w t) replaced by a Trotter product (order 1 or 2, trotter_steps user-chosen) of exactly exponentiated bond terms and on-site term. Reason: Opaque dense unitaries are disallowed; each bond is a two-level coupling that can be exponentiated exactly with standard gates, so only the product-formula error remains.
- eq_4, eq_5: Initial-state preparation and computational-basis measurement removed from the module. Reason: The deliverable is an operation; the runner prepares inputs and measures.
- eq_3: Marked site is a general parameter marked_site in [0, 2n^2) rather than fixed to idx(0,0,A) = 0; epsilon and mu are free real inputs. Reason: Allow the operation to vary over valid instances; the specification treats (epsilon, mu) as scan parameters.
- eq_1, eq_2: n is required to be a positive multiple of 3. Reason: Follows the symbol domain in the specification (Dirac points are allowed momenta only when 3 divides n); the Hamiltonian itself would be well defined for other n >= 2.
