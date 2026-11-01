# Equation to Qiskit

Qiskit operation for T steps of a Hadamard-coin discrete-time quantum walk on a cyclic 2^n-site lattice. Each step applies H on the coin, a coin-conditioned increment/decrement of the position register, and spin and spatial dephasing realized as unitary dilations with fresh ancillas per step. An optional fixed coin Rz(theta0) models quasi-stationary dephasing. The initial state, measurement, and coherence-length/Wigner post-processing are left to the runner.

Source equation run: `b61ff766-4505-4f06-8a38-7070c048d881`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: pos register, little-endian integer position x (qubit 0 = least significant bit); n=3 -> qubits 0,1,2
- qubit n: coin/spin (|0> -> increment, |1> -> decrement); n=3 -> qubit 3
- qubits n+1..n+T: fresh spin-dephasing ancillas, one per step, assumed |0>; example -> qubits 4,5
- qubits n+T+1..n+2T: fresh spatial-dephasing ancillas, one per step, assumed |0>; example -> qubits 6,7
- total qubits = n+1+2T <= 12

## Assumptions

- Hadamard coin; increment for spin 0 and decrement for spin 1; cyclic boundary mod 2^n.
- Position is a little-endian integer on the pos register.
- Ancilla qubits start in |0> and are traced out by the runner.
- Spin dephasing is a Z-type phase flip. Spatial dephasing is Z on position qubit 0, which damps coherence between sites of opposite parity.
- The 'p_s' and 'q' defaults are 0 and 'theta0' defaults to 0 if keys are omitted.

## Unresolved issues

- The paper's real decoherence parametrization and Wigner function definition are unknown, so this is a phenomenological reconstruction.
- The spatial dephasing model (parity-only) is a limited toy model.
- Averaging over random theta0 and the ancilla trace must be done by the runner.

## Equation mapping

- `eq_1`: implemented; build_circuit: H on coin followed by the loop of two MCXGate with ctrl_state (coin-conditioned increment/decrement). Step operator U=S(I⊗H) on a cyclic lattice of 2^n sites, implemented with multi-controlled X gates, no dense unitary.
- `eq_2`: out_of_scope; no code location. Initial state preparation is done by the runner, not by this operation. The suggested center site N/2 with coin (|0>+i|1>)/sqrt2 is not built into the circuit.
- `eq_3`: implemented; build_circuit: ry(2 asin(sqrt(p_s))) on aspin[t], then cz(aspin[t], coin). Unitary dilation of the phase-flip channel with probability p_s per step. Tracing out the ancilla is left to the runner. The optional rz(theta0) is a separate coherent quasi-stationary dephasing extension.
- `eq_4`: implemented; build_circuit: ry(2 asin(sqrt(q))) on aspace[t], then cz(aspace[t], pos[0]). Unitary dilation of Z dephasing on the least significant position qubit with probability q per step.
- `eq_5`: out_of_scope; no code location. Coherence profile C(d), coherence length, and discrete Wigner function are classical post-processing of the reduced density matrix, not circuit operations.

## Specification changes

- eq_2: Initial-state preparation removed from the circuit. Reason: The task requires an operation without input-state preparation, so the runner must prepare the walker position, coin state, and |0> ancillas.
- eq_3: Added an optional coherent Rz(theta0) on the coin after each shift, default 0 (not applied). Reason: This represents the quasi-stationary dephasing noted in the steps. The averaging over random theta0 across runs is left to the runner, since a single circuit has one fixed angle.
- eq_1, eq_3, eq_4: Scope narrowed to one parametrized family: n position qubits (1 to 10), T steps (1 to 5), n+1+2T <= 12. Ancillas are fresh per step and the dephasing order is shift, then spin, then spatial. Reason: The qubit cap of 12 and the fresh-ancilla dilation limit the instance size. The paper's actual decoherence model is not specified.
- eq_5: Excluded from the circuit. Reason: It requires classical post-processing from the statevector or density matrix.
