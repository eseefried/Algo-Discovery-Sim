# Equation to Qiskit

Implements the order-finding core of Shor's algorithm for N=15 with a chosen coprime base a. The circuit has an optional Hadamard layer on the counting register, controlled U_a^(2^k) built from controlled swaps and CX gates, and an inverse QFT on the counting register. The inverse QFT is QFTGate(t).inverse() when noiseless. When epsilon or sigma is nonzero, it is a gate-level inverse QFT whose controlled-phase angles are scaled by (1+delta), with delta = epsilon (systematic), a Gaussian draw with std sigma (random), or both (combined). The runner must prepare the work register as |0001> and handle measurement.

Source equation run: `d8ed7d59-f523-4747-9de9-fef4ffb185e1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubits 0..t-1: counting register 'count' (little-endian, qubit i has weight 2^i in m; qubit k controls U_a^(2^k))
- Qiskit qubits t..t+3: work register 'work' (little-endian, work[0]=qubit t is least significant bit of y); the runner must prepare |0001> (y=1)
- Example (t=8): count = qubits 0-7, work = qubits 8-11, 12 qubits total
- No classical bits; measurement is left to the runner

## Assumptions

- N=15 only; the work register has n=4 qubits.
- The runner prepares the work register in |0001> (y=1) before applying the circuit.
- Counting qubit k controls multiplication by a^(2^k) mod 15.
- Qiskit little-endian ordering: qubit 0 of the count register is the least significant bit of m.
- The same noise shift delta applies to a gate's whole angle (relative scaling), independent of the gate's nominal angle.
- If epsilon=0 and sigma=0 the circuit is the ideal Shor order-finding circuit; seed is then ignored.

## Unresolved issues

- The paper's actual gate-error model, error placement, and threshold definition are not given in the abstract, so the noise model is an assumption.
- The N-dependent threshold formula is not reconstructed.
- General N is not supported; only N=15 is implemented.
- Averaging over random noise realizations must be done externally by varying seed.

## Equation mapping

- `eq_1`: implemented; build_circuit (Hadamard layer and loop over k calling _cmult) and _cmult. Hadamards on the counting register (optional) followed by controlled U_a^(2^k), where U_a^(2^k) is multiplication by pow(a,2^k,15) built from controlled bit-rotation swaps and optional controlled complement. The |1> work initialisation is done by the runner.
- `eq_2`: background; no code location. The ideal peak distribution is a property of the output state of the noiseless circuit. It is not constructed in code. For r=4 and t=8 the circuit should yield peaks at m=0,64,128,192.
- `eq_3`: implemented; _noisy_iqft (and the epsilon/sigma branch in build_circuit). Each controlled-phase angle in the inverse QFT is scaled by (1+delta), with delta = epsilon, a Gaussian draw with std sigma, or epsilon plus a Gaussian draw. Draws are made once at build time from numpy default_rng(seed), giving one noise realization per seed.
- `eq_4`: out_of_scope; no code location. The success probability needs statevector probabilities, classical continued-fraction post-processing, and averaging over noise seeds. These are experiment-level actions, not part of the circuit operation.
- `eq_5`: out_of_scope; no code location. The threshold scaling heuristic is a heuristic analysis of the success probability and is not a circuit construction. It is also not stated in the abstract.

## Specification changes

- eq_1: Restricted to N=15 and a in {2,4,7,8,11,13,14}, with t<=8 counting qubits. U_a is implemented as a bit rotation (times 2^s) plus an optional bitwise complement (times -1 mod 15) rather than a generic modular-multiplication permutation. Reason: Cap of 12 total qubits and a gate-level construction without dense unitaries. Complement maps 0<->15, so the unitary differs from the specified action (identity on y>=N) on y=0 and y=15. These states are unreachable from the work input y=1, so the reachable subspace is unaffected.
- eq_1, eq_2: The work register is not initialised to |1> inside the circuit. The Hadamard layer on the counting register is included by default and can be disabled with include_hadamards=false. Reason: The circuit is an operation and must not prepare input states. The runner prepares work=|0001>.
- eq_2, eq_3: The inverse QFT is QFTGate(t).inverse() on counting qubits [0..t-1] when noiseless. The noisy path is the exact gate-level inverse of Qiskit's QFT circuit (swaps first, then for j ascending: CP(-pi*2^(k-j)) for k=j-1..0 with control k and target j, then H(j)), not a copy of the factorised QFT index order. Reason: Resolves little-endian bit order and bit-reversal so that the noiseless and noisy paths implement the same unitary at zero noise.
- eq_3: Noise is applied only to the inverse-QFT controlled-phase gates. The optional extra Rz(delta) and noise on Hadamards or modular multiplication are omitted. The angle of a CP gate is pi/2^(j-k) for target j and control k, scaled by (1+delta). Reason: The sketch marks Rz as optional, and the abstract does not specify where the paper places errors, so the narrowest consistent model was chosen.
- eq_3, eq_4: Random errors are sampled at circuit-construction time from a seeded numpy generator, giving one deterministic realization per (sigma, seed). Averaging over noise realizations is left to the runner via different seeds. Reason: build_circuit must return a bound, unitary circuit with no stochastic runtime behavior.
- eq_4, eq_5: Success probability, post-processing and threshold estimation are not implemented in the circuit. Reason: They are measurement or analysis steps outside the operation, and the threshold formula is not given in the abstract.
