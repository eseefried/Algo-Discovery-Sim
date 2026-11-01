# Equation to Qiskit

build_circuit(instance) returns a 3-qubit unitary circuit for one fixed-mask trajectory of the coined Hadamard walk on a 4-cycle with reflecting closed edges. Each step applies H on the coin qubit and then the shift permutation for that step's classical edge mask. The permutation is compiled into CX and Toffoli gates by cycle decomposition into transpositions. The initial coin Hadamard from eq_3 is optional via the prepare_initial_coin flag. The random-unitary channel, peripheral analysis and Monte Carlo averaging are classical background or out of scope.

Source equation run: `cc74bc6e-ee32-45ba-a736-160f4db2e1ca`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: position bit x0 (least significant)
- qubit 1: position bit x1
- qubit 2: coin c (0=L, 1=R)
- basis index = x + 4*c (little-endian)

## Assumptions

- Edge e joins sites e and e+1 mod 4.
- Coin value 0 is L and 1 is R.
- H = (1/sqrt2)[[1,1],[1,-1]].
- Closed edges reflect: |x,R> -> |x,L> and |x,L> -> |x,R> when the relevant edge is closed.
- Masks are supplied by the caller as lists of 0 or 1 of length 4.

## Unresolved issues

- The paper's own chain shift and coin definitions are not reproduced.
- The paper's asymptotic formulas, numerical example and 2D Grover-coin results are not implemented.
- The circuit has not been checked against the dense matrix of eq_1, because verification is done afterwards by software.

## Equation mapping

- `eq_1`: implemented; _permutation and build_circuit. Coin H on qubit 2 followed by the shift S_omega as a basis permutation with reflection at closed edges, built from the classical mask for each step.
- `eq_2`: implemented; _apply_permutation and _transposition. The circuit maps basis state s to pi(s) in the forward direction. Cycles are decomposed into ordered transpositions, each compiled with CX conjugation and a Toffoli with X-fixed control polarity.
- `eq_3`: implemented; build_circuit loop and the optional prepare_initial_coin branch. The trajectory unitary is U_T...U_1 for the supplied mask sequence. The initial coin Hadamard is emitted only when prepare_initial_coin is true.
- `eq_4`: background; no code location. The mask-averaged random unitary channel is a classical ensemble over trajectories and is not a unitary circuit. Masks are sampled by the caller.
- `eq_5`: background; no code location. Peripheral-spectrum asymptotics are classical analysis of the superoperator and not part of the circuit.
- `eq_6`: out_of_scope; no code location. Position distributions and Monte Carlo averaging are measurement and post-processing steps, which the circuit does not include.

## Specification changes

- eq_3: The initial coin Hadamard is optional (prepare_initial_coin, default false when the key is absent) instead of mandatory. Reason: The task states that the circuit is an operation without input-state preparation. Setting the flag to true reproduces eq_3 exactly when the runner starts from |0,0>.
- eq_1, eq_2, eq_3: Scope is narrowed to a single trajectory with a classical mask sequence of 1 to 64 steps on a fixed 4-site cycle. Masks are validated and invalid ones raise ValueError. Reason: A circuit is unitary and cannot realize the random channel. The fixed size keeps the circuit at 3 qubits, under the 12-qubit cap.
- eq_2: The permutation is compiled by explicit cycle-to-transposition decomposition with CX and CCX gates, not with a dense permutation unitary. Reason: Opaque dense unitaries are disallowed.
