# Equation to Qiskit

Builds the unitary for t steps of a coin-flip-shift quantum walk on a finite 1D chain (open or periodic, N=2^n sites, 1 coin qubit). Each step uses one supplied percolation edge configuration omega, giving U_omega = S_omega (Ry(theta) on coin). The circuit is a single sampled branch of the random unitary map, not the averaged channel. Present edges swap the arcs |x,coin 0> and |x+1,coin 1> (flip-flop shift). Missing edges leave the walker unchanged. Each swap is built from CX gates and multi-controlled X gates.

Source equation run: `52027585-796b-4b93-b28f-8c96ac448ecc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin (|0> = arc pointing right, |1> = arc pointing left)
- qubits 1..n: position register, little-endian (qubit 1 is the least significant bit of site x in 0..2^n-1)
- basis index = coin + 2*x; total qubits = n+1 <= 12
- edge e_x joins site x and x+1; open chain has 2^n-1 edges, periodic ring has 2^n edges (edge 2^n-1 joins site 2^n-1 and site 0)

## Assumptions

- Chain length is N=2^n sites, so the position register is fully used.
- Coin dimension is 2. The coin is Ry(theta), and theta=pi/2 gives a real Hadamard-like coin.
- Edge configurations are supplied by the runner per step, as lists of 0/1 over edges.
- The open chain has no edge between site N-1 and site 0. The periodic option adds it and needs n>=2.
- The initial state is prepared externally.

## Unresolved issues

- The paper's actual coin operators, shift convention on missing edges, and percolation probabilities are not known.
- The averaged channel Phi and its asymptotics must be handled outside this circuit, for example by averaging over sampled configurations.
- The 2D lattice with the Grover coin is not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit (one U_omega per supplied edge configuration, with the shift built by _transpose). Implements the unitary branches U_omega of the random unitary map. The mixture sum_omega p_omega U_omega rho U_omega^dagger is not unitary, so it is not built in a single circuit. The caller chooses the omega sequence and can average externally.
- `eq_2`: background; no code location. The long-time limit of Phi^t is an analysis of the averaged channel. The circuit only gives a finite sequence of t sampled unitaries and does not compute a limit.

## Specification changes

- eq_1: Scope narrowed from the averaged channel Phi to a single sampled realization, a product of U_omega_t...U_omega_1 with edge configurations given explicitly in the instance. Reason: A circuit must be unitary and cannot contain the probabilistic mixture. The probabilities p_omega are not used.
- eq_1: Concrete choices were fixed because the abstract does not give them: a flip-flop shift (a present edge x-(x+1) swaps |x,coin 0> with |x+1,coin 1>), a missing edge leaves the walker unchanged (stay put, no coin flip), and the coin is Ry(coin_angle) applied before the shift. Reason: The abstract does not specify the shift rule on missing edges or the coin operator. These were listed as missing information, and the choices give a valid permutation-based shift.
- eq_2: No asymptotic or limit computation is included. Only a finite number of steps (at most 64) is built. Reason: The limit is a property of the averaged non-unitary channel iterated indefinitely.
