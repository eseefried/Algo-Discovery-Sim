# Equation to Qiskit

Implements only eq_1: the permutation operator U_sigma|j> = |sigma(j)> on an n-qubit register (default 2 qubits = one ququart) as a unitary circuit built from CX, X and multi-controlled X gates. The one-step parity-determining algorithm and the linear-optics layout are not specified in the abstract, so they are not implemented.

Source equation run: `9440bbf3-4773-41c7-b442-bf7b6c4708b5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0]: least significant bit of ququart index j
- q[1]: most significant bit of ququart index j (j = q0 + 2*q1)
- Computational basis |j>, j in {0,1,2,3}, stands for the ququart (2 polarization x 2 spatial modes) encoding

## Assumptions

- Ququart basis |j> maps to the 2-qubit computational basis with j = q0 + 2*q1
- Permutation is supplied as the list sigma with sigma[j] the image of j
- Default is S_4 on 2 qubits; the generalization to n<=4 qubits is an extension
- No input-state preparation or measurement is included, as the runner prepares inputs

## Unresolved issues

- The one-step quantum parity determination algorithm is not reconstructed
- The input state, the interferometric parity-encoding step and the detection-to-parity mapping are unknown
- The mapping from the actual photonic implementation to qubit gates is not specified

## Equation mapping

- `eq_1`: implemented; build_circuit (cycle decomposition) and _transposition (basis-state swaps). U_sigma|j>=|sigma(j)> is realized by decomposing sigma into cycles, then into transpositions of basis states. Each transposition is a CX-conjugated multi-controlled X.
- `eq_2`: background; no code location. The permutation sign is a classical definition. The circuit does not compute or encode parity, because the abstract does not give the one-step quantum mechanism.

## Specification changes

- eq_1: Scope narrowed to the permutation operator on a qubit-encoded register (2 qubits for the ququart by default, optionally up to 4 qubits). The linear-optics encoding (polarization x path) is replaced by a 2-qubit register. Reason: The abstract gives no optical layout, and a circuit model needs a qubit encoding.
- eq_2: The parity-determining algorithm (input state, interference, measurement mapping) is not implemented. Reason: The specification lists the quantum mechanism for one-step parity determination as missing information, and inventing it would not preserve the source.
