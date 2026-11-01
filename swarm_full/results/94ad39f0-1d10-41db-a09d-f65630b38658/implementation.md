# Equation to Qiskit

Implements only eq_1: the ordered composition U_{sigma(n)} o ... o U_{sigma(1)}. The abstract gives no switch or query construction and the gates are black boxes, so the module uses the direct composition with each U_i described explicitly by the instance. The gates are restricted to a small standard set (single-qubit U, CP, CX, RZZ) on a data register of up to 12 qubits. Gate k of the circuit is U_{sigma(k)}, with sigma given as a 1-based list. The complexity bounds eq_2 to eq_4 are not implemented.

Source equation run: `22cbeb4c-a378-44c0-890c-d03c75c02769`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- data register: qubits 0..num_qubits-1, little-endian (qubit 0 least significant)
- no control or ancilla qubits; sigma is classical and fixes the gate order at build time
- total qubits = num_qubits (max 12)

## Assumptions

- Instance fields are num_qubits (1..12), gates (1..64 entries of the form {kind, qubits, params}) and sigma (1-based permutation list).
- Supported gate kinds are u (3 params, 1 qubit), cp (1 param, 2 qubits), rzz (1 param, 2 qubits) and cx (no params, 2 qubits).
- Input states are prepared by the runner, and the circuit contains no measurements.

## Unresolved issues

- The switch and query constructions that achieve the abstract's bounds are not reconstructed.
- The additional gate-family assumption behind the query lower bound is unspecified.
- The circuit is a direct composition and does not test the black-box or second-order models.

## Equation mapping

- `eq_1`: implemented; build_circuit (loop over k applying gates[sigma[k]-1] via _apply). Gates are appended in the order U_sigma(1) first through U_sigma(n) last, which is the composition U_sigma(n) o ... o U_sigma(1).
- `eq_2`: out_of_scope; no code location. Quantum-switch complexity n log2(n)+Theta(n) is a complexity bound. The abstract gives no switch construction, so nothing is implemented.
- `eq_3`: out_of_scope; no code location. The n^2-2n+4 query upper bound relies on a permutation-as-substring construction that the abstract does not give. The module does not treat the gates as black-box queries.
- `eq_4`: out_of_scope; no code location. The query lower bound is a proof-based statement that depends on an unspecified assumption on the gate family. It does not describe a circuit.

## Specification changes

- eq_1: The unitaries U_i are described explicitly in the instance (U, CP, RZZ or CX on data qubits) and applied directly, not as black-box oracles. Each U_i is applied exactly once, with no control register or quantum switch. Reason: The abstract gives no gate family or encoding, and black-box gates cannot be built without opaque unitaries. This is the simplest faithful realization of the target composition.
- eq_2, eq_3, eq_4: Scope narrowed to the target operation only. The complexity bounds are neither implemented nor reproduced. The circuit uses n explicit gates, not n^2-2n+4 black-box queries or n log2(n)+Theta(n) switches. Reason: The abstract states these bounds without any construction.
- eq_1: sigma is given as a 1-based list with sigma[k-1] = sigma(k). The gate applied at step k is U_{sigma(k)}. Reason: The abstract does not fix an indexing convention, so this one is chosen and disclosed.
