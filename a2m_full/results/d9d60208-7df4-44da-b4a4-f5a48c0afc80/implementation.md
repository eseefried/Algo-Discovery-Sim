# Equation to Qiskit

build_circuit(instance) returns the unitary exp(-i H2 t) with H2 = A⊗I + I⊗A for a user-supplied symmetric 0/1 adjacency matrix (N<=8, zero-padded to 2^m vertices). It acts on two m-qubit position registers (6 qubits for m=3). A is decomposed into Pauli strings classically. Since the two single-particle terms commute, each register is evolved separately by a product-formula (Trotter, order 1 or 2) of Pauli rotations built from standard gates. The circuit preserves the antisymmetric subspace. State preparation, measurement, and TV-distance comparison are left to the runner.

Source equation run: `f65f5e7a-3b27-4402-b3d1-41bbaf893357`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0-2: register r1 (particle 1 position), little-endian binary vertex index (qubit 0 is the least significant bit)
- Qubits 3-5: register r2 (particle 2 position), little-endian binary vertex index (qubit 3 is the least significant bit)
- For N<=4 vertices, m=2 and the registers are qubits 0-1 (r1) and 2-3 (r2)
- No ancilla qubit is used
- Vertex v is the basis state |v> in each register; vertices >= N are zero-padded and isolated

## Assumptions

- The adjacency matrix is given in instance['adjacency'] as a symmetric 0/1 matrix with zero diagonal and 2<=N<=8
- Vertex v maps to the little-endian computational basis state |v> on each position register
- Padding vertices (index >= N) are isolated and have zero rows and columns
- The same graph Hamiltonian acts on both particles (noninteracting fermions)
- Trotter step count and order are user parameters, with defaults 1 and 2
- The global phase from the identity Pauli component is dropped; it is zero for a zero-diagonal A anyway
- The example graph is the star K_{1,4} plus 3 padding vertices. Its cospectral partner (C4 plus an isolated vertex) is not given in the abstract and must be supplied by the runner

## Unresolved issues

- The abstract does not give the edge lists of G4(n;n+2), G5(n;n+2), T4 or T5, so no instance of those graphs is built in
- The paper's initial state, observable and time values are unknown
- Trotter error is not bounded in the code; accuracy depends on trotter_steps and t
- The entanglement-entropy part of the paper is excluded

## Equation mapping

- `eq_1`: background; no code location. The antisymmetric-basis matrix elements are not built explicitly. The circuit acts on the full tensor-product space, and H2 commutes with SWAP, so the antisymmetric subspace is preserved automatically. The matrix elements describe the restriction of the implemented operator to that subspace.
- `eq_2`: implemented; build_circuit / _evolve: A is Pauli-decomposed in _pauli_terms and applied to r1 and to r2. H2 = A⊗I + I⊗A is implemented as the sum of the same single-particle Hamiltonian on each register. Because the two terms commute, the evolution factorises into two per-register evolutions.
- `eq_3`: implemented; build_circuit / _evolve / _rot (the evolution operator only). Only the evolution operator exp(-iH2 t) is implemented, approximated by a Trotter product formula. The antisymmetric initial state and the position-basis readout are supplied by the runner.
- `eq_4`: out_of_scope; no code location. The total variation distance is classical post-processing of simulated distributions, not part of the unitary circuit.
- `eq_5`: out_of_scope; no code location. The trace or moment criterion is classical spectral analysis. The equation is also incomplete as written (the exact formula is omitted), so it is not implemented.

## Specification changes

- eq_2, eq_3: exp(-iH2 t) is implemented as a Pauli-rotation Trotter product formula (order 1 or 2, user-chosen number of steps) rather than exactly. Reason: Opaque dense unitaries and operator construction are disallowed. A is not generally a sum of commuting Pauli terms, so the result is approximate with an error that shrinks as trotter_steps increases.
- eq_3: The circuit contains only the evolution operation. The antisymmetric initial state preparation and readout are removed from the circuit. Reason: The task requires an operation without state preparation or measurement; the runner prepares inputs.
- eq_1, eq_2: H2 acts on the full N^2 (padded 2^m x 2^m) tensor space rather than being projected onto the antisymmetric subspace. Reason: Unitary evolution by H2 preserves the antisymmetric sector, so no projection is needed in the circuit. Antisymmetry is a property of the input state.
- eq_2, eq_3: Scope narrowed to N<=8 vertices with explicit adjacency matrices (symmetric, 0/1, zero diagonal), zero-padded to 2^m vertices. The optional Hadamard-test ancilla is omitted. Reason: Qubit cap and the stated scope. The return-amplitude variant needs a controlled evolution, which is not implemented.
- eq_4, eq_5: Distinguishing criteria and trace moments are not implemented. Reason: They are classical post-processing; eq_5 is also an incompletely specified formula.
