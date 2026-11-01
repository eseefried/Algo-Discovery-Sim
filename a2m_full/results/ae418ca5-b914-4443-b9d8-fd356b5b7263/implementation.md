# Equation to Qiskit

Qiskit operation for perfect state transfer on an N-site XX+YY chain with Krawtchouk couplings J_j=sqrt(j(N-j)) at t=pi/2. This is a spin-chain stand-in for the abstract's coined quantum walk, not the walk itself. Default method 'exact' uses the closed form of the free-fermion evolution: qubit-order reversal, CZ on all pairs and a uniform phase gate per site. Method 'trotter' applies RXX*RYY bond gates in first-order Trotter steps. Option 'corrected' appends the inverse of the CZ and phase factors, so the net operation is the pure mirror reversal of the sites (site j goes to N-1-j). There is no state preparation or measurement.

Source equation run: `7a853630-e1cd-4d1a-8a65-df4a3e5454c7`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register 'site' of n_sites qubits; qubit i = chain site i (0-indexed), qubit 0 least significant.
- Input two-qubit state is placed by the runner on qubits 0 and 1; it arrives on qubits n-1 and n-2 respectively (qubit 0 -> n-1, qubit 1 -> n-2).
- Remaining qubits start in |0> and return to |0> (up to the phase structure) because the excitation count is conserved.
- Encoding: computational basis, |1> = excitation (spin up in the XX+YY chain), no ancillas.

## Assumptions

- Krawtchouk couplings J_j=sqrt(j*(n-j)) with sites indexed 1..N in the formula and 0..N-1 on qubits.
- Jordan-Wigner convention sigma+_j sigma-_{j+1} = c_j^dagger c_{j+1}, so the XX+YY terms give positive hopping amplitudes.
- Qiskit RXX(theta)=exp(-i theta XX/2), so the bond angle equals J_j*tau.
- The runner supplies inputs on qubits 0 and 1 with the other qubits in |0>.

## Unresolved issues

- The exact closed form (uniform phase and pairwise CZ sign) is derived analytically, not yet checked numerically.
- The Trotter method has first-order error that decreases with trotter_steps.
- The abstract's coined quantum-walk construction, hypercube distribution and routing are not reconstructed.

## Equation mapping

- `eq_1`: implemented; _trotter_evolution (couplings sqrt(j*(n-j)), total time pi/2); closed-form equivalent in _exact_evolution. The chain Hamiltonian is realised either by first-order Trotterization of the bond terms, or by the exact closed-form many-body result that follows from it for the Krawtchouk couplings.
- `eq_2`: implemented; _exact_evolution. Mirror transfer at t=pi/2, written as a site reversal, a uniform phase (-i)^(n-1) per excitation and a pairwise CZ sign from the Jordan-Wigner ordering. The phase law is corrected relative to the spec (see specification_changes).
- `eq_3`: implemented; _trotter_evolution: qc.rxx(theta,j-1,j); qc.ryy(theta,j-1,j). Bond gate RXX(theta)RYY(theta) with theta=J_j*tau, tau=(pi/2)/trotter_steps. Both factors commute on one bond, so each bond gate is exact. Only the ordering of different bonds is approximate.
- `eq_4`: implemented; _undo_diagonal and the 'corrected' option; register_layout. With corrected=True the circuit is the site reversal (exact method), so site 0 goes to n-1 and site 1 to n-2. The phase correction is uniform p gates plus CZ on all pairs rather than site-dependent S gates.
- `eq_5`: out_of_scope; no code location. Fidelity readout needs U_prep, U_prep^dagger and measurement, which are the runner's job. The module returns only the transfer operation.

## Specification changes

- eq_2, eq_4: The single-excitation phase is uniform, (-i)^(N-1), not linear in j as in phi_j=phi_0+j*pi/2. The multi-excitation sectors get an extra sign (-1)^(k(k-1)/2), implemented as CZ on all pairs. The correction is therefore a global per-excitation phase plus CZ gates, not site-dependent S/Z rotations. Reason: For a spin-s rotation by pi about x, exp(-i*pi*Jx)|s,m> = e^{-i*pi*s}|s,-m> with no m dependence. Reversing the fermion mode order contributes the pair sign.
- eq_1, eq_2, eq_3: The default method is an exact closed-form circuit, not Trotterization. Trotterization is kept as an option with first-order error. Reason: The free-fermion structure gives the exact many-body unitary without a numerical compilation.
- eq_4: The output order is not swapped relative to the readout: qubit 0 maps to n-1 and qubit 1 maps to n-2, so reading (n-1, n-2) in that order recovers the original two-qubit state. Reason: The mirror map j -> n-1-j preserves the pairing of the input qubits with their output qubits.
- eq_5: Preparation, undo-preparation and measurement are removed from the module. Reason: The task requires an operation without state preparation or measurement.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to a single-chain mirror transfer. The coined discrete-time quantum walk, multi-dimensional distribution, multi-qubit entangled state distribution and routing are not implemented. The chain size is extended to n_sites in 2..12 instead of 4..8. Reason: The abstract gives no walk or coin operators, so the spin-chain stand-in from the specification is implemented.
