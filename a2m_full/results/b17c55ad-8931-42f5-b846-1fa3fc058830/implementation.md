# Equation to Qiskit

Builds the operation U^T, where U = S·(Ry(2θ) on coin ⊗ I) is a coin-controlled increment/decrement shift on a 2^n-site ring. The n position qubits are little-endian and the coin is the extra qubit n. The default n=5 gives 32 sites and 6 qubits. The circuit has no state preparation, measurement, decision rule or GA.

Source equation run: `94fcd2bb-3f28-4265-81d1-b8bd72db36b2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-4: position register pos, little-endian (qubit i = bit i of position index j; for n=5 the 32 sites encode the input index x)
- qubit 5: coin qubit (coin index = n); |0> moves +1, |1> moves -1
- for general n in 2..11: position qubits 0..n-1, coin qubit n
- no classical bits; the runner prepares input states and handles measurement

## Assumptions

- The coin-shift form of U is a stand-in for the paper's unspecified QPA operator.
- Position qubit i holds bit i, and the shift is arithmetic +1 or -1 modulo 2^n on that little-endian register.
- The coin is qubit n, with |0> meaning +1 and |1> meaning -1.
- Ry(2 theta) uses Qiskit's Ry convention.
- The mcx ctrl_state integer bit i corresponds to control i in the control list, with the coin first.

## Unresolved issues

- The paper's exact unitary and parameterization (extra Ry/Rz/CX layers) are unknown.
- The GA-found theta, T and boundary partition P are not available.
- It is not known whether the paper uses a coin or another internal degree of freedom.
- The task supplied no validation contract or requested instance, so the example instance is arbitrary.

## Equation mapping

- `eq_1`: background; no code location. The initial state |c=0>|x> is prepared by the runner, so the circuit contains no X-gate loading. build_circuit acts on whatever state it receives, and its position encoding is little-endian to match eq_1.
- `eq_2`: implemented; build_circuit: ry(2*theta) on the coin, then the coin-controlled mcx increment (coin=0) and decrement (coin=1) blocks inside the steps loop. U = S (C(theta) ⊗ I) with C = Ry(2 theta). V (+1 mod 2^n) is a ripple of multi-controlled X gates, and V† is its inverse sequence. Each is controlled on the coin via ctrl_state.
- `eq_3`: implemented; build_circuit: loop over steps repeats U, giving U^T. The circuit implements the unitary U^T. Measuring the position qubits and marginalizing over the coin is left to the runner and is not in the circuit.
- `eq_4`: out_of_scope; no code location. The boundary-partition decision rule is classical post-processing of measurement outcomes and is not part of the unitary operation. The partition P was also not specified.
- `eq_5`: out_of_scope; no code location. The GA fitness is an offline classical optimization objective. It is not a circuit operation, and no GA-found parameters are available.

## Specification changes

- eq_1: The initial-state preparation was removed from the circuit. Reason: The task requires the operation to contain no input-state preparation. The runner supplies |c=0>|x>.
- eq_2, eq_3: The position register was generalized from fixed n=5 (32 sites) to a validated n in 2..11 with default 5. The ring size is 2^n, and the total qubit count is n+1, capped at 12. Reason: The task asks for varying valid parameters with a qubit cap. The default n=5 reproduces the specified 32-site instance.
- eq_2: The coin is mandatory in the implementation, as qubit n. The spec described it as optional. Reason: The coin-controlled shift form of U requires a coin qubit.
- eq_2, eq_3: T (steps) and theta are taken from the instance, with steps in 1..64 and theta any finite real. The spec's domain for theta was [0, pi]. Reason: No GA-found values exist, so they must be supplied. Ry(2 theta) is well defined for any real theta.
- eq_3, eq_4, eq_5: Measurement, probability marginalization, thresholding and GA fitness are excluded from the circuit. Reason: The circuit must be a measurement-free unitary operation. The decision and optimization steps are classical.
