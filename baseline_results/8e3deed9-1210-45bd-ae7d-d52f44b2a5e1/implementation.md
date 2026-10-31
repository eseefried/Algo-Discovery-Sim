# Equation to Qiskit

Implements the two-fermion continuous-time quantum walk unitary U^(2)(t) = exp(-i t (A⊗I + I⊗A)) = exp(-i t A) ⊗ exp(-i t A) acting on two binary vertex registers v1, v2 (eq_3/eq_4). Because the two single-register factors commute and are identical, the operator is built as the same Trotterised circuit on each register; each edge term exp(-i θ(|i><j|+|j><i|)) is realised exactly as a CNOT/X basis change conjugating a multi-controlled RX(2θ). The adjacency matrix is supplied as an edge list in the instance since the explicit G_4/G_5 edge sets are not available; the example uses the 3-regular triangular prism graph (N=6) as a stand-in tiny instance. The classical cospectrality check and the harmonic-oscillator entropy test are not part of the circuit.

Source equation run: `d0ce3296-4aa2-4acf-9547-9b09e21e7c04`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- v1 = qubits 0,1,2: binary position of fermion 1 (vertex index 0..5, qubit 0 = least significant bit; basis states 6,7 are unused and left invariant)
- v2 = qubits 3,4,5: binary position of fermion 2 (vertex index 0..5, qubit 3 = least significant bit; basis states 6,7 are unused and left invariant)
- Total 6 qubits for the example (N=6 triangular prism, m=3 per register); general N uses 2*ceil(log2 N) <= 12 qubits

## Assumptions

- Two non-interacting particles with Hamiltonian equal to the adjacency matrix (unit hopping, hbar=1); the walk unitary is exp(-i t A^(2)) with A^(2) induced by A⊗I + I⊗A.
- Vertices are labelled 0..N-1 and encoded in binary with m = ceil(log2 N) qubits per register; unused basis states (N <= x < 2^m) are left invariant.
- The antisymmetric initial state |i0 j0>_- is prepared by the runner; the module returns only the walk operation.
- Product-formula error is controlled by the user via trotter_steps/trotter_order; the operation is exact only in the limit of many steps (or exactly when all edge terms commute, e.g. a perfect matching).
- Regularity of the graph is only enforced if an optional 'degree' key is supplied; otherwise any simple graph is accepted.

## Unresolved issues

- Explicit construction of G_4(n;n+2), G_5(n;n+2), T_4, T_5 (vertex count as a function of n and edge sets) is unknown, so the true cospectral pair cannot be encoded in the example.
- The paper's criterion for declaring the antisymmetric-basis adjacency matrices 'different' (an invariant beyond the two-particle spectrum, which is identical for cospectral non-interacting pairs) is not specified; comparing circuits for G and G' requires a fixed labelling convention chosen by the user.
- Number of particles and any interaction term in the paper's multiparticle walk are unknown; only the two-particle non-interacting case is implemented.
- Multi-controlled RX gates with up to 5 controls are used; transpilation depth may be large for N near 64.

## Equation mapping

- `eq_1`: background; no code location. Definition of isomorphism via relabeling; it motivates the test but is not a quantum operation. The circuit uses the vertex labels given in the instance.
- `eq_2`: background; no code location. Cospectrality/non-isomorphism of the pair is a classical property of A and A'; no spectral computation is performed in the module (operator construction is disallowed).
- `eq_3`: implemented; build_circuit docstring and the two-register structure (v1, v2); comment 'antisymmetric subspace |ij>_- (eq_3) is preserved'. The two-particle hopping operator A⊗I + I⊗A is realised on two vertex registers; since the same single-particle circuit is applied to both registers, the antisymmetric (fermionic) subspace is exactly invariant. The antisymmetric initial state itself is prepared by the runner, not the module.
- `eq_4`: implemented; build_circuit, _apply_single_particle_walk, _apply_edge_term. U^(2)(t)=exp(-itA^(2)) is built as exp(-itA)_v1 ⊗ exp(-itA)_v2, each factor via a first/second-order product formula over exactly-implemented edge terms exp(-iθ(|i><j|+|j><i|)). The pair-occupation distribution p_t and spectrum are not computed (measurement/simulation out of module scope).
- `eq_5`: out_of_scope; no code location. Harmonic-oscillator network ground state is a classical Gaussian-state computation outside the chosen quantum-walk construction.
- `eq_6`: out_of_scope; no code location. Entanglement entropy from symplectic eigenvalues is classical post-processing not part of the circuit.

## Specification changes

- eq_4: exp(-i t A) on each register is approximated by a Lie-Trotter (order 1) or Strang (order 2) product formula over edge terms with r steps instead of the exact exponential. Reason: Exact exponentiation would require either an opaque dense unitary or classical diagonalisation/operator construction, both disallowed; the product formula uses only standard gates and converges to the exact walk as r grows.
- eq_3, eq_4: The operator is implemented as U⊗U with the single-particle circuit applied to both registers, using the commutation of A⊗I and I⊗A; the module does not restrict to or project onto the antisymmetric subspace. Reason: Exact factorisation; the antisymmetric subspace is preserved automatically because both factors are identical, so an antisymmetric input (prepared by the runner) stays antisymmetric.
- eq_1, eq_2: The graphs G_4(n;n+2)/G_5(n;n+2) are replaced by a generic user-supplied edge list; the example instance is the 3-regular triangular prism (N=6), not G_4(1;3). Reason: The abstract does not provide the vertex/edge sets of G_4, G_5, T_4, T_5; the operation is implemented for any simple graph with N<=64 so the actual pair can be supplied once known.
- eq_5, eq_6: Oscillator entanglement-entropy test dropped from the implementation. Reason: Scope narrowed to one construction (two-fermion walk); the entropy test is classical and its coupling matrix and bipartition are unspecified.
