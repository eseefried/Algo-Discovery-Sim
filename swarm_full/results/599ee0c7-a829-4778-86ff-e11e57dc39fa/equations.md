# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search on a 2D graphene (honeycomb) lattice, using the Dirac point of the spectrum, with modified site-marking so that the marked site is found without extra degrees of freedom; also adapting the search to transfer amplitude between specific lattice sites.

Scope: Theoretical Hamiltonian-evolution (analog continuous-time) search on a finite graphene lattice; not a gate-circuit algorithm. Specific marking Hamiltonians and scaling results are not given in the abstract and are reconstructed only as generic background.

## Symbols

- $H$: Total search Hamiltonian; domain: Hermitian operator on lattice site space
- $\gamma$: Hopping rate of the walk on the lattice; domain: positive real
- $A$: Adjacency matrix of the graphene lattice; domain: real symmetric N x N matrix
- $w$: Marked (target) site; domain: lattice site index
- $\epsilon$: Marking strength (on-site potential); domain: real

## eq_1: Search Hamiltonian

$$
H=-\gamma A-\epsilon\,|w\rangle\langle w|
$$

Generic walk Hamiltonian on graphene lattice plus on-site marking of site w; the abstract says marking differs from standard methods, so this is a generic form only.

Provenance: `standard_background`. Standard continuous-time quantum walk search form; the paper's modified marking is not specified in the abstract.

Equation assumptions:

- Marking by on-site potential is only one of several possible marking methods

## eq_2: Time evolution

$$
|\psi(t)\rangle=e^{-iHt}|\psi(0)\rangle
$$

Unitary evolution of the walker amplitude over the lattice.

Provenance: `standard_background`. Definition of continuous-time quantum walk dynamics.

## eq_3: Success probability

$$
p_w(t)=|\langle w|\psi(t)\rangle|^2
$$

Probability of finding the walker at marked site w; for transfer, w is the receiving site with start at a specific site.

Provenance: `assumption`. Natural figure of merit for search and for state transfer between sites.

Equation assumptions:

- Initial state is delocalized for search or localized at a source site for transfer

## Registers

- lattice: N (number of lattice sites; log2 N qubits if embedded) qubits; Single-particle position register; walker occupies one site (the graphene lattice includes both sublattices)

## Initial state

Search: uniform superposition over all sites (or a state near the Dirac-point eigenstates), |s> = N^{-1/2} sum_x |x>. Transfer: localized state |v> at the source site.

## Measurement

Position-basis measurement of the lattice register after evolution time t; the outcome is the site w with probability p_w(t) (eq_3). Repeat over runs to estimate p_w.

## Classical postprocessing

Scan or choose evolution time t to maximize the estimated p_w(t); declare the most frequent outcome as the marked site (search) or check arrival at the receiver site (transfer). Repeat runs as needed for amplification.

## Algorithm steps

1. Build the graphene adjacency matrix A on a finite lattice with assumed periodic boundaries and choose the marked site w (or receiver site) with marking strength epsilon. (eq_1)
2. Prepare the initial state on the lattice register (uniform superposition for search, localized source site for transfer). (no equation reference)
3. Evolve under the marked Hamiltonian H for time t, tuned to the time where the probability at w peaks. (eq_1, eq_2)
4. Evaluate the amplitude at the target site to assess search or transfer success. (eq_3)

## Assumptions

- Finite graphene lattice with periodic boundaries assumed
- Analog Hamiltonian simulation; any gate-circuit embedding is not specified
- Lattice register treated as a single-particle position space; qubit encoding is not given
- Ideal projective position measurement assumed

## Missing information

- Exact marking Hamiltonians
- Lattice size and boundary conditions
- Initial state and optimal times
- Scaling of success probability and runtime
- Value of gamma and epsilon tuned to the Dirac point energy
