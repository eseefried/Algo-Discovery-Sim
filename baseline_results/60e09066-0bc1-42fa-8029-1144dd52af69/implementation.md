# Equation to Qiskit

Implements the trusted small-simulator operation of the scoped construction: the time-evolution unitary e^{-i H_S(x) t} for the truncated open-chain transverse-field Ising patch Hamiltonian H_S(x)=sum_i J_i Z_i Z_{i+1} + sum_i h_i X_i (eq_2) as a first- or second-order Trotter product of RZZ and RX gates on an n-qubit 'sim' register (2<=n<=12). State preparation |0...0>, the Z measurement on the edge site (eq_3's projector), the Lieb-Robinson time selection (eq_4), the particle-filter Bayes update (eq_5) and the Fisher-information argument (eq_6) are classical/runner-side and not part of the returned circuit.

Source equation run: `0ce8d2ac-2973-412c-bb32-a64678e3ed65`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- sim[0] (Qiskit qubit 0, least significant bit): patch site 1 = measured edge site; receives h_1 and one leg of J_1
- sim[1] (Qiskit qubit 1): patch site 2 = neighbour of the edge site; receives h_2 and the other leg of J_1
- general n: patch site i -> sim[i-1]; coupling J_i acts on (sim[i-1], sim[i]); total qubits = n <= 12
- The 4-qubit 'device' register of the specification is NOT allocated: it is the physical data source, not a simulated object

## Assumptions

- Gate conventions: RZZ(theta)=exp(-i theta Z⊗Z/2) and RX(theta)=exp(-i theta X/2), so theta = 2*coefficient*dt reproduces exp(-i coefficient * P * dt).
- Second-order (symmetric) Trotter is the default; order 1 is available via 'order': 1. Default trotter_steps is 1 if omitted.
- Any finite real t (including 0 or negative) is accepted; enforcing the Lieb-Robinson condition v t < l is left to the classical experiment-design layer.
- The example instance corresponds to the specification's scoped patch: n=2, J_1=0.5, h_1=0.3 (unknown parameters as a particle value), h_2=0.7 (known), t=1.0.
- Ideal (noiseless) simulator gates.

## Unresolved issues

- Trotter step count and order needed to make the product-formula error negligible relative to the Lieb-Robinson truncation error (eq_4) is not determined by the specification.
- The paper's actual bootstrapping schedule (which patches, which times, transfer of learned parameters) and the interactive learning variant remain unreconstructed; this module only provides the per-particle simulator unitary used in step 4 of the specification.

## Equation mapping

- `eq_1`: background; no code location. Full N-qubit device Hamiltonian; it is the physical system being characterized and is not simulated by the trusted small simulator, so it is not part of the returned operation.
- `eq_2`: implemented; _append_zz_layer, _append_x_layer (comments '[eq_2 coupling terms]' and '[eq_2 transverse-field terms]'); parameters J, h parsed in _parse_instance. The truncated patch Hamiltonian H_S(x) is realised term-by-term: exp(-i J_i Z_i Z_{i+1} dt) as RZZ(2 J_i dt) and exp(-i h_i X_i dt) as RX(2 h_i dt).
- `eq_3`: implemented; build_circuit (comment 'eq_3 (unitary part)'): Trotter loop producing exp(-i H_S(x) t). Only the unitary evolution e^{-i H_S(x) t} is built; the |00> input and the Z-measurement projector Pi_d (whose Born-rule probability gives the likelihood) are supplied by the runner, per the operation-only contract.
- `eq_4`: background; no code location. Lieb-Robinson truncation bound constrains the admissible experiment time t classically; it is not a quantum operation. The module accepts any finite t and does not enforce v t < l.
- `eq_5`: out_of_scope; no code location. Particle-filter Bayesian update is classical post-processing over many circuit runs and cannot be part of a single measurement-free unitary circuit.
- `eq_6`: background; no code location. Fisher-information scaling motivates choosing longer t; it is an analytical statement with no circuit counterpart.

## Specification changes

- eq_3: The exact propagator e^{-i H_S(x) t} is replaced by a product formula (first-order Lie-Trotter or second-order Strang splitting) with a user-chosen number of steps; the non-commuting ZZ and X layers are split accordingly. Reason: Opaque dense unitaries are disallowed; H_S(x) terms do not commute, so a gate-level decomposition requires Trotterization. Error is O(t^2/steps) (order 1) or O(t^3/steps^2) (order 2).
- eq_3, eq_5: Scope narrowed to the simulator-side unitary only: no |00> preparation, no Z measurement, no likelihood estimation, no Bayes update, and no device-side experiment. Reason: The deliverable is a measurement-free unitary operation; preparation, measurement, sampling and classical inference are performed by the runner / classical code.
- eq_2: Generalised from the fixed n=2 patch {1,2} to an open chain of n patch qubits (2<=n<=12) with arbitrary real J_1..J_{n-1} and h_1..h_n, all supplied as instance parameters (no distinction between 'unknown' and 'known' parameters inside the circuit). Reason: The circuit must work for varying valid instances; which parameters are being learned is a property of the classical inference loop, not of the simulator unitary. n=2 with (J_1,h_1,h_2) reproduces the specification exactly.
- eq_2: Qubit index mapping: specification site i (site 1 = leftmost tensor factor / measured site) is placed on Qiskit qubit i-1, i.e. the measured edge site is the least-significant qubit. Reason: Qiskit's little-endian convention differs from the leftmost-tensor-factor convention of the specification; the mapping is disclosed so the runner measures sim[0] for site 1.
