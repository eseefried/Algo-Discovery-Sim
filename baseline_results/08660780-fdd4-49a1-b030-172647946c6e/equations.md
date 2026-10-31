# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Realise a single-qubit generalised measurement (POVM) on a photon-polarisation qubit by means of a discrete-time quantum walk in which the position (optical path) register is expanded through polarisation-dependent translations and position-dependent coin (polarisation) rotations, and the POVM outcome is read out from the final position of the photon.

Scope: Smallest useful construction (chosen because no experiment_scope was supplied): the 3-outcome Trine-POVM on one qubit, implemented by a 3-step quantum walk on three positions x in {0,1,2} with an asymmetric polarisation-dependent shift (beam-displacer model) and explicit site-dependent coins. The SIC-POVM (4 outcomes), the unambiguous state discrimination scheme, and all experimental details (wave-plate angles, beam-displacer geometry, detector calibration, imperfections) are outside this scope.

## Symbols

- $|H\rangle, |V\rangle$: Horizontal and vertical polarisation basis states of the photon, identified with the computational basis |0\rangle, |1\rangle of the coin qubit; domain: Orthonormal basis of \mathbb{C}^2
- $|x\rangle$: Position (optical path) basis state of the walker; domain: x \in \{0,1,2\}, orthonormal basis of \mathbb{C}^3
- $|\psi\rangle = \alpha|H\rangle + \beta|V\rangle$: Unknown input polarisation qubit state to be measured; domain: \alpha,\beta \in \mathbb{C}, |\alpha|^2+|\beta|^2=1
- $\rho$: Density operator of the input qubit (allows mixed states); domain: Positive semidefinite 2x2 matrix with unit trace
- $|\psi_k\rangle$: Trine states, three pure states with Bloch vectors uniformly spaced (120 degrees apart) on a great circle; domain: k \in \{0,1,2\}, unit vectors in \mathbb{C}^2
- $E_k$: POVM element associated with outcome k (detection at position x=k); domain: Positive semidefinite 2x2 operators with \sum_k E_k = I
- $K_x$: Kraus operator (on the coin space) mapping the initial coin state to the unnormalised coin state found at final position x; domain: 2x2 complex matrices with \sum_x K_x^\dagger K_x = I
- $C_x^{(t)}$: Coin (polarisation) unitary applied at position x during walk step t (realised by wave-plates); domain: t \in \{1,2,3\}, x \in \{0,1,2\}, elements of U(2)
- $S$: Polarisation-dependent shift (translation) operator realised by a birefringent beam displacer; domain: Isometry on \mathbb{C}^2 \otimes \mathbb{C}^3 (unitary on the infinite line)
- $p_k$: Probability of outcome k; domain: [0,1], \sum_k p_k = 1
- $\vec r$: Bloch vector of the input state; domain: \mathbb{R}^3, |\vec r| \le 1

## eq_1: Trine POVM

$$
E_k = \tfrac{2}{3}\,|\psi_k\rangle\langle\psi_k|,\qquad |\psi_k\rangle = \cos\!\left(\tfrac{k\pi}{3}\right)|H\rangle + \sin\!\left(\tfrac{k\pi}{3}\right)|V\rangle,\qquad k=0,1,2,\qquad \sum_{k=0}^{2} E_k = I
$$

Three rank-one POVM elements whose Bloch vectors \vec n_k = (\sin(2k\pi/3), 0, \cos(2k\pi/3)) are uniformly distributed on a great circle (here the x-z plane) of the Bloch sphere; the weight 2/3 enforces completeness.

Provenance: `abstract_inferred`. The abstract defines the trine as POVM elements uniformly distributed on an equatorial plane; three equally weighted rank-one elements at 120-degree Bloch spacing is the standard mathematical content of that statement. The specific plane (x-z, real amplitudes) and phase convention are chosen here.

Abstract evidence: Trine-POVM, i.e., the POVM elements uniformly distributed on an equatorial plane of the Bloch sphere

Equation assumptions:

- The great circle is taken to be the x-z plane with |\psi_0\rangle = |H\rangle; any other equatorial plane is related by a fixed polarisation unitary.
- Rank-one elements with equal weights 2/3 are assumed (the minimal informationally symmetric trine).

## eq_2: Quantum-walk step with polarisation-dependent translation

