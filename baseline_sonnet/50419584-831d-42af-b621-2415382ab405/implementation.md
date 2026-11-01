# Equation to Qiskit

Ideal Grover iterate G = (2|s><s| - I)(I - 2|w><w|) on n data qubits (default n=2, N=4) with one marked basis state w, repeated a given number of times. It is built from X, H and multi-controlled phase gates. No state preparation and no measurement. The Ising-chain Hamiltonian, pulse-level dynamics, fidelity scans and the 2*pi*k condition are not implemented.

Source equation run: `3b764e73-06fb-4e39-8935-55cab8942f5b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 's' of n_qubits qubits (example n=2: qubits 0..1).
- Qiskit qubit i = bit i of the search index x (qubit 0 least significant), so marked w=2 means qubit0=0, qubit1=1.
- The runner must prepare the input, e.g. the uniform superposition |s> = H^n|0>, before applying this operation.
- No ancilla qubits, no measurements.

## Assumptions

- Single marked item w given as an integer in [0, 2^n - 1].
- The oracle is an ideal phase oracle, I - 2|w><w|, with no ancilla.
- The 4-spin chain is not mapped; the default instance uses 2 data qubits, and n_qubits up to 12 is allowed.
- The global phase pi from the sign of 2|s><s| - I is included so the operator matches eq_2 exactly.
- 'iterations' defaults to 1 if omitted, and is limited to 0..64.

## Unresolved issues

- Mapping of the search problem onto the 4 physical spins is unknown.
- Coupling constants, pulse sequences and the exact 2*pi*k condition are unavailable, so the physical-dynamics part of the paper is not reconstructed.
- The exact fidelity definition is only assumed, and it is not computed here.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The Ising-chain Hamiltonian for nearest and next-nearest couplings has unspecified coupling values and normalization, and it is a physical-dynamics model. It is not part of the ideal Grover circuit. Its latex also contains a redundant '4/4' factor.
- `eq_2`: implemented; build_circuit: oracle block (X on zero bits of w, multi-controlled Z, X) followed by the diffusion block (H, X, multi-controlled Z, X, H) and a global phase of pi. Implements G = (2|s><s| - I)(I - 2|w><w|) exactly, including the sign of the diffusion operator via the global phase. The circuit is repeated 'iterations' times.
- `eq_3`: background; no code location. For N=4 and one marked item, G|s> = |w>. This is a property of the circuit that downstream verification can check. It is not coded separately.
- `eq_4`: out_of_scope; no code location. Fidelity is an analysis quantity, not an operation. Computing it needs simulation, which this module must not perform.
- `eq_5`: out_of_scope; no code location. The generic 2*pi*k condition is a pulse-level criterion on Rabi frequency and coupling. It is not used in the ideal gate-level circuit, and its exact form is unknown.

## Specification changes

- eq_2, eq_3: Scope narrowed to the ideal, gate-level Grover iterate on n data qubits (default 2 qubits, N=4), with no Ising couplings and no pulses. The marked index and iteration count are instance parameters. Reason: The abstract does not specify the physical pulse implementation, couplings or the mapping of search qubits onto the 4 spins, so only the well-defined ideal operation can be reconstructed.
- eq_2: The uniform-superposition preparation (step 1) is excluded from the circuit. Only the iterate (oracle plus diffusion) is built. Reason: The task requires an operation with no input-state preparation. The runner supplies the input state.
- eq_1, eq_4, eq_5: These equations are not implemented: no Hamiltonian evolution, fidelity computation or Rabi-frequency scan. Reason: They require unspecified parameters, simulation or analysis, and cannot be expressed as a faithful unitary operation from the given information.
- eq_2: The bit ordering is little-endian: qubit 0 is the least significant bit of x. The earlier register note assumed spin s1 as most significant bit. Reason: This follows the Qiskit convention required by the task.
