# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Continuous-time quantum walk (CTQW) spatial search on a 2D graphene (honeycomb) lattice, using the Dirac point in the spectrum, with a modified site-marking scheme. The abstract gives no explicit equations, so only the standard CTQW search framework is reconstructed.

Scope: One small instance: a CTQW search with Hamiltonian H = -gamma*A + oracle term on a tiny honeycomb lattice (periodic, e.g. 2x2 unit cells = 8 sites), with a single marked site. The paper's specific marking modification, the Dirac-point tuning of parameters, multi-marking variants and the amplitude-transfer protocol are outside the scope and not reconstructed.

## Symbols

- $N$: number of lattice sites; domain: positive integer, N=8 in the tiny instance (assumed)
- $A$: adjacency matrix of the honeycomb lattice graph; domain: N x N real symmetric 0/1 matrix
- $\gamma$: hopping rate; domain: positive real
- $w$: marked site; domain: {0,...,N-1}
- $\epsilon$: strength of the marking term on site w (the abstract's modified marking scheme is unspecified); domain: real
- $t$: evolution time; domain: nonnegative real
- $|\psi(t)\rangle$: walker state; domain: unit vector in C^N

## eq_1: Schrodinger evolution

$$
|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle
$$

Continuous-time quantum walk evolution under a time-independent Hamiltonian (hbar=1).

Provenance: `standard_background`. Standard definition of a CTQW; the abstract only mentions continuous-time quantum walk search.

Equation assumptions:

- Time-independent H
- hbar=1

## eq_2: Lattice hopping Hamiltonian

$$
H_0 = -\gamma A
$$

Walk Hamiltonian on the graphene lattice via the adjacency matrix; its spectrum has a Dirac point for the infinite lattice.

Provenance: `standard_background`. Common CTQW convention; the abstract mentions the graphene lattice and the Dirac point but gives no Hamiltonian.

Equation assumptions:

- Nearest-neighbour hopping with uniform rate
- Periodic boundary conditions in the tiny instance

## eq_3: Marked-site search Hamiltonian

$$
H = H_0 - \epsilon |w\rangle\langle w|
$$

Standard oracle-type marking by an on-site potential. The abstract says the paper changes the standard marking method, so this is only a generic placeholder.

Provenance: `assumption`. Generic Chen-style marking chosen as the simplest construction; it is not the paper's modified marking.

Equation assumptions:

- Single marked site
- Value of epsilon is not given and is to be tuned numerically

## eq_4: Initial state

$$
|\psi(0)\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle
$$

Uniform superposition over lattice sites as the starting state.

Provenance: `assumption`. Standard choice in spatial search; the paper's initial state is not stated in the abstract.

Equation assumptions:

- Uniform start rather than a Dirac-point eigenstate

## eq_5: Success probability

$$
P_w(t) = |\langle w|e^{-iHt}|\psi(0)\rangle|^2
$$

Probability of finding the walker at the marked site at time t; search succeeds if it is large at some t*.

Provenance: `standard_background`. Standard figure of merit for spatial search.

## Registers

- site: ceil(log2 N) = 3 qubits for N=8 (or N-dimensional single-particle space) qubits; walker position on lattice sites, with sites indexed by integers 0..N-1 in computational-basis encoding

## Initial state

Uniform superposition over all lattice sites (assumed).

## Measurement

Measure the site register in the computational basis at time t*; success means obtaining w.

## Classical postprocessing

Scan epsilon and t to locate the maximum of P_w(t); no other postprocessing is justified.

## Algorithm steps

1. Build the adjacency matrix A of the small periodic honeycomb lattice and set H_0 = -gamma A. (eq_2)
2. Add a marking term at site w to form H. (eq_3)
3. Prepare the uniform superposition. (eq_4)
4. Evolve under H for time t, scanning epsilon, gamma and t. (eq_1)
5. Compute P_w(t) and select the time t* that maximizes it. (eq_5)

## Assumptions

- Tiny instance: honeycomb lattice with 8 sites, periodic boundaries, one marked site
- Generic on-site marking is used in place of the paper's modified marking
- Uniform initial state

## Missing information

- Exact modified marking scheme used in the paper
- Parameter values (gamma, epsilon) tuned to the Dirac point
- Lattice size and boundary conditions
- Initial state used
- Amplitude-transfer protocol between sites
- Scaling of search time and success probability
