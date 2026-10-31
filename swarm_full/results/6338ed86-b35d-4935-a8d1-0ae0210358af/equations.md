# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Estimate key systematic gate parameters (amplitude error and off-resonance error) of a universal single-qubit gate-set efficiently and robustly, using only single-qubit operations without entanglement, achieving Heisenberg scaling via a robust version of the Higgins et al. phase estimation procedure.

Scope: Abstract-level reconstruction of the robust phase-estimation-based calibration task for a single qubit; the circuits, the robustness proof, and the exact error model are not given in the abstract, so only a small illustrative finite instance is sketched.

## Symbols

- $\phi$: unknown systematic rotation parameter (e.g. amplitude or off-resonance error) to be estimated; domain: real, \phi\in[0,2\pi)
- $\hat{\phi}$: estimate of \phi; domain: real
- $k$: number of repeated applications of the gate in one experiment; domain: positive integer
- $N$: total number of gate applications (resource count); domain: positive integer
- $\epsilon$: estimation error; domain: nonnegative real

## eq_1: Heisenberg scaling

$$
\epsilon = O(1/N)
$$

Estimation error scales inversely with total number of gate applications, the optimal efficiency.

Provenance: `abstract_inferred`. Heisenberg scaling means error ~ 1/resource; the exact constants are not given in the abstract.

Abstract evidence: our estimates achieve the optimal efficiency, Heisenberg scaling

Equation assumptions:

- N counts total gate applications

## eq_2: Repeated gate phase

$$
U^k = e^{-i k\phi \,\hat{n}\cdot\vec{\sigma}/2}
$$

Applying a gate with a systematic rotation error k times amplifies the unknown angle to k\phi.

Provenance: `assumption`. Standard model of phase-estimation-style amplification of a rotation angle; the actual gate model is not in the abstract.

Equation assumptions:

- Error acts as coherent rotation about a fixed axis

## eq_3: Outcome probability

$$
P(0\mid k)=\cos^2(k\phi/2)
$$

Illustrative single-qubit measurement probability whose k-dependence encodes \phi.

Provenance: `assumption`. Illustrative model for noiseless SPAM; the paper's robust procedure handles imperfections not modeled here.

Equation assumptions:

- Ideal state preparation and measurement for illustration

## Registers

- q: 1 qubits; single qubit on which the gate under calibration is repeatedly applied

## Initial state

|0> on q (idealized; the paper's robustness to SPAM errors is not modeled here)

## Measurement

Single-qubit computational-basis measurement after the k-fold gate and a basis-change rotation, repeated for several shots per k to estimate P(0|k) (and the orthogonal-quadrature probability).

## Classical postprocessing

Estimate k\phi mod 2\pi from outcome frequencies for each k in the sequence, then combine across increasing k to refine \hat{\phi} (unwrapping the phase ambiguity); the robust estimator is not given in the abstract.

## Algorithm steps

1. Prepare the qubit in |0>. (no equation reference)
2. Apply the gate under test k times for k in an increasing sequence (e.g. powers of 2) so the error angle is amplified to k\phi. (eq_2)
3. Apply a basis-change rotation, then measure in the computational basis. Repeat for each k, with total gate count N to give 1/N error. (eq_1, eq_3)

## Assumptions

- Illustrative coherent-rotation model used because the abstract lacks the explicit one.
- Doubling k sequence is assumed, not stated in the abstract.
- Shot counts per k and quadrature measurements are assumed.
- Shot counts per k and two-quadrature measurements assumed.

## Missing information

- Exact gate-set and error model
- Specific circuits and choice of k sequence
- Robustness guarantees and constants
- Postprocessing/estimator details
