# Equation to Qiskit

Builds a unitary Naimark dilation of a single-qubit trine or SIC POVM on 2 qubits. Qubit 0 is the system (polarisation) qubit and qubit 1 is the ancilla (walk position). With the input state |psi> on qubit 0 and |0> on qubit 1, the computational-basis index k = q0 + 2*q1 occurs with probability <psi|E_k|psi>. The 4x4 unitary is built from two-level (Givens) controlled rotations plus phase gates, using standard gates only. It is not a literal beam-displacer or wave-plate model.

Source equation run: `2b1ebc9f-5c93-4ddd-abd5-bd386dd43c05`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = sys: polarisation qubit, input system state; low bit of the outcome label
- qubit 1 = anc: walk-position/Naimark ancilla, prepared in |0> by the runner; high bit of the outcome label
- outcome k = q0 + 2*q1 (little-endian). Trine uses k=0..2 (k=3 has zero probability). SIC uses k=0..3.
- input convention: state |psi> on qubit 0 tensor |0> on qubit 1; computational basis outcome probabilities equal Tr(rho E_k)

## Assumptions

- The ancilla qubit starts in |0> and the system qubit holds the input state, both prepared by the runner.
- Output spatial modes map one-to-one to POVM outcomes, labelled by the two-qubit basis index.
- The unitary completion beyond the two physical input columns is arbitrary and is fixed by the Givens construction.

## Unresolved issues

- Unambiguous state discrimination is not implemented because its states and overlap are not specified.
- The physical walk geometry, wave-plate angles, step count and detectors are not reconstructed.
- The Givens-based unitary completion has not been verified in this stage.

## Equation mapping

- `eq_1`: implemented; _isometry and build_circuit. The isometry V[k,j] = sqrt(w)<psi_k|j> satisfies V^dag V = sum_k E_k = I. build_circuit extends it to a unitary on sys+anc, so outcome probabilities follow the Born rule Tr(rho E_k).
- `eq_2`: implemented; _bloch_vectors (povm == 'trine' branch). Three equatorial Bloch vectors at angles 2*pi*k/3 (plus optional azimuth_offset) with weight 2/3, so E_k = (2/3)|psi_k><psi_k|.
- `eq_3`: implemented; _bloch_vectors (sic branch). Four tetrahedron Bloch vectors with weight 1/2, so E_k = (1/2)|phi_k><phi_k| and pairwise overlaps |<phi_j|phi_k>|^2 = 1/3. The tetrahedron orientation is a choice and is rotated by azimuth_offset about z.

## Specification changes

- eq_1, eq_2, eq_3: The physical beam-displacer/wave-plate quantum walk is replaced by an abstract Naimark dilation on two qubits: one polarisation qubit and one position/ancilla qubit. Reason: The abstract gives no walk geometry or wave-plate angles. The Naimark isometry is the mathematically specified content, so it is realised through Givens-type controlled rotations.
- eq_1: Scope is narrowed to the trine and SIC POVMs. Unambiguous discrimination of two non-orthogonal states is not implemented. Reason: No equation, states or overlap are specified for the discrimination POVM, and no equation ID covers it.
- eq_2, eq_3: The states |psi_k> and |phi_k> are defined explicitly from the Bloch vectors. The SIC tetrahedron orientation is fixed with one vertex on +z. An optional azimuth_offset rotates all vectors about z. Reason: The supplied equations leave the state definitions and orientation unspecified.
- eq_1: The detected output spatial mode is represented by computational-basis index k = q0 + 2*q1, with no measurement included. Only the unitary on sys+anc is returned. Outcome 3 is unused for the trine. Reason: The task requires a measurement-free unitary operation, with inputs prepared by the runner.
