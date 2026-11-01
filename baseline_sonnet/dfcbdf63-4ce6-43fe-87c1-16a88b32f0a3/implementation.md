# Equation to Qiskit

Qiskit implementation of the background Szegedy quantum-walk operator W = S(2Π - I) for a classical Markov chain with 2^n nodes (n from 1 to 6), repeated `steps` times. The isometry U|i>|0> = |i>|phi_i> is built from multiplexed RY rotations. The reflection 2Π - I = U(I ⊗ (2|0><0| - I))U†. The paper-specific OQW-to-unitary conversion is not implemented because the abstract does not specify it.

Source equation run: `75c16c40-4433-4e32-b8e5-b1ba05539be2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: first (node/position) register |i>, qubit 0 least significant bit of i
- qubits n..2n-1: second register |j> (Szegedy neighbour register), qubit n least significant bit of j
- example: n=1, qubit 0 = node register, qubit 1 = second register
- basis state index = i + 2^n * j in Qiskit little-endian ordering

## Assumptions

- Number of nodes is a power of two, 2^n with n from 1 to 6, so the total is at most 12 qubits.
- Transition matrix has nonnegative real entries with rows summing to 1 (tolerance 1e-9).
- Input state is prepared by the runner.
- The example uses a 2-node chain with an asymmetric transition matrix and two walk steps.

## Unresolved issues

- The paper's OQW-to-unitary construction (Hilbert space, Kraus operators in the walk, coin and reflection) is unspecified and not implemented.
- The asymptotic mean probability formula is not derived.
- The paper's variant of the Szegedy operator may differ from the standard form used here.

## Equation mapping

- `eq_1`: out_of_scope; no code location. OQW Kraus-operator update is a non-unitary channel and the paper's unitary conversion is not specified; it is not implemented.
- `eq_2`: implemented; _prep (|phi_i> isometry U), _walk_step (W = S(2Π-I)), build_circuit (repeats W). Szegedy walk for a classical Markov chain with 2^n nodes. 2Π-I is built as U(I ⊗ (2|0><0|-I))U† using multiplexed RY rotations, then the registers are swapped.
- `eq_3`: background; no code location. Node probability is obtained by the runner measuring or projecting the node register; no measurement is in the circuit.
- `eq_4`: out_of_scope; no code location. Time averaging and the asymptotic limit are classical post-processing, not part of the circuit.

## Specification changes

- eq_1, eq_2: Scope narrowed to the background Szegedy walk operator for a classical Markov chain; the OQW-to-unitary conversion is not implemented. Reason: The abstract gives no explicit OQW-to-unitary construction, so it cannot be reconstructed.
- eq_2: Pi is realized via U with U|i>|0> = |i>|phi_i>. 2Π-I = U(I ⊗ (2|0><0|-I))U†, where 2|0><0|-I is built from X, multi-controlled Z, X plus a global phase pi. Reason: Gives an exact decomposition into standard gates without a dense opaque unitary.
- eq_2: Operator order is reflection first, then swap, with the node register as the first (low-index) register. The state |phi_i> is read as |i>|j> with qubits 0..n-1 holding i. Reason: Fixes a concrete register order for W = S(2Π-I).
- eq_3, eq_4: Probabilities and averages are not computed in the circuit. Reason: The task requires a measurement-free operation.