$$
U_t = S\,\Big(\sum_{x} C^{(t)}_x \otimes |x\rangle\langle x|\Big),\qquad S = |H\rangle\langle H| \otimes \sum_x |x\rangle\langle x| + |V\rangle\langle V| \otimes \sum_x |x+1\rangle\langle x|
$$

One step of the walk: a position-dependent coin acts on the polarisation, then the shift leaves H-polarised amplitude in place and displaces V-polarised amplitude by one position (beam-displacer model).

Provenance: `abstract_inferred`. The abstract states that the walk consists of polarisation-dependent translations (beam displacers) and polarisation changes (wave-plates); the operator form is the standard quantum-walk decomposition into coin and conditional shift. The asymmetric (one polarisation displaced, the other transmitted) form models a birefringent beam displacer.

Abstract evidence: the polarisation-dependent translation is performed via birefringent beam displacers and a change of the polarisation is implemented with the help of wave-plates

Equation assumptions:

- Asymmetric shift (H stays, V moves by +1) rather than the symmetric ±1 shift; the two are equivalent up to relabelling of positions.
- Coins may depend on both position and step number (different wave-plates in different paths).

## eq_3: POVM induced by position readout

$$
K_x = (I \otimes \langle x|)\,U_3 U_2 U_1\,(I \otimes |0\rangle),\qquad E_x = K_x^\dagger K_x,\qquad p_x = \mathrm{Tr}(E_x \rho) = \sum_{c\in\{H,V\}} \big|\langle c, x|\,U_3U_2U_1\,|\psi,0\rangle\big|^2
$$

Starting the walker at position 0 and detecting its final position x (without resolving polarisation) implements a POVM on the coin qubit whose elements are determined by the Kraus operators K_x; completeness \sum_x E_x = I follows from unitarity.

Provenance: `standard_background`. Standard Naimark-dilation reading of a quantum walk as a generalised measurement on the coin: the position register is the ancilla, the walk is the dilating unitary, and position detection is the projective readout.

Equation assumptions:

- Three walk steps are sufficient for the trine (true for the construction in eq_4).
- Detectors resolve position only; polarisation at the detector is traced out.

## eq_4: Explicit coin schedule for the trine walk (proposed instance)

$$
C^{(1)}_0 = I,\quad C^{(2)}_0 = \begin{pmatrix} \sqrt{2/3} & -\sqrt{1/3} \\ \sqrt{1/3} & \sqrt{2/3} \end{pmatrix},\quad C^{(2)}_1 = \sigma_x,\quad C^{(3)}_0 = I,\quad C^{(3)}_1 = \tfrac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix},\quad C^{(3)}_2 = I
$$

Step 1 only separates H (x=0) from V (x=1). Step 2 peels off the first POVM element at x=0 with a rotation of amplitude \sqrt{2/3}, sends the remaining amplitude to x=1, and flips polarisation at x=1 so that the two contributions merge at x=1. Step 3 applies a Hadamard at x=1 followed by the shift, splitting the merged state into outcomes x=1 (H) and x=2 (V).

Provenance: `assumption`. A concrete coin schedule constructed here so that eq_3 reproduces eq_1; it is not taken from the abstract, which gives no coin parameters.

Equation assumptions:

- Matrices written in the ordered basis (|H\rangle, |V\rangle).
- Coins at unoccupied positions are irrelevant and set to I.
- Mapping of these coins to physical wave-plate angles is not specified.

## eq_5: Resulting Kraus operators and POVM elements

$$
K_0 = \sqrt{\tfrac{2}{3}}\,|H\rangle\langle H|,\qquad K_1 = \sqrt{\tfrac{2}{3}}\,|H\rangle\langle\psi_1|,\qquad K_2 = -\sqrt{\tfrac{2}{3}}\,|V\rangle\langle\psi_2|,\qquad K_x^\dagger K_x = \tfrac{2}{3}|\psi_x\rangle\langle\psi_x| = E_x
$$

Applying eq_3 to the schedule of eq_4 yields rank-one Kraus operators whose squares are exactly the trine elements of eq_1; the equality is exact (no approximation).

