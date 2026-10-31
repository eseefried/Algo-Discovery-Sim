# Equation to Qiskit

Qiskit module implementing t steps of a coined discrete-time quantum walk on the N-cycle, U^t with U = S (I ⊗ C), where the memory-dependent coin C(λ) (unknown explicit form) is represented by a generic single-qubit U(2) gate u(theta, phi, lam) supplied in the instance, and S is a coin-controlled modular ±1 shift on an n = ceil(log2 N)-qubit little-endian position register (general N ≥ 3, including non-powers of two, via an exact basis-state permutation). Measurement, time averaging and the uniformity diagnostic are left to the runner.

Source equation run: `b5c40532-a26f-41e3-b42e-ef99d139c3c2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: position bit 0 (least significant bit of vertex x in Z_N, little-endian)
- qubit 1: position bit 1 (most significant bit for N = 4, n = 2)
- qubit 2: coin qubit c (c = 0 -> shift +1 mod N, c = 1 -> shift -1 mod N)
- Example: N = 4, n = 2 position qubits + 1 coin qubit = 3 qubits; coin u(pi/2, 0, pi) = Hadamard; circuit = U^8

## Assumptions

- The recycled-coin walk is modelled as a standard time-homogeneous coined walk with a 2-dimensional coin; the true recycled-coin mechanism may differ.
- Direction convention: coin value 0 -> +1 (clockwise), coin value 1 -> -1; the paper may use the opposite convention.
- Initial state preparation (e.g. |x=0>|c=0>) is done by the runner; the circuit is the bare evolution operator.
- Example instance uses the Hadamard coin u(pi/2, 0, pi) purely as an illustrative placeholder for C(lambda).
- MCX gates with up to n open/closed controls are acceptable standard gates; no dense unitaries are used.

## Unresolved issues

- Explicit functional form of the coin C(lambda) and how lambda in [0,8] enters it is unknown, so lambda cannot be accepted as an instance parameter.
- Whether the recycled-coin model requires a larger coin space or a non-product step operator cannot be determined from the abstract.
- Which lambda values give non-uniform time-averaged distributions, the N mod 4 dependence, and the relation to the other memory-based walk are not reproducible from this construction.

## Equation mapping

- `eq_1`: implemented; build_circuit: QuantumRegister(n_pos, 'position'), QuantumRegister(1, 'coin'); n_pos = (N-1).bit_length(). Position register of n = ceil(log2 N) qubits encoding x in little-endian unsigned binary, followed by a single coin qubit; registers ordered position then coin as specified.
- `eq_2`: implemented; _controlled_increment_mod_n (controlled +1 mod N) and its .inverse() (controlled -1 mod N), applied in build_circuit with X-conjugation for the c=0 branch. Conditional shift: c=0 moves x -> x+1 mod N, c=1 moves x -> x-1 mod N. For N a power of two the MCX increment ladder realises the modular wrap directly; otherwise a controlled swap of basis states |N> and |0> is appended so that N-1 -> 0 and 0 -> N-1 under the inverse.
- `eq_3`: implemented; build_circuit: loop over steps applying qc.u(theta, phi, lam, coin) then the shift sub-circuits. U = S (I ⊗ C) applied `steps` times; the lambda-dependent coin C(lambda) is replaced by a generic U(2) gate u(theta, phi, lam) whose angles are instance inputs, since the explicit lambda-dependence is unknown.
- `eq_4`: out_of_scope; no code location. P_t(x) is obtained by measuring the position register; the module returns a measurement-free operation, so the Born-rule marginal is computed by the runner.
- `eq_5`: out_of_scope; no code location. The time average requires running the circuit for each t = 0..T-1 (separate build_circuit calls with steps = t) and classical averaging; this is runner post-processing, not part of the unitary.
- `eq_6`: out_of_scope; no code location. Uniformity criterion and Delta_T diagnostic are classical post-processing on measured distributions.

## Specification changes

- eq_3: C(lambda) is replaced by a generic single-qubit unitary u(theta, phi, lam) whose Euler angles are instance parameters; the memory parameter lambda in [0,8] is not an input and no lambda -> C mapping is invented. Reason: The abstract does not give the explicit form of the recycled-coin flip operator, so only a placeholder U(2) coin can be implemented without fabrication.
- eq_2: The modular shift for N not a power of two is realised by a binary increment followed by a controlled permutation swapping basis states |N> and |0>; unused basis states x >= N are permuted among themselves (2^n-1 -> N, etc.) rather than left fixed. Reason: Keeps the gate unitary on the full n-qubit register while acting exactly as x -> (x±1) mod N on the valid subspace x < N.
- eq_3: Only a single circuit U^steps for one chosen t is produced per call; the time average over t must be assembled by the runner from multiple calls. steps is capped at 1024 and total qubits at 12 (N <= 2048). Reason: The module must return one bound unitary operation; resource caps are required by the task constraints.
- eq_1: Position register restricted to N >= 3 with n = ceil(log2 N) qubits; qubit ordering is position bits 0..n-1 (little-endian) then coin at index n. Reason: Makes the register layout explicit in Qiskit's little-endian convention; the specification's 'position first, coin last' ordering is preserved.
