# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Time-optimal synthesis of a target unitary in SU(2) (a single-qubit gate, up to global phase) using piecewise-constant controls restricted to rotations about two fixed non-parallel Bloch-sphere axes with given rotation speeds, i.e. find the concatenation of axis rotations of minimal total duration that realizes the target.

Scope: One single-qubit instance: two axes n_1 = z and n_2 at angle gamma from z (chosen gamma = pi/2, i.e. x), equal rotation speeds omega_1 = omega_2 = 1, bidirectional (clockwise and counterclockwise) rotations allowed, and a fixed target such as the Hadamard gate. The scope covers the control model, the alternating-sequence form, the total-time objective, the abstract's five-segment bound, and the resulting finite-dimensional search over sequences of at most five segments. Outside scope: the paper's algebraic framework and proofs, the explicit angle bounds as functions of relative speed and axis angle, the exact form of the three-angle parametrization, and the unidirectional (clockwise-only) scaling laws, none of which are stated in the abstract.

## Symbols

- $\vec{\sigma}$: Vector of Pauli matrices (sigma_x, sigma_y, sigma_z); domain: 2x2 Hermitian traceless matrices
- $\hat{n}_1,\hat{n}_2$: Unit vectors of the two allowed rotation axes on the Bloch sphere; domain: S^2, non-parallel
- $\gamma$: Angle between the two control axes; domain: (0,\pi)
- $\omega_1,\omega_2$: Rotation speeds (angular velocities) of the controls about axes 1 and 2; domain: positive reals
- $R_{\hat{n}}(\theta)$: Rotation of the qubit Bloch vector by angle theta about axis n; domain: SU(2)
- $\theta_k$: Signed rotation angle of the k-th segment (sign gives sense of rotation); domain: real; in bidirectional case (-2\pi,2\pi), in clockwise-only case [0,2\pi)
- $i_k$: Axis index used in the k-th segment; domain: \{1,2\}, with i_{k+1} \neq i_k
- $N$: Number of control segments (concatenations) in a sequence; domain: positive integers
- $T$: Total duration of a control sequence; domain: nonnegative reals
- $U_{\mathrm{target}}$: Target unitary to be synthesized; domain: SU(2) (U(2) targets taken modulo global phase)
- $\phi$: Irrelevant global phase; domain: [0,2\pi)

## eq_1: Axis rotation generator

$$
R_{\hat{n}}(\theta)=\exp\!\left(-\tfrac{i\theta}{2}\,\hat{n}\cdot\vec{\sigma}\right)=\cos\tfrac{\theta}{2}\,I-i\sin\tfrac{\theta}{2}\,\hat{n}\cdot\vec{\sigma}
$$

SU(2) element implementing a Bloch-sphere rotation by angle theta about unit axis n.

Provenance: `standard_background`. Standard SU(2)/Bloch-sphere correspondence used to define the control set.

Equation assumptions:

- Angle convention: positive theta is counterclockwise about n (sign convention is a choice).

## eq_2: Control set and axis geometry

$$
\mathcal{C}=\{R_{\hat{n}_1}(\pm\omega_1 t),\,R_{\hat{n}_2}(\pm\omega_2 t):t\ge 0\},\qquad \hat{n}_1\cdot\hat{n}_2=\cos\gamma,\ \gamma\in(0,\pi)
$$

Available evolutions: rotation about either axis at its own fixed speed, in either sense (bidirectional case); the clockwise-only case keeps only the + sign.

Provenance: `abstract_inferred`. The abstract specifies two non-parallel axes, a relative rotation speed of each control, and the angle between axes; constant rotation speed per axis is the natural reading of 'relative rotation speed'.

Abstract evidence: the control set is restricted to rotations around two non-parallel axes in the Bloch sphere

Equation assumptions:

- Controls are bang-bang: at any time exactly one axis rotation at full speed is applied (consistent with 'control concatenations').

## eq_3: Concatenated sequence and total time

$$
U(\theta_1,\dots,\theta_N)=R_{\hat{n}_{i_N}}(\theta_N)\cdots R_{\hat{n}_{i_2}}(\theta_2)\,R_{\hat{n}_{i_1}}(\theta_1),\quad i_{k+1}\neq i_k,\qquad T=\sum_{k=1}^{N}\frac{|\theta_k|}{\omega_{i_k}}
$$

A sequence of N alternating axis rotations (first applied segment is rightmost) and its total duration.

Provenance: `abstract_inferred`. Sequences of concatenated controls are the objects whose length the abstract bounds; consecutive segments about the same axis merge, so segments alternate axes; duration follows from constant speeds.

Abstract evidence: any finite time-optimal sequence is composed at most of five control concatenations

Equation assumptions:

- Time-ordered product with earliest segment on the right.
- Duration of a segment is |theta|/omega, i.e. no faster path than direct rotation within one axis.

## eq_4: Time-optimal synthesis problem

$$
T^{*}(U_{\mathrm{target}})=\min_{N,\{i_k\},\{\theta_k\}}\;T\quad\text{s.t.}\quad U(\theta_1,\dots,\theta_N)=e^{i\phi}\,U_{\mathrm{target}}
$$

Minimize total duration over all admissible sequences reproducing the target up to global phase.

Provenance: `abstract_inferred`. Direct formalization of the stated problem; global-phase equivalence is standard for SU(2) gate synthesis.

