# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Distinguish non-isomorphic cospectral regular graphs G4(n;n+2) and G5(n;n+2), and the derived T4, T5, via multiparticle (fermionic) quantum walk adjacency matrices and via entanglement entropy between two parts of a network of identical quantum harmonic oscillators.

Scope: Theoretical graph-isomorphism analysis (analytic, not a circuit experiment); reconstruct only the formal setup that the abstract supports. Explicit graph constructions and entropy results are not in the abstract.

## Symbols

- $A$: Adjacency matrix of a graph; domain: real symmetric N x N matrix
- $n$: Scalable graph size parameter; domain: positive integer
- $S$: Entanglement entropy between two parts of the oscillator network; domain: nonnegative real

## eq_1: Cospectrality

$$
\mathrm{spec}(A_{G_4})=\mathrm{spec}(A_{G_5}),\ G_4\not\cong G_5
$$

The graphs share an adjacency spectrum but are non-isomorphic.

Provenance: `abstract_inferred`. Directly stated in the abstract.

Abstract evidence: a pair of non-isomorphic connected cospectral regular graphs

## eq_2: Entropy of subsystem

$$
S=-\mathrm{Tr}(\rho_A\ln\rho_A)
$$

Von Neumann entanglement entropy of a reduced state of one part.

Provenance: `standard_background`. Standard definition for entanglement entropy.

Equation assumptions:

- Von Neumann entropy is used

## Registers

- walkers: unknown (number of fermionic walkers not given) qubits; Antisymmetric multiparticle quantum walk states on graph vertices
- oscillators: one oscillator per graph node qubits; Identical harmonic oscillators for entanglement entropy calculation

## Initial state

Not specified in abstract; assumed an antisymmetrized fermionic multiparticle vertex state, or oscillator ground state for the entropy part.

## Measurement

No physical measurement is specified; the analysis is analytic. Graphs are distinguished by comparing the multiparticle (fermionic-basis) adjacency matrices or spectra of G4 vs G5 (and T4 vs T5), and by comparing the entanglement entropy S between two parts of each network.

## Classical postprocessing

Compare the fermionic-basis adjacency matrices/spectra and the entropy values for each graph pair; differing results indicate non-isomorphism. No numerical procedure is given in the abstract.

## Algorithm steps

1. Build the adjacency matrices of G4 and G5 (and T4, T5) and confirm they are cospectral for the single-particle walk. (eq_1)
2. Rewrite the adjacency matrices in the antisymmetric fermionic multiparticle basis and compare them between the two graphs. (eq_1)
3. Model nodes as coupled identical harmonic oscillators, partition the network into two parts, and compute the entanglement entropy of the reduced state. (eq_2)

## Assumptions

- Entanglement entropy is von Neumann entropy of a reduced state
- Analytic study; the circuit plan is a conceptual outline, not a gate-level circuit
- Circuit plan is a conceptual outline of the analytic procedure
- Measurement is interpreted as analytic comparison, not an experimental readout

## Missing information

- Explicit graph definitions
- Fermionic-basis matrices
- Oscillator coupling Hamiltonian
- Entropy formulas
- Number of walkers and initial state
- Which two parts of the network are used for the entropy
