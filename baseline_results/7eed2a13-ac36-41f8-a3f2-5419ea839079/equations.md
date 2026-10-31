# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct a minimal mathematical specification of a disordered two-dimensional discrete-time quantum walk (DTQW) on a regular lattice in which some links are cut along a single line joining a source site A to a target site B, so that the A-to-B transport probability after t steps can be defined and later simulated as a circuit.

Scope: One split-step-type 2D coined DTQW on an L x L periodic square lattice with a single coin qubit, site-dependent (disordered) coin angles, and a set of cut links along a straight line from A to B implemented as reflecting boundaries; tiny instance L=4 (2+2 position qubits, 1 coin qubit), walker initialized at A, evolved for a fixed number of steps t, and measured in the position basis to estimate the arrival probability at B. Outside scope: the paper's specific walk protocol, its disorder model, the periodically driven lattice Hamiltonian realization, the computation of the bulk Chern number, and the quasienergy winding invariant (only the generic Floquet relation is recorded).

## Symbols

- $L$: linear size of the square lattice (sites per direction); periodic boundary conditions assumed; domain: positive integer, power of two for qubit encoding; instance L=4
- $(x,y)$: lattice site coordinates; domain: x,y \in \{0,\dots,L-1\}, arithmetic mod L
- $c$: internal coin state of the walker; domain: c \in \{0,1\}
- $\theta_1(x,y),\theta_2(x,y)$: site-dependent coin rotation angles carrying the disorder; domain: real, drawn from [\bar\theta_j - W, \bar\theta_j + W]
- $W$: disorder strength (half-width of coin-angle distribution); domain: real, W \ge 0
- $\Lambda$: set of cut links (unordered pairs of nearest-neighbour sites whose connecting link is removed); domain: subset of lattice edges
- $A, B$: fixed source and target sites; domain: A,B \in \{0,\dots,L-1\}^2
- $t$: number of walk steps; domain: non-negative integer
- $U$: one-step DTQW unitary (Floquet operator); domain: unitary on \mathbb{C}^{L^2}\otimes\mathbb{C}^2
- $H_F$: effective (Floquet) Hamiltonian whose quasienergies are the phases of U; domain: Hermitian operator, quasienergies defined mod 2\pi/T
- $T$: driving period of the lattice Hamiltonian realization; domain: real, T>0
- $P_B(t)$: probability of finding the walker at target B after t steps; domain: [0,1]

## eq_1: Split-step 2D DTQW unitary

$$
U = S_y\, C(\theta_2)\, S_x\, C(\theta_1)
$$

One time step: a disordered coin rotation, a coin-conditioned shift along x, a second coin rotation, and a coin-conditioned shift along y. Chosen as the minimal 2D coined walk; the paper's actual protocol is not given in the abstract.

Provenance: `assumption`. The abstract specifies a 2D discrete-time quantum walk but not its coin/shift structure; a split-step walk is the smallest standard 2D construction supporting topological edge states.

Equation assumptions:

- Single two-level coin
- Two shift substeps per period
- Operator ordering right-to-left as written

## eq_2: Site-dependent (disordered) coin rotation

$$
C(\theta_j) = \sum_{x,y} |x,y\rangle\langle x,y| \otimes e^{-i\theta_j(x,y)\sigma_y},\qquad \theta_j(x,y) = \bar\theta_j + \delta\theta_j(x,y),\ \delta\theta_j(x,y)\sim \mathrm{Unif}[-W,W]
$$

Coin rotation about sigma_y whose angle fluctuates independently from site to site; W=0 recovers the translation-invariant walk.

Provenance: `assumption`. The abstract states the walk is disordered but not how; coin-angle disorder is a common choice that preserves unitarity and lattice structure.

Equation assumptions:

- Uniform independent disorder in coin angles
- No disorder in the shift operators

## eq_3: Coin-conditioned shift with cut links as reflections

$$
S_x|x,y,c\rangle = \begin{cases} |x+(-1)^{c}\bmod L,\ y,\ c\rangle & \{(x,y),(x+(-1)^c,y)\}\notin\Lambda \\ |x,y,1-c\rangle & \{(x,y),(x+(-1)^c,y)\}\in\Lambda \end{cases}
$$

Coin value 0 moves +1, coin value 1 moves -1 along x (modulo L); if the required link is cut the walker stays put and its coin is flipped, which keeps S_x unitary. S_y is defined identically with the roles of x and y exchanged.

Provenance: `assumption`. The abstract says links are cut but not how the walk is modified at a cut; replacing the hop by a reflection (stay + coin flip) is the standard unitary way to remove a link.

Equation assumptions:

- Cut links act as perfectly reflecting boundaries
- Periodic boundary conditions on the uncut lattice

## eq_4: Cut line joining A to B (instance)

$$
L=4,\ A=(0,1),\ B=(3,1),\ \Lambda=\{\{(x,1),(x,2)\}: x=0,1,2,3\}\setminus\{\{(3,1),(3,2)\}\}
$$

Tiny explicit instance: horizontal cut along the row of A and B, removing the vertical links between rows y=1 and y=2 for x=0,1,2 so the cut is a single open line from A towards B.

