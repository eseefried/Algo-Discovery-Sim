# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Implement single-qubit POVMs (Trine, SIC, unambiguous state discrimination of two non-orthogonal states) with a single-photon polarisation qubit performing a quantum walk, using birefringent beam displacers for polarisation-dependent translation and wave-plates for polarisation changes.

Scope: Abstract-level reconstruction of the single-qubit POVM via quantum-walk (Naimark-style dilation into a walk position space); no experimental parameters, angles, or data are given. Equations are standard background or assumed finite instances.

## Symbols

- $E_k$: POVM element k; domain: positive semidefinite 2x2 operators with sum_k E_k = I
- $\vec{n}_k$: Bloch vector of the k-th POVM direction; domain: unit vectors in R^3
- $p_k$: probability of outcome k; domain: [0,1]
- $\rho$: input polarisation qubit state; domain: 2x2 density matrix

## eq_1: POVM completeness and Born rule

$$
E_k\ge 0,\ \sum_k E_k=\mathbb{I},\ p_k=\mathrm{Tr}(\rho E_k)
$$

General POVM definition and outcome probabilities.

Provenance: `standard_background`. Standard definition of a generalised measurement (POVM).

## eq_2: Trine POVM

$$
E_k=\tfrac{2}{3}|\psi_k\rangle\langle\psi_k|,\ \vec{n}_k=(\cos\tfrac{2\pi k}{3},\sin\tfrac{2\pi k}{3},0),\ k=0,1,2
$$

Three elements uniformly spaced in an equatorial plane of the Bloch sphere.

Provenance: `abstract_inferred`. Abstract describes uniform equatorial distribution; explicit form is the standard trine.

Abstract evidence: POVM elements uniformly distributed on an equatorial plane of the Bloch sphere

Equation assumptions:

- Three elements, equatorial plane taken as x-y plane

## eq_3: SIC POVM

$$
E_k=\tfrac{1}{2}|\phi_k\rangle\langle\phi_k|,\ |\langle\phi_j|\phi_k\rangle|^2=\tfrac{1}{3}\ (j\ne k),\ k=0..3
$$

Four elements forming a tetrahedron on the Bloch sphere.

Provenance: `standard_background`. Standard qubit SIC-POVM; the abstract only names it.

## Registers

- pol: 1 qubit qubits; Photon polarisation (H/V) encoding the system qubit
- pos: small walk-position space (assumed a few modes, e.g. 3-4 spatial paths) qubits; Spatial mode set by beam displacers; serves as the Naimark ancilla and the outcome label

## Initial state

Single photon in a single input spatial mode with polarisation state rho (arbitrary input qubit) to be measured.

## Measurement

Detect the photon (e.g. single-photon detectors) in the output spatial modes after the final displacer, ignoring polarisation; the detected mode k labels POVM outcome k with probability p_k=Tr(rho E_k). Collect counts over many photons.

## Classical postprocessing

Normalise counts per output mode to estimated frequencies p_k and compare with Tr(rho E_k) for the trine, SIC and unambiguous-discrimination POVMs. For discrimination, interpret the inconclusive mode as the failure outcome and the other modes as conclusive state identifications.

## Algorithm steps

1. Prepare the photon in the input spatial mode with polarisation state rho. (eq_1)
2. Apply wave-plates (assumed set to POVM-specific angles) to rotate polarisation before each displacement. (eq_1, eq_2, eq_3)
3. Apply a beam displacer to translate the photon path conditioned on polarisation, entangling pol with pos. (eq_1)
4. Repeat wave-plate and displacer layers for the assumed number of walk steps so the overall isometry maps rho into pos-labelled outcomes with amplitudes realising E_k. (eq_1, eq_2, eq_3)

## Assumptions

- Standard POVM forms are used for the named measurements.
- The walk acts as a Naimark-type isometry, with each output spatial mode corresponding to one POVM outcome.
- Output spatial modes map one-to-one to POVM outcomes (the inconclusive outcome included for unambiguous discrimination).
- Detection is by spatially resolved photon counting; the abstract does not specify the detectors.
- Detection is by spatially resolved photon counting.

## Missing information

- Explicit unambiguous discrimination states and overlap
- Walk geometry and wave-plate angles
- Number of walk steps and detection scheme
- Exact number of spatial modes and layer count per POVM
- Detector type and data analysis details
