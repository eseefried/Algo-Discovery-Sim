# Equation to Qiskit

Implements eq_1 only: a reversible cascade G_n o ... o G_1 of NOT, CNOT and Toffoli gates on a 4-line register (n_qubits is configurable up to 12). The instance supplies the ordered gate list, with the first gate applied first, and the circuit is a measurement-free unitary operation. The quantum-cost sum, GC/QC minimization and saving computation are classical and are not part of the circuit.

Source equation run: `977693ac-9d1e-482b-8b02-dabe31439f45`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = x_0 (least significant bit of the 4-bit integer)
- qubit 1 = x_1
- qubit 2 = x_2
- qubit 3 = x_3 (most significant bit)
- Computational-basis encoding: basis state |x> with x = sum_i x_i 2^i; the circuit acts as the permutation f on basis states

## Assumptions

- Gate library is NOT, CNOT and Toffoli (controls list of length 0, 1 or 2).
- Gates are applied in list order, with gates[0] = G_1 applied first.
- Qubit i holds bit x_i, with qubit 0 the least significant bit.
- n_qubits defaults to 4 when absent; values from 1 to 12 are accepted, with at most 500 gates.
- The circuit is a pure operation with no input-state preparation or measurement.

## Unresolved issues

- How the optimal-GC tool is adapted to minimize quantum cost is not specified.
- The exact quantum-cost table is not specified in the abstract.
- No benchmark functions or reference circuits are supplied, so no specific permutation is reconstructed.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop over parsed gates appending x/cx/ccx in order. The cascade G_n o ... o G_1 is realized by applying the listed gates sequentially, with the first listed gate applied first. The permutation f is whatever the supplied network computes.
- `eq_2`: out_of_scope; no code location. Exact gate-count minimization is a classical search by an unspecified tool. The code only validates the library (NOT, CNOT, Toffoli) and does not minimize anything.
- `eq_3`: background; no code location. Quantum cost is a classical cost metric on the gate list (assumed NOT=1, CNOT=1, Toffoli=5). It does not alter the unitary and is not emitted by the circuit builder.
- `eq_4`: out_of_scope; no code location. QC minimization is a classical synthesis/optimization objective whose mechanism is unspecified in the abstract.
- `eq_5`: out_of_scope; no code location. The percentage saving is classical post-processing comparing published circuits and has no circuit counterpart.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to building the Toffoli-network operation for a user-supplied gate list (eq_1). Synthesis, optimization, cost evaluation and saving computation are not implemented. Reason: The abstract gives no synthesis algorithm, and the cost and optimization steps are classical and cannot be expressed as a quantum operation.
- eq_1: The gate network is supplied as instance input rather than derived from a target permutation f. Reason: Deriving the network requires the unspecified optimal synthesis tool; no benchmark function was provided.
