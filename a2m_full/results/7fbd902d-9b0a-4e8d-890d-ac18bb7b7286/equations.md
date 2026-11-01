# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Continuous-time quantum walk spatial search for a marked site w on a small periodic honeycomb (graphene) lattice, using the Dirac point at E=0, with a tunable marking onsite energy; plus a two-site marked state-transfer variant. Output is the probability of the bitstring of w read from position-register counts.

Scope: One smallest instance: periodic honeycomb of 2x2 unit cells (8 sites, 3 position qubits, no padding), Hamiltonian H=-gamma A - epsilon|w><w|, first-order Trotterized evolution, uniform-superposition initial state, gamma and epsilon scanned numerically, and measurement of all 3 qubits. Outside scope: analytic scaling in N, the paper's specific marking variants and exact parameters, the Dirac-eigenstate preparation circuit for larger lattices, larger lattices, and a full transfer study.

## Symbols

- $A$: adjacency matrix of the periodic honeycomb lattice (bipartite); domain: N x N real symmetric 0/1 matrix, N=8
- $\gamma$: hopping rate; domain: positive real
- $\epsilon$: marking onsite energy strength (tunable, not necessarily gamma); domain: real
- $w$: marked site index; site i corresponds to bit i of the position register (little-endian); domain: integer 0..N-1
- $\Delta t$: Trotter step; domain: positive real
- $r$: Trotter step count, t=r\Delta t; domain: positive integer
- $|s\rangle,|r\rangle$: source and receiver sites in the transfer variant; domain: basis states

## eq_1: Search Hamiltonian

$$
H=-\gamma A-\epsilon\,|w\rangle\langle w|
$$

Lattice hopping plus onsite marking potential on the target site

Provenance: `abstract_inferred`. The abstract implies a CTQW on a graphene lattice with a modified marking; the specific form is the standard Hamiltonian with a tunable epsilon (assumption).

Abstract evidence: making a change to standard methods of marking a particular site in the lattice

Equation assumptions:

- Marking is diagonal onsite
- epsilon is tuned, not fixed to gamma

## eq_2: Dirac point of the bipartite lattice

$$
A\,|\psi_D\rangle=0,\quad E_D=0
$$

The Dirac point lies at zero energy of the unmarked graphene spectrum; the resonance scan targets coupling of this state to the marked site

Provenance: `abstract_inferred`. The abstract says the Dirac point is used; E=0 is standard for the honeycomb tight-binding model.

Abstract evidence: utilising the Dirac point in the energy spectrum

Equation assumptions:

- Nearest-neighbour hopping only
- On a tiny periodic lattice the zero-energy states may be few or degenerate and should be checked numerically

## eq_3: Trotterized evolution

$$
U(t)\approx\Big[\prod_{c=1}^{3}e^{i\gamma\Delta t A_c}\;e^{i\epsilon\Delta t|w\rangle\langle w|}\Big]^{r},\quad A=A_1+A_2+A_3
$$

First-order product formula with the three perfect matchings of the honeycomb as commuting edge-colour layers; the oracle phase is a multi-controlled phase gate. Layers should be ordered consistently.

Provenance: `assumption`. A standard Trotter decomposition proposed for circuit implementation; step size and order are not from the abstract.

Equation assumptions:

- Delta t small enough for fidelity
- Edge colouring into 3 matchings exists (the 2x2 periodic case may have multi-edges, so the lattice must be checked)
- Each edge term is a two-qubit gate in permutation-conjugated form

## eq_4: Initial state and success probability

$$
|\psi_0\rangle=\frac{1}{\sqrt N}\sum_{x}|x\rangle,\quad P_w(t)=|\langle w|U(t)|\psi_0\rangle|^2
$$

Uniform superposition start by Hadamards; readout is the counts frequency of the bitstring of w

Provenance: `assumption`. Sketch choice; the Dirac eigenstate start is an alternative.

Equation assumptions:

- Counts bitstring key read as bits[::-1] gives the site index

## eq_5: Two-site transfer

$$
|\psi_0\rangle=|s\rangle,\quad H_T=-\gamma A-\epsilon(|s\rangle\langle s|+|r\rangle\langle r|),\quad t^*\approx\frac{\pi}{2J_{\rm eff}}
$$

Amplitude transfer between s and r with equal onsite energies; J_eff is the effective coupling splitting between the two resonant eigenstates, determined numerically

Provenance: `abstract_inferred`. The abstract claims transfer between sites; the Hamiltonian and t* form follow the sketch and are assumed, not stated.

Abstract evidence: transfer probability amplitude across the lattice between specific lattice sites

Equation assumptions:

- Two-level resonance approximation
- J_eff computed numerically from the spectrum

## Registers

- pos: 3 (8 sites; 4 for 16 sites) qubits; site index, little-endian, measured at the end

## Initial state

Hadamard on all position qubits (uniform superposition) for search; basis state |s> for transfer

## Measurement

Measure all position qubits into classical bits with measure(i,i); site index i is bit i, read with bits[::-1].

## Classical postprocessing

Estimate P_w as the count fraction of w's bitstring; choose the gamma, epsilon and t with the maximum value.

## Algorithm steps

1. Classically build A for the 2x2 periodic honeycomb, verify the bipartite structure and Dirac-point zero modes, and choose the edge colouring and site-to-bit map. (eq_2)
2. Prepare the initial state with H gates. (eq_4)
3. Apply r Trotter steps of the three matching layers plus the marking phase (a multi-controlled phase with X conjugation on the zero bits of w). Each oracle placement is one query. (eq_1, eq_3)
4. Scan gamma, epsilon and r classically (statevector or numeric) to pick the resonance and the peak time; for transfer use eq_5. (eq_4, eq_5)
5. Measure all position qubits and read the frequency of the bitstring of w, reversing the key to map bits to sites. (eq_4)

## Assumptions

- 8-site periodic honeycomb, all qubits within the cap
- Trotter instead of exact exponentiation
- Marking strength epsilon differs from gamma and is tuned numerically
- Optimal parameters are found numerically, not analytically

## Missing information

- Exact lattice geometry and boundary conditions
- Paper's marking variants and optimal parameter values
- Scaling of the search time
- Whether the Dirac eigenstate or uniform state is used
- Transfer protocol details
