# Equation to Qiskit

Builds T steps of a disordered 2D split-step discrete-time quantum walk on a periodic 2^n x 2^n lattice (default 4x4, 2n+2 qubits). Each step applies a seeded site-dependent Ry coin on each axis coin qubit, a coin-controlled x shift, a unitary reflection on the cut horizontal links of one row (an optional cut), and a coin-controlled y shift. The cut and uncut circuits share the same disorder angles for the same seed. Input preparation and measurement are left to the runner.

Source equation run: `1a4663bb-c9d6-4466-bf78-9126945c606e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: x position, little-endian (qubit 0 = LSB)
- qubits n..2n-1: y position, little-endian
- qubit 2n: coin c_x (0 means +1 hop, 1 means -1 hop)
- qubit 2n+1: coin c_y (0 means +1 hop, 1 means -1 hop)
- default n_bits=2: x=q0,q1; y=q2,q3; c_x=q4; c_y=q5; A=(0,0), B=(2,0)
- site index for the disorder table is x + 2^n * y

## Assumptions

- Disorder is a fixed seeded uniform [0,2pi) angle per site and per coin axis, identical for cut and uncut circuits with the same seed
- The initial state (walker at A, coin 00) is prepared by the runner
- Cut links are horizontal links on a single row and do not include periodic wrap-around links
- exp(-i theta Y) is implemented as Ry(2*theta)
- Coin qubit value 0 means +1 hop and 1 means -1 hop

## Unresolved issues

- The paper's exact coin and shift definitions and split-step ordering are unknown, so this is a plausible concrete model rather than a verified reproduction
- The disorder distribution and cut-reflection rule are assumptions
- The Hamiltonian realization, quasienergy winding number and Chern number are not implemented
- A 4x4 lattice is far too small to demonstrate edge-state transport or scaling

## Equation mapping

- `eq_1`: implemented; _coin. Per-site, per-axis multiplexed Ry(2*theta) (= exp(-i theta Y)) on each coin qubit. Each is controlled on the position register through ctrl_state=site index. Angles are uniform in [0,2pi) from numpy default_rng(seed).
- `eq_2`: implemented; _shift (with _inc). Coin-controlled modular increment (coin 0) or decrement (coin 1) built from cascaded multi-controlled X gates. It is applied per axis in sequence (split-step) rather than as a simultaneous diagonal hop.
- `eq_3`: implemented; _reflect (with _swap_states), called in build_circuit when cut is true. Unitary reflecting links on the chosen row between x=cut_x_start and x=cut_x_end. After the x shift, the basis states |x+1,c_x=0> and |x,c_x=1> are swapped for each cut link. This is equivalent to flipping the coin and skipping the hop (reflection).
- `eq_4`: background; no code location. U^T applied to |A>|c0> is realised by the T-step loop in build_circuit. The initial state |0,0>|00> is prepared by the runner, so no state preparation appears in the circuit.
- `eq_5`: out_of_scope; no code location. The arrival-probability readout is a measurement or statevector post-processing step. The circuit is measurement-free.

## Specification changes

- eq_2, eq_3: Replaced the simultaneous diagonal shift S with a split-step shift: an x shift (with reflection on cut links) followed by a y shift. The step is U = S_y S_x' C. Reason: With a simultaneous x and y hop, a horizontal link cut cannot be applied unambiguously, because the walker would also move in y. The split-step ordering is listed as missing information in the specification.
- eq_3: The reflection R is implemented as a post-shift transposition of basis states |x+1,c_x=0> and |x,c_x=1>, instead of a pre-shift coin flip followed by a shift S' restricted to non-reflected components. Reason: This gives the same permutation (reflected walker stays at its site with flipped coin) and is manifestly unitary and bijective.
- eq_1, eq_2, eq_3, eq_4: Generalised the lattice to a parameterised 2^n x 2^n lattice with n_bits in {2,3}, steps 1..32, an optional cut, and a configurable cut row and x-range. The default is the 4x4 instance. Link (x,x+1) is cut for x in [cut_x_start, cut_x_end-1], with no wrap-around links. Reason: Satisfies the requirement to accept varying valid instance parameters while staying within the 12-qubit cap and the gate-count budget.