Provenance: `assumption`. The abstract describes cutting links along a single line connecting A to B; this is one smallest concrete realization chosen for a 5-qubit instance.

Equation assumptions:

- Specific geometry of the cut is a modeling choice
- The cut does not wrap fully around the torus

## eq_5: A-to-B transport probability

$$
P_B(t) = \sum_{c\in\{0,1\}} \left|\langle B, c|\, U^t\, |A, c_0\rangle\right|^2
$$

Exact arrival probability at B after t steps for a walker initialized at A with coin c_0; the transport-channel efficiency is quantified through P_B(t) (e.g. its maximum over t or its time average).

Provenance: `abstract_inferred`. An efficient transport channel from A to B is naturally quantified by the site-B occupation probability of the time-evolved walker; the precise efficiency figure of merit used in the paper is not stated.

Abstract evidence: We ask how to create an efficient transport channel from a fixed source site (A) to fixed target site (B)

Equation assumptions:

- Initial state is fully localized at A
- Efficiency metric derived from P_B(t) is a reconstruction choice

## eq_6: Floquet (periodically driven) realization

$$
U = \mathcal{T}\exp\!\left(-i\int_0^T H(\tau)\,d\tau\right) = e^{-iH_F T},\qquad U|\psi_n\rangle = e^{-i\varepsilon_n T}|\psi_n\rangle,\ \varepsilon_n \in [-\pi/T,\pi/T)
$$

The one-step walk unitary is identified with the stroboscopic evolution of a periodically driven lattice Hamiltonian; quasienergies are defined modulo 2\pi/T. The specific H(\tau) and the winding invariant built from it are not reconstructed here.

Provenance: `abstract_inferred`. Any DTQW step unitary can be written as a time-ordered exponential of a piecewise-constant driving Hamiltonian; the abstract asserts such a realization exists and that its quasienergy winding is the relevant invariant, but gives neither H(\tau) nor the invariant's formula.

Abstract evidence: We give a realization of the walk as a periodically driven lattice Hamiltonian, and identify the bulk topological invariant responsible for the edge states as the quasienergy winding of this Hamiltonian.

Equation assumptions:

- Standard Floquet definitions
- Explicit driving protocol and invariant left unspecified

## Registers

- x: log2(L) qubits (2 for L=4) qubits; x-coordinate of the walker, integer x = sum_k x_k 2^k with qubit k holding bit k (little-endian)
- y: log2(L) qubits (2 for L=4) qubits; y-coordinate of the walker, same little-endian encoding
- coin: 1 qubits; internal coin state c controlling the direction of each shift

## Initial state

|\psi_0\rangle = |x_A\rangle|y_A\rangle|c_0\rangle with A=(0,1), c_0=0, i.e. the computational basis state |00\rangle|10\rangle|0\rangle in the ordering (x register, y register, coin); overall state space ordered as |x\rangle\otimes|y\rangle\otimes|c\rangle.

## Measurement

Measure the x and y position registers in the computational basis (coin traced out); record the frequency of outcome (x,y) = B.

## Classical postprocessing

Estimate P_B(t) from the empirical frequency of outcome B; optionally repeat for several t and several disorder realizations, averaging to obtain a disorder-averaged transport efficiency, and compare the cut-line lattice (\Lambda as in eq_4) against the uncut lattice (\Lambda = \emptyset).

## Algorithm steps

1. Fix L, the cut set \Lambda, the disorder realization \theta_1(x,y),\theta_2(x,y) and the step count t; prepare the walker localized at A. (eq_2, eq_4)
2. Apply the site-dependent coin rotation C(\theta_1) (coin rotation controlled on the position registers). (eq_2)
3. Apply the coin-conditioned shift S_x along x, with reflections (stay + coin flip) on links in \Lambda. (eq_3, eq_4)
4. Apply the second coin rotation C(\theta_2) and the shift S_y along y, completing one step U. (eq_1, eq_2, eq_3)
5. Repeat the step unitary U a total of t times to obtain U^t|\psi_0\rangle. (eq_1, eq_6)

## Assumptions

- No experiment scope was supplied; a single smallest construction (split-step 2D coined DTQW on a 4x4 periodic lattice, 5 qubits) was chosen as the reconstruction target.
- The walk protocol (eq_1), disorder model (eq_2), cut implementation as reflection (eq_3) and cut geometry (eq_4) are modeling assumptions, not statements from the abstract.
- Transport efficiency is quantified via the arrival probability at B (eq_5); the paper's exact figure of merit is unknown.
- The topological statements (chiral edge states, vanishing bulk Chern number, quasienergy winding) are recorded as claims only; no invariant is computed or defined here beyond the generic Floquet relation (eq_6).

## Missing information

- The specific 2D DTQW protocol used in the paper (number of substeps, coin operators, shift directions).
- The disorder model (which parameters are random, their distribution and strength).
- How a cut link modifies the walk dynamics (reflection, phase, or other unitary completion).
- The exact definition of transport efficiency and the number of time steps considered.
- The explicit periodically driven lattice Hamiltonian H(\tau) realizing the walk.
- The formula for the quasienergy winding invariant and the argument linking it to chiral edge states along the cut.
- Any numerical results or system sizes used in the paper.
