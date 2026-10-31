# Equation to Qiskit

Discrete-time quantum walk on a circle of N = 2^n sites with one coin qubit, driven by a chosen coin (identity for the in-scope instance) for t steps, followed by a state-independent final coin operator C_f. The conditional shift (coin |0> -> x-1, coin |1> -> x+1 mod N) is realised as a QFT-based controlled increment/decrement; because the coin acts on a different register than the QFT, a single QFT / inverse-QFT pair encloses all steps. The example instance (N=4, t=2, C=I, C_f=I) transfers the coin state from site 0 to site 2 (eq_5). Input state preparation (eq_3) and periodicity checks (eq_6) are left to the runner.

Source equation run: `719f206b-a595-4c48-a0df-5c0a1586dad6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin register (carries the unknown state alpha|0> + beta|1>; |0> moves walker to x-1, |1> to x+1)
- qubits 1..log2(N): position register, x = sum_m x_m 2^m with qubit 1 = x_0 (least significant bit); example N=4 uses qubits 1 (LSB) and 2 (MSB)
- example: input (alpha|0>+beta|1>) x |x=0> on 3 qubits is mapped to (alpha|0>+beta|1>) x |x=2> = coin x |10> (qubit 2 = 1, qubit 1 = 0)

## Assumptions

- Shift convention: coin |0> moves the walker to x-1 and coin |1> to x+1 (mod N); the paper's convention may be the label-flipped equivalent.
- Coin is applied before the shift in each step.
- Perfect transfer is understood up to a global phase; the identity-coin instance produces no extra phase.
- The angle 2*pi*2^m/N on position qubit m (qubit 1 = LSB) is consistent with QFTGate's convention |j> -> sum_k exp(2 pi i j k / 2^n)|k> with the same index ordering.

## Unresolved issues

- Explicit final coin C_f for Hadamard/biased coins and the finite distances at which they allow perfect transfer are not reconstructed; selecting coin='hadamard' yields a valid walk but no transfer guarantee.
- Flip coin with the standard shift used here gives a period-2 walk without transfer; the paper's setting for the flip-coin arbitrary-distance claim is unknown.
- Infinite-line case is not implemented (circle only).

## Equation mapping

- `eq_1`: implemented; build_circuit: QFTGate / p / cp / inverse QFTGate block (comment 'eq_1 / eq_2: shift S realised in the Fourier basis'). Conditional shift: coin |0> decrements and coin |1> increments the position modulo N via Fourier-basis phases.
- `eq_2`: implemented; build_circuit: for _step in range(steps) loop with _apply_coin then controlled phases. Each step applies coin C then the shift; repeated t times (QFT pair factored outside the loop since it commutes with the coin).
- `eq_3`: background; no code location. Initial state (alpha|0>+beta|1>) x |x_0> is prepared by the runner; the module returns only the operation.
- `eq_4`: implemented; build_circuit: final _apply_coin(qc, coin[0], final_name) (comment 'eq_4 / eq_5'). State-independent final coin C_f applied once after the t-step walk.
- `eq_5`: implemented; build_circuit with example instance N=4, steps=2, coin='identity', final_coin='identity'. Identity-coin walk on the 4-cycle for t = N/2 = 2 steps with trivial C_f, transferring the coin state to the antipodal site.
- `eq_6`: background; no code location. Periodicity is a property to be checked by the runner (e.g. steps=N with identity coin returns the input); not a separate operation.

## Specification changes

- eq_1: Circle size restricted to N = 2^n so positions are encoded as an n-bit integer and the mod-N shift equals the natural 2^n wrap-around of the Fourier-basis adder. Reason: Binary position register; non-power-of-two cycles would require a different modular adder outside the minimal scope.
- eq_2: The QFT and inverse QFT are applied once around all t steps instead of once per step. Reason: Coin operators act only on qubit 0 and commute with the QFT on the position register, so the circuit is exactly equal to the per-step construction with fewer gates.
- eq_2, eq_4: Driving coin and final coin are restricted to the named set {identity, flip, hadamard}; general biased coins are not parameterised. Reason: Only the identity-coin instance is in scope; the two other named coins are offered for exploration without claiming perfect transfer for them.
- eq_3, eq_6: Input preparation and periodicity verification are not part of the returned operation. Reason: Runner prepares inputs and performs checks; the module must return a pure unitary operation.
