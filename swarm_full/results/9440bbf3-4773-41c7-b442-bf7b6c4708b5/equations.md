# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Experimentally demonstrate a quantum permutation-parity determining algorithm using linear optics: photon polarization and spatial modes encode ququart states and implement the permutation transformations, determining permutation parity in a single evaluation step.

Scope: Abstract-level reconstruction assuming a 4-element permutation parity problem (ququart, d=4) with single-photon linear optics; the abstract gives no gate-level, state, or setup details, so d=4 and S_4 are inferred from 'ququart'.

## Symbols

- $\sigma$: Permutation of four elements (assumed S_4); domain: S_4
- $|j\rangle$: Ququart basis state encoded in polarization and spatial mode; domain: j in {0,1,2,3}
- $U_\sigma$: Unitary permutation transformation on the ququart; domain: 4x4 permutation matrices
- $\mathrm{sgn}(\sigma)$: Parity of the permutation; domain: {+1,-1}

## eq_1: Permutation operator

$$
U_\sigma|j\rangle=|\sigma(j)\rangle
$$

Action of a permutation transformation on ququart basis states.

Provenance: `standard_background`. Standard definition of a permutation operator; the abstract only mentions permutation transformations on ququart states.

Equation assumptions:

- Computational basis encoding of ququart states

## eq_2: Parity of permutation

$$
\mathrm{sgn}(\sigma)=\prod_{0\le i<j\le 3}\frac{\sigma(j)-\sigma(i)}{j-i}
$$

Parity of the permutation, which the algorithm determines.

Provenance: `standard_background`. Standard definition of the permutation sign; the abstract states only that the parity is determined.

## Registers

- photon_ququart: 1 photon, 4 modes (2 spatial x 2 polarization), i.e. 2 qubits equivalent qubits; Ququart encoded in polarization and spatial path of a single photon

## Initial state

Assumed: single photon prepared in a ququart superposition (e.g. uniform or Fourier-type state over |0>..|3>); exact state not given in the abstract.

## Measurement

Assumed: single-photon detection in the output spatial/polarization modes, with the outcome distinguishing even from odd permutations; the exact basis is not given in the abstract.

## Classical postprocessing

Assumed: map the detected output mode to parity (+1/-1) from the counts; no further processing is specified in the abstract.

## Algorithm steps

1. Prepare single photon in assumed ququart input state using polarization and spatial mode optics. (eq_1)
2. Apply the permutation transformation U_sigma with linear optical elements (wave plates, beam displacers/splitters) acting on polarization and path. (eq_1)
3. Interfere/recombine modes in a single evaluation so that the output encodes the permutation parity sgn(sigma). (eq_2)

## Assumptions

- Ququart dimension d=4 and permutations in S_4
- Circuit plan is an assumed generic linear-optics realization, not taken from the paper
- Ququart encoded as 2 polarization x 2 spatial modes of one photon
- Measurement and postprocessing are assumed generic, not from the paper
- Measurement and postprocessing entries are generic placeholders

## Missing information

- Specific initial state, interferometer layout, and measurement basis
- Explicit form of the one-step quantum algorithm
- Actual optical component layout and interference mapping to parity
- Mapping of detection outcomes to parity
- Explicit demonstration that a single evaluation suffices, since eq_2 is a classical definition rather than the quantum mechanism
- Detector-outcome-to-parity mapping is unspecified
- The quantum mechanism for one-step parity determination is not captured by the equations
