# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Implement a single-qubit POVM via a discrete-time quantum walk (polarisation qubit plus position degree of freedom), realised as a Naimark-type dilation. The abstract names three POVMs: Trine, SIC, and unambiguous state discrimination (USD). No explicit equations or parameters are given.

Scope: Smallest useful construction: the Trine POVM on one polarisation qubit, using a generic Naimark-style dilation with a position register of 3 sites. The SIC POVM, USD, and the optical layout, wave-plate angles and experimental results are out of scope.

## Symbols

- $E_k$: POVM element for outcome k; domain: positive semidefinite 2x2 operators
- $|\psi_k\rangle$: Bloch-sphere pure state defining Trine element k; domain: C^2, unit norm
- $\rho$: input polarisation state; domain: 2x2 density matrix
- $p_k$: probability of outcome k; domain: [0,1]
- $V$: isometry from polarisation space into polarisation-position space; domain: C^2 -> C^2 tensor C^3
- $|x\rangle$: walker position basis state, x in {0,1,2}, read out as the outcome k; domain: x in {0,1,2}
- $\theta_k$: azimuthal angle of Trine direction k on the equator; domain: {0, 2\pi/3, 4\pi/3}

## eq_1: POVM completeness and Born rule

$$
E_k\ge 0,\quad \sum_k E_k=I,\quad p_k=\mathrm{Tr}(E_k\rho)
$$

General definition of a POVM and its outcome probabilities.

Provenance: `standard_background`. Standard definition of a generalised measurement; the abstract only names POVMs.

## eq_2: Trine POVM elements

$$
E_k=\tfrac{2}{3}|\psi_k\rangle\langle\psi_k|,\quad |\psi_k\rangle=\tfrac{1}{\sqrt2}\left(|H\rangle+e^{i\theta_k}|V\rangle\right)
$$

Three rank-1 elements with Bloch vectors equally spaced on an equatorial great circle, with theta_k = 2 pi k/3 for k=0,1,2.

Provenance: `abstract_inferred`. Uniform distribution on the equator for three elements implies 120-degree spacing; the 2/3 weight follows from sum E_k = I. The use of exactly three elements is the standard Trine, assumed here.

Abstract evidence: POVM elements uniformly distributed on an equatorial plane of the Bloch sphere

Equation assumptions:

- Three elements; equal weights; equator is the xy plane (the choice of plane is a convention).

## eq_3: Dilation isometry

$$
V|\phi\rangle=\sum_{k=0}^{2}\left(\sqrt{E_k}|\phi\rangle\right)\otimes|k\rangle,\quad V^\dagger V=\sum_k E_k=I
$$

Isometry mapping the input qubit to polarisation and position. The position outcome k has probability p_k = <phi|E_k|phi>.

Provenance: `standard_background`. Generic Naimark-type dilation. The abstract states the walk realises the POVM but not this specific construction.

Equation assumptions:

- Implementable by a walk with polarisation-dependent displacement and wave-plate rotations; the actual angles are not given.

## eq_4: Walk step structure

$$
U=\prod_{t}\left(S\,(C_t\otimes I_{\mathrm{pos}})\right),\quad S=|H\rangle\langle H|\otimes T_{+}+|V\rangle\langle V|\otimes T_{-}
$$

Generic quantum-walk unitary: wave-plate coin operations C_t alternating with a polarisation-dependent shift S, where T_pm shifts position by one site.

Provenance: `abstract_inferred`. Describes the stated roles of displacers (conditional shift) and wave-plates (polarisation rotation). The coin angles and number of steps are not given.

Abstract evidence: polarisation-dependent translation is performed via birefringent beam displacers and a change of the polarisation is implemented with the help of wave-plates

Equation assumptions:

- Shift sign convention and the number of steps are placeholders.

## Registers

- pol: 1 qubit qubits; photon polarisation, basis |H>,|V>
- pos: 3 sites (2 qubits if binary-encoded) qubits; walker position; the final site labels the POVM outcome k

## Initial state

|\phi\rangle_{pol}\otimes|0\rangle_{pos}, with |\phi\rangle an arbitrary input polarisation state

## Measurement

Photon-counting detection in the position basis (polarisation is discarded or ignored); the site k corresponds to POVM outcome k.

## Classical postprocessing

Estimate p_k from normalised count frequencies and compare with Tr(E_k rho) for the Trine elements.

## Algorithm steps

1. Prepare the input polarisation state and set the walker at the initial position. (no equation reference)
2. Apply the walk (wave-plate coins plus displacer shifts) that realises the dilation V. The coin angles must be solved so that V matches eq_3. (eq_3, eq_4)
3. Detect the photon position; the site k gives the outcome with probability p_k=Tr(E_k rho). (eq_1, eq_2)

## Assumptions

- No scope was provided, so the Trine POVM was chosen as the one smallest construction.
- The 3-site dilation is a generic choice; the actual experimental walk layout and number of steps are unknown.
- Abstract-inferred equations are not explicit in the abstract.

## Missing information

- Wave-plate angles and the coin sequence
- Number of walk steps and the geometry of the displacer array
- Explicit SIC and USD POVM elements and parameters
- Experimental data, fidelities and error analysis
- How a non-unitary POVM is mapped onto the walk, e.g. which ancilla degrees of freedom are used
