# Equation to Qiskit

Builds one unitary realization of a percolated coined quantum walk on an open chain of N=2^n_pos sites with a Hadamard coin. The circuit is the product U_{w_T}...U_{w_1} for a caller-supplied sequence of per-step edge configurations. The random-unitary channel average is not a single unitary circuit, so it is out of scope.

Source equation run: `28a59cb7-ab92-43ab-95bf-4d4e2ea375a4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n_pos-1: position register x in {0..2^n_pos-1}, qubit 0 least significant
- qubit n_pos: coin qubit (|0> = move right, |1> = move left)
- example: n_pos=2 gives 4 sites, 3 edges, qubits 0,1 = position, qubit 2 = coin; basis index = x + 4*c

## Assumptions

- Initial states are prepared by the runner; the circuit contains no state preparation.
- Edge x connects sites x and x+1. A 1 entry means the edge is present.
- Chain ends are always blocked and reflect.
- Qubit 0 is the least significant position bit and the coin is the most significant qubit.
- Steps are applied in list order, so the circuit is U_{w_T}...U_{w_1}.

## Unresolved issues

- The paper's actual coin operators, boundary conditions and percolation correlations are unknown and not reconstructed.
- Averaging over random configurations, which gives the open-system channel, is not realized in a single circuit.
- The 2D Grover-coin case is not implemented.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The channel average over configurations is not a unitary circuit. Only individual realizations U_w composed along a given sequence of configurations are built.
- `eq_2`: out_of_scope; no code location. Sampling configurations with independent-edge probabilities is classical and is left to the caller, who supplies the edge_configs.
- `eq_3`: implemented; build_circuit (per-step loop: H on coin, then ring-increment shift with _swap_states reflections for absent edges). U_w = S_w (I_pos (x) C) with a Hadamard coin and reflecting shift at missing edges and chain ends.
- `eq_4`: background; no code location. Asymptotic analysis of random unitary maps is classical post-processing and is not part of the circuit.
- `eq_5`: background; no code location. The peripheral eigen-equation is a standard property used in the analysis and is not implemented as an operation.

## Specification changes

- eq_1, eq_2: The random-unitary channel average is replaced by a deterministic product of unitaries for an explicit, caller-supplied sequence of edge configurations. Reason: A measurement-free unitary circuit cannot represent a mixed-state channel without an environment register prepared by the circuit. Input-state preparation is not allowed.
- eq_3: Number of sites restricted to N=2^n_pos, an open chain, a fixed Hadamard coin, and the explicit reflection rule: coin 0 moves right, coin 1 moves left, and a blocked move keeps the position and flips the coin. The shift is built from a ring-increment on y=(coin, x or ~x) followed by transpositions for absent edges. Reason: The spec left the blocked-edge rule and the boundary open. This choice gives a bijective, unitary shift for every configuration and an efficient gate decomposition. The instance is reduced to a power-of-two chain.
- eq_4, eq_5: Treated as background only. Reason: They describe asymptotic spectral properties and not a circuit operation.
