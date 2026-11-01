# Equation to Qiskit

Trotterized CTQW search operator exp(-iHt), H = -gamma*A - epsilon|w><w|, on the smallest periodic honeycomb lattice (2x2 unit cells, 8 sites). With simple-graph periodic wrapping this lattice is the cube graph Q3, so A = X0+X1+X2 on 3 qubits. The hopping layers are exact RX rotations and the marking layer is a phase on |w>. A second-order Strang splitting is used with a user-set number of steps. The circuit contains no state preparation or measurement.

Source equation run: `7e9d2bc4-03bc-4e92-9033-c537dd93013f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: site-index bit 0 (LSB) = cell coordinate x
- qubit 1: site-index bit 1 = cell coordinate y
- qubit 2: site-index bit 2 = sublattice-dependent bit (A(x,y) -> (x,y,x^y); B(u,v) -> (u,v,1^u^v))
- site index s = q0 + 2*q1 + 4*q2 in computational basis, N = 8 sites, marked_site w is this index

## Assumptions

- hbar = 1 and the Hamiltonian is time-independent
- gamma > 0, epsilon is real and given directly (no Dirac-point tuning)
- 8 sites with periodic boundaries; the doubled edges of the 2x2 torus are treated as single edges
- Single marked site w in 0..7
- Computational-basis site encoding with qubit 0 as LSB

## Unresolved issues

- The paper's modified marking scheme and the optimal gamma and epsilon are unknown.
- The 8-site lattice is too small to show Dirac-point scaling, so the Trotter error and the physical relevance of the instance are unverified.
- The amplitude-transfer protocol and multiple marked sites are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: the loop over Trotter steps builds exp(-iHt) as a product of r Strang-split steps. Time evolution is approximated by second-order Trotterization; the hopping part is exact per layer, only the splitting between hopping and marking is approximate.
- `eq_2`: implemented; build_circuit: the rx(-gamma*dt) layers on qubits 0..2. For the 2x2 periodic honeycomb lattice A = X0+X1+X2, so exp(+i gamma dt/2 A) is a product of RX(-gamma*dt) gates.
- `eq_3`: implemented; build_circuit: the X-conjugated mcp(eps*dt, [0,1], 2) block. The marking term -eps|w><w| gives the phase exp(+i eps dt) on basis state |w>, implemented with X gates and a multi-controlled phase gate. This is the generic on-site marking, not the paper's modified marking.
- `eq_4`: out_of_scope; no code location. Initial state preparation is done by the runner; the circuit is an operation only.
- `eq_5`: out_of_scope; no code location. The success probability is a measurement or post-processing quantity; the circuit contains no measurement.

## Specification changes

- eq_2: Fixed the lattice to the 2x2 periodic honeycomb with simple-graph wrapping. This collapses the doubled edges and gives the cube graph Q3, so A = X0+X1+X2 with an explicit site relabeling. Reason: This gives an exact, compact gate decomposition with standard gates and no dense unitary. The spec left the lattice size and boundary conditions open (8 sites assumed). With 8 sites the Dirac-point physics is not meaningfully resolved.
- eq_1, eq_3: exp(-iHt) is implemented approximately by Strang-split Trotterization with a user-chosen number of steps (1..500), not exactly. Reason: The hopping and marking terms do not commute and no opaque dense unitary or operator construction is allowed.
- eq_3: The marking is the generic on-site potential -epsilon|w><w|. The paper's modified marking, the Dirac-point tuning, multi-site marking and the transfer protocol are not implemented. Reason: They are not specified in the abstract.
- eq_4, eq_5: The state preparation and success probability are excluded from the circuit. Reason: The task requires an operation with no input preparation or measurement.
