# Equation to Qiskit

Builds the unitary product U_{w_T}...U_{w_1} for a coined Hadamard walk on a 4-cycle, with one classical edge mask per step compiled into gates. Each step applies H on the coin, then the reflecting shift S_w as a basis-state permutation built from CX and multi-controlled X gates. This is a single mask-sequence trajectory, not the ensemble channel. Input-state preparation is left to the runner.

Source equation run: `ac8f08de-82d6-4e5c-9d80-6e7a457cc1a6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pos bit 0 (least significant bit of x)
- qubit 1: pos bit 1 (x = q0 + 2*q1)
- qubit 2: coin (0=L, 1=R)
- basis index = x + 4*coin; edge e joins sites e and e+1 mod 4; input state is prepared by the runner

## Assumptions

- The 4-cycle, Hadamard coin and reflecting closed-edge rule are choices of the reconstruction, as stated in the specification.
- Mask entries are 0/1 or booleans, with 1 meaning the edge is open.
- The 3-qubit permutation is decomposed into basis-state transpositions using CX conjugation and multi-controlled X gates.

## Unresolved issues

- The paper's actual shift and coin definitions for chains are unknown.
- The paper's asymptotic formulas and numerical example are not reproduced.
- The 2D Grover-coin lattice results are out of scope.

## Equation mapping

- `eq_1`: implemented; _perm (permutation for S_w) and _swap_states; coin H applied in build_circuit. Step unitary U_w = S_w (I x H) with reflection at closed edges. The shift permutation is compiled into transpositions of basis states, each built from CX and multi-controlled X gates.
- `eq_2`: implemented; build_circuit loop over masks. The ordered product of step unitaries for the supplied mask sequence. Initial-state preparation |x=0>|+> is excluded because the runner prepares inputs.
- `eq_3`: out_of_scope; no code location. The mask-averaged random unitary channel is not a unitary circuit. Only individual trajectories are built, and averaging over masks is classical.
- `eq_4`: background; no code location. Peripheral-spectrum asymptotics of random unitary channels, recalled background computed classically. It is not implemented in the circuit.
- `eq_5`: out_of_scope; no code location. Position distributions and Monte Carlo averaging are measurement and post-processing, which the circuit module excludes.

## Specification changes

- eq_2: The coin Hadamard state preparation of |+> is omitted from the circuit. The circuit implements only the unitary product U_{w_T}...U_{w_1}. Reason: build_circuit must return an operation with no input preparation. The runner supplies |x=0>|+>.
- eq_1, eq_2: Mask sequences are passed as instance parameter 'masks' (T = length, 1..32). The mask for each step is fixed classically rather than random. Reason: The circuit must be a bound unitary, so it realizes one trajectory.
- eq_3, eq_4, eq_5: Scope narrowed to a single trajectory. The ensemble channel, attractor analysis and averaging are not part of the circuit. Reason: The random unitary channel is non-unitary and cannot be built as a unitary circuit.
