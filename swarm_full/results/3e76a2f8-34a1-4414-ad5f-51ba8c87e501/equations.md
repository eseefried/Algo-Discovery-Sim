# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Implement Grover's quantum search on a nuclear spin chain quantum computer with Ising-type couplings between nearest and second-nearest neighbours, and study by numerical simulation with four spins the fidelity over time and the final fidelity as a function of Rabi frequency.

Scope: Four-spin simulation of Grover search with nearest and next-nearest Ising couplings; fidelity vs time and final fidelity vs Rabi frequency, with maxima at the 2πk condition for second-nearest-neighbour coupling. Pulse sequences and coupling values are not given in the abstract.

## Symbols

- $F$: fidelity of the state with the ideal Grover state; domain: [0,1]
- $\Omega$: Rabi frequency of the driving pulses; domain: positive real
- $J_{ij}$: Ising coupling between spins i and j; domain: real, nearest and second-nearest neighbours
- $k$: integer in the 2πk condition; domain: positive integers

## eq_1: Ising coupling Hamiltonian

$$
H_{J}=\sum_{i}J_{i,i+1}I_{z}^{i}I_{z}^{i+1}+\sum_{i}J_{i,i+2}I_{z}^{i}I_{z}^{i+2}
$$

Ising interactions between nearest and second-nearest neighbours in the spin chain

Provenance: `abstract_inferred`. Form is the standard Ising model; the abstract names only the interaction range, not the coupling values.

Abstract evidence: Ising type interactions between nearest and second nearest neighbours

Equation assumptions:

- Spin-1/2 operators; the coupling constants are unspecified

## eq_2: Fidelity

$$
F(t)=\left|\langle\psi_{\mathrm{ideal}}|\psi(t)\rangle\right|^{2}
$$

Fidelity of the simulated state relative to the ideal state

Provenance: `assumption`. The abstract mentions fidelity but not its definition; this common definition is assumed.

Equation assumptions:

- Pure-state overlap fidelity

## eq_3: 2πk condition

$$
\frac{\pi}{\Omega}\,J_{i,i+2}\cdot\frac{1}{2}=2\pi k
$$

Schematic form: the pulse duration is chosen so that the second-nearest-neighbour coupling phase is a multiple of 2π; the exact form is not given.

Provenance: `assumption`. The abstract names only the 2πk method, so the exact expression is a placeholder assumption.

Equation assumptions:

- Exact expression is not given in the abstract; placeholder form only

## Registers

- spins: 4 qubits; Four nuclear spin-1/2 qubits in a chain holding the search index

## Initial state

Assumed computational basis state |0000>, a standard Grover start, before Hadamard-like pulses create the uniform superposition.

## Measurement

Simulation-level readout: the final state is compared with the ideal Grover state via the fidelity F (computed at each time step and at the end of the algorithm). Computational-basis measurement of the four spins would reveal the marked item (assumed; the abstract does not describe a readout scheme).

## Classical postprocessing

Record F(t) during the algorithm, then scan the Rabi frequency Omega and plot the final F against Omega. Identify maxima and compare them with the 2πk condition for the second-nearest-neighbour coupling.

## Algorithm steps

1. Apply selective rf pulses with Rabi frequency Omega, equivalent to Hadamards, to create the uniform superposition over 16 states. (eq_1, eq_3)
2. Apply the oracle as a pulse sequence flipping the phase of an assumed marked state; the marked state and decomposition are not given in the abstract. (eq_1)
3. Apply the inversion about the mean as a pulse sequence, with free Ising evolution during pulses and the 2πk choice of Omega to suppress second-nearest-neighbour errors. (eq_1, eq_3)
4. Repeat the oracle and diffusion for about (π/4)√16 ≈ 3 iterations (assumed), and track F(t) throughout the run. (eq_2)

## Assumptions

- The 2πk condition formula is a schematic placeholder
- The fidelity definition is the standard overlap
- Initial state |0000>, a single marked item, and about 3 Grover iterations are assumed
- Measurement is assumed to be a simulated fidelity evaluation plus a computational-basis readout

## Missing information

- Coupling values
- Pulse sequence and oracle details
- Marked item
- Exact 2πk formula
- Experimental measurement scheme
- Exact pulse decomposition of oracle and diffusion
