# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Determine the parity (even/odd) of a permutation of 4 elements (S_4) using a single evaluation of a permutation oracle acting on a ququart (4-level system encoded in photon polarization and spatial modes).

Scope: One smallest construction: a standard background parity-determining scheme for permutations of {0,1,2,3} on a single ququart, using a tiny explicit instance, with a generic Fourier-type interference measurement. Outside scope: the actual linear-optical implementation (polarization/path encoding, interferometer layout), the paper's exact algorithm, the full set of permutation transformations, experimental fidelities and the speedup claim details.

## Symbols

- $\sigma$: permutation of the four basis labels; domain: \sigma \in S_4
- $P_\sigma$: permutation operator on the ququart; domain: 4x4 unitary matrix
- $|j\rangle$: ququart basis state, j=0..3 (assumed encoding: 2 polarization x 2 spatial modes); domain: j \in \{0,1,2,3\}
- $\mathrm{sgn}(\sigma)$: parity of the permutation, +1 even, -1 odd; domain: \{+1,-1\}
- $|\psi_0\rangle$: assumed input state; domain: unit vector in C^4

## eq_1: Permutation action

$$
P_\sigma |j\rangle = |\sigma(j)\rangle,\quad j\in\{0,1,2,3\}
$$

Permutation transformation acting on the ququart basis.

Provenance: `assumption`. The abstract mentions permutation transformations on ququart states but gives no explicit formula; this is the natural definition.

Equation assumptions:

- Basis states labeled by integers 0-3

## eq_2: Parity as determinant

$$
\mathrm{sgn}(\sigma)=\det P_\sigma\in\{+1,-1\}
$$

The parity of a permutation equals the determinant of its permutation matrix.

Provenance: `standard_background`. Standard group-theory fact; the abstract only states that parity is determined in one evaluation.

## eq_3: Parity via a Fourier-type input state

$$
|\psi_0\rangle=\tfrac12\sum_{j=0}^{3}\omega^{j}|j\rangle,\ \omega=i
$$

Illustrative input state; in general parity is not an overlap with a fixed state, so this is only an illustrative choice.

Provenance: `assumption`. A proposed construction not established by the abstract. The paper's actual input state and measurement are unknown.

Equation assumptions:

- Illustrative only; not claimed to determine parity for all S_4 elements

## eq_4: Single-query distinguishing criterion

$$
\text{parity determined in one query iff } \exists\, M:\ \langle\psi_\sigma|M|\psi_\sigma\rangle \text{ separates even and odd }\sigma,\ |\psi_\sigma\rangle=P_\sigma|\psi_0\rangle
$$

Condition for a one-evaluation parity test: the output states for even and odd permutations must be perfectly distinguishable (orthogonal subspaces).

Provenance: `abstract_inferred`. Inferred from the one-step claim; the precise states used are not given.

Abstract evidence: this work determines the parity of the permutation in only one step of evaluation

Equation assumptions:

- Perfect distinguishability needed for deterministic output

## Registers

- ququart: 2 qubits (4 levels): 1 polarization qubit + 1 spatial-mode qubit qubits; Carries the permuted state; assumed ordering |j> = |spatial, polarization> with j=2s+p

## Initial state

Not specified in the abstract; an assumed single-photon ququart state |psi_0> (eq_3 is only illustrative).

## Measurement

Single-photon detection in an unspecified basis separating even- and odd-permutation outputs; details not given in the abstract.

## Classical postprocessing

Map detection outcome to parity label +1/-1 (assumed).

## Algorithm steps

1. Prepare single photon in ququart state |psi_0> using polarization and spatial modes (assumed). (eq_3)
2. Apply the permutation transformation P_sigma once (one evaluation). (eq_1)
3. Measure in a basis that distinguishes even from odd permutations (basis not given in abstract). (eq_2, eq_4)

## Assumptions

- Ququart encoded as 2 spatial modes x 2 polarizations
- Permutations are in S_4
- The actual algorithm's input state, measurement basis and any ancilla are not reconstructed
- Classical comparison (needing multiple evaluations) is background only

## Missing information

- Exact input state and measurement basis used in the experiment
- Explicit construction of the permutation oracles in linear optics
- Which subset of S_4 permutations was implemented
- Whether the algorithm uses additional ancillary degrees of freedom
- Quantitative results and fidelity
