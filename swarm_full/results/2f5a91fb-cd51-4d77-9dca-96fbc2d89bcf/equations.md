# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Time-optimal synthesis of arbitrary SU(2) unitaries when controls are limited to rotations about two non-parallel Bloch-sphere axes with different relative rotation speeds. Determine necessary conditions and bounds on time-optimal sequences, parametrized by three rotation angles, for the case with both clockwise and counterclockwise rotations and the case with clockwise only.

Scope: Abstract-level problem statement plus a minimal background model of two-axis SU(2) control sequences. Specific bounds, proofs and scaling laws are not reconstructed because the abstract does not give them.

## Symbols

- $U$: target unitary to synthesize; domain: SU(2)
- $\hat n_1,\hat n_2$: the two non-parallel rotation axes; domain: unit vectors in R^3
- $\theta$: angle between the two axes; domain: (0,\pi)
- $\Omega_1,\Omega_2$: rotation speeds of the two controls; domain: positive reals
- $\alpha_j$: rotation angle of the j-th control segment; domain: real; nonnegative if only clockwise rotations are allowed

## eq_1: Control rotations

$$
R_k(\alpha)=\exp\!\left(-i\,\frac{\alpha}{2}\,\hat n_k\cdot\vec\sigma\right),\quad k=1,2
$$

Elementary rotations about the two allowed axes.

Provenance: `standard_background`. Standard SU(2) rotation form for the abstract's rotations about two axes in the Bloch sphere.

Equation assumptions:

- Axes fixed, with a standard spin-1/2 representation.

## eq_2: Sequence synthesis

$$
U=R_{2}(\alpha_n)R_{1}(\alpha_{n-1})\cdots R_{1}(\alpha_1)
$$

Target unitary as an alternating product of rotations about the two axes.

Provenance: `assumption`. Assumed concatenation model matching the abstract's 'control concatenations'. Exact form of the sequences is not given.

Equation assumptions:

- Alternating axes; the first and last axis may vary.

## eq_3: Total time

$$
T=\sum_j \frac{|\alpha_j|}{\Omega_{k_j}}
$$

Duration to be minimized, with each segment's time set by its angle and axis speed.

Provenance: `assumption`. Assumed time cost consistent with relative rotation speeds; not stated explicitly.

Equation assumptions:

- Constant speed per control.

## Registers

- q: 1 qubits; single qubit (Bloch sphere state) on which U is synthesized

## Initial state

Arbitrary single-qubit state |psi>; the synthesized unitary acts on it. Identity is the starting point of the control sequence.

## Measurement

The abstract specifies no measurement. As an assumed verification, apply the synthesized sequence to a known input state and perform single-qubit state or process tomography (Pauli X, Y, Z expectation values) to estimate fidelity with the target U.

## Classical postprocessing

Classical numerical search over the three bounded rotation angles to minimize T subject to reproducing U (as the abstract suggests). Optionally compare tomography-reconstructed unitary fidelity with U. The search details are not given in the abstract.

## Algorithm steps

1. Fix axes n1, n2 with angle theta and speeds Omega1, Omega2; choose the allowed rotation direction set (both signs or clockwise only). (eq_1)
2. Write the target U as an alternating product of rotations about the two axes with angles alpha_j, as a finite instance of the concatenation model. (eq_1, eq_2)
3. Minimize the total time over sequences reproducing U. The abstract says optimal sequences are parametrized by three angles and bounded, enabling an efficient numerical search, but the bounds are not given here. (eq_2, eq_3)

## Assumptions

- Equations are background or assumed models, not the paper's derived results.
- Alternating-rotation model with time cost proportional to angle over speed.
- Single-qubit register is an assumed realization.
- Single-qubit register, no ancilla.
- Tomographic verification is an assumed addition, not from the abstract.

## Missing information

- Explicit bounds on angles
- Proof details
- Scaling laws for the clockwise-only case
- Explicit bounds on angles and sequence length are not in the abstract.
- Measurement protocol (none in the abstract)
- Explicit numerical search procedure and the three-angle parametrization are not given.
