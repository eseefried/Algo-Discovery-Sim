# Equation to Qiskit

Trotterized continuous-time quantum walk search operator on a periodic 2x2-cell honeycomb lattice (8 sites, 3 qubits). Each step applies the three perfect-matching hopping layers exp(i*gamma*dt*A_c), which are exact X-parity rotations, followed by a multi-controlled phase exp(i*epsilon*dt|w><w|) on each marked site. This implements U=exp(-iHt) for H=-gamma*A-epsilon*sum|w><w|. Hadamard initial state, measurement and scans are left to the runner.

Source equation run: `7fbd902d-9b0a-4e8d-890d-ac18bb7b7286`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = x cell coordinate bit (site bit 0, little-endian)
- q1 = y cell coordinate bit (site bit 1)
- q2 = sublattice bit (0 = A, 1 = B; site bit 2)
- site index = 4*q2 + 2*q1 + q0; total 3 qubits, no ancillas

## Assumptions

- The lattice is the periodic 2x2-cell honeycomb with the explicit site labelling given in the register layout.
- Nearest-neighbour hopping amplitude is gamma, and the marking onsite energy epsilon is a free parameter.
- The runner prepares the initial state and interprets qubit q_i as site bit i (little-endian).
- Steps are capped at 500 and the marked sites are distinct.

## Unresolved issues

- The 2x2 periodic honeycomb has no E=0 Dirac point, so the physics of the paper's Dirac-point search needs a larger lattice, which is beyond the 3-qubit scope.
- The paper's exact lattice geometry, marking variants and optimal parameters are unknown.
- The J_eff and t* for transfer must be determined numerically by the runner.
- Trotter error from the hopping/marking splitting depends on dt and is not controlled here.

## Equation mapping

- `eq_1`: implemented; build_circuit: hopping layers (masks loop) and marking phase (marked loop). H=-gamma*A-epsilon*|w><w| is evolved as exp(-iHt)=exp(i*gamma*t*A+i*epsilon*t|w><w|), with the hopping and onsite parts applied in alternating Trotter steps.
- `eq_2`: background; no code location. The Dirac-point condition A|psi_D>=0 is not a gate. It only guides the choice of gamma and epsilon by the runner. See unresolved issues: the 2x2 torus has no zero mode.
- `eq_3`: implemented; build_circuit: loop over steps, masks and marked sites. First-order product formula with three matching layers, each exp(i*gamma*dt*A_c) with A_c a Pauli-X string, then the multi-controlled phase for each marked site, repeated r=steps times.
- `eq_4`: out_of_scope; no code location. The Hadamard uniform initial state, measurement and the P_w estimate belong to the runner, because the circuit is only the operation.
- `eq_5`: implemented; build_circuit: marked_sites list with two entries [s, r]. The transfer Hamiltonian H_T with equal onsite energies on s and r is implemented as the operator with two marked sites. The runner supplies the initial state |s>. The transfer time t* and J_eff are determined numerically outside the circuit.

## Specification changes

- eq_3: On the 2x2 torus A(x,y) neighbours B(x,y), B(x-1,y), B(x,y-1). These are three distinct sites, so the graph is the simple cube graph Q3 with no multi-edges. The three matchings are XOR with masks 100, 101, 110, each a Pauli-X string. Reason: This resolves the multi-edge concern in the spec and gives an explicit site-to-bit map. The three hopping layers commute, so Trotter error comes only from the hopping/oracle splitting.
- eq_1, eq_3: The sign convention is fixed as U=exp(-iHt)=exp(+i*gamma*t*A+i*epsilon*t|w><w|), which uses rx(-2*gamma*dt) and cp-type phase +epsilon*dt. Reason: The spec leaves the sign of the exponent implicit and this matches eq_3.
- eq_4: State preparation and measurement are removed from the circuit. Reason: The module must return an operation only and inputs are prepared by the runner.
- eq_1, eq_5: Generalized the single marked site w to a list marked_sites of 1..8 distinct sites with a common epsilon. Reason: This lets one function cover both search and two-site transfer.
- eq_2: No Dirac eigenstate preparation circuit is included and the E=0 resonance is not claimed for this lattice. Reason: The cube graph spectrum is {3,1,1,1,-1,-1,-1,-3}, so there is no zero mode on this tiny lattice.
