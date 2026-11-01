# Equation to Qiskit

Unitary-dilation circuit for a 1D Hadamard discrete-time quantum walk on a periodic lattice of 2^n sites. Each step applies a coin and a QFT-based spin-dependent shift. Spin dephasing (probability p) and spatial dephasing (probability q) are implemented as phase-flip channels via fresh environment qubits, each rotated by RY and coupled by CZ. Initial state, measurement and tracing out the environment are left to the runner.

Source equation run: `5ede9bdc-d5d4-4c94-aa77-9005163ea773`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: spin (|up>=|0>, |down>=|1>)
- qubits 1..n: position register, little-endian binary x mod 2^n (qubit 1 is LSB); example n=3 -> qubits 1,2,3
- next steps qubits (only if p_spin>0): env_spin, one fresh environment qubit per step; example qubits 4,5
- next steps qubits (only if q_space>0): env_pos, one fresh environment qubit per step; example qubits 6,7
- total qubits = 1 + n + steps*[p>0] + steps*[q>0], max 12

## Assumptions

- Spin up = |0>, spin down = |1>.
- Position x is encoded as little-endian binary on the position register, modulo 2^n.
- The Hadamard coin and the phase-flip stand-in channels from the specification are used as given.
- p_spin and q_space default to 0 if absent, which omits their environment qubits.
- Coin first, then shift, then spin channel, then spatial channel at every step.

## Unresolved issues

- The paper's actual decoherence model, coherence length and discrete Wigner function are not reconstructed.
- The fitting of p and q to measured distributions is not implemented.
- The lattice is periodic, and the qubit cap of 12 limits steps and lattice size when environment qubits are used.

## Equation mapping

- `eq_1`: implemented; build_circuit (coin h) and _shift (QFT-based conditional shift). Hadamard coin followed by spin-controlled shift +-1 on a cyclic lattice, built as QFT, phases, inverse QFT.
- `eq_2`: implemented; build_circuit: ry on env_spin qubit + cz(env, spin). Phase-flip channel (1-p)rho + p Z rho Z realised as a unitary dilation with a fresh environment qubit having P(1)=p.
- `eq_3`: implemented; build_circuit: ry on env_pos qubit + cz(env, pos[0]). Z_x=(-1)^x equals Z on the least significant position qubit; applied with probability q via a dilation.
- `eq_4`: implemented; build_circuit step loop. Each step applies U, then the spin channel, then the spatial channel, repeated for 'steps' steps with constant p, q.
- `eq_5`: out_of_scope; no code location. Position distribution is a measurement and post-processing, handled by the runner. The environment qubits must be traced out there; the circuit contains no measurement.

## Specification changes

- eq_2, eq_3, eq_4: Non-unitary channels are implemented as unitary dilations with one fresh environment qubit per step per channel, each rotated by RY(2 asin(sqrt(prob))) from |0> and coupled by CZ. The reduced state on spin and position then equals the channel output only if the runner traces out the environment. Reason: The circuit must be unitary and measurement-free, and reset is not allowed, so environment qubits cannot be reused. Qubit cap 12 limits steps.
- eq_1: Lattice is finite and periodic with 2^n sites (shift is mod 2^n) instead of the infinite line. Reason: A finite register is needed. The walk matches the infinite line while the walker has not wrapped around.
- eq_5: Position distribution readout is excluded from the circuit. Reason: The operation returns no measurement; the runner handles readout and the fitting is out of scope.
- eq_1, eq_2, eq_3, eq_4, eq_5: The initial state |up>|x=0> is not prepared in the circuit. The runner must prepare it, with the environment in |0>. Reason: The task requires an operation without state preparation.
