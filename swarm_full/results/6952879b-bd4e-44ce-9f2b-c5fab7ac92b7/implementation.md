# Equation to Qiskit

Circuit-level implementation of the logical gate set in eq_2 (RX, RZ, CPHASE with angle pi, SWAP) on n encoded qubits, applied from an ordered gate list in the instance. It is not a simulation of Bose-Hubbard walker dynamics. Each logical qubit is one Qiskit qubit, which stands for a walker's position-encoded two-level system.

Source equation run: `8b5a47e4-6387-4b7c-be59-7356476a600d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit i (0..n-1) = logical encoded qubit i, i.e. the two-level position degree of freedom of walker i
- Qubit 0 is the least significant computational-basis bit
- No ancilla qubits; total qubits = num_qubits <= 12

## Assumptions

- One walker per encoded qubit, with the logical qubit as a two-level subspace
- CPHASE has angle pi, equivalent to CZ
- Rotation angles are in radians with the standard convention exp(-i theta P/2)
- Gate sequence order is the circuit order, with the first listed gate applied first

## Unresolved issues

- Graph geometry and walker encoding are not given in the abstract
- Mapping from Bose-Hubbard evolution times and parameters to gate angles is unknown
- Steane code logical encoding and the third-dimension extension are not implemented
- Possible leakage or non-ideal behavior of the physical walkers is not modeled

## Equation mapping

- `eq_1`: background; no code location. The Bose-Hubbard Hamiltonian is the physical background. Its graph, couplings and timings are unspecified in the abstract, so the walker dynamics are not simulated or compiled.
- `eq_2`: implemented; build_circuit: rx/rz branches use qc.rx/qc.rz, and the cphase branch uses qc.cp(pi); swap uses qc.swap. The logical gate set is implemented directly with standard gates: R_X, R_Z, CPHASE=diag(1,1,1,-1), and SWAP.

## Specification changes

- eq_1, eq_2: Scope narrowed to the logical gate-level operation. The Bose-Hubbard walker dynamics that would realize the gates are not implemented. Reason: The abstract gives no graph geometry, parameters or pulse timings, so a faithful Hamiltonian-level construction is not possible.
- eq_2: Each logical qubit is mapped to one Qiskit qubit, and the gate sequence is supplied by the instance. The CPHASE angle is fixed at pi, as assumed in the spec. Reason: A concrete, parametrizable unitary operation is needed. The abstract does not specify the encoding in more detail.
- eq_2: The Steane-code encoding, measurement, and classical postprocessing steps are omitted. Reason: The operation must be measurement-free, and the abstract does not give the code details.