Provenance: `assumption`. Direct algebraic consequence of eq_2-eq_4: after step 2 the coin state at x=1 is M|\psi\rangle with M = |H\rangle\langle V| + 3^{-1/2}|V\rangle\langle H|, and M^\dagger|\pm\rangle \propto |\psi_{1,2}\rangle with squared norm 2/3. Not verified numerically here.

Equation assumptions:

- Ideal lossless optics and perfect interference of the two paths merging at x=1 (interferometric phase stability).

## eq_6: Outcome statistics in Bloch form

$$
p_k = \langle\psi|E_k|\psi\rangle = \tfrac{2}{3}|\langle\psi_k|\psi\rangle|^2 = \tfrac{1}{3}\big(1 + \vec r\cdot\vec n_k\big),\qquad \vec n_k = \big(\sin\tfrac{2k\pi}{3},\,0,\,\cos\tfrac{2k\pi}{3}\big)
$$

Probability of detecting the photon at position k as a function of the input Bloch vector; the three probabilities determine the two Bloch components lying in the trine plane.

Provenance: `standard_background`. Born rule for rank-one POVM elements written in Bloch-vector form; standard for the trine measurement.

Equation assumptions:

- Trine plane and labelling as in eq_1.

## Registers

- coin (polarisation qubit): 1 qubits; System qubit to be measured; |H\rangle = |0\rangle, |V\rangle = |1\rangle
- position (optical path): 3 levels (2 qubits if binary-encoded, x = 2 x_1 + x_0) qubits; Ancilla / walker position; the final position x in {0,1,2} is the POVM outcome label

## Initial state

|\Psi_0\rangle = |\psi\rangle \otimes |x=0\rangle = (\alpha|H\rangle + \beta|V\rangle)\otimes|0\rangle, with the position register on the top (x=0) path.

## Measurement

Single-photon detection in each of the three output paths x = 0, 1, 2 (position basis of the walker), without resolving polarisation. Outcome k corresponds to the POVM element E_k = (2/3)|\psi_k\rangle\langle\psi_k|.

## Classical postprocessing

Estimate p_k from detection frequencies over many repetitions; compare with eq_6 (p_k = (1 + \vec r\cdot\vec n_k)/3), optionally inverting to estimate the two in-plane Bloch components of the input state. Check \sum_k p_k = 1 (after loss normalisation).

## Algorithm steps

1. Prepare the input polarisation state |\psi\rangle on a single photon in path x=0. (eq_3)
2. Walk step 1: identity coin, then polarisation-dependent shift S; H amplitude stays in x=0, V amplitude moves to x=1. (eq_2, eq_4)
3. Walk step 2: apply coin C^{(2)}_0 (rotation with amplitude \sqrt{2/3} on H) at x=0 and \sigma_x at x=1, then shift S; the H part at x=0 becomes outcome 0, the V part of x=0 moves to x=1 and merges with the flipped amplitude already at x=1. (eq_2, eq_4)
4. Walk step 3: apply the Hadamard coin at x=1 (identity at x=0), then shift S; H output stays at x=1 (outcome 1), V output moves to x=2 (outcome 2). (eq_2, eq_4, eq_5)
5. Detect the photon's final position x in {0,1,2}, which realises the trine POVM with elements E_x. (eq_3, eq_5, eq_1)

## Assumptions

- Scope choice: only the Trine-POVM is reconstructed; the SIC-POVM and the unambiguous-discrimination POVM named in the abstract are left outside this scope.
- Trine plane fixed to the x-z Bloch plane with |\psi_0\rangle = |H\rangle (real amplitudes); other equatorial planes differ by a fixed polarisation unitary.
- Beam displacer modelled as the asymmetric shift (H transmitted, V displaced by one position).
- Coin schedule of eq_4 is a proposed construction, not extracted from the paper; the paper's actual coins/wave-plate settings may differ.
- Ideal, lossless, phase-stable optics; position-only detection.

## Missing information

- The paper's actual quantum-walk layout (number of steps, positions, symmetric vs asymmetric shift) and its wave-plate angles for each coin.
- Construction details for the SIC-POVM (4 outcomes, presumably more walk steps) and for the unambiguous discrimination POVM (including the inconclusive outcome and the pair of non-orthogonal states used).
- Experimental figures of merit (fidelities, detection efficiencies, losses) and any error model.
- Mapping of abstract coins to physical half-/quarter-wave-plate settings and the treatment of relative phases between merging paths.
