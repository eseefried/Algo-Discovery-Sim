# Equation to Qiskit

Builds the controlled operation C-(U_a^dagger V) for a Hadamard-test overlap estimate on an open-boundary rows x cols square lattice. An ancilla (qubit 0) controls the lattice register. V is H on every site followed by CZ on every nearest-neighbour edge, and U_a^dagger undoes per-site product-state rotations whose angles are supplied directly in the instance. The circuit has no ancilla preparation, no measurement and no J/h-to-angle conversion. With the ancilla in |+> and the lattice in |0^n>, the ancilla's X and Y expectations give Re A and Im A for A = <0^n|U_a^dagger V|0^n> = <a|psi_G>.

Source equation run: `c2b40b4a-3d61-430f-8fa9-0c57cb472538`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: anc (Hadamard-test control ancilla; runner prepares |+> and measures in X/Y basis)
- qubits 1..n: lat, lattice sites, site (r,c) -> qubit 1 + r*cols + c (row-major, little-endian index)
- example 2x2: qubits 1,2,3,4 = sites (0,0),(0,1),(1,0),(1,1); total 5 qubits
- lattice input expected as |0^n> prepared by the runner

## Assumptions

- Open-boundary rows x cols square lattice with one qubit per site
- U_a|0> = cos(theta/2)|0> + e^{i phi} sin(theta/2)|1> per site, implemented as P(phi)Ry(theta)
- Row-major site ordering, site (r,c) on qubit 1 + r*cols + c
- Runner prepares ancilla in |+> and lattice in |0^n>, and measures the ancilla in the X and Y bases
- Total qubits rows*cols + 1 must be at most 12

## Unresolved issues

- Exact weights of |a> in terms of J and h, and the normalization N, are not specified
- The decorated-lattice graph of the original overlap mapping is not reconstructed
- The relation between the output overlap and Z holds only if a proper (theta, phi) mapping is later supplied
- The sign convention for Im A in the Y-basis readout must be confirmed by the runner
- BQP-completeness, approximation scale and real-parameter extension are not addressed

## Equation mapping

- `eq_1`: background; no code location. Target partition function definition; it is not computed in the circuit. The J,h-to-angle conversion is not implemented.
- `eq_2`: out_of_scope; no code location. The exact overlap mapping (weights for |a> from J and h, normalization N, decorated-lattice graph) was not resolved in the specification. The product-state angles theta and phi are therefore supplied directly and no claim is made that the overlap equals Z/N.
- `eq_3`: implemented; build_circuit: controlled-H loop and ccz edge loop (V); cp/cry loop (U_a^dagger). Implements the controlled version of U_a^dagger V with V = prod CZ * H^n on a rows x cols open-boundary grid and U_a built from Ry and phase gates.
- `eq_4`: implemented; build_circuit: all lattice gates controlled on anc[0]. Implements the controlled-W part of the Hadamard test. The ancilla |+> preparation and the final X/Y-basis readout are left to the runner. Because the ancilla is the control, the ancilla coherence equals <0^n|W|0^n> with W = U_a^dagger V; the Im sign convention should be checked at readout.
- `eq_5`: out_of_scope; no code location. Shot-based estimator and additive-error scaling are classical post-processing. N is not computed here.

## Specification changes

- eq_2: Scope narrowed: the product state |a> is specified by per-site angles (theta, phi) given in the instance, not derived from J_ij and h_i. The decorated-lattice construction is replaced by one qubit per lattice site. Reason: The abstract and the specification do not give the weight formulas, N, or the decorated graph, so a faithful J,h-to-state conversion cannot be reconstructed.
- eq_3, eq_4: The circuit contains only the controlled operation C-(U_a^dagger V). The Hadamard on the ancilla and the measurements are omitted, and the controlled-V/controlled-U_a^dagger structure is used, with all lattice gates controlled. Reason: The task requires an operation without state preparation or measurement. Controlling both V and U_a^dagger gives the correct Hadamard-test amplitude <0^n|U_a^dagger V|0^n>.
- eq_2, eq_5: Non-unitary (real J,h) weights and the normalization N are not implemented. Reason: Only a unitary circuit is allowed, and non-unitary weights would need an unspecified normalization.