Abstract evidence: time-optimal synthesis of arbitrary unitaries in $SU(2)$

Equation assumptions:

- Target is specified up to global phase.

## eq_5: Bidirectional length bound and reduced search space

$$
N\le 5\quad(\text{both senses allowed}),\qquad T^{*}=\min_{N\le 5}\;\min_{i_1\in\{1,2\}}\;\min_{\theta\in\Theta_N}\sum_{k=1}^{N}\frac{|\theta_k|}{\omega_{i_k}}
$$

The abstract's bound reduces the optimization to a finite enumeration over at most five alternating segments with two choices of starting axis; Theta_N denotes the admissible angle set further restricted by the paper's (unstated here) angle bounds.

Provenance: `abstract_explicit`. The five-concatenation bound is stated verbatim; the search-space reduction is its immediate consequence.

Abstract evidence: we prove that any finite time-optimal sequence is composed at most of five control concatenations

Equation assumptions:

- Bidirectional case only; the clockwise-only case has a different, length-scaling bound not given in the abstract.
- Theta_N is left as the full admissible box since the paper's explicit angle bounds are not in the abstract.

## eq_6: Three-angle parametrization (form only)

$$
(\theta_1,\dots,\theta_N)=F(\alpha,\beta,\delta),\qquad \dim\{\text{time-optimal sequences of length }N\}\le 3
$$

Time-optimal sequences depend on only three rotation angles; the explicit map F (e.g. first, last and common interior angle) is not given in the abstract and is treated as unknown.

Provenance: `abstract_explicit`. Stated directly in the abstract; only the existence of a three-parameter description is asserted, so F is left unspecified rather than invented.

Abstract evidence: time-optimal sequences are solely parametrized by three rotation angles

Equation assumptions:

- A plausible but unverified choice is that interior angles are equal and the free angles are first, interior, last; this is NOT claimed by the abstract.

## eq_7: Tiny explicit instance

$$
\hat{n}_1=\hat{z},\ \hat{n}_2=\hat{x}\ (\gamma=\tfrac{\pi}{2}),\ \omega_1=\omega_2=1,\qquad U_{\mathrm{target}}=H=\tfrac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\simeq R_{\hat{z}}(\tfrac{\pi}{2})R_{\hat{x}}(\tfrac{\pi}{2})R_{\hat{z}}(\tfrac{\pi}{2})
$$

Concrete instance for a later circuit stage: orthogonal axes, equal speeds, Hadamard target; the ZXZ decomposition shown gives a feasible N=3 sequence with T=3pi/2, serving as an upper bound on T^*, not as a claimed optimum.

Provenance: `assumption`. Smallest useful instance chosen in the absence of an experiment scope; the ZXZ decomposition of H up to global phase is standard.

Equation assumptions:

- This instance and target are the author's choice, not from the paper.
- Optimality of the N=3 sequence is not asserted; it is only a feasible candidate to be compared against the N<=5 search.

## Registers

- q: 1 qubits; Single qubit whose SU(2) evolution is synthesized by the two-axis control sequence

## Initial state

Not fixed by the problem (gate synthesis, not state preparation); for verification one may take |0> or run process tomography.

## Measurement

None intrinsic to the synthesis problem. For verification, compare the compiled circuit against U_target by exact matrix product (classical) or by process tomography / randomized benchmarking on hardware.

## Classical postprocessing

Classical: solve the constrained minimization over N<=5, i_1, and angles (root-finding on the SU(2) equality or minimizing a fidelity-based cost 1-|Tr(U^dagger U_target)|/2 to zero), then select the minimal T. Report T^* and the optimal (i_k, theta_k).

## Algorithm steps

1. Fix the control geometry: axes n_1, n_2 with angle gamma, speeds omega_1, omega_2, and whether both rotation senses are allowed (instance: eq_7). (eq_1, eq_2, eq_7)
2. Specify the target unitary up to global phase and the time-optimal objective. (eq_4)
3. Enumerate sequence structures: N in {1,...,5}, starting axis i_1 in {1,2}, alternating axes thereafter (bidirectional case). (eq_3, eq_5)
4. For each structure, solve for angles theta_k such that the product equals the target up to phase, using the three-angle reduction where available, and compute T; retain the minimum over all structures. (eq_3, eq_4, eq_6)
5. Compile the optimal sequence as a circuit of R_{n_1}, R_{n_2} gates (first segment applied first) on the single qubit; the feasible ZXZ Hadamard sequence provides a baseline T for comparison. (eq_1, eq_7)

## Assumptions

- No experiment scope supplied; a single tiny instance (orthogonal axes, equal unit speeds, Hadamard target, bidirectional controls) was chosen by the reconstruction.
- Controls are bang-bang at fixed per-axis speed; segment duration is |theta|/omega.
- Global phase is irrelevant (SU(2) synthesis).
- The paper's algebraic framework, proofs, explicit angle bounds, and clockwise-only scaling laws are not reconstructed.

## Missing information

- Explicit form of the three-angle parametrization (which angles are free and how interior angles are related).
- Explicit bounds on the rotation angles as functions of relative speed omega_1/omega_2 and axis angle gamma.
- Scaling law for the maximum sequence length in the clockwise-only case.
- The algebraic method itself and the necessary conditions it imposes on time-optimal sequences.
- Whether the paper's time-optimal result for a target like Hadamard with orthogonal axes is N=3 or shorter in time; not claimed here.
