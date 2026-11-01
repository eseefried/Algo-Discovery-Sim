# Equation to Qiskit

Qiskit implementation of the operator (I_x ⊗ C_f) U^t on a 2^m-site circular walk with one coin qubit, where U = S (I ⊗ C). The coin C is chosen from identity, flip (X), Hadamard, or a biased real reflection coin. The shift S moves the walker +1 on coin |0> and -1 on coin |1>, mod 2^m. The final coin C_f is a state-independent single-qubit U(theta, phi, lam) gate on the coin. Only the operation is built. Input preparation and the check of eq_2 are left to the runner.

Source equation run: `37224a3d-856b-44a4-947a-0b49cda8582c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin (carries the unknown qubit state; computational basis |0>,|1>)
- qubits 1..m: position register, little-endian binary encoding of x in 0..2^m-1 (qubit 1 is the least significant bit), circular boundary
- Shift convention: coin |0> moves x -> x+1 mod 2^m; coin |1> moves x -> x-1 mod 2^m
- Total qubits = position_qubits + 1 <= 12

## Assumptions

- Walker starts at the origin and the unknown qubit is in the coin, prepared by the runner.
- Homogeneous single-coin walk with the same C at every step.
- Coin gates act before the shift in each step.
- Biased coin = RY(2*theta) applied after Z, which gives [[cos, sin],[sin, -cos]]; theta = pi/4 reproduces the Hadamard.
- Position qubit 1 is the least significant bit of x.

## Unresolved issues

- The paper's explicit final coin operator is unknown.
- The finite transfer-distance bounds for Hadamard and biased coins are not encoded.
- The periodicity statements and periods are not encoded.
- The relation between circle size and transfer distance d is unspecified.
- Whether the target coin state equals psi or a fixed unitary transform of it is unresolved.

## Equation mapping

- `eq_1`: implemented; build_circuit: per-step loop (coin gate block, then increment/decrement ladders of controlled-X gates). One walk step U = S (I_x ⊗ C): the coin gate on qubit 0, then a coin-conditioned shift on the cyclic position register.
- `eq_2`: implemented; build_circuit: t-step loop followed by the final qc.u(...) on the coin qubit. Only the operator (I_x ⊗ C_f) U^t on the left-hand side is built. The equality with |d>|psi> is a verification target left to the runner and is not enforced. The runner prepares |0>_x|psi>. C_f is user-supplied because the paper's form is not given in the abstract.

## Specification changes

- eq_1, eq_2: Narrowed the infinite line or N-site circle to a circle with N = 2^m sites (m between 1 and 11) with periodic boundary. Reason: Qubit-register encoding needs a power-of-two position space and a cap of 12 qubits. Line behaviour is reproduced only while the walker does not wrap around.
- eq_2: The final coin C_f is an arbitrary user-supplied U(theta, phi, lam) gate (default identity) rather than the paper's specific operator. Reason: The abstract does not give the explicit C_f, so no specific choice can be reconstructed.
- eq_1: The walk coin is restricted to identity, flip (X), Hadamard, or the biased real coin [[cos th, sin th],[sin th, -cos th]]. The shift sign convention (coin 0 -> +1, coin 1 -> -1) is fixed. Reason: These cover the coin families named in the abstract. The exact biased-coin parametrization and shift convention are assumptions.
- eq_2: The transfer distance d and the perfect-transfer equality are not parameters or checks in the circuit. Periodicity and the identity/flip versus Hadamard/biased results are not encoded. Reason: The circuit is an operation only. The abstract gives no equations for these claims.
