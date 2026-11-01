# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Time-optimal synthesis of SU(2) unitaries using only rotations about two non-parallel Bloch-sphere axes with different rotation speeds; the abstract gives structural claims (three-angle parametrization, at most five concatenations when both rotation senses are allowed) but not the explicit bounds.

Scope: Smallest useful construction: the control-set model with two axes, the generic alternating-rotation sequence parametrization, and total time as the cost. The explicit angle bounds, scaling laws, proofs, and numerical search are outside scope. The tiny instance (axes at angle alpha, speed ratio r) is an assumption.

## Symbols

- $\hat n_1,\hat n_2$: unit rotation axes of the two controls; domain: unit vectors in R^3, non-parallel
- $\alpha$: angle between the axes; domain: (0,\pi)
- $\Omega_1,\Omega_2$: rotation speeds of the two controls; domain: positive reals
- $r$: relative rotation speed \Omega_2/\Omega_1; domain: positive real
- $\theta_k$: rotation angle of the k-th control segment; domain: real; sign gives rotation sense
- $N$: number of control segments; domain: positive integer
- $T$: total sequence time; domain: nonnegative real
- $U_{target}$: target unitary; domain: SU(2)

## eq_1: Rotation generators

$$
R_j(\theta)=\exp\!\left(-i\frac{\theta}{2}\,\hat n_j\cdot\vec\sigma\right),\quad j\in\{1,2\},\quad \hat n_1\cdot\hat n_2=\cos\alpha
$$

Single-axis SU(2) rotations for the two controls, with angle alpha between the axes.

Provenance: `assumption`. The abstract states rotations about two non-parallel axes; the explicit exponential form is the standard SU(2) convention, not stated in the abstract.

Equation assumptions:

- Standard spin-1/2 convention
- Pauli vector sigma

## eq_2: Alternating sequence

$$
U(\theta_1,\dots,\theta_N)=R_{j_N}(\theta_N)\cdots R_{j_2}(\theta_2)R_{j_1}(\theta_1),\quad j_{k+1}\neq j_k
$$

A control sequence is a concatenation of rotations about alternating axes.

Provenance: `abstract_inferred`. The abstract speaks of concatenations of controls. Merging adjacent same-axis rotations gives the alternating form, which is an inference.

Abstract evidence: any finite time-optimal sequence is composed at most of five control concatenations

Equation assumptions:

- Consecutive same-axis rotations are merged
- Sign of theta_k encodes rotation sense

## eq_3: Total time cost

$$
T=\sum_{k=1}^{N}\frac{|\theta_k|}{\Omega_{j_k}}
$$

Time cost of a sequence, with each axis rotating at its own speed.

Provenance: `abstract_inferred`. Distinct rotation speeds imply the duration of a segment is angle divided by speed. The explicit formula is inferred.

Abstract evidence: as a function of the relative rotation speed of each control

Equation assumptions:

- Constant speed on each axis
- Counterclockwise rotation is a negative angle, costing |theta|/Omega when allowed; with clockwise only, theta_k>=0 mod 2pi

## eq_4: Time-optimal synthesis problem

$$
\min_{N,\,j_1,\,\theta_k} T\quad \text{s.t. } U(\theta_1,\dots,\theta_N)=U_{target}\ \text{(up to global phase if desired)}
$$

Optimization problem: the shortest-time sequence realizing the target.

Provenance: `abstract_inferred`. This is the problem the abstract names, written as a formal optimization.

Abstract evidence: time-optimal synthesis of arbitrary unitaries in $SU(2)$

## eq_5: Length bound with both rotation senses

$$
N\le 5
$$

For finite time-optimal sequences with clockwise and counterclockwise rotations allowed, at most five concatenated controls are needed.

Provenance: `abstract_explicit`. Direct claim in the abstract. The precise counting convention is not given.

Abstract evidence: any finite time-optimal sequence is composed at most of five control concatenations

Equation assumptions:

- N counts alternating-axis segments

## Registers

- q: 1 qubits; Single qubit on which the SU(2) unitary acts

## Classical postprocessing

Numerical search over the bounded angle parameters to find the minimum-time sequence; the bounds themselves are not given in the abstract.

## Algorithm steps

1. Fix the axes, angle alpha, and speed ratio r. Choose a target U_target in SU(2). (eq_1)
2. Parametrize candidate sequences as alternating rotations. (eq_2)
3. Evaluate the time cost and impose the length bound N<=5 for the two-sense case. (eq_3, eq_5)
4. Solve the constrained minimization over angles, a numerical search whose angle bounds the abstract does not give. (eq_4)

## Assumptions

- No scope was supplied; the chosen scope is the generic two-axis model and cost function.
- The tiny instance is an arbitrary alpha and r with a target in SU(2).
- The model is analyzed at the level of unitary composition; no gate-level circuit is derived.

## Missing information

- Explicit bounds on the three rotation angles as functions of alpha and r
- Scaling laws on maximum sequence length for the clockwise-only case
- The three-angle parametrization of optimal sequences
- Proofs and the algebraic method
- Comparison with previously published bounds
- Numerical search procedure details
