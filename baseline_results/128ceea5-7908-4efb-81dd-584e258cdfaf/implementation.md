# Equation to Qiskit

Qiskit module implementing the first-order Trotterized, fast-signal-assisted linear-interpolation adiabatic evolution for an EC3 instance: U = prod_{k=M..1} exp(-i f(t_k) V dt) exp(-i s_k dt H_P) exp(-i (1-s_k) dt H_B), with the transverse-field H_B (eq_2), the EC3 quadratic clause-penalty Hamiltonian H_P expanded exactly into Z/ZZ rotations (eq_3), and a placeholder fast signal f(t_k) (regular alternating, seeded random telegraph, custom, or none) coupled to a global single-qubit Pauli V (eq_4). No state preparation or measurement is included; the runner prepares |+>^n.

Source equation run: `b9c0518c-46a2-4945-b467-9fa1610dcec8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register q, n=3 qubits total (example); qubit index i-1 holds EC3 bit x_i with |0> <-> x_i=0, |1> <-> x_i=1 (Z_i|x_i> = (-1)^{x_i}|x_i>).
- q[0] = x_1, q[1] = x_2, q[2] = x_3 for the example single-clause instance (1,2,3).
- Qiskit bitstrings print qubit 0 rightmost, so a measured string reads x_3 x_2 x_1; the specification's x_1 x_2 x_3 convention is reversed.
- Expected input state (prepared by the runner, not by this module): |+>^{\otimes n}, the ground state of H_B.
- Solutions of the example instance in the spec's x_1x_2x_3 order: 100, 010, 001 (Qiskit order: 001, 010, 100 respectively).

## Assumptions

- Closed-system unitary dynamics only; the system-bath decoherence discussed in the abstract is not modeled.
- Deterministic first-order Trotter formula stands in for the paper's randomized Trotter formula, whose randomization rule is unknown.
- Clause indices are 1-based in the instance JSON, following the specification's x_1..x_n notation; clauses are triples of distinct indices and at least one clause is required.
- Total qubits are capped at MAX_QUBITS = 12 and Trotter steps at MAX_STEPS = 2000; all parameters are validated before the register is allocated.
- The random signal uses numpy.random.default_rng(seed) with an integer seed from the instance so the circuit is reproducible and fully bound.
- Expected input state is |+>^n (ground state of H_B); the returned circuit is the evolution operator only.

## Unresolved issues

- The paper's actual fast-signal sequence, its coupling operator, and the randomized Trotter formula are not recoverable from the abstract; the implemented signal is a placeholder.
- The claimed runtime reduction and coherence protection cannot be assessed with this closed-system construction.
- Trapped-ion native-gate compilation of H_B, H_P, and the signals is out of scope.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop computing s_k = k/m and the step angles (1-s_k)*dt for H_B and s_k*dt for H_P (comment 'eq_5 / eq_1'). Linear interpolation H(s)=(1-s)H_B+sH_P is realized by weighting the H_B and H_P exponentials with (1-s_k) and s_k at each Trotter step, s_k = t_k/T = k/M.
- `eq_2`: implemented; _apply_hb (docstring 'eq_2'). exp(-i theta H_B) with H_B = sum_i (1-X_i)/2 implemented exactly as RX(-theta) on each qubit plus tracked global phase -theta*n/2. The ground-state preparation |+>^n part of eq_2 is intentionally not included because the runner prepares inputs.
- `eq_3`: implemented; _ising_coefficients and _apply_hp (docstrings 'eq_3'). Each clause penalty (x_a+x_b+x_c-1)^2 is expanded exactly to 1 - (Z_a+Z_b+Z_c)/2 + (Z_aZ_b+Z_aZ_c+Z_bZ_c)/2; coefficients are accumulated over clauses and exp(-i theta H_P) is applied exactly via RZ/RZZ rotations and a global phase.
- `eq_4`: implemented; _signal_values and _apply_signal (docstrings 'eq_4'). The additive fast-signal term f(t)V is implemented as exp(-i f(t_k) dt V) with V = sum_i P_i (P in {X,Y,Z}) and f(t_k) a placeholder regular alternating, seeded random telegraph, user-supplied, or zero sequence; this is the generic stand-in from the specification, not the paper's actual signal.
- `eq_5`: implemented; build_circuit main loop (comment 'eq_5 / eq_1') and module docstring. Time-ordered first-order product over k=1..M: per step exp(-i(1-s_k)dt H_B), exp(-i s_k dt H_P), then exp(-i f(t_k) dt V); k=M is appended last. The H(s_k) exponential is itself split into its H_B and H_P parts (additional first-order Trotter approximation).
- `eq_6`: implemented; example_instance_json (n=3, clauses=[[1,2,3]]) processed by _parse_clauses/_ising_coefficients. The single-clause 3-qubit EC3 instance is the example instance; its H_P diagonal (E=1,0,0,0,1,1,1,4 pattern) follows from the exact Z/ZZ expansion in _ising_coefficients.
- `eq_7`: out_of_scope; no code location. Success probability requires final measurement and classical post-processing, which are excluded from the returned operation; the runner may evaluate it on the output state.

## Specification changes

- eq_5: Within each Trotter step the exponential exp(-i H(s_k) dt) is further split as exp(-i s_k dt H_P) exp(-i (1-s_k) dt H_B) (H_B part applied first), so the circuit uses a first-order splitting of H_B and H_P rather than exponentiating the full H(s_k) directly. Reason: H_B and H_P do not commute; exponentiating their sum exactly would require an opaque dense unitary, which is disallowed. Each factor is implemented exactly with standard rotation gates, introducing an additional O(dt^2) error per step.
- eq_4: The unspecified fast signal f(t)V is concretized as V = sum_i P_i (P chosen among X, Y, Z; default X) and f(t_k) in {A(-1)^k (regular), A r_k with r_k uniform in {-1,+1} from a seeded NumPy generator (random), user-supplied values (custom), or zero (none)}, sampled once per Trotter step. Reason: The abstract gives neither the signal statistics nor the coupling operator; these are explicit placeholder choices needed to produce a concrete circuit, and are disclosed as not being the paper's construction.
- eq_2: Preparation of the initial state |+>^n is not performed by the module; only the H_B exponential is implemented. Reason: The task requires an operation without input-state preparation; the runner prepares inputs.
- eq_6: Bit-to-qubit mapping is x_i -> qubit i-1; Qiskit's little-endian bitstring printing therefore shows x_n...x_1, the reverse of the specification's x_1x_2x_3 notation. Reason: Resolution of the specification's left-to-right ordering with Qiskit's qubit-0-least-significant convention.
- eq_1, eq_5: The schedule is sampled at the end of each step, s_k = k/M (so the first step uses s_1 = 1/M rather than s=0 and the last uses s_M = 1). Reason: Direct transcription of the specification's t_k = k dt; a midpoint rule would be an alternative not chosen here.
- eq_2, eq_3: Identity (constant) terms of H_B and H_P are tracked as a global phase on the circuit rather than dropped. Reason: Preserves the exact unitary of the specified Hamiltonians, including relative phases between signal-free and signal steps in principle; harmless for measurement statistics.
