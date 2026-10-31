# Equation to Qiskit

Implements the coherent (unitary) core of the scoped single-qubit weak-measurement decomposition: a fixed number n of iterations of the constant-Hamiltonian probe interaction U = exp(-i*eps*Z_S (x) Y_P) (eq_2/eq_3), each on a fresh probe qubit, followed by the X-basis readout rotation (Hadamard) on that probe. Probe measurements, resets and the classical stopping-time feedback (eq_5) are not part of the returned operation; by the deferred-measurement principle the n probes are kept as separate qubits so that a later Z-basis readout of probe k yields outcome m_k and the system is acted on by the product Kraus operator of eq_4. Qubits: index 0 = system, indices 1..n = probes (step order).

Source equation run: `77beebab-f58e-4bb1-9eba-0879fb497036`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 (register s[0]): system qubit S, least significant bit; carries the arbitrary input state |psi>
- qubit 1 (p[0]): probe for weak-measurement step 1, expected input |0>; after the circuit, Z-basis value 0/1 corresponds to outcome +/- of eq_3
- qubit 2 (p[1]): probe for step 2, expected input |0>
- qubit 3 (p[2]): probe for step 3, expected input |0>
- total qubits = 1 + num_steps (example: 4); maximum allowed num_steps = 11 (12 qubits)

## Assumptions

- exp(-i eps Z (x) Y) is realised exactly as (I (x) S H) RZZ(2 eps) (I (x) H S^dag) using Qiskit's RZZ(t) = exp(-i t/2 Z(x)Z), S X S^dag = Y and H Z H = X.
- The runner prepares all probe qubits in |0> and the system in an arbitrary state; with readout_hadamard=true a Z-basis readout of probe k equals the X-basis outcome of eq_3 ('+' -> 0, '-' -> 1).
- The weak-coupling angle is restricted to 0 < epsilon < pi/4 so that both K_+ and K_- are proper weak measurements with two distinct singular values.
- All steps commute (diagonal target), so the order of steps and the number of steps beyond the stopping time do not change the system's Kraus operator form up to the extra factors; no inter-step unitary pulses are included.

## Unresolved issues

- The stopping-time feedback of eq_5 and the resulting approximation to the target measurement eq_1 cannot be expressed in a static unitary; verifying the O(epsilon) convergence requires the runner to simulate probe readouts and apply the classical rule.
- The paper's actual Hamiltonian, probe preparation/readout basis and feedback law are unknown; the Z (x) Y choice is an assumption from the math stage.
- Interpretation subtlety: when truncating at a classical stopping time k < num_steps the runner must treat probes k+1..n as traced out / unread; since all K_+/- commute and sum to identity in the completeness sense, tracing them out leaves the system's conditional dynamics for the first k steps unchanged.

## Equation mapping

- `eq_1`: background; no code location. The diagonal target measurement M_0, M_1 and angle theta only enter the classical stopping thresholds; they do not appear in the unitary operation and are not parameters of build_circuit.
- `eq_2`: implemented; _weak_interaction (U = exp(-i H dt) with H dt = eps Z_S (x) Y_P); the probe readout basis change is the qc.h(p) in build_circuit. One iteration's system-probe unitary is built from sdg, h, rzz(2*eps), h, s on the probe/system pair; the projective probe readout itself is left to the runner (deferred measurement).
- `eq_3`: implemented; _weak_interaction docstring and the readout Hadamard in build_circuit loop. The specific choice H = g Z (x) Y with X-basis readout is realised: U|0>_P = cos(eps) I|0> + sin(eps) Z|1>, and the trailing Hadamard maps |+/-> to |0/1> so the induced Kraus operators are K_+/- of eq_3.
- `eq_4`: implemented; build_circuit for-loop over range(n) with one fresh probe per step. The product K_{m_n}...K_{m_1} after n steps is realised coherently by applying the step unitary sequentially to the system and n distinct probes; num_steps is fixed by the instance rather than by a stopping time.
- `eq_5`: out_of_scope; no code location. The stopping-time feedback rule requires mid-circuit probe measurement, classical counters and a data-dependent circuit length (dynamic circuit), all excluded from this measurement-free unitary operation; it belongs to the runner's classical post-processing.
- `eq_6`: background; no code location. The two-singular-value characterization is a structural theorem about the achievable class; the implemented diagonal weak steps trivially lie within it but the theorem itself is not an executable construction.

## Specification changes

- eq_2, eq_3: Probe measurement and probe reset per iteration are removed; instead each iteration uses its own fresh probe qubit prepared in |0> by the runner and the X-basis readout is replaced by its unitary part (Hadamard) so that a later computational-basis readout reproduces the outcome. Reason: The returned object must be a measurement-free, reset-free unitary; the deferred-measurement principle makes this equivalent for the statistics of the n probe outcomes and the conditional system state.
- eq_4, eq_5: The random stopping time T is replaced by a fixed, instance-specified number of steps num_steps (1..11); the two-threshold feedback and outcome declaration are not implemented. Reason: Classical feedback and data-dependent circuit length are outside the scope of a static unitary circuit; the runner can evaluate the stopping rule on the probe readouts classically (stopping at step k means ignoring probes k+1..n, which commute with and do not affect the system's Kraus operator up to the later-discarded steps only if the runner post-selects/truncates appropriately).
- eq_2: Qubit ordering: the specification placed the system S as the first (most significant) tensor factor; the circuit places S at Qiskit index 0 (least significant) and probes at indices 1..n. Reason: Explicit, simple physical layout under Qiskit's little-endian convention; disclosed so that state vectors are interpreted correctly.
- eq_1: theta (target strength) and the explicit instance value pi/8 are not circuit parameters. Reason: They only affect the classical stopping thresholds, which are out of scope.
