# Equation to Qiskit

Builds a first- or second-order Trotterized continuous-time quantum walk e^{-iHt} with H = -gamma*A - epsilon*|w><w| on a periodic honeycomb (graphene) lattice with 2*2^nx*2^ny sites. Sites are binary-encoded as one sublattice qubit plus x and y cell-coordinate registers. The three hopping directions are applied through QFT-diagonalised shift operators with controlled-phase conjugation and an RX rotation on the sublattice qubit. The marking term is a multi-controlled phase. The circuit has no state preparation or measurement.

Source equation run: `599ee0c7-a829-4778-86ff-e11e57dc39fa`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0: sublattice bit s (0 = A, 1 = B)
- q1..q_nx: x unit-cell coordinate, q1 least significant
- q_{nx+1}..q_{nx+ny}: y unit-cell coordinate, least significant first
- Example (nx=2, ny=2, 5 qubits): q0=s, q1,q2=x, q3,q4=y; site index = s + 2*x + 8*y in little-endian basis order
- Lattice: A(x,y) is adjacent to B(x,y), B(x-1,y) and B(x,y-1), with periodic boundaries in x and y

## Assumptions

- Basis index = s + 2*x + 2^(1+nx)*y with qubit 0 least significant
- Hopping amplitude is gamma on every edge (H = -gamma*A)
- QFTGate(n) on the coordinate register has |j> -> sum_k exp(2 pi i j k/2^n)|k>, so S|j>=|j+1> equals QFT^dag diag(exp(2 pi i k/L)) QFT
- Periodic boundaries and 1+nx+ny <= 12 qubits

## Unresolved issues

- The paper's actual modified marking scheme and any Dirac-point-tuned epsilon, gamma, and time are unknown
- Optimal evolution time and success-probability scaling are not given
- The state-transfer variant between two sites is not implemented as a separate protocol
- Trotter error is uncontrolled and depends on trotter_steps and order
- Small tori (nx or ny = 1) give a degenerate geometry in which the x-1 and x+1 neighbors coincide

## Equation mapping

- `eq_1`: implemented; _onsite, _shift_hop (the -gamma*A hopping terms) and _mark (the -epsilon|w><w| term) in build_circuit. Adjacency A is split into three commuting-within-term bond classes. The intra-cell term is implemented as RX on the sublattice qubit. The two shift terms are implemented through a QFT-diagonalised shift with cp conjugation. On-site marking is a multi-controlled phase on |w>.
- `eq_2`: implemented; build_circuit Trotter loop (first- or second-order product formula). e^{-iHt} is approximated by the product of exact term exponentials over trotter_steps steps of size t/steps. The result is an approximation to the unitary, not an exact one, because the terms do not commute.
- `eq_3`: out_of_scope; no code location. Success probability is a measurement and analysis quantity. The circuit is measurement-free, so p_w(t) is evaluated outside it.

## Specification changes

- eq_1: Fixed a concrete geometry: a periodic honeycomb lattice on an L_x by L_y torus of unit cells, with L_x and L_y powers of two, two sites per cell, and the specific adjacency A(x,y)~B(x,y), B(x-1,y), B(x,y-1). The marking is restricted to a single on-site potential. Reason: The specification gives no lattice size, boundary conditions, or marking Hamiltonian. A binary-encoded, QFT-diagonalisable shift needs power-of-two periodic dimensions.
- eq_2: Exact continuous evolution is replaced by a Trotter-Suzuki product (order 1 or 2) with a user-set number of steps. Reason: Standard gates cannot implement e^{-iHt} exactly for the sum of non-commuting terms without building a dense unitary, which is disallowed.
- eq_1, eq_2, eq_3: Narrowed to the evolution operator only. The circuit contains no initial state (uniform superposition or localized source), no measurement, no scan over t, and no tuning of gamma and epsilon to the Dirac point. The paper's modified marking and the state-transfer protocol are not implemented. Reason: Inputs are prepared by the runner and the circuit must be an operation. The abstract does not give the modified marking details.
