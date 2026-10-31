# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct a quantum algorithm for additive approximation of Ising partition functions on square lattices using the overlap mapping of Van den Nest, Dür and Briegel and its MBQC interpretation. Specify the algorithmic domain and approximation scale, show BQP-completeness with complex couplings and fields, and extend to real parameters with an explicit approximation scale.

Scope: Abstract-level reconstruction of the problem statement and a few standard background equations for the Ising partition function and additive approximation. The detailed overlap mapping, MBQC circuit, and approximation-scale formula are not given in the abstract and are not reconstructed.

## Symbols

- $Z$: Ising partition function; domain: complex number
- $J_{ij}$: coupling strength on edge (i,j) of the square lattice; domain: complex in the BQP-complete construction; real in the physical region
- $h_i$: magnetic field at site i; domain: complex in the BQP-complete construction; real in the physical region
- $s_i$: Ising spin at site i; domain: {+1,-1}
- $\epsilon$: accuracy parameter; domain: positive real
- $\Delta$: approximation scale; its explicit form is not given in the abstract; domain: positive real

## eq_1: Ising partition function

$$
Z=\sum_{s\in\{\pm1\}^N}\exp\Big(\sum_{\langle i,j\rangle}J_{ij}s_is_j+\sum_i h_i s_i\Big)
$$

Partition function of an Ising model on a square lattice with N sites, in a sign convention that absorbs the inverse temperature.

Provenance: `standard_background`. Standard definition of the Ising partition function; the abstract only names the problem.

Equation assumptions:

- Sign and temperature conventions are assumed.
- Couplings and fields may be complex.

## eq_2: Additive approximation

$$
|\tilde Z-Z|\le\epsilon\,\Delta
$$

Additive approximation of Z with error measured relative to the approximation scale Delta.

Provenance: `abstract_inferred`. The abstract states an additive approximation with an accuracy set by an approximation scale; the precise form is assumed.

Abstract evidence: an additive approximation of Ising partition functions on square lattices

Equation assumptions:

- The error bound form is assumed; Delta is not defined in the abstract.

## Registers

- lattice: O(N) qubits (assumed) qubits; Qubits on a square-lattice resource state for the MBQC interpretation of the overlap mapping; the precise state is not given in the abstract
- output: 1 qubit (assumed) qubits; Readout qubit whose measurement statistics encode the overlap/amplitude proportional to Z

## Initial state

Assumed: a square-lattice graph-state-like MBQC resource state, with exact form not specified in the abstract.

## Measurement

Assumed: single-qubit measurements of the lattice qubits in bases set by the couplings and fields (MBQC), then a final readout of the output qubit; its statistics over repeated runs estimate the real and imaginary parts of the overlap proportional to Z. Exact angles are not given in the abstract.

## Classical postprocessing

Assumed: average the measurement outcomes over repeated runs, with number of runs scaling as 1/epsilon^2, to estimate the overlap; rescale by the known normalization to obtain an estimate of Z with additive error epsilon times Delta. The normalization and Delta are not given in the abstract.

## Algorithm steps

1. Map the Ising instance (J_ij, h_i) to an overlap between a lattice stabilizer-type state and a product state, following the overlap mapping, so that Z is proportional to the overlap (details assumed). (eq_1)
2. Interpret the overlap as an MBQC computation: prepare the lattice resource state and apply single-qubit measurements with angles set by the couplings and fields (details assumed). (eq_1)
3. Estimate the overlap amplitude by repeated runs to precision epsilon, giving an additive estimate of Z at scale Delta. (eq_2)

## Assumptions

- Equation forms are generic background, not taken from the paper.
- The circuit plan is a generic outline consistent with the abstract, not the paper's explicit construction.
- Register sizes and the resource state are assumed generically.
- Measurement and postprocessing are a generic MBQC amplitude-estimation outline, not the paper's explicit protocol.
- Measurement and postprocessing are a generic MBQC amplitude-estimation outline.

## Missing information

- Explicit overlap mapping
- MBQC circuit and resource state
- Formula for the approximation scale
- Exact measurement angles and basis choices
- Normalization factor relating overlap to Z
- Register layout of the paper's construction
- Real-parameter domain boundaries
